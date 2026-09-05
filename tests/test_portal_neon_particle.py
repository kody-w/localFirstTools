import json
from pathlib import Path
import re
import subprocess

import pytest


ROOT = Path(__file__).resolve().parents[1]
NEON = ROOT / 'exhibitions/ai-research/neon-synthwave-city.html'
PARTICLE = ROOT / 'exhibitions/the-arcade/particle-physics-playground.html'


def assert_neon_buttons_receive_pointer_events(html):
    style = re.search(r'<style>(.*?)</style>', html, re.S).group(1)
    buttons = re.search(r'^\s*button\s*\{([^}]+)\}', style, re.M).group(1)
    assert re.search(r'pointer-events:\s*(?:auto|all)\s*;', buttons), 'Neon buttons must opt into pointer events'


def test_neon_toolbar_and_mobile_buttons_override_the_noninteractive_overlay():
    assert_neon_buttons_receive_pointer_events(NEON.read_text(encoding='utf-8'))


def test_neon_pointer_regression_rejects_the_original_inheritance_bug():
    html = NEON.read_text(encoding='utf-8')
    assert_neon_buttons_receive_pointer_events(html)
    with pytest.raises(AssertionError, match='pointer events'):
        assert_neon_buttons_receive_pointer_events(html.replace('pointer-events: auto;', 'pointer-events: none;', 1))


HARNESS = r"""
const assert = require('node:assert/strict');
const vm = require('node:vm');
const input = JSON.parse(require('node:fs').readFileSync(0, 'utf8'));
const script = [...input.html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].at(-1)[1];
const elements = new Map(), frames = new Map(), calls = [], saved = new Map(), windowEvents = {};
const storage = { readDenied: false, writeDenied: false };
let nextFrame = 0;
const finite = values => assert.ok(values.every(Number.isFinite), 'Canvas arguments must be finite');
const ctx = {
    beginPath() {}, stroke() {}, fill() {},
    moveTo(...values) { finite(values); calls.push(['move', ...values]); },
    lineTo(...values) { finite(values); calls.push(['line', ...values]); },
    fillRect(...values) { finite(values); calls.push(['rect', ...values]); },
    strokeRect(...values) { finite(values); },
    fillText(text, ...values) { finite(values); },
    arc(x, y, radius) {
        finite([x, y, radius]);
        assert.ok(radius >= 0, 'Canvas arc radius cannot be negative');
        calls.push(['arc', x, y, radius]);
    },
    createRadialGradient(...values) {
        finite(values);
        assert.ok(values[2] >= 0 && values[5] >= 0, 'Gradient radius cannot be negative');
        calls.push(['gradient', ...values]);
        return { addColorStop() {} };
    },
};
class Element {
    constructor(id) {
        this.id = id; this.style = {}; this.dataset = {}; this.textContent = '';
        this.listeners = {};
        const classes = new Set();
        this.classList = {
            add: name => classes.add(name), remove: name => classes.delete(name),
            contains: name => classes.has(name),
            toggle(name, force) {
                const enabled = force ?? !classes.has(name);
                if (enabled) classes.add(name); else classes.delete(name);
                return enabled;
            },
        };
    }
    getContext() { return ctx; }
    addEventListener(name, callback) { this.listeners[name] = callback; }
}
const element = id => {
    if (!elements.has(id)) elements.set(id, new Element(id));
    return elements.get(id);
};
const buttons = ['electron', 'proton', 'neutron'].map(type => {
    const button = element(type);
    button.dataset.particle = type;
    return button;
});
const document = {
    getElementById: element,
    addEventListener() {},
    querySelectorAll: () => buttons,
    querySelector: selector => element(selector.match(/"(.*?)"/)[1]),
};
const math = Object.create(Math);
math.random = () => 0.25;
class Reader {
    readAsText(file) {
        if (file.error) throw new Error('Read denied');
        this.onload({ target: { result: file.text } });
    }
}
const context = {
    assert, document, calls, frames, saved, storage, windowEvents, FileReader: Reader, Math: math, console,
    window: { innerWidth: 1280, innerHeight: 720,
        addEventListener(name, callback) { windowEvents[name] = callback; } },
    localStorage: {
        getItem(key) { if (storage.readDenied) throw new Error('Read denied'); return saved.get(key) ?? null; },
        setItem(key, value) { if (storage.writeDenied) throw new Error('Write denied'); saved.set(key, value); },
    },
    setInterval: () => 1,
    requestAnimationFrame: callback => { frames.set(++nextFrame, callback); return nextFrame; },
    step() {
        const next = frames.entries().next().value;
        assert.ok(next, 'An animation frame must remain scheduled');
        frames.delete(next[0]);
        next[1]();
    },
};
vm.runInNewContext(script + '\ninit();\n' + input.scenario, context);
"""


