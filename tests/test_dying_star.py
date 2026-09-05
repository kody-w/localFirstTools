import subprocess
from pathlib import Path
import re

import pytest


PAGE = Path(__file__).resolve().parents[1] / 'exhibitions/the-arcade/ancient-ruins-dying-star.html'

HARNESS = r"""
const assert = require('node:assert/strict');
const vm = require('node:vm');
const html = require('node:fs').readFileSync(0, 'utf8');
const script = [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].at(-1)[1];
const source = script.replace(/const game = new Game\(\);\s*$/, '');
const elements = new Map();
const frames = { count: 0 };
const stored = new Map(), storage = { denied: false };
const windowEvents = {}, documentEvents = {};
function on(events, name, callback) {
    if (!events[name]) events[name] = [];
    events[name].push(callback);
}
function emit(events, name, event = {}) {
    for (const callback of events[name] || []) callback(event);
}
const document = {
    getElementById(id) {
        if (!elements.has(id)) {
            const classes = new Set();
            elements.set(id, {
                style: {}, textContent: '',
                classList: { add: name => classes.add(name), remove: name => classes.delete(name),
                    contains: name => classes.has(name) },
                getContext: () => ({}), addEventListener() {},
                querySelector: selector => document.getElementById(id + selector),
                querySelectorAll: () => [0, 1, 2].map(index => document.getElementById(id + index)),
            });
        }
        return elements.get(id);
    },
    addEventListener: (name, callback) => on(documentEvents, name, callback),
};
const context = {
    assert, document, frames, console, stored, storage, windowEvents, documentEvents, emit,
    window: { innerWidth: 1280, innerHeight: 720,
        addEventListener: (name, callback) => on(windowEvents, name, callback) },
    localStorage: {
        getItem(key) { if (storage.denied) throw new Error('Storage denied'); return stored.get(key) ?? null; },
        setItem(key, value) { if (storage.denied) throw new Error('Storage denied'); stored.set(key, String(value)); },
    },
    requestAnimationFrame: () => ++frames.count,
    setTimeout: () => 1,
};
const setup = `
    function createGame() {
        const game = new Game();
        game.render = () => {};
        return game;
    }
`;
vm.runInNewContext(source + setup + process.argv[1], context);
"""


