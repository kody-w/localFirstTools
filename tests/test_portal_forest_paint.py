"""Deterministic inline-runtime gates; settled canvas pixels are checked in Chrome."""

import json
from pathlib import Path
import re
import subprocess

import pytest


ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "forest": ROOT / "exhibitions/ai-research/fractal-forest.html",
    "paint": ROOT / "exhibitions/visual-arts/living-paint-dimension.html",
}

HARNESS = r"""
const assert = require('node:assert/strict');
const vm = require('node:vm');
const input = JSON.parse(require('node:fs').readFileSync(0, 'utf8'));
const elements = new Map(), storage = new Map(), downloads = [], images = [];
let randomState = 123456, rafCalls = 0, imageHold = false;
const faults = { read: false, write: false };
function target(extra = {}) {
    return Object.assign({
        listeners: {},
        addEventListener(name, callback) { (this.listeners[name] ||= []).push(callback); },
        dispatchEvent(event) {
            event.target ||= this;
            for (const callback of this.listeners[event.type] || []) callback(event);
        }
    }, extra);
}
function context2d() {
    return {
        calls: [], globalAlpha: 1, globalCompositeOperation: 'source-over',
        beginPath() { this.path = []; },
        moveTo(x, y) { this.path.push(['moveTo', x, y]); },
        lineTo(x, y) { this.path.push(['lineTo', x, y]); },
        stroke() { this.calls.push(['stroke', this.lineWidth, this.strokeStyle, this.path]); },
        fill() { this.calls.push(['fill', this.fillStyle, this.path]); },
        arc(x, y, radius) {
            assert.ok([x, y, radius].every(Number.isFinite) && radius >= 0, 'finite positive arc');
            this.path.push(['arc', x, y, radius]);
        },
        ellipse(x, y, rx, ry) {
            assert.ok([x, y, rx, ry].every(Number.isFinite) && rx >= 0 && ry >= 0);
            this.path.push(['ellipse', x, y, rx, ry]);
        },
        fillRect(...args) { this.calls.push(['fillRect', ...args]); },
        clearRect() { this.bitmap = 'data:image/png;base64,Y2xlYXI='; },
        drawImage(image) { this.bitmap = image.src; },
        getImageData() { return { data: new Uint8ClampedArray(4) }; },
        putImageData() {}, save() {}, restore() {}, translate() {}, rotate() {},
        fillText() {},
        createLinearGradient() { return { addColorStop() {} }; },
        createRadialGradient() { return { addColorStop() {} }; }
    };
}
function element(id) {
    if (!elements.has(id)) {
        const classes = new Set(), ctx = context2d();
        elements.set(id, target({
            id, style: {}, value: '', textContent: '', hidden: false, tagName: 'DIV',
            width: 1200, height: 800, parentElement: { clientWidth: 1280, clientHeight: 900 },
            classList: {
                add: name => classes.add(name), remove: name => classes.delete(name),
                contains: name => classes.has(name)
            },
            getContext: () => ctx,
            toDataURL: () => ctx.bitmap || 'data:image/png;base64,YXJ0',
            getBoundingClientRect: () => ({ left: 0, top: 0, width: 1200, height: 800 }),
            requestPointerLock() { document.pointerLockElement = this; },
            setAttribute() {}, appendChild() {}, remove() {}, click() {},
            focus() { document.activeElement = this; }
        }));
    }
    return elements.get(id);
}
const document = target({
    pointerLockElement: null, activeElement: null,
    getElementById: element,
    createElement: name => element('created-' + name + '-' + elements.size),
    body: { appendChild() {} }, head: { appendChild() {} },
    exitPointerLock() { this.pointerLockElement = null; }
});
const window = target({ innerWidth: 1200, innerHeight: 800 });
const localStorage = {
    getItem(key) {
        if (faults.read) throw new DOMException('Storage denied', 'SecurityError');
        return storage.get(key) ?? null;
    },
    setItem(key, value) {
        if (faults.write) throw new DOMException('Storage full', 'QuotaExceededError');
        storage.set(key, value);
    },
    removeItem(key) { storage.delete(key); }
};
class Image {
    constructor() { this.width = this.naturalWidth = 1200; this.height = this.naturalHeight = 800; }
    set src(value) {
        this.value = value;
        const complete = () => value.includes('INVALID') ? this.onerror() : this.onload();
        if (imageHold) images.push(complete); else queueMicrotask(complete);
    }
    get src() { return this.value; }
}
const math = Object.create(Math);
math.random = () => {
    randomState = (Math.imul(randomState, 1664525) + 1013904223) >>> 0;
    return randomState / 4294967296;
};
const context = vm.createContext({
    assert, document, window, storage, localStorage, faults, downloads, images, Image,
    Blob, DOMException, Map, Math: math, Number, Uint8ClampedArray,
    URL: { createObjectURL(blob) { downloads.push(blob); return 'blob:test'; }, revokeObjectURL() {} },
    Date: class extends Date {
        constructor(...args) { super(...(args.length ? args : [1788620000000])); }
        static now() { return 1788620000000; }
    },
    performance: { now: () => 1000 },
    console: { log() {}, warn() {}, error() {} },
    requestAnimationFrame() { return ++rafCalls; }, cancelAnimationFrame() {},
    setTimeout: () => 1, clearTimeout() {}, setInterval: () => 1,
    confirm: () => true, alert() {},
    holdImages(value) { imageHold = value; },
    rafCount: () => rafCalls,
    emit(target, type, event = {}) {
        target.dispatchEvent({ type, key: '', preventDefault() {}, ...event });
    }
});
vm.runInContext(input.source, context);
vm.runInContext(`
    const copy = value => JSON.parse(JSON.stringify(value));
    function geometry(forest) {
        return JSON.stringify(forest.trees);
    }
    function drawing(forest) {
        forest.ctx.calls = [];
        forest.render();
        return JSON.stringify(forest.ctx.calls);
    }
    function countBranches(branches) {
        return branches.reduce((n, b) => n + 1 + countBranches(b.subBranches), 0);
    }
    function paintFixture(paint) {
        paint.createPaintStroke({x:100,y:200}, {x:500,y:200});
        paint.createPaintStroke({x:100,y:400}, {x:500,y:400});
        paint.brushSize = 50;
    }
`, context);
vm.runInContext('(async () => {' + input.scenario + '})()', context)
    .catch(error => { console.error(error); process.exitCode = 1; });
"""