def run_scenario(scenario, html=None):
    result = subprocess.run(
        ['node', '-e', HARNESS],
        input=json.dumps({'html': html or PARTICLE.read_text(encoding='utf-8'), 'scenario': scenario}),
        text=True,
        capture_output=True,
        timeout=15,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_projection_uses_the_follow_cameras_forward_direction_and_clips_invalid_points():
    run_scenario(r"""
        GameState.camera = {x: 0, y: 0, z: 0};
        const visible = project3D(1, 0, -10);
        assert.ok(visible);
        assert.equal(visible.scale, 40);
        assert.equal(visible.x, GameState.width / 2 + 40);
        assert.equal(project3D(0, 0, 0), null);
        assert.equal(project3D(0, 0, 10), null);
        assert.equal(project3D(Infinity, 0, -10), null);
        assert.equal(project3D(0, NaN, -10), null);
        assert.equal(project3D(0, 0, -Infinity), null);
    """)


def test_accelerator_segments_are_clipped_instead_of_disappearing_at_the_near_plane():
    run_scenario(r"""
        GameState.camera = {x: 0, y: 0, z: 0};
        const start = {x: -2, y: 0, z: -10}, end = {x: 2, y: 0, z: 10};
        const line = projectSegment(start, end);
        assert.ok(line);
        assert.equal(line[0].scale, 40);
        assert.equal(line[1].scale, 400);
        assert.equal(end.z, 10);
        assert.equal(projectSegment({x: 0, y: 0, z: 2}, end), null);
    """)


@pytest.mark.parametrize('particle_type', ['electron', 'proton', 'neutron'])
def test_all_particle_starts_keep_rendering_through_movement_abilities_and_reset(particle_type):
    run_scenario(f"""
        selectParticle({json.dumps(particle_type)});
        startGame();
        assert.equal(frames.size, 1);
        GameState.keys.w = true;
        activateTunneling();
        activateSuperposition();
        for (let i = 0; i < 150; i++) step();
        assert.ok(GameState.player.z < 0);
        assert.ok(GameState.stats.distance > 0);
        assert.ok(calls.some(call => call[0] === 'arc'));
        assert.ok(calls.some(call => call[0] === 'gradient'));
        resetGame();
        for (let i = 0; i < 20; i++) step();
        assert.equal(frames.size, 1);
        assert.equal(GameState.quantum.superposition, false);
        assert.equal(GameState.quantum.tunneling, false);
        assert.equal(GameState.quantum.superpositionClones.length, 0);
    """)


def test_every_draw_path_ignores_points_behind_the_camera_without_invalid_canvas_calls():
    run_scenario(r"""
        GameState.camera = {x: 0, y: 0, z: 0};
        GameState.accelerators = [{x1: 0, y1: 0, z1: -10, x2: 0, y2: 0, z2: 10, radius: 30}];
        GameState.barriers = [{x: 0, y: 0, z: 10, width: 100}];
        GameState.magneticFields = [{x: 0, y: 0, z: 10, radius: 80}];
        GameState.particles = [{x: 0, y: 0, z: 10, radius: 5, type: 'electron'}];
        GameState.player.z = 10;
        GameState.player.trail = [{x: 0, y: 0, z: -10}, {x: 0, y: 0, z: 10}, {x: 2, y: 0, z: -10}];
        GameState.quantum.superposition = true;
        GameState.quantum.superpositionClones = [{x: 0, y: 0, z: 10}];
        render();
        assert.equal(GameState.ctx.globalAlpha, 1);
        assert.equal(calls.filter(call => call[0] === 'arc').length, 0);
        assert.equal(calls.filter(call => call[0] === 'gradient').length, 0);
    """)


def test_pause_resume_does_not_reset_position_or_duplicate_the_animation_loop():
    run_scenario(r"""
        toggleMenu();
        assert.equal(document.getElementById('menu').classList.contains('hidden'), false);
        startGame();
        GameState.player.z = -25;
        GameState.keys.w = true;
        toggleMenu();
        assert.equal(GameState.paused, true);
        assert.equal(Object.keys(GameState.keys).length, 0);
        startGame();
        assert.equal(GameState.player.z, -25);
        assert.equal(frames.size, 1);
        step();
        assert.equal(frames.size, 1);
    """)


def test_displayed_speed_and_distance_use_the_limited_velocity():
    run_scenario(r"""
        GameState.accelerators = [];
        GameState.magneticFields = [];
        GameState.barriers = [];
        GameState.player.vx = 10;
        updatePlayer();
        assert.ok(GameState.player.speed <= GameState.MAX_SPEED + 1e-12);
        assert.ok(Math.abs(GameState.stats.distance - GameState.MAX_SPEED) < 1e-12);
        updateUI();
        assert.equal(document.getElementById('speedDisplay').textContent, '99.00');
    """)


def test_particle_gate_rejects_the_original_negative_radius_projection():
    html = PARTICLE.read_text(encoding='utf-8')
    scenario = "startGame(); for (let i = 0; i < 5; i++) step();"
    run_scenario(scenario, html)
    start = html.index('        function project3D(')
    end = html.index('        function projectSegment(', start)
    legacy = """        function project3D(x, y, z) {
            const scale = 400 / (400 + z - GameState.camera.z);
            return {x: GameState.width / 2 + (x - GameState.camera.x) * scale,
                y: GameState.height / 2 + (y - GameState.camera.y) * scale, scale};
        }
"""
    with pytest.raises(AssertionError, match='ERR_ASSERTION'):
        run_scenario(scenario, html[:start] + legacy + html[end:])


def test_particle_gate_rejects_duplicate_start_loops():
    html = PARTICLE.read_text(encoding='utf-8')
    before = 'if (GameState.animationId === null) gameLoop();'
    assert html.count(before) == 1
    scenario = 'startGame(); startGame(); assert.equal(frames.size, 1);'
    run_scenario(scenario, html)
    with pytest.raises(AssertionError, match='ERR_ASSERTION'):
        run_scenario(scenario, html.replace(before, 'gameLoop();', 1))


def test_portal_return_saves_and_restores_position_progress_and_element_counters():
    run_scenario(r"""
        selectParticle('proton');
        startGame();
        GameState.player.x = 42;
        GameState.player.y = -350;
        GameState.player.z = -75;
        GameState.player.energy = 250;
        GameState.stats.collisions = 3;
        GameState.stats.distance = 123.5;
        GameState.stats.elementsCreated.hydrogen = 3;
        windowEvents.pagehide();
        const snapshot = JSON.parse(saved.get('particlePhysicsPlayground'));
        assert.equal(snapshot.player.z, -75);
        resetGame();
        loadGameData();
        GameState.running = false;
        startGame();
        assert.equal(GameState.particleType, 'proton');
        assert.equal(GameState.player.x, 42);
        assert.equal(GameState.player.y, -350);
        assert.equal(GameState.player.z, -75);
        assert.equal(GameState.player.energy, 250);
        assert.equal(GameState.stats.collisions, 3);
        assert.equal(Number(document.getElementById('hydrogen').textContent), 3);
    """)


def test_valid_legacy_snapshots_without_coordinates_keep_the_current_position():
    run_scenario(r"""
        GameState.player.x = 12;
        const legacy = getGameData();
        legacy.player = { energy: 0 };
        applyGameData(validateGameData(legacy));
        assert.equal(GameState.player.x, 12);
        assert.equal(GameState.player.energy, 0);
        assert.equal(GameState.player.vx, 0);
    """)


@pytest.mark.parametrize('mutation', [
    "data.particleType = 'not-a-particle'",
    "data.stats.elementsCreated = null",
    "data.stats.collisions = -1",
    "data.player.energy = '100'",
    "data.player.x = null",
])
def test_invalid_particle_imports_leave_the_running_experiment_unchanged(mutation):
    run_scenario(f"""
        startGame();
        const before = JSON.stringify(getGameData());
        const data = getGameData();
        {mutation};
        const text = JSON.stringify(data);
        handleFileImport({{ target: {{ files: [{{ text, size: text.length }}], value: 'snapshot.json' }} }});
        assert.equal(JSON.stringify(getGameData()), before);
        assert.match(document.getElementById('dataStatus').textContent, /Current experiment kept/);
    """)


def test_denied_storage_does_not_block_play_and_is_visibly_disclosed():
    run_scenario(r"""
        storage.readDenied = true;
        loadGameData();
        assert.match(document.getElementById('dataStatus').textContent, /storage is unavailable/);
        startGame();
        storage.writeDenied = true;
        assert.equal(saveGameData(), false);
        assert.match(document.getElementById('dataStatus').textContent, /Local save unavailable/);
        for (let i = 0; i < 10; i++) step();
        assert.equal(frames.size, 1);
    """)


def test_physics_information_tracks_reset_expiration_and_combined_quantum_effects():
    run_scenario(r"""
        GameState.initialInfoText = 'Baseline physics information.';
        startGame();
        activateSuperposition();
        assert.match(document.getElementById('infoText').textContent, /Superposition Active/);
        resetGame();
        assert.equal(document.getElementById('infoText').textContent, GameState.initialInfoText);
        toggleMenu();
        startGame();
        assert.equal(document.getElementById('infoText').textContent, GameState.initialInfoText);
        activateTunneling();
        activateSuperposition();
        assert.match(document.getElementById('infoText').textContent, /Tunneling and Superposition/);
        GameState.quantum.tunnelingCooldown = GameState.quantum.superpositionCooldown = 1;
        updateQuantumEffects();
        updateUI();
        assert.equal(document.getElementById('infoText').textContent, GameState.initialInfoText);
    """)


def test_information_gate_rejects_retaining_a_stale_active_effect_message():
    html = PARTICLE.read_text(encoding='utf-8')
    before = 'let info = GameState.initialInfoText;'
    assert html.count(before) == 1
    scenario = """
        GameState.initialInfoText = 'Baseline physics information.';
        startGame(); activateSuperposition(); resetGame();
        assert.equal(document.getElementById('infoText').textContent, GameState.initialInfoText);
    """
    run_scenario(scenario, html)
    with pytest.raises(AssertionError, match='ERR_ASSERTION'):
        run_scenario(scenario, html.replace(before, "let info = document.getElementById('infoText').textContent;", 1))
