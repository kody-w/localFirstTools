"""Deterministic garden logic checks; real WebGL is verified separately in Chrome."""

import json
from pathlib import Path
import re
import subprocess

import pytest


ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "exhibitions/simulation-lab/quantum-garden.html").read_text()
SCRIPT = re.search(r"<script>(.*?)</script>", HTML, re.DOTALL).group(1)

NODE_HARNESS = r"""
const assert = require('node:assert/strict');
const vm = require('node:vm');
const input = JSON.parse(require('node:fs').readFileSync(0, 'utf8'));
function eventTarget(extra = {}) {
    return Object.assign({
        listeners: {},
        addEventListener(type, fn) { (this.listeners[type] ||= []).push(fn); }
    }, extra);
}
const elements = new Map();
function element(id) {
    if (!elements.has(id)) {
        const classes = new Set();
        elements.set(id, eventTarget({
            id, tagName: 'DIV', style: {}, value: '', textContent: '', innerHTML: '',
            classList: {
                add(name) { classes.add(name); }, remove(name) { classes.delete(name); },
                contains(name) { return classes.has(name); }
            },
            focus() { document.activeElement = this; },
            remove() { this.removed = true; },
            appendChild(child) { this.child = child; },
            setPointerCapture(id) { this.pointerId = id; },
            getBoundingClientRect() { return { left: 0, top: 0, width: 120, height: 120 }; }
        }));
    }
    return elements.get(id);
}
const document = eventTarget({
    hidden: false, pointerLockElement: null,
    getElementById: element,
    querySelector() { return element('textarea'); },
    exitPointerLock() { this.pointerLockElement = null; }
});
class Vector3 {
    constructor(x = 0, y = 0, z = 0) { this.set(x, y, z); }
    set(x, y, z) { Object.assign(this, { x, y, z }); return this; }
    setScalar(s) { return this.set(s, s, s); }
    copy(v) { return this.set(v.x, v.y, v.z); }
    clone() { return new Vector3().copy(this); }
    add(v) { return this.set(this.x + v.x, this.y + v.y, this.z + v.z); }
    sub(v) { return this.set(this.x - v.x, this.y - v.y, this.z - v.z); }
    subVectors(a, b) { return this.set(a.x - b.x, a.y - b.y, a.z - b.z); }
    addScaledVector(v, s) { return this.set(this.x + v.x * s, this.y + v.y * s, this.z + v.z * s); }
    multiplyScalar(s) { return this.set(this.x * s, this.y * s, this.z * s); }
    dot(v) { return this.x * v.x + this.y * v.y + this.z * v.z; }
    lengthSq() { return this.dot(this); }
    length() { return Math.sqrt(this.lengthSq()); }
    normalize() { return this.multiplyScalar(1 / (this.length() || 1)); }
    distanceTo(v) { return Math.hypot(this.x - v.x, this.y - v.y, this.z - v.z); }
    toArray(array = [], offset = 0) {
        array[offset] = this.x; array[offset + 1] = this.y; array[offset + 2] = this.z;
        return array;
    }
}
class Color {
    constructor(value = 0xffffff) { this.value = value instanceof Color ? value.value : value; }
    setHex(value) { this.value = value; return this; }
    getHex() { return this.value; }
    setHSL(h, s, l) { this.value = Math.floor(h * 255) * 65536 + Math.floor(s * 255) * 256 +
        Math.floor(l * 255); return this; }
    toArray(array, offset) {
        array[offset] = (this.value >> 16 & 255) / 255;
        array[offset + 1] = (this.value >> 8 & 255) / 255;
        array[offset + 2] = (this.value & 255) / 255;
        return array;
    }
}
class Object3D {
    constructor() {
        this.position = new Vector3(); this.scale = new Vector3(1, 1, 1);
        this.rotation = { x: 0, y: 0, z: 0, order: 'XYZ' }; this.children = [];
    }
    add(object) { this.children.push(object); object.parent = this; }
    remove(object) { this.children = this.children.filter(child => child !== object); object.parent = null; }
    traverse(fn) { fn(this); this.children.forEach(child => child.traverse(fn)); }
}
class Geometry {
    constructor(radius) { this.parameters = { radius }; this.attributes = {}; }
    setAttribute(name, attribute) { this.attributes[name] = attribute; return this; }
    getAttribute(name) { return this.attributes[name]; }
    dispose() { this.disposed = true; }
}
class BufferAttribute {
    constructor(array, itemSize) { Object.assign(this, { array, itemSize, needsUpdate: false }); }
    setUsage(usage) { this.usage = usage; return this; }
}
class Material {
    constructor(options = {}) { Object.assign(this, options); this.color = new Color(options.color); }
    dispose() { this.disposed = true; }
}
class Mesh extends Object3D {
    constructor(geometry, material) { super(); Object.assign(this, { geometry, material }); }
}
class Light extends Object3D {
    constructor(color, intensity, distance) { super(); Object.assign(this,
        { color: new Color(color), intensity, distance }); }
}
class Camera extends Object3D {
    constructor(fov, aspect) { super(); Object.assign(this, { fov, aspect, projections: 0 }); }
    updateProjectionMatrix() { this.projections++; }
}
class Renderer {
    constructor() {
        if (Renderer.fail) throw new Error('WebGL unavailable');
        this.domElement = element('canvas'); this.calls = 0;
    }
    setSize(width, height) { Object.assign(this, { width, height }); }
    setPixelRatio(ratio) { this.pixelRatio = ratio; }
    setClearColor() {}
    render() { this.calls++; }
    dispose() { this.disposed = true; }
}
const math = Object.create(Math);
math.random = () => 0.25;
const THREE = {
    Vector3, Color, Scene: Object3D, Mesh, Points: Mesh, BufferGeometry: Geometry,
    SphereGeometry: Geometry, BufferAttribute, MeshBasicMaterial: Material,
    MeshStandardMaterial: Material, PointsMaterial: Material, AmbientLight: Light,
    DirectionalLight: Light, PointLight: Light, PerspectiveCamera: Camera, WebGLRenderer: Renderer,
    DynamicDrawUsage: 35048, AdditiveBlending: 2, sRGBEncoding: 3001,
    MathUtils: { randFloat: (min, max) => (min + max) / 2, randFloatSpread: value => value / 4 }
};
const storage = new Map();
const localStorage = {
    getItem: key => storage.get(key) ?? null,
    setItem: (key, value) => storage.set(key, value)
};
const window = eventTarget({ THREE, innerWidth: 1200, innerHeight: 800, devicePixelRatio: 3 });
const context = vm.createContext({
    assert, document, window, THREE, localStorage, storage, Renderer, Math: math,
    Date: class extends Date { static now() { return 1700000000000; } },
    navigator: { userAgent: 'test' }, Float32Array, Map,
    console: { log() {}, warn() {}, error() {} },
    requestAnimationFrame: () => 1, cancelAnimationFrame() {},
    setTimeout: () => 1, setInterval: () => 1, clearInterval() {},
    emit(target, type, event = {}) {
        const e = { target, preventDefault() { this.defaultPrevented = true; }, ...event };
        for (const fn of target.listeners[type] || []) fn(e);
        return e;
    }
});
vm.runInContext(input.source, context);
vm.runInContext(`
function makeGarden() {
    const init = QuantumGarden.prototype.init;
    QuantumGarden.prototype.init = function() {};
    let garden;
    try { garden = new QuantumGarden(); } finally { QuantumGarden.prototype.init = init; }
    garden.scene = new Scene();
    garden.camera = new PerspectiveCamera(75, 1.5);
    garden.renderer = new WebGLRenderer();
    return garden;
}
function fixture() {
    return {
        version: '1.0', timestamp: Date.now(),
        player: { position: { x: 0, y: 17, z: 0 }, rotation: { x: -0.2, y: 0.3 }, seeds: 0 },
        islands: [{ position: { x: 0, y: 0, z: 0 }, size: 15, type: 'central', color: 0 }],
        plants: [{ position: { x: 0, y: 15, z: 0 }, growthStage: 0.5,
            color: 0, createdAt: 0, ownerId: 'original-owner' }]
    };
}
`, context);
Promise.resolve(vm.runInContext('(async () => {' + input.test + '\n})()', context))
    .catch(error => { console.error(error); process.exitCode = 1; });
"""