def run_scenario(world, scenario, mutation=None):
    source = re.search(r"<script>(.*?)</script>", PAGES[world].read_text(), re.S).group(1)
    if mutation:
        before, after = mutation
        assert before in source, f"Mutation target missing: {before}"
        source = source.replace(before, after, 1)
    return subprocess.run(
        ["node", "-e", HARNESS],
        input=json.dumps({"source": source, "scenario": scenario}),
        text=True, capture_output=True, cwd=ROOT, timeout=20,
    )


def check(world, scenario):
    result = run_scenario(world, scenario)
    assert result.returncode == 0, result.stdout + result.stderr


FOREST_REPLAY = r"""
    const forest = new FractalForestEngine();
    const before = geometry(forest), pixels = drawing(forest);
    forest.saveState();
    assert.equal(forest.loadState(), true);
    assert.equal(geometry(forest), before, 'saved seeds reconstruct actual branches');
    assert.equal(drawing(forest), pixels, 'saved camera and geometry replay draw commands');
    forest.exportData();
    const portable = JSON.parse(await downloads.at(-1).text());
    forest.generateForest();
    assert.equal(forest.importData(portable), true);
    assert.equal(geometry(forest), before);
    const reopened = new FractalForestEngine();
    assert.equal(reopened.loadState(), true);
    assert.equal(geometry(reopened), before);
"""


def test_forest_save_import_and_reentry_reconstruct_branches():
    check("forest", FOREST_REPLAY)