def run_scenario(scenario):
    result = subprocess.run(
        ['node', '-e', HARNESS, scenario],
        input=PAGE.read_text(encoding='utf-8'),
        text=True,
        capture_output=True,
        timeout=15,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_player_starts_and_respawns_on_the_safe_platform():
    run_scenario(r"""
        const game = createGame();
        game.generateWorld();
        assert.ok(game.lavaAreas.every(lava => Math.hypot(lava.pos.x, lava.pos.z) >= 12 - 1e-9));
        for (let i = 0; i < 300; i++) game.updatePlayer(1 / 60);
        assert.equal(game.player.pos.y, 1);
        assert.equal(game.player.pos.z, 0);
        assert.equal(game.player.onGround, true);
        game.player.pos.y = -20;
        game.respawnPlayer();
        for (let i = 0; i < 60; i++) game.updatePlayer(1 / 60);
        assert.equal(game.player.pos.y, 1);
        assert.equal(game.player.health, 100);
    """)


def test_forward_movement_agrees_with_camera_projection():
    run_scenario(r"""
        const game = createGame();
        game.generateWorld();
        game.keys.w = true;
        const ahead = game.camera.project(new Vec3(0, 3, -10), game.canvas);
        assert.ok(ahead, 'A point in front of the camera must be visible');
        assert.equal(ahead.x, game.canvas.width / 2);
        assert.equal(game.camera.project(new Vec3(0, 3, 10), game.canvas), null);
        game.updatePlayer(0.1);
        assert.equal(game.player.pos.z, -1);
        game.camera.rot.y = -Math.PI / 2;
        const right = game.camera.project(new Vec3(10, 3, 0), game.canvas);
        assert.ok(Math.abs(right.x - game.canvas.width / 2) < 0.001);
        game.updatePlayer(0.1);
        assert.ok(game.player.pos.x > 0.99);
        game.camera.rot.y = 0;
        game.camera.rot.x = -Math.PI / 4;
        const below = game.camera.project(new Vec3(0, -7, -10), game.canvas);
        assert.ok(Math.abs(below.y - game.canvas.height / 2) < 0.001);
    """)


def test_jump_physics_are_consistent_at_different_frame_rates():
    run_scenario(r"""
        function jump(fps) {
            const game = createGame();
            game.generateWorld();
            game.player.vel.y = 16;
            game.player.onGround = false;
            game.keys.w = true;
            for (let i = 0; i < fps / 2; i++) game.updatePlayer(1 / fps);
            return game.player.pos;
        }
        const at60 = jump(60), at120 = jump(120);
        assert.ok(at60.y > 5);
        assert.ok(Math.abs(at60.y - at120.y) < 0.06);
        assert.ok(Math.abs(at60.z - at120.z) < 0.001);
    """)


def test_fast_falls_land_on_platforms_without_tunneling_through():
    run_scenario(r"""
        const game = createGame();
        game.generateWorld();
        game.player.pos.y = 2;
        game.player.vel.y = -30;
        game.player.onGround = false;
        game.updatePlayer(0.1);
        assert.equal(game.player.pos.y, 1);
        assert.equal(game.player.vel.y, 0);
        assert.equal(game.player.onGround, true);
    """)


def test_resume_and_restart_never_create_duplicate_animation_loops():
    run_scenario(r"""
        const game = createGame();
        game.startGame();
        assert.equal(frames.count, 1);
        game.timeRemaining = 120;
        game.score = 200;
        game.paused = true;
        game.startGame();
        assert.equal(game.timeRemaining, 120);
        assert.equal(game.score, 200);
        assert.equal(frames.count, 1);
        game.running = false;
        game.startGame();
        assert.equal(game.timeRemaining, 300);
        assert.equal(game.score, 0);
        assert.equal(frames.count, 1);
    """)


def test_space_preserves_native_button_activation_instead_of_jumping():
    run_scenario(r"""
        const game = createGame();
        game.startGame();
        const event = { key: ' ', target: { closest: () => ({}) }, prevented: false,
            preventDefault() { this.prevented = true; } };
        emit(windowEvents, 'keydown', event);
        assert.equal(event.prevented, false);
        assert.equal(game.player.vel.y, 0);
        assert.equal(game.player.onGround, true);
        event.target = { closest: () => null };
        emit(windowEvents, 'keydown', event);
        assert.equal(event.prevented, true);
        assert.equal(game.player.vel.y, 16);
    """)


def test_early_and_finished_game_escape_never_hides_the_stopped_menu():
    run_scenario(r"""
        const game = createGame();
        game.togglePause();
        game.togglePause();
        assert.equal(game.running, false);
        assert.equal(document.getElementById('menu').classList.contains('hidden'), false);
        game.startGame();
        game.endGame(false);
        game.togglePause();
        assert.equal(game.running, false);
        assert.equal(game.paused, true);
        assert.equal(document.getElementById('menu').classList.contains('hidden'), false);
    """)


def test_focus_loss_and_released_pointer_lock_clear_movement():
    run_scenario(r"""
        const game = createGame();
        game.startGame();
        game.keys.w = true;
        emit(windowEvents, 'blur');
        assert.equal(game.keys.w, undefined);
        game.keys.w = true;
        document.hidden = true;
        emit(documentEvents, 'visibilitychange');
        assert.equal(game.keys.w, undefined);
        game.keys.w = true;
        document.pointerLockElement = null;
        emit(documentEvents, 'pointerlockchange');
        assert.equal(game.keys.w, undefined);
    """)


def test_corrupt_statistics_do_not_prevent_start_or_erase_valid_legacy_scores():
    run_scenario(r"""
        stored.set('dyingStarData', '{broken');
        stored.set('dyingStarHighScore', '150');
        stored.set('dyingStarGamesPlayed', '4');
        let game;
        assert.doesNotThrow(() => { game = createGame(); });
        assert.match(document.getElementById('notification').textContent, /statistics are unavailable/);
        game.startGame();
        assert.equal(game.running, true);
        game.score = 200;
        assert.equal(game.saveGameData(), true);
        assert.equal(stored.get('dyingStarHighScore'), '200');
        assert.equal(stored.get('dyingStarGamesPlayed'), '5');
    """)


def test_unavailable_statistics_storage_does_not_break_start_or_end_game():
    run_scenario(r"""
        storage.denied = true;
        const game = createGame();
        game.startGame();
        game.endGame(false);
        assert.equal(game.running, false);
        assert.equal(document.getElementById('menu').classList.contains('hidden'), false);
        assert.match(document.getElementById('notification').textContent, /could not be saved/);
        assert.doesNotThrow(() => game.exportData());
        assert.match(document.getElementById('notification').textContent, /export could not finish/);
    """)


def assert_menu_scroll_bounds(html):
    menu = re.search(r'#menu\s*\{([^}]+)\}', html).group(1)
    assert 'width: calc(100% - 32px)' in menu
    assert 'max-height: calc(100vh - 32px)' in menu
    assert 'overflow-y: auto' in menu, 'The start menu must allow user scrolling'


def test_small_screen_start_menu_has_explicit_scroll_bounds():
    assert_menu_scroll_bounds(PAGE.read_text(encoding='utf-8'))


def test_start_menu_contract_rejects_an_unscrollable_overflow():
    html = PAGE.read_text(encoding='utf-8')
    assert_menu_scroll_bounds(html)
    with pytest.raises(AssertionError, match='user scrolling'):
        assert_menu_scroll_bounds(html.replace('overflow-y: auto;', 'overflow-y: visible;', 1))
