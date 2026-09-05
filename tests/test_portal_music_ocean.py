import json
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
MUSIC = ROOT / "exhibitions/sound-studio/collaborative-music-garden.html"
OCEAN = ROOT / "exhibitions/simulation-lab/bioluminescent-ocean-trench.html"

HARNESS = r"""
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const html = fs.readFileSync(0, 'utf8');
const script = [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].at(-1)[1];
const world = process.argv[1];
const source = script.split(world === 'music' ? '// ==================== INITIALIZATION' : '// Initialize game')[0];
const timers = new Map(), frames = new Map(), stored = new Map(), elements = new Map(), warnings = [];
let nextId = 0;
const audio = {created: 0, resumed: 0, initialState: 'suspended', failCreate: false, failResume: false, pending: false, resumes: []};
const storage = {denied: false};
const gpu = {buffers: 0, draws: 0, uniforms: {}, sources: [], uploads: []};
const gl = {
    VERTEX_SHADER: 1, FRAGMENT_SHADER: 2, COMPILE_STATUS: 3, LINK_STATUS: 4,
    DEPTH_TEST: 5, BLEND: 6, SRC_ALPHA: 7, ONE_MINUS_SRC_ALPHA: 8, ONE: 15,
    ALIASED_POINT_SIZE_RANGE: 9, COLOR_BUFFER_BIT: 16, DEPTH_BUFFER_BIT: 32,
    ARRAY_BUFFER: 10, STATIC_DRAW: 11, DYNAMIC_DRAW: 12, FLOAT: 13, POINTS: 14,
    getParameter: () => new Float32Array([1, 64]),
    createShader: type => ({type}), shaderSource: (shader, text) => { gpu.sources.push(text); },
    compileShader() {}, getShaderParameter: () => true, deleteShader() {},
    createProgram: () => ({}), attachShader() {}, linkProgram() {},
    getProgramParameter: () => true, useProgram() {}, enable() {}, blendFunc() {}, depthMask() {},
    getAttribLocation: (_p, name) => name, getUniformLocation: (_p, name) => name,
    viewport() {}, clearColor() {}, clear() {},
    uniformMatrix4fv: (name, _transpose, value) => { gpu.uniforms[name] = [...value]; },
    uniform1f: (name, value) => { gpu.uniforms[name] = value; },
    uniform2f: (name, x, y) => { gpu.uniforms[name] = [x, y]; },
    createBuffer: () => ({id: ++gpu.buffers}), bindBuffer() {},
    bufferData: (_type, value) => { gpu.uploads.push([...value]); },
    enableVertexAttribArray() {}, vertexAttribPointer() {}, uniform3f() {},
    drawArrays: () => { gpu.draws++; },
};
class Element {
    constructor(id = '') {
        this.id = id; this.width = 1440; this.height = 900;
        this.style = {}; this.dataset = {}; this.textContent = ''; this.disabled = false;
        this.listeners = {}; this.classes = new Set(); this.children = [];
        this.classList = {
            add: name => this.classes.add(name), remove: name => this.classes.delete(name),
            toggle: (name, on) => on ? this.classes.add(name) : this.classes.delete(name),
            contains: name => this.classes.has(name),
        };
    }
    addEventListener(name, callback) { this.listeners[name] = callback; }
    appendChild(child) { this.children.push(child); }
    click() { this.onclick?.(); this.listeners.click?.({target: this}); }
    remove() {}
    getContext(type) { return type === '2d' ? {} : gl; }
    getBoundingClientRect() { return this.rect || {left: 0, top: 0, width: this.width, height: this.height}; }
    requestPointerLock() { document.pointerLockElement = this; return Promise.resolve(); }
}
const document = {
    hidden: false, body: new Element('body'),
    getElementById(id) { if (!elements.has(id)) elements.set(id, new Element(id)); return elements.get(id); },
    createElement: tag => new Element(tag), querySelectorAll: () => [],
    addEventListener() {}, exitPointerLock() { this.pointerLockElement = null; },
};
class Param {
    constructor() { this.value = 0; }
    setValueAtTime(value) { this.value = value; }
    linearRampToValueAtTime(value) { this.value = value; }
    cancelScheduledValues() {}
}
class AudioNode {
    constructor() { this.gain = new Param(); this.frequency = new Param(); this.Q = new Param(); this.stops = []; }
    connect() {} disconnect() { this.disconnected = true; }
    start() { this.started = true; }
    stop(time) { this.stops.push(time); }
}
class AudioContext {
    constructor() {
        if (audio.failCreate) throw new Error('Audio construction blocked');
        audio.created++; this.state = audio.initialState; this.currentTime = 1;
        this.destination = {};
    }
    createGain() { return new AudioNode(); }
    createOscillator() { return new AudioNode(); }
    createBiquadFilter() { return new AudioNode(); }
    resume() {
        audio.resumed++;
        if (audio.failResume) return Promise.reject(new Error('Audio resume denied'));
        if (audio.pending) return new Promise(resolve => audio.resumes.push(() => { this.state = 'running'; resolve(); }));
        this.state = 'running'; return Promise.resolve();
    }
    close() { this.state = 'closed'; return Promise.resolve(); }
}
const window = {innerWidth: 1440, innerHeight: 900, AudioContext, addEventListener() {}};
const localStorage = {
    getItem(key) { if (storage.denied) throw new Error('Storage denied'); return stored.get(key) ?? null; },
    setItem(key, value) { if (storage.denied) throw new Error('Storage denied'); stored.set(key, value); },
    removeItem(key) { if (storage.denied) throw new Error('Storage denied'); stored.delete(key); },
};
const context = {
    assert, document, window, localStorage, storage, stored, audio, gpu, timers, frames,
    warnings, console: {warn: (...args) => warnings.push(args), error: (...args) => warnings.push(args)},
    setTimeout: callback => { const id = ++nextId; timers.set(id, callback); return id; },
    clearTimeout: id => timers.delete(id),
    requestAnimationFrame: callback => { const id = ++nextId; frames.set(id, callback); return id; },
    cancelAnimationFrame: id => frames.delete(id),
    confirm: () => true, alert: message => warnings.push(message),
};
const setup = world === 'music' ? `
    MusicGarden.prototype.animate = function() {};
    const garden = new MusicGarden();
` : '';
let completed = false;
process.on('beforeExit', () => {
    if (!completed) { console.error('Scenario did not complete'); process.exitCode = 1; }
});
vm.runInNewContext(source + '\n(async () => {' + setup + process.argv[2] + '})()', context)
    .then(() => { completed = true; }, error => { completed = true; console.error(error); process.exitCode = 1; });
"""