FOREST_SCALE = r"""
    const forest = new FractalForestEngine();
    const visible = forest.trees.filter(tree => {
        const p = forest.project(tree.pos);
        return p && p.x >= 0 && p.x <= forest.width && p.y >= 0 && p.y <= forest.height;
    });
    assert.ok(visible.length >= 8, 'the default camera frames the grove');
    const point = new Vector3(10, 8, 0);
    const before = copy(forest.project(point));
    forest.setScale(48);
    assert.notDeepEqual(copy(forest.project(point)), before, 'scale reaches projection');
    forest.setScale(100);
    const macro = drawing(forest), macroDepth = forest.recursionDepth;
    forest.setScale(0);
    assert.notEqual(drawing(forest), macro, 'micro and macro draw different geometry');
    assert.notEqual(forest.recursionDepth, macroDepth, 'detail follows the explored layer');
    for (const tree of forest.trees) assert.ok(countBranches(tree.branches) <= 256);
    const scale = forest.scale;
    assert.equal(forest.setScale(NaN), false);
    assert.equal(forest.setScale(Infinity), false);
    assert.equal(forest.scale, scale);
    assert.equal(forest.project(new Vector3(Infinity, 0, 0)), null);
    forest.setScale(50);
    assert.equal(forest.project(forest.camera.pos), null);
    assert.equal(forest.project(new Vector3(Number.MAX_VALUE, 0, 0)), null);
    assert.equal(forest.project(new Vector3(0, 0, -10000)), null);
    assert.equal(forest.project(new Vector3(0, 0, 10000)), null);
    for (const scale of [-100, 5, 16, 25, 33, 50, 66, 75, 83, 95, 1000]) {
        forest.setScale(scale);
        assert.ok(forest.worldZoom > 0 && forest.worldZoom <= Math.sqrt(10) + 1e-10);
        forest.render();
        assert.ok(forest.trees.length <= 12);
        for (const tree of forest.trees) assert.ok(countBranches(tree.branches) <= 256);
    }
"""


def test_forest_scale_reaches_projection_and_bounded_layer_geometry():
    check("forest", FOREST_SCALE)


FOREST_LEAF = r"""
    const forest = new FractalForestEngine();
    forest.render();
    const target = forest.leafTargets.find(leaf => leaf.x > 230 && leaf.x < 900
        && leaf.y > 100 && leaf.y < 650);
    assert.ok(target, 'actual drawn leaves expose a hit target');
    const before = geometry(forest), layer = forest.layer;
    emit(forest.canvas, 'click', {clientX:target.x, clientY:target.y});
    assert.notEqual(geometry(forest), before, 'clicking a visible leaf enters its seeded ecosystem');
    assert.notEqual(forest.layer, layer);
    assert.equal(document.pointerLockElement, null, 'leaf click is not swallowed by mouse look');
    const child = geometry(forest);
    forest.jumpLayer();
    assert.notEqual(geometry(forest), child, 'Space explores another actual layer');
    forest.setScale(50);
    assert.equal(geometry(forest), before, 'returning to the parent restores its grove');
"""


def test_forest_leaf_hit_and_space_enter_repeatable_ecosystems():
    check("forest", FOREST_LEAF)


def test_forest_space_after_slider_and_repeated_keys_keep_controls_usable():
    check("forest", r"""
        const forest = new FractalForestEngine();
        const slider = document.getElementById('scale-slider');
        slider.tagName = 'INPUT';
        slider.type = 'range';
        forest.setScale(0);
        emit(document, 'keydown', {target:slider, key:' ', repeat:false});
        assert.equal(forest.layer, -3, 'Space remains usable immediately after changing the slider');
        const before = geometry(forest);
        emit(document, 'keydown', {target:slider, key:' ', repeat:true});
        assert.equal(geometry(forest), before, 'held Space must not repeatedly generate new layers');
        emit(document, 'keydown', {key:'w'});
        const camera = copy(forest.camera.pos);
        forest.updateCamera(1);
        assert.ok(Math.hypot(forest.camera.pos.x-camera.x, forest.camera.pos.z-camera.z) <= 1.00001);
        assert.notDeepEqual(copy(forest.camera.pos), camera, 'W moves at a usable bounded local speed');
        emit(window, 'blur');
        assert.equal(Object.keys(forest.keys).length, 0);
    """)