def run_js(test):
    result = subprocess.run(
        ["node", "-e", NODE_HARNESS],
        input=json.dumps({"source": SCRIPT, "test": test}),
        text=True,
        capture_output=True,
        cwd=ROOT,
        timeout=15,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_uses_real_pinned_three_instead_of_non_rendering_stubs():
    assert 'src="https://cdn.jsdelivr.net/npm/three@0.150.0/build/three.min.js"' in HTML
    assert "class WebGLRenderer" not in HTML
    assert "class Color" not in HTML
    assert "THREE.JS R150 MINIMAL BUILD" not in HTML


def test_camera_resize_updates_projection_and_caps_pixel_ratio():
    run_js("""
        const garden = makeGarden();
        garden.setupScene();
        assert.equal(garden.camera.rotation.order, 'YXZ');
        assert.equal(garden.renderer.pixelRatio, 2);
        window.innerWidth = 600;
        garden.onResize();
        assert.equal(garden.camera.aspect, 0.75);
        assert.equal(garden.camera.projections, 1);
        assert.equal(garden.renderer.width, 600);
    """)


def test_generated_plants_are_on_island_surfaces_with_unit_geometry():
    run_js("""
        const garden = makeGarden();
        garden.generateWorld();
        assert.equal(garden.islands.length, 21);
        assert.ok(garden.plants.length >= 5);
        assert.equal(garden.waterfalls.length, 3);
        for (const plant of garden.plants) {
            assert.ok(plant.island);
            assert.ok(Math.abs(plant.position.distanceTo(plant.island.position) - plant.island.size) < 1e-10);
            assert.equal(plant.mesh.geometry.parameters.radius, 1);
            assert.equal(plant.mesh.scale.x, 0.5 + plant.growthStage * 2);
        }
    """)


def test_particles_and_waterfalls_have_animated_gpu_buffers():
    run_js("""
        const garden = makeGarden();
        garden.createParticleField();
        const island = garden.createIsland(new Vector3(), 15, 'central');
        garden.createWaterfall(island);
        const particlePositions = garden.particleMesh.geometry.getAttribute('position');
        const waterfall = garden.waterfalls[0];
        const waterfallPositions = waterfall.mesh.geometry.getAttribute('position');
        assert.equal(particlePositions.array.length, 1500);
        assert.equal(waterfallPositions.array.length, 150);
        assert.ok(garden.scene.children.includes(garden.particleMesh));
        assert.ok(garden.scene.children.includes(waterfall.mesh));
        const particleX = particlePositions.array[0], waterfallY = waterfallPositions.array[1];
        garden.updateParticles(1 / 60);
        garden.updateWaterfalls(1 / 60);
        assert.notEqual(particlePositions.array[0], particleX);
        assert.equal(waterfallPositions.array[1], waterfallY + 0.5);
        assert.equal(particlePositions.needsUpdate, true);
        assert.equal(waterfallPositions.needsUpdate, true);
    """)


@pytest.mark.parametrize("fps", [30, 60, 120])
def test_movement_and_growth_are_frame_rate_independent(fps):
    run_js(f"""
        const garden = makeGarden();
        garden.keys.KeyW = true;
        const plant = garden.createPlant(new Vector3(0, 15, 0), 0.4);
        for (let i = 0; i < {fps}; i++) {{
            garden.updatePlayer(1 / {fps});
            garden.updatePlants(1 / {fps});
        }}
        assert.ok(Math.abs(garden.player.position.z + 12) < 1e-10);
        assert.ok(Math.abs(plant.growthStage - 0.46) < 1e-10);
        assert.ok(Math.abs(plant.mesh.scale.x - 1.42) < 1e-10);
    """)


def test_collision_keeps_a_unit_normal_and_does_not_launch_player():
    run_js("""
        const garden = makeGarden();
        garden.createIsland(new Vector3(), 15, 'central');
        garden.player.position.set(0, 15.5, 0);
        garden.player.velocity.set(0, -0.2, 0);
        garden.updatePhysics(1 / 60);
        assert.equal(garden.player.position.y, 16);
        assert.ok(garden.player.velocity.length() < 1e-10);
        assert.equal(garden.player.isGrounded, true);
        garden.jump();
        assert.equal(garden.player.velocity.y, 0.5);
        for (let i = 0; i < 180; i++) {
            garden.updatePlayer(1 / 60);
            garden.updatePhysics(1 / 60);
            assert.ok(garden.player.velocity.length() < 1);
        }
        assert.ok(Math.abs(garden.player.position.y - 16) < 1e-10);
        assert.equal(garden.player.isGrounded, true);
    """)


def test_center_collision_and_respawn_use_the_actual_island():
    run_js("""
        const garden = makeGarden();
        const island = garden.createIsland(new Vector3(40, 20, 10), 8, 'central');
        garden.player.position.copy(island.position);
        garden.updatePhysics(1 / 60);
        assert.equal(garden.player.position.y, 29);
        garden.player.position.y = -200;
        garden.updatePhysics(1 / 60);
        assert.equal(garden.player.position.x, 40);
        assert.equal(garden.player.position.y, 30);
        assert.equal(garden.player.position.z, 10);
        assert.equal(garden.player.velocity.length(), 0);
    """)


def test_player_can_jump_from_the_starting_island_to_a_surrounding_island():
    run_js("""
        const garden = makeGarden();
        garden.createIsland(new Vector3(), 15, 'central');
        garden.createIsland(new Vector3(40, 0, 0), 10, 'ring');
        garden.player.position.set(0, 16, 0);
        garden.keys.KeyD = true;
        let reachedRing = false;
        for (let i = 0; i < 600; i++) {
            if (i === 20) garden.jump();
            garden.updatePlayer(1 / 60);
            garden.updatePhysics(1 / 60);
            if (garden.player.currentIsland?.type === 'ring' && garden.player.isGrounded) {
                reachedRing = true;
                break;
            }
        }
        assert.equal(reachedRing, true);
    """)


def test_planting_and_collecting_persist_even_when_seeds_reach_zero():
    run_js("""
        const garden = makeGarden();
        const island = garden.createIsland(new Vector3(), 15, 'central');
        island.mesh.position.y = 0.5;
        garden.player.position.set(0, 16.5, 0);
        garden.player.currentIsland = island;
        garden.player.seeds = 1;
        garden.plantSeed();
        assert.equal(garden.plants.length, 1);
        assert.equal(garden.player.seeds, 0);
        assert.ok(Math.abs(garden.plants[0].position.length() - 15) < 1e-10);
        assert.equal(JSON.parse(storage.get('quantum_garden_state')).player.seeds, 0);
        garden.plantSeed();
        assert.equal(garden.plants.length, 1);
        garden.collectSeed();
        assert.equal(JSON.parse(storage.get('quantum_garden_state')).player.seeds, 1);
    """)


def test_json_and_local_save_roundtrip_preserve_layout_colors_and_metadata():
    run_js("""
        const garden = makeGarden();
        const state = fixture();
        state.plants[0].ownerId = '</textarea><img src=x>';
        assert.equal(garden.importWorld(JSON.stringify(state)), true);
        assert.deepEqual(garden.getWorldState(), state);
        const json = garden.exportWorld();
        assert.deepEqual(JSON.parse(json), state);
        assert.equal(document.getElementById('export-data').value, json);
        assert.ok(!document.getElementById('modal-body').innerHTML.includes(state.plants[0].ownerId));
        const reopened = makeGarden();
        assert.equal(reopened.loadState(), true);
        assert.deepEqual(reopened.getWorldState(), state);
        assert.equal(reopened.plants[0].mesh.material.color.getHex(), 0);
        assert.equal(reopened.plants[0].light.color.getHex(), 0);
        assert.equal(reopened.player.velocity.length(), 0);
        assert.equal(reopened.player.currentIsland, null);
    """)


def test_startup_restores_saved_world_without_generating_duplicates():
    run_js("""
        const state = fixture();
        storage.set('quantum_garden_state', JSON.stringify(state));
        const garden = new QuantumGarden();
        assert.equal(garden.islands.length, 1);
        assert.equal(garden.plants.length, 1);
        assert.equal(garden.waterfalls.length, 1);
        assert.equal(garden.particles.length, 500);
        assert.equal(garden.player.seeds, 0);
        assert.equal(garden.plants[0].createdAt, 0);
        assert.equal(garden.renderer.calls, 1);
    """)


def test_legacy_saves_restore_plants_and_migrate_to_complete_world_state():
    run_js("""
        const state = fixture();
        delete state.version;
        delete state.islands;
        delete state.player.rotation;
        storage.set('quantum_garden_state', JSON.stringify(state));
        const garden = new QuantumGarden();
        assert.equal(garden.islands.length, 21);
        assert.equal(garden.plants.length, 1);
        assert.equal(garden.player.seeds, 0);
        assert.equal(garden.plants[0].color.getHex(), 0);
        assert.equal(garden.saveState(), true);
        const migrated = JSON.parse(storage.get('quantum_garden_state'));
        assert.equal(migrated.version, '1.0');
        assert.equal(migrated.islands.length, 21);
        const reopened = new QuantumGarden();
        assert.deepEqual(reopened.getWorldState().islands, migrated.islands);
        assert.equal(reopened.plants.length, 1);
    """)


@pytest.mark.parametrize(
    "mutation",
    [
        "state.version = '2.0'",
        "delete state.islands",
        "state.islands = []",
        "state.islands[0].size = 0",
        "state.islands[0].position.x = 'NaN'",
        "state.player.seeds = -1",
        "state.player.rotation = null",
        "state.plants[0].color = -1",
        "state.plants[0].growthStage = null",
        "state.plants[0].ownerId = {}",
    ],
)
def test_invalid_import_is_rejected_before_replacing_the_live_world(mutation):
    run_js("""
        const garden = makeGarden();
        garden.importWorld(JSON.stringify(fixture()));
        const previous = JSON.stringify(garden.getWorldState());
        const mesh = garden.islands[0].mesh;
        const saved = storage.get('quantum_garden_state');
        const state = fixture();
    """ + mutation + """;
        assert.equal(garden.importWorld(JSON.stringify(state)), false);
        assert.equal(JSON.stringify(garden.getWorldState()), previous);
        assert.equal(garden.islands[0].mesh, mesh);
        assert.equal(mesh.geometry.disposed, undefined);
        assert.equal(storage.get('quantum_garden_state'), saved);
        assert.match(document.getElementById('import-error').textContent, /unchanged/);
    """)


def test_malformed_json_is_non_destructive_and_corrupt_saves_can_start():
    run_js("""
        const garden = makeGarden();
        garden.importWorld(JSON.stringify(fixture()));
        const previous = JSON.stringify(garden.getWorldState());
        assert.equal(garden.importWorld('{bad'), false);
        assert.equal(JSON.stringify(garden.getWorldState()), previous);
        storage.set('quantum_garden_state', '{bad');
        const fresh = new QuantumGarden();
        assert.equal(fresh.islands.length, 21);
        assert.ok(fresh.plants.length >= 5);
        assert.match(document.getElementById('save-status').textContent, /Saved world unavailable/);
    """)


def test_blocked_storage_does_not_prevent_rendering_or_json_export():
    run_js("""
        localStorage.getItem = () => { throw new Error('Storage blocked'); };
        localStorage.setItem = () => { throw new Error('Storage blocked'); };
        const garden = new QuantumGarden();
        assert.equal(garden.islands.length, 21);
        assert.equal(garden.renderer.calls, 1);
        assert.equal(garden.saveState(), false);
        garden.collectSeed();
        assert.equal(JSON.parse(garden.exportWorld()).player.seeds, 11);
        assert.match(document.getElementById('save-status').textContent, /Export World/);
    """)


def test_clearing_world_disposes_meshes_and_waterfalls_but_keeps_particle_field():
    run_js("""
        const garden = makeGarden();
        garden.createParticleField();
        garden.generateWorld();
        const oldMeshes = [...garden.islands, ...garden.plants, ...garden.waterfalls].map(item => item.mesh);
        const field = garden.particleMesh;
        garden.player.currentIsland = garden.islands[0];
        garden.clearWorld();
        assert.equal(garden.islands.length + garden.plants.length + garden.waterfalls.length, 0);
        assert.equal(garden.player.currentIsland, null);
        for (const mesh of oldMeshes) {
            assert.equal(mesh.geometry.disposed, true);
            assert.equal(mesh.material.disposed, true);
            assert.ok(!garden.scene.children.includes(mesh));
        }
        assert.ok(garden.scene.children.includes(field));
        assert.equal(field.geometry.disposed, undefined);
    """)


def test_keyboard_does_not_move_or_plant_while_typing_and_blur_clears_input():
    run_js("""
        const garden = makeGarden();
        garden.createIsland(new Vector3(), 15, 'central');
        garden.player.currentIsland = garden.islands[0];
        garden.setupControls();
        emit(window, 'keydown', { code: 'KeyW', target: { tagName: 'TEXTAREA' } });
        assert.equal(garden.keys.KeyW, undefined);
        emit(window, 'keydown', { code: 'KeyW', target: garden.renderer.domElement });
        assert.equal(garden.keys.KeyW, true);
        emit(window, 'blur');
        assert.equal(garden.keys.KeyW, undefined);
        garden.showImportModal();
        emit(window, 'keydown', { code: 'KeyP' });
        assert.equal(garden.plants.length, 0);
        garden.hideModal();
        emit(window, 'keydown', { code: 'KeyP' });
        emit(window, 'keydown', { code: 'KeyP', repeat: true });
        assert.equal(garden.plants.length, 1);
    """)


def test_rejected_pointer_lock_keeps_drag_look_and_click_planting_available():
    run_js("""
        const garden = makeGarden();
        garden.createIsland(new Vector3(), 15, 'central');
        garden.player.currentIsland = garden.islands[0];
        garden.setupControls();
        const canvas = garden.renderer.domElement;
        canvas.requestPointerLock = () => Promise.reject(new Error('Permission denied'));
        emit(canvas, 'click', { pointerType: 'mouse' });
        await Promise.resolve();
        assert.equal(garden.pointerLockUnavailable, true);
        emit(canvas, 'pointerdown', { button: 0, pointerId: 1, clientX: 100, clientY: 100 });
        emit(canvas, 'pointermove', { pointerId: 1, clientX: 120, clientY: 110 });
        emit(canvas, 'pointerup', { pointerId: 1 });
        emit(canvas, 'click', { pointerType: 'mouse' });
        assert.equal(garden.player.rotation.y, -0.04);
        assert.equal(garden.plants.length, 0);
        emit(canvas, 'pointerdown', { button: 0, pointerId: 1, clientX: 120, clientY: 110 });
        emit(canvas, 'pointerup', { pointerId: 1 });
        emit(canvas, 'click', { pointerType: 'mouse' });
        assert.equal(garden.plants.length, 1);
    """)


def test_mobile_joystick_tracks_its_pointer_and_cancellation_stops_movement():
    assert "@media (max-width: 768px), (pointer: coarse)" in HTML
    run_js("""
        const garden = makeGarden();
        garden.setupTouchControls();
        const joystick = document.getElementById('joystick');
        emit(joystick, 'pointerdown', { pointerId: 7, clientX: 60, clientY: 20 });
        assert.equal(garden.keys.KeyW, true);
        assert.equal(joystick.pointerId, 7);
        assert.equal(document.getElementById('joystick-knob').style.top, 'calc(50% + -35px)');
        emit(joystick, 'pointermove', { pointerId: 8, clientX: 100, clientY: 100 });
        assert.equal(garden.keys.KeyW, true);
        emit(joystick, 'pointercancel', { pointerId: 8 });
        assert.equal(garden.keys.KeyW, true);
        garden.touch.active = true;
        emit(joystick, 'pointercancel', { pointerId: 7 });
        assert.equal(garden.keys.KeyW, undefined);
        assert.equal(garden.touch.active, true);
        assert.equal(document.getElementById('joystick-knob').style.top, '50%');
    """)


@pytest.mark.parametrize("failure", ["window.THREE = undefined", "Renderer.fail = true"])
def test_startup_failures_are_actionable_instead_of_blank_canvases(failure):
    run_js(failure + """;
        emit(window, 'load');
        assert.equal(app, null);
        assert.match(document.getElementById('loading-message').textContent, /reload/);
    """)


def test_pagehide_saves_without_destroying_a_back_forward_cache_entry():
    run_js("""
        app = makeGarden();
        app.importWorld(JSON.stringify(fixture()));
        app.player.seeds = 4;
        app.keys.KeyW = true;
        emit(window, 'pagehide');
        assert.equal(JSON.parse(storage.get('quantum_garden_state')).player.seeds, 4);
        assert.equal(app.keys.KeyW, undefined);
        assert.equal(app.renderer.disposed, undefined);
        assert.equal(app.renderer.domElement.removed, undefined);
        app.player.seeds = 2;
        document.hidden = true;
        emit(document, 'visibilitychange');
        assert.equal(JSON.parse(storage.get('quantum_garden_state')).player.seeds, 2);
    """)