def run_world(world, scenario, source=None):
    page = MUSIC if world == "music" else OCEAN
    result = subprocess.run(
        ["node", "-e", HARNESS, world, scenario],
        input=source if source is not None else page.read_text(encoding="utf-8"),
        text=True,
        capture_output=True,
        cwd=ROOT,
        timeout=15,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_music_clicked_ground_points_project_back_to_distinct_pointer_positions():
    run_world("music", r"""
        for (const [x, y] of [[620, 480], [890, 610], [430, 720]]) {
            await garden.placeObject(x, y);
            const object = garden.objects.at(-1);
            const point = garden.camera.project(object.pos, garden.canvas);
            assert.equal(object.pos.y, 0);
            assert.ok(Math.abs(point.x - x) < 1e-6, 'Placement x must follow the actual click');
            assert.ok(Math.abs(point.y - y) < 1e-6, 'Placement y must follow the actual click');
        }
        assert.equal(new Set(garden.objects.map(obj => JSON.stringify(obj.pos))).size, 3);
    """)


def test_music_inverse_projection_handles_camera_rotation_canvas_scaling_and_sky():
    run_world("music", r"""
        garden.camera.rot = {x: -0.55, y: 0.8};
        garden.canvas.rect = {left: 40, top: 60, width: 720, height: 450};
        await garden.placeObject(400, 310);
        const projected = garden.camera.project(garden.objects[0].pos, garden.canvas);
        assert.ok(Math.abs(projected.x - 720) < 1e-6);
        assert.ok(Math.abs(projected.y - 500) < 1e-6);
        garden.camera.rot.x = 0.5;
        const before = garden.objects.length;
        await garden.placeObject(400, 280);
        assert.equal(garden.objects.length, before);
        assert.match(document.getElementById('music-status').textContent, /ground/i);
    """)


def test_music_restored_composition_plays_without_adding_objects_or_audio_contexts():
    run_world("music", r"""
        garden.loadData({version: 1, scale: 'minor', objects: [
            {pos: {x: 0, y: 0, z: 250}, type: 'tower', noteIndex: 4},
            {pos: {x: 20, y: 0, z: 220}, type: 'crystal', noteIndex: 7},
        ]});
        const before = JSON.stringify(garden.objects.map(obj => obj.toJSON()));
        assert.equal(garden.audioSystem.context, null);
        assert.equal(isPlaying, false);
        await garden.togglePlayPause();
        assert.equal(garden.audioSystem.context.state, 'running');
        assert.equal(isPlaying, true);
        await garden.startPlayback();
        assert.equal(audio.created, 1);
        assert.equal(JSON.stringify(garden.objects.map(obj => obj.toJSON())), before);
        garden.pausePlayback();
        assert.equal(isPlaying, false);
        assert.equal(garden.audioSystem.oscillators.size, 0);
        assert.equal(garden.audioSystem.pendingNotes.size, 0);
        await garden.togglePlayPause();
        assert.equal(audio.created, 1);
        assert.equal(isPlaying, true);
    """)


@pytest.mark.parametrize("failure", ["audio.failCreate = true;", "audio.failResume = true;", "window.AudioContext = undefined;"])
def test_music_audio_failures_leave_play_retryable_and_do_not_claim_sound(failure):
    run_world("music", failure + r"""
        assert.equal(await garden.startPlayback(), false);
        assert.equal(isPlaying, false);
        assert.equal(document.getElementById('play-pause-btn').disabled, false);
        assert.match(document.getElementById('play-pause-btn').textContent, /Play/);
        assert.match(document.getElementById('music-status').textContent, /audio|sound/i);
        assert.ok(warnings.length > 0);
    """)


def test_music_pausing_pending_resume_prevents_late_playback():
    run_world("music", r"""
        audio.pending = true;
        const pending = garden.startPlayback();
        assert.equal(audio.resumes.length, 1);
        garden.pausePlayback();
        audio.resumes[0]();
        assert.equal(await pending, false);
        assert.equal(isPlaying, false);
        assert.equal(garden.audioSystem.oscillators.size, 0);
        assert.match(document.getElementById('play-pause-btn').textContent, /Play/);
    """)


def test_music_tracks_short_voices_and_cancels_harmonics_on_pause():
    run_world("music", r"""
        await garden.startPlayback();
        const audioSystem = garden.audioSystem;
        assert.equal(audioSystem.playNote('same', 1, 'sine', 0.5), true);
        const oldVoice = audioSystem.oscillators.get('same');
        audioSystem.playNote('same', 2, 'sine', 0.5);
        const newVoice = audioSystem.oscillators.get('same');
        assert.notEqual(oldVoice, newVoice);
        oldVoice.osc.onended();
        assert.equal(audioSystem.oscillators.get('same'), newVoice);
        const a = new MusicalObject(new Vec3(0, 0, 200), 'tower', 1);
        const b = new MusicalObject(new Vec3(10, 0, 200), 'crystal', 2);
        a.play(audioSystem, [a, b]);
        assert.ok(audioSystem.pendingNotes.size > 0);
        garden.pausePlayback();
        assert.equal(audioSystem.pendingNotes.size, 0);
        assert.equal(audioSystem.oscillators.size, 0);
        assert.equal(audioSystem.playNote('paused', 1), false);
        assert.equal(newVoice.osc.stops.at(-1) <= audioSystem.context.currentTime + 0.1, true);
    """)


@pytest.mark.parametrize("invalid", [
    None, [], {}, {"objects": "wrong"}, {"scale": "unknown", "objects": []},
    {"objects": [{"pos": {"x": 1, "y": None, "z": 1}, "type": "tower", "noteIndex": 1}]},
    {"objects": [{"pos": {"x": 1, "y": 0, "z": 1}, "type": "unknown", "noteIndex": 1}]},
    {"objects": [{"pos": {"x": 1, "y": 0, "z": 1}, "type": "tower", "noteIndex": "1"}]},
    {"objects": [], "camera": {"pos": {"x": 0, "y": 50, "z": 100}, "rot": {"x": None, "y": 0}}},
])
def test_music_invalid_composition_is_rejected_before_mutation(invalid):
    run_world("music", r"""
        const good = {version: 1, scale: 'major', objects: [
            {pos: {x: 1, y: 0, z: 200}, type: 'tower', noteIndex: 1}
        ]};
        garden.loadData(good);
        const before = JSON.stringify(garden.objects.map(obj => obj.toJSON()));
        const persisted = stored.get('musicGarden');
        assert.throws(() => garden.loadData(INVALID));
        assert.equal(JSON.stringify(garden.objects.map(obj => obj.toJSON())), before);
        assert.equal(stored.get('musicGarden'), persisted);
    """.replace("INVALID", json.dumps(invalid)))


def test_music_denied_storage_does_not_stop_placement_or_audio():
    run_world("music", r"""
        storage.denied = true;
        garden.loadFromStorage();
        await garden.placeObject(700, 500);
        assert.equal(garden.objects.length, 1);
        assert.equal(isPlaying, true);
        assert.match(document.getElementById('music-status').textContent, /storage|saved/i);
        assert.ok(warnings.length >= 1);
    """)


def test_ocean_uploads_focal_pixel_scale_and_respects_hardware_bounds_on_resize():
    run_world("ocean", r"""
        const renderer = new Renderer(document.getElementById('gameCanvas'));
        const camera = new Camera();
        renderer.render([], camera);
        assert.ok(Math.abs(gpu.uniforms.uPointScale - 450 / Math.tan(Math.PI / 6)) < 0.001);
        assert.equal(JSON.stringify(gpu.uniforms.uPointSizeRange), '[1,64]');
        assert.equal(gpu.uniforms.uNear, 0.1);
        assert.match(gpu.sources[0], /aSize\s*\*\s*uPointScale/);
        assert.match(gpu.sources[0], /max\(gl_Position\.w,\s*uNear\)/);
        assert.match(gpu.sources[0], /clamp\(/);
        window.innerWidth = 480;
        window.innerHeight = 800;
        renderer.resize();
        renderer.render([], camera);
        assert.ok(Math.abs(gpu.uniforms.uPointScale - 400 / Math.tan(Math.PI / 6)) < 0.001);
        assert.ok(Math.abs(gpu.uniforms.uProjection[0] - (1 / Math.tan(Math.PI / 6)) / 0.6) < 0.001);
    """)


def test_ocean_reuses_gpu_buffers_instead_of_allocating_per_sprite_frame():
    run_world("ocean", r"""
        const renderer = new Renderer(document.getElementById('gameCanvas'));
        const allocated = gpu.buffers;
        assert.equal(allocated, 3);
        for (let i = 0; i < 60; i++)
            renderer.drawPoints([0, -50, 100], [0, 1, 1], [10]);
        assert.equal(gpu.buffers, allocated);
        assert.equal(gpu.draws, 60);
        assert.equal(gpu.uploads.length, 180);
    """)


def test_ocean_pause_resume_keeps_one_loop_and_does_not_regenerate_entities():
    run_world("ocean", r"""
        const game = new Game();
        game.startGame();
        const first = game.creatures[0];
        assert.equal(frames.size, 1);
        game.startGame();
        assert.equal(frames.size, 1);
        for (let i = 0; i < 5; i++) {
            game.pauseGame();
            assert.equal(frames.size, 0);
            game.startGame();
            assert.equal(frames.size, 1);
        }
        assert.equal(game.creatures[0], first);
        assert.equal(game.creatures.length, 30);
        assert.equal(game.entities.length, 37);
        game.pauseGame();
    """)


def test_ocean_illumination_retains_existing_discovery_ranges():
    run_world("ocean", r"""
        const camera = new Camera();
        const creature = new Creature('random', new Vec3(0, -50, 22));
        assert.equal(creature.checkDiscovery(camera.position, false), false);
        assert.equal(creature.checkDiscovery(camera.position, true), true);
        assert.equal(creature.checkDiscovery(camera.position, true), false);
    """)


def test_audio_resume_timeout_fails_visibly_instead_of_claiming_playback():
    run_world("music", r"""
        audio.pending = true;
        const pending = garden.startPlayback();
        assert.equal(timers.size, 1);
        [...timers.values()][0]();
        assert.equal(await pending, false);
        assert.equal(isPlaying, false);
        assert.equal(document.getElementById('play-pause-btn').disabled, false);
        assert.match(document.getElementById('music-status').textContent, /did not start/i);
    """)


def test_generated_music_notes_remain_importable_after_changing_scale():
    run_world("music", r"""
        garden.loadData({version: 1, scale: 'pentatonic', objects: [
            {pos: {x: 10, y: 0, z: 220}, type: 'crystal', noteIndex: 35}
        ]});
        assert.equal(garden.objects[0].noteIndex, 35);
        assert.equal(currentScale, 'pentatonic');
    """)


@pytest.mark.parametrize("invalid", [
    None, [], {}, {"discoveredSpecies": "Jellyfish"},
    {"version": "2.0", "discoveredSpecies": []},
    {"discoveredSpecies": [None]},
    {"discoveredSpecies": ["Jellyfish"], "position": {"x": 0, "y": None, "z": 10}},
])
def test_ocean_invalid_log_preserves_last_good_discoveries_and_position(invalid):
    run_world("ocean", r"""
        const game = new Game();
        game.applyDiscoveryData({version: '1.0', discoveredSpecies: ['Giant Jellyfish'], position: {x: 2, y: -30, z: 12}});
        game.saveData();
        const saved = stored.get('oceanTrenchData');
        assert.throws(() => game.applyDiscoveryData(INVALID));
        assert.equal([...game.discoveredSpecies].join(','), 'Giant Jellyfish');
        assert.equal(game.camera.position.y, -30);
        assert.equal(stored.get('oceanTrenchData'), saved);
    """.replace("INVALID", json.dumps(invalid)))


def test_ocean_storage_denial_is_visible_and_reset_is_not_falsely_reported():
    run_world("ocean", r"""
        const game = new Game();
        game.applyDiscoveryData({version: '1.0', discoveredSpecies: ['Giant Jellyfish']});
        storage.denied = true;
        game.loadData();
        assert.equal(game.saveData(), false);
        game.resetData();
        assert.equal(game.discoveredSpecies.size, 1);
        assert.match(document.getElementById('data-status').textContent, /Storage unavailable/i);
        assert.ok(warnings.length > 0);
    """)


def test_ocean_reset_allows_the_same_creatures_to_be_discovered_again():
    run_world("ocean", r"""
        const game = new Game();
        game.startGame();
        game.creatures[0].discovered = true;
        game.camera.velocity = new Vec3(1, 2, 3);
        game.resetData();
        assert.equal(game.creatures[0].discovered, false);
        assert.equal(game.camera.velocity.length(), 0);
        game.pauseGame();
    """)


@pytest.mark.parametrize("world,before,after,scenario", [
    (
        "music",
        "const rx = (x - canvas.width / 2) / focal;",
        "const rx = 0;",
        """
        await garden.placeObject(620, 480);
        const projected = garden.camera.project(garden.objects[0].pos, garden.canvas);
        assert.ok(Math.abs(projected.x - 620) < 1e-6);
        """,
    ),
    (
        "music",
        "await this.audioSystem.init();",
        "",
        """
        await garden.startPlayback();
        assert.ok(garden.audioSystem.context, 'Play must create actual audio capability');
        """,
    ),
    (
        "music",
        "this.oscillators.set(id, voice);",
        "if (!duration) this.oscillators.set(id, voice);",
        """
        await garden.startPlayback();
        garden.audioSystem.playNote('timed', 1, 'sine', 0.5);
        assert.equal(garden.audioSystem.oscillators.size, 1);
        """,
    ),
    (
        "ocean",
        "aSize * uPointScale",
        "aSize",
        """
        new Renderer(document.getElementById('gameCanvas'));
        assert.match(gpu.sources[0], /aSize\\s*\\*\\s*uPointScale/);
        """,
    ),
    (
        "ocean",
        "gl.bindBuffer(gl.ARRAY_BUFFER, this.buffers[name]);",
        "this.buffers[name] = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, this.buffers[name]);",
        """
        const renderer = new Renderer(document.getElementById('gameCanvas'));
        renderer.drawPoints([0, 0, 100], [1, 1, 1], [10]);
        assert.equal(gpu.buffers, 3);
        """,
    ),
    (
        "ocean",
        "if (!this.isPaused) return;",
        "",
        """
        const game = new Game();
        game.startGame();
        game.startGame();
        assert.equal(frames.size, 1);
        """,
    ),
])
def test_core_regressions_reject_controlled_in_memory_mutations(world, before, after, scenario):
    source = (MUSIC if world == "music" else OCEAN).read_text(encoding="utf-8")
    assert source.count(before) == 1
    run_world(world, scenario, source)
    with pytest.raises(AssertionError, match="ERR_ASSERTION"):
        run_world(world, scenario, source.replace(before, after, 1))


def test_harness_fails_closed_for_an_unresolved_async_scenario():
    with pytest.raises(AssertionError, match="Scenario did not complete"):
        run_world("music", "await new Promise(() => {});")