def test_forest_legacy_and_invalid_imports_are_transactional():
    check("forest", r"""
        const forest = new FractalForestEngine();
        const state = forest.saveState();
        const legacy = {camera:copy(state.camera), scale:1, recursionDepth:3, trees:copy(state.trees)};
        assert.equal(forest.importData(legacy), true);
        const before = geometry(forest), saved = storage.get('fractalForestState');
        for (const scale of [0, -1, Infinity, '1', null]) {
            assert.equal(forest.importData({...legacy, scale}), false);
            assert.equal(geometry(forest), before);
            assert.equal(storage.get('fractalForestState'), saved);
        }
        assert.equal(forest.importData({...legacy, recursionDepth:100}), false);
        assert.equal(forest.importData({...legacy, trees:Array(500).fill(legacy.trees[0])}), false);
        storage.set('fractalForestState', '{"broken":');
        assert.equal(forest.loadState(), false);
        assert.equal(storage.get('fractalForestState'), '{"broken":');
        assert.equal(geometry(forest), before);
    """)


PAINT_ERASE = r"""
    const paint = new LivingPaintDimension();
    await paint.ready;
    paintFixture(paint);
    const distant = copy(paint.paintStrokes[1]);
    paint.erase({x:300, y:200});
    assert.equal(paint.paintStrokes.length, 3, 'a long live stroke splits around the eraser');
    assert.deepEqual(copy(paint.paintStrokes.at(-1)), distant, 'un-erased work survives');
    const fragments = paint.paintStrokes.filter(stroke => stroke.start.y === 200);
    assert.ok(fragments.some(stroke => stroke.end.x <= 240.001));
    assert.ok(fragments.some(stroke => stroke.start.x >= 359.999));
    for (let i = 0; i < 12; i++) { paint.updateEntities(16); paint.renderEntities(); }
    assert.equal(paint.paintStrokes.length, 3, 'the next frames cannot replay deleted content');
    paint.createAnimatedStroke({x:290,y:200}, {x:310,y:200});
    paint.updateEntities(16);
    assert.ok(paint.paintStrokes.some(stroke => stroke.start.x === 290),
        'new art may cross a previously erased region');
"""


def test_paint_erasure_edits_live_segments_and_allows_new_art():
    check("paint", PAINT_ERASE)


def test_paint_swept_eraser_removes_intersected_entities_not_distant_work():
    check("paint", r"""
        const paint = new LivingPaintDimension();
        await paint.ready;
        paintFixture(paint);
        paint.createFlower({x:300,y:200});
        paint.createFlower({x:100,y:400});
        paint.lastPos = {x:300,y:200};
        paint.performJump();
        paint.performSpin();
        paint.performDash();
        paint.lastPos = {x:1000,y:600};
        paint.performSpin();
        paint.erase({x:300,y:300}, {x:300,y:100});
        assert.equal(paint.paintStrokes.length, 3, 'a fast drag erases the whole swept path');
        assert.equal(paint.flowers.length, 1);
        assert.ok(paint.flowers[0].y > 350);
        assert.equal(paint.creatures.length, 0);
        assert.equal(paint.comets.length, 0);
        assert.equal(paint.galaxies.length, 1);
        assert.equal(paint.galaxies[0].x, 1000, 'only the touched living galaxy is removed');
        paint.createPaintStroke({x:300,y:200}, {x:300,y:200});
        paint.erase({x:300,y:200});
        assert.ok(!paint.paintStrokes.some(stroke => stroke.start.x === 300 && stroke.end.x === 300));
    """)


def test_paint_capsule_clipping_preserves_diagonal_parallel_and_tangent_work():
    check("paint", r"""
        const paint = new LivingPaintDimension();
        await paint.ready;
        const cases = [
            [{x:0,y:0}, {x:100,y:100}, {x:40,y:30}, {x:60,y:80}, 10],
            [{x:100,y:100}, {x:0,y:0}, {x:40,y:30}, {x:60,y:80}, 10],
            [{x:0,y:0}, {x:100,y:0}, {x:50,y:0}, {x:80,y:0}, 5],
            [{x:0,y:0}, {x:100,y:0}, {x:50,y:10}, {x:50,y:10}, 10]
        ];
        for (const [start, end, from, to, radius] of cases) {
            const pieces = paint.strokeOutsideEraser({start, end, color:'#ff00ff'}, from, to, radius);
            const dx = end.x - start.x, dy = end.y - start.y, length = dx*dx + dy*dy;
            const parameter = point => ((point.x-start.x)*dx + (point.y-start.y)*dy) / length;
            for (let i = 0; i <= 500; i++) {
                const t = i / 500, point = {x:start.x + t*dx, y:start.y + t*dy};
                const distance = paint.distanceToSegment(point, from, to);
                const covered = pieces.some(piece => t >= parameter(piece.start)-1e-8 &&
                    t <= parameter(piece.end)+1e-8);
                if (distance > radius+1e-6) assert.equal(covered, true, 'un-erased segment preserved');
                if (distance < radius-1e-6) assert.equal(covered, false, 'intersected segment removed');
            }
        }
    """)


def test_paint_erased_state_roundtrips_through_export_import_and_storage():
    check("paint", r"""
        const paint = new LivingPaintDimension();
        await paint.ready;
        paintFixture(paint);
        paint.erase({x:300,y:200});
        paint.exportData();
        const portable = JSON.parse(await downloads.at(-1).text());
        assert.equal(portable.paintStrokes.length, 3);
        assert.equal(paint.saveToStorage(), true);
        const reopened = new LivingPaintDimension();
        await reopened.ready;
        assert.deepEqual(copy(reopened.paintStrokes), copy(paint.paintStrokes));
        reopened.clearCanvas();
        assert.equal(await reopened.restoreData(portable), true);
        assert.equal(reopened.saveToStorage(), true);
        assert.deepEqual(copy(reopened.paintStrokes), copy(paint.paintStrokes));
        assert.equal(JSON.parse(storage.get('livingPaintDimension')).canvasData, portable.canvasData,
            'save captures the decoded imported bitmap, not the previous canvas');
    """)


PAINT_STORAGE = r"""
    faults.read = true;
    faults.write = true;
    const paint = new LivingPaintDimension();
    await paint.ready;
    paintFixture(paint);
    assert.ok(rafCount() > 0, 'drawing initializes without browser storage');
    assert.equal(paint.saveToStorage(), false);
    const status = document.getElementById('storageStatus');
    assert.equal(status.hidden, false);
    assert.match(status.textContent, /export/i);
    paint.exportData();
    const portable = JSON.parse(await downloads.at(-1).text());
    assert.equal(portable.paintStrokes.length, 2, 'portable export does not need localStorage');
"""


def test_paint_storage_denial_keeps_drawing_and_export_with_visible_warning():
    check("paint", PAINT_STORAGE)


PAINT_CORRUPTION = r"""
        storage.set('livingPaintDimension', '{"recoverable":');
        const paint = new LivingPaintDimension();
        await paint.ready;
        paintFixture(paint);
        assert.equal(paint.saveToStorage(), false);
        assert.equal(storage.get('livingPaintDimension'), '{"recoverable":',
            'autosave must not overwrite a corrupt but recoverable record');
        assert.match(document.getElementById('storageStatus').textContent, /export/i);
        paint.clearCanvas();
        paintFixture(paint);
        faults.write = true;
        const previous = storage.get('livingPaintDimension');
        assert.equal(paint.saveToStorage(), false);
        assert.equal(storage.get('livingPaintDimension'), previous);
        faults.write = false;
        assert.equal(paint.saveToStorage(), true);
        assert.equal(document.getElementById('storageStatus').hidden, true);
"""


def test_paint_quota_and_corruption_preserve_recoverable_storage():
    check("paint", PAINT_CORRUPTION)


def test_paint_daily_reset_waits_for_restore_and_persists_the_reset():
    check("paint", r"""
        const paint = new LivingPaintDimension();
        await paint.ready;
        paintFixture(paint);
        const saved = paint.serializeData();
        saved.lastReset = new Date(Date.now()-86400000).toDateString();
        storage.set('livingPaintDimension', JSON.stringify(saved));
        storage.set('lpd_lastReset', saved.lastReset);
        const nextDay = new LivingPaintDimension();
        await nextDay.ready;
        assert.equal(nextDay.paintStrokes.length, 0);
        assert.equal(nextDay.canvas.toDataURL(), 'data:image/png;base64,Y2xlYXI=');
        assert.equal(JSON.parse(storage.get('livingPaintDimension')).paintStrokes.length, 0);
        assert.equal(nextDay.lastReset, new Date().toDateString());
    """)


PAINT_IMPORT = r"""
        const paint = new LivingPaintDimension();
        await paint.ready;
        paintFixture(paint);
        paint.exportData();
        const portable = JSON.parse(await downloads.at(-1).text());
        const before = JSON.stringify(paint.paintStrokes);
        for (const bad of [
            {...portable, paintStrokes:'not an array'},
            {...portable, flowers:[{x:0,y:0,size:-10}]},
            {...portable, canvasData:'https://example.test/picture.png'},
            {...portable, canvasData:'data:image/png;base64,INVALID'}
        ]) {
            await assert.rejects(() => paint.restoreData(bad));
            assert.equal(JSON.stringify(paint.paintStrokes), before);
        }
        holdImages(true);
        const pending = paint.restoreData(portable);
        paint.clearCanvas();
        images.splice(0).forEach(complete => complete());
        assert.equal(await pending, false, 'a pending image cannot undo Clear or later erasure');
        assert.equal(paint.paintStrokes.length, 0);
"""


def test_paint_invalid_import_and_stale_image_do_not_restore_erased_art():
    check("paint", PAINT_IMPORT)


@pytest.mark.parametrize("world,scenario,mutation", [
    ("forest", FOREST_REPLAY,
     ("const random = this.seededRandom(tree.seed);", "const random = Math.random;")),
    ("forest", FOREST_SCALE,
     ("this.worldZoom = Math.pow(10, -Math.log10(scale) - this.layer);", "this.worldZoom = 1;")),
    ("forest", FOREST_SCALE,
     ("let remaining = 256;", "let remaining = 100000;")),
    ("forest", FOREST_LEAF,
     ("if (leaf) {", "if (false && leaf) {")),
    ("forest", FOREST_LEAF,
     ("this.setScale(50 - next * 100 / 6);", "this.updateScaleUI();")),
    ("paint", PAINT_ERASE,
     ("this.paintStrokes = this.paintStrokes.flatMap(", "[].flatMap(")),
    ("paint", PAINT_STORAGE,
     ("this.checkDailyReset();", "localStorage.getItem('lpd_lastReset'); this.checkDailyReset();")),
    ("paint", PAINT_STORAGE,
     ("status.hidden = false;", "status.hidden = true;")),
    ("paint", PAINT_CORRUPTION,
     ("if (this.restoring || this.preserveStoredData) return false;", "if (this.restoring) return false;")),
    ("paint", PAINT_IMPORT,
     ("const valid = this.validateData(data);", "const valid = data;")),
    ("paint", PAINT_IMPORT,
     ("if (sequence !== this.restoreSequence) return false;", "// Accept even a cancelled restoration.")),
])
def test_regression_gates_reject_controlled_mutations(world, scenario, mutation):
    result = run_scenario(world, scenario, mutation)
    assert result.returncode != 0, "Controlled regression escaped its gate"
    assert "AssertionError" in result.stderr or "Storage denied" in result.stderr, result.stderr
