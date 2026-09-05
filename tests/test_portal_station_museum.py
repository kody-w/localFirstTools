"""Actual inline runtimes with deterministic I/O; Chrome pixel checks supplement these gates."""

import json
from pathlib import Path
import re
import subprocess

import pytest


ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "station": ROOT / "exhibitions/ai-research/zero-g-space-station.html",
    "museum": ROOT / "exhibitions/the-arcade/impossible-architecture-museum.html",
}

HARNESS = r"""
const assert = require('node:assert/strict');
const vm = require('node:vm');
const input = JSON.parse(require('node:fs').readFileSync(0, 'utf8'));
function target(extra = {}) {
    return Object.assign({listeners: {}, addEventListener(type, fn) {
        (this.listeners[type] ||= []).push(fn);
    }}, extra);
}
function emit(object, type, extra = {}) {
    const event = {key: '', target: object, preventDefault() {}, ...extra};
    for (const fn of object.listeners[type] || []) fn(event);
}
function clip(polygon, distance) {
    const out = [];
    for (let i = 0; i < polygon.length; i++) {
        const a = polygon[i], b = polygon[(i + 1) % polygon.length];
        const da = distance(a), db = distance(b);
        if (da >= 0) out.push(a);
        if ((da >= 0) !== (db >= 0)) {
            const t = da / (da - db);
            out.push(a.map((v, j) => v + t * (b[j] - v)));
        }
    }
    return out;
}
function area(points) {
    let sum = 0;
    for (let i = 0; i < points.length; i++) {
        const a = points[i], b = points[(i + 1) % points.length];
        sum += a[0] * b[1] - a[1] * b[0];
    }
    return Math.abs(sum) / 2;
}
function screenArea(points) {
    for (const distance of [p => p[0], p => 1200 - p[0], p => p[1], p => 800 - p[1]])
        points = clip(points, distance);
    return area(points);
}
function context2d() {
    return {
        paths: [], path: [],
        fillRect() {}, fillText() {}, stroke() {}, arc() {},
        createRadialGradient() { return {addColorStop() {}}; },
        beginPath() { this.path = []; },
        moveTo(x, y) { this.path.push([x, y]); },
        lineTo(x, y) { this.path.push([x, y]); },
        closePath() {},
        fill() { this.paths.push(this.path.slice()); }
    };
}
function webgl() {
    let bound;
    const attrs = {}, uniforms = {};
    const mul = (m, v) => [0, 1, 2, 3].map(i =>
        m[i] * v[0] + m[i + 4] * v[1] + m[i + 8] * v[2] + m[i + 12] * v[3]);
    return {
        TRIANGLE_FAN: 6, TRIANGLES: 4, area: 0, draws: [],
        createShader() { return {}; }, shaderSource() {}, compileShader() {},
        getShaderParameter() { return true; }, createProgram() { return {}; },
        attachShader() {}, linkProgram() {}, getProgramParameter() { return true; },
        useProgram() {}, getAttribLocation(_, name) { return name; },
        getUniformLocation(_, name) { return name; },
        enable() {}, depthFunc() {}, clearColor() {}, viewport() {},
        createBuffer() { return {}; }, bindBuffer(_, buffer) { bound = buffer; },
        bufferData(_, data) { bound.data = [...data]; },
        enableVertexAttribArray() {}, vertexAttribPointer(name) { attrs[name] = bound; },
        uniformMatrix4fv(name, _, data) { uniforms[name] = [...data]; },
        uniform1f() {}, deleteBuffer() {},
        clear() { this.area = 0; this.draws = []; },
        drawArrays(mode, first, count) {
            const vertices = attrs.aPosition.data;
            this.draws.push(vertices);
            const triangles = [];
            for (let i = mode === this.TRIANGLE_FAN ? 1 : 0; i < count - 1;
                 i += mode === this.TRIANGLE_FAN ? 1 : 3)
                triangles.push(mode === this.TRIANGLE_FAN ? [0, i, i + 1] : [i, i + 1, i + 2]);
            for (const triangle of triangles) {
                let points = triangle.map(index => mul(uniforms.uProjection, mul(uniforms.uView,
                    [...vertices.slice((index + first) * 3, (index + first) * 3 + 3), 1])));
                for (const distance of [p => p[3] + p[0], p => p[3] - p[0],
                        p => p[3] + p[1], p => p[3] - p[1],
                        p => p[3] + p[2], p => p[3] - p[2]])
                    points = clip(points, distance);
                if (points.length >= 3) this.area += area(points.map(p => [p[0] / p[3], p[1] / p[3]]));
            }
        }
    };
}
const elements = new Map(), created = [], blobs = [], storage = new Map();
function element(id) {
    if (!elements.has(id)) {
        const classes = new Set();
        const canvas2d = context2d(), gl = webgl();
        elements.set(id, target({
            id, style: {}, dataset: {}, textContent: '', width: 1200, height: 800,
            clientWidth: 1200, clientHeight: 800,
            classList: {add: s => classes.add(s), remove: s => classes.delete(s),
                contains: s => classes.has(s)},
            getContext: type => type === '2d' ? canvas2d : gl,
            click() { emit(this, 'click'); },
            requestPointerLock() {}, requestFullscreen() {}
        }));
    }
    return elements.get(id);
}
const buttons = ['habitat', 'solar', 'lab', 'docking', 'storage'].map(type => {
    const button = element(type); button.dataset.type = type; return button;
});
const document = target({
    getElementById: element, querySelectorAll: () => buttons, querySelector: () => buttons[0],
    createElement(tag) { const value = element(`created-${created.length}-${tag}`); created.push(value); return value; },
    body: element('body'), documentElement: element('html'), exitPointerLock() {}, exitFullscreen() {}
});
const clock = {now: 0};
const math = Object.create(Math); math.random = () => 0.4;
const context = vm.createContext({
    assert, document, elements, created, blobs, storage, emit, screenArea, clock,
    html: input.html,
    Math: math, Blob,
    URL: {createObjectURL(blob) { blobs.push(blob); return 'blob:test'; }, revokeObjectURL() {}},
    FileReader: class {
        readAsText(file) { this.onload({target: {result: file.content}}); }
    },
    window: target({innerWidth: 1200, innerHeight: 800, devicePixelRatio: 1}),
    localStorage: {getItem: key => storage.get(key) ?? null,
        setItem: (key, value) => storage.set(key, value)},
    performance: {now: () => clock.now},
    console: {log() {}, error() {}, warn() {}},
    setTimeout: () => 1, setInterval: () => 1, requestAnimationFrame: () => 1,
    alert() {}, confirm: () => true
});
vm.runInContext(input.source, context);
vm.runInContext(`
function makeStation() {
    const app = new SpaceStationApp();
    app.stars = [];
    return app;
}
function picture(app, module, config = MODULE_TYPES[module.type]) {
    app.ctx.paths = [];
    app.drawModule(app.ctx, app.canvas.width, app.canvas.height, module, config);
    assert.ok(app.ctx.paths.flat(2).every(Number.isFinite), 'render coordinates must stay finite');
    return app.ctx.paths.filter(path => screenArea(path) > 1);
}
function makeMuseum() {
    world = new MuseumWorld();
    physics = new PhysicsController(world);
    input = new InputHandler();
    dataManager = new DataManager();
    renderer = new SimpleRenderer(document.getElementById('world-canvas'));
    renderer.resize();
    gameLoop = new GameLoop(renderer, world, physics, input);
}
function roomPicture(room) {
    gameLoop.updateCamera();
    renderer.render({rooms: new Map([[room.name, room]]), staircases: [], hallways: [], portals: []});
    return renderer.gl.area;
}
const directions = [[0,-1,0], [0,1,0], [1,0,0], [-1,0,0], [0,0,1], [0,0,-1]];
function components(v) { return [v.x, v.y, v.z]; }
function playerSnapshot() { return JSON.stringify(GAME_STATE.player); }
`, context);
vm.runInContext(input.mutation || '', context);
Promise.resolve(vm.runInContext('(async () => {' + input.scenario + '\n})()', context))
    .catch(error => { console.error(error); process.exitCode = 1; });
"""


CASES = {
    "placement-paints-forward": ("station", r"""
        const app = makeStation();
        const rotations = [new Quat(), Quat.fromAxisAngle(new Vec3(0,1,0), 1.2),
            Quat.fromAxisAngle(new Vec3(1,0,0), 0.9),
            Quat.fromAxisAngle(new Vec3(0,0,1), 0.7).mul(Quat.fromAxisAngle(new Vec3(0,1,0), -1.8))];
        for (const rotation of rotations) for (const type of Object.keys(MODULE_TYPES)) {
            app.modules = []; app.camera.rot = rotation;
            emit(document.getElementById(type), 'click');
            app.tryPlaceModule(600, 400);
            assert.equal(app.modules.length, 1);
            assert.equal(app.modules[0].type, type);
            assert.ok(picture(app, app.modules[0]).length, 'placed module must paint visible faces');
            app.tryPlaceModule(600, 400);
            assert.equal(app.modules.length, 1, 'blocked placement must not duplicate a module');
            const front = app.camera.pos.add(rotation.rotateVec(new Vec3(0,0,-10)));
            const center = app.worldToScreen(front, 1200, 800);
            assert.ok(Math.abs(center.x - 600) < 1e-8 && Math.abs(center.y - 400) < 1e-8);
            assert.equal(app.worldToScreen(app.camera.pos.add(rotation.rotateVec(new Vec3(0,0,10))),
                1200, 800), null);
            app.camera.vel = new Vec3(); app.keys = {w: true};
            const previous = app.camera.pos;
            app.updatePhysics(0.1);
            assert.ok(app.camera.pos.sub(previous).dot(rotation.rotateVec(new Vec3(0,0,-1))) > 0);
        }
    """, r"""
        SpaceStationApp.prototype.worldToCamera = function(pos) {
            const v = pos.sub(this.camera.pos);
            return new Vec3(this.camera.rot.rotateVec(new Vec3(1,0,0)).dot(v),
                this.camera.rot.rotateVec(new Vec3(0,1,0)).dot(v),
                -this.camera.rot.rotateVec(new Vec3(0,0,-1)).dot(v));
        };
    """, "placed module must paint visible faces"),
    "station-roundtrip-paints": ("station", r"""
        const app = makeStation();
        app.tryPlaceModule(600,400);
        app.keys = {d: true};
        for (let i = 0; i < 90; i++) app.updatePhysics(1/60);
        app.keys = {}; emit(window, 'keydown', {key: ' '});
        emit(document.getElementById('solar'), 'click'); app.tryPlaceModule(600,400);
        assert.equal(app.modules.length, 2);
        app.camera.rot = Quat.fromAxisAngle(new Vec3(0,1,0),0.25)
            .mul(Quat.fromAxisAngle(new Vec3(0,0,1),0.15));
        app.exportData();
        const exported = JSON.parse(await blobs.at(-1).text());
        assert.equal(exported.modules.length, 2);
        app.modules = [];
        app.importData();
        created.at(-1).onchange({target: {files: [{content: JSON.stringify(exported)}]}});
        const restored = makeStation();
        assert.equal(restored.modules.length, 2, 'reopened station must retain both rendered modules');
        for (const module of restored.modules)
            assert.ok(picture(restored, module).length, 'roundtrip module must paint visible faces');
        assert.deepEqual(components(restored.camera.pos), Object.values(exported.camera.pos));
        assert.deepEqual({...restored.camera.rot}, exported.camera.rot);
    """, "SpaceStationApp.prototype.loadData = function() {};",
        "reopened station must retain both rendered modules"),
    "near-plane-paints-clipped-faces": ("station", r"""
        const app = makeStation();
        app.camera.pos = new Vec3();
        const module = {type: 'habitat', pos: new Vec3(), rot: new Quat()};
        const paths = picture(app, module, {...MODULE_TYPES.habitat, size: {x: 0.2,y: 0.2,z: 1}});
        assert.ok(paths.length >= 5, 'near-plane crossings must paint the clipped side faces');
        assert.ok(paths.reduce((sum, path) => sum + screenArea(path), 0) > 1200 * 800 * 0.95);
        module.pos.z = 10;
        assert.equal(picture(app, module).length, 0, 'fully behind modules must paint nothing');
        assert.equal(app.worldToScreen(new Vec3(0,0,-0.05), 1200,800), null);
        assert.ok(app.worldToScreen(new Vec3(0,0,-0.11), 1200,800));
    """, r"""
        SpaceStationApp.prototype.clipToNearPlane = function(vertices) {
            return vertices.filter(v => v.z >= this.camera.near);
        };
    """, "near-plane crossings must paint the clipped side faces"),
    "solar-normal-and-render-agree": ("station", r"""
        const app = makeStation();
        app.camera.pos = new Vec3(0,0,30);
        const module = {type:'solar', pos:new Vec3(), rot:new Quat()};
        app.modules = [module];
        for (const angle of [0.15, 0.5, 1.1]) {
            app.orbitAngle = angle;
            assert.ok(Math.abs(app.calculatePower() - 20) < 1e-8,
                'sun-facing panels must calculate their configured generation');
            const rotation = app.getModuleRotation(module);
            const normal = rotation.rotateVec(new Vec3(0,1,0));
            assert.ok(normal.dot(app.getSunDirection()) > 0.999999);
            const paths = picture(app, module);
            const expected = app.worldToScreen(rotation.rotateVec(new Vec3(-4,-0.1,-2)),1200,800);
            assert.ok(paths.some(path => path.some(([x,y]) =>
                Math.abs(x - expected.x) < 1e-8 && Math.abs(y - expected.y) < 1e-8)),
                'painted solar vertices must use the same tracked orientation as physics');
        }
        app.getModuleRotation = () => new Quat();
        assert.equal(app.calculatePower(), 0, 'generation must depend on actual panel incidence');
    """, "SpaceStationApp.prototype.getModuleRotation = function(module) { return module.rot; };",
        "sun-facing panels must calculate their configured generation"),
    "solar-orbit-shadow-and-load": ("station", r"""
        const app = makeStation();
        app.modules = [{type:'solar',pos:new Vec3(),rot:new Quat()},
            {type:'habitat',pos:new Vec3(5,0,0),rot:new Quat()}];
        const phases = [];
        for (let i = 0; i < 1300; i++) {
            app.updatePhysics(0.05);
            if (i % 50) continue;
            const expected = Math.cos(app.orbitAngle) > 0 ? 15 : -5;
            assert.ok(Math.abs(app.calculatePower() - expected) < 1e-8,
                'orbital shadow must stop solar generation without dropping habitat demand');
            app.updateUI();
            assert.equal(document.getElementById('power').textContent, `${expected.toFixed(1)} kW`);
            phases.push(expected);
        }
        assert.ok(phases.includes(15) && phases.includes(-5));
        assert.equal(phases.at(-1), 15);
    """, "SpaceStationApp.prototype.isSunlit = function() { return true; };",
        "orbital shadow must stop solar generation without dropping habitat demand"),
    "all-room-surfaces-and-rotations": ("museum", r"""
        makeMuseum();
        const p = GAME_STATE.player;
        for (const room of world.rooms.values()) {
            const b = room.bounds;
            p.currentRoom = room.name;
            p.position.set(b.x+b.width/2, b.y+b.height/2, b.z+b.depth/2);
            p.velocity.set(0,0,0); p.gravityDir.set(0,-1,0);
            for (let turn = 0; turn < 12; turn++) {
                for (let i = 0; i < 700; i++) physics.update(1);
                for (const [axis, dimension] of [['x','width'],['y','height'],['z','depth']]) {
                    assert.ok(p.position[axis] >= b[axis]+2-1e-9 &&
                        p.position[axis] <= b[axis]+b[dimension]-2+1e-9,
                        'gravity must contain the player inside the current room');
                    if (p.gravityDir[axis]) assert.equal(p.position[axis],
                        p.gravityDir[axis] < 0 ? b[axis]+2 : b[axis]+b[dimension]-2);
                }
                assert.equal(p.onGround, true);
                assert.ok(Math.abs(p.velocity.dot(p.gravityDir)) < 1e-9);
                assert.ok(roomPicture(room) > 0.5, 'every supporting room must emit visible surface geometry');
                physics.rotateGravity();
            }
        }
    """, "PhysicsController.prototype.constrainToRoom = function() {};",
        "gravity must contain the player inside the current room"),
    "gravity-relative-movement-jump-view": ("museum", r"""
        makeMuseum();
        const p = GAME_STATE.player, room = world.rooms.get('entrance');
        for (const direction of directions) {
            p.position.set(0,5,0); p.velocity.set(0,0,0);
            p.rotation = {yaw:0.35,pitch:0,roll:0}; p.gravityDir.set(...direction);
            for (let i=0;i<300;i++) physics.update(1);
            const before = p.position.clone();
            GAME_STATE.input.forward = true;
            for (let i=0;i<6;i++) { input.processInput(1); physics.update(1); }
            GAME_STATE.input.forward = false;
            const motion = p.position.clone().sub(before);
            assert.ok(motion.length() > 0.1);
            assert.ok(Math.abs(motion.dot(p.gravityDir)) < 1e-8,
                'walking must stay tangent to the gravity surface');
            gameLoop.updateCamera();
            const gaze = GAME_STATE.camera.target.clone().sub(GAME_STATE.camera.position);
            assert.ok(gaze.dot(motion) > 0);
            assert.ok(Math.abs(gaze.dot(p.gravityDir)) < 1e-8,
                'level views must follow the active gravity plane');
            assert.equal(GAME_STATE.camera.up.dot(p.gravityDir),-1);
            p.velocity.set(0,0,0); GAME_STATE.input.jump = true;
            input.processInput(1); GAME_STATE.input.jump = false;
            assert.ok(p.velocity.dot(p.gravityDir) < 0,
                'jump must push away from the active gravity surface');
            physics.update(1);
            assert.equal(p.onGround, false);
            for (let i=0;i<200;i++) physics.update(1);
            assert.equal(p.onGround, true);
            for (const pitch of [-Math.PI/2, 0, Math.PI/2]) {
                p.rotation.pitch = pitch;
                assert.ok(roomPicture(room) > 0.5, 'gravity-relative views must retain visible room output');
                const m = renderer.viewMatrix.elements;
                assert.ok([...m].every(Number.isFinite));
                assert.ok(Math.hypot(m[0],m[4],m[8]) > 0.99);
            }
        }
    """, r"""
        InputHandler.prototype.processInput = function() {
            const p = GAME_STATE.player;
            if (GAME_STATE.input.forward) {
                p.velocity.x += Math.sin(p.rotation.yaw) * WORLD_CONFIG.playerSpeed;
                p.velocity.z -= Math.cos(p.rotation.yaw) * WORLD_CONFIG.playerSpeed;
            }
            if (GAME_STATE.input.jump && p.onGround) p.velocity.y = WORLD_CONFIG.jumpForce;
        };
    """, "jump must push away from the active gravity surface"),
    "portals-update-room-and-camera": ("museum", r"""
        makeMuseum();
        const p = GAME_STATE.player;
        const names = ['entrance','penrose','gallery'];
        for (let index=0;index<world.portals.length;index++) {
            const portal = world.portals[index];
            p.currentRoom = names[index]; p.gravityDir.set(0,-1,0);
            p.position.copy(portal.position).add(new Vector3(0,0,4));
            p.position.y = Math.max(p.position.y,2);
            p.velocity.set(0,0,0); p.rotation = {yaw:0,pitch:0,roll:0};
            GAME_STATE.input.forward = true;
            const expected = names[(index+1)%names.length];
            for (let i=0;i<40 && p.currentRoom === names[index];i++) {
                clock.now += 16.67; gameLoop.running = true; gameLoop.loop();
                if (p.position.x === portal.destination.x && p.position.z === portal.destination.z) {
                    assert.equal(p.currentRoom, expected, 'proximity portals must change collision-room ownership');
                    assert.equal(p.velocity.length(), 0);
                }
            }
            GAME_STATE.input.forward = false;
            assert.equal(p.currentRoom, expected, 'proximity portals must change collision-room ownership');
            assert.deepEqual(components(GAME_STATE.camera.position), components(p.position),
                'portal transport must render from its destination in the same frame');
            assert.ok(roomPicture(world.rooms.get(expected)) > 0.5);
            for (let i=0;i<12;i++) { physics.rotateGravity(); for (let j=0;j<300;j++) physics.update(1); }
            assert.equal(p.currentRoom, expected);
        }
    """, r"""
        GameLoop.prototype.checkPortals = function() {
            this.world.portals.forEach(portal => portal.teleport(GAME_STATE.player));
        };
    """, "proximity portals must change collision-room ownership"),
    "museum-gravity-json-reload-legacy": ("museum", r"""
        makeMuseum();
        const p = GAME_STATE.player;
        for (const direction of directions) {
            p.position.set(-50,5,0); p.currentRoom = 'gallery';
            p.gravityDir.set(...direction); p.rotation = {yaw:0.3,pitch:-0.2,roll:0};
            dataManager.export();
            const exported = JSON.parse(await blobs.at(-1).text());
            assert.deepEqual(Object.values(exported.data.player.gravityDir || {}), direction,
                'export must preserve the active gravity direction');
            p.gravityDir.set(0,-1,0); p.currentRoom = 'entrance'; p.position.set(0,2,10);
            await dataManager.import({content:JSON.stringify(exported)});
            assert.deepEqual(components(p.gravityDir), direction, 'import must restore the exported gravity direction');
            assert.equal(p.currentRoom, 'gallery');
            assert.deepEqual(components(GAME_STATE.camera.up), direction.map(v => -v));
            const saved = storage.get('impossible-architecture-museum');
            assert.ok(saved, 'successful imports must survive reopening');
            p.gravityDir.set(0,-1,0); p.position.set(0,2,10);
            assert.equal(dataManager.load(),true);
            assert.deepEqual(components(p.gravityDir), direction, 'reload must restore the stored gravity direction');
            assert.ok(roomPicture(world.rooms.get('gallery')) > 0.5);
        }
        const legacy = {version:'1.0.0', data:{player:{
            position:{x:30,y:5,z:0}, rotation:{yaw:0,pitch:0,roll:0}}}};
        await dataManager.import({content:JSON.stringify(legacy)});
        assert.deepEqual(components(p.gravityDir),[0,-1,0]);
        assert.equal(p.currentRoom,'penrose');
        storage.set('impossible-architecture-museum',JSON.stringify({
            version:'1.0.0',player:{...legacy.data.player,currentRoom:'entrance'},
            settings:{mouseSensitivity:0.002,renderDistance:100}}));
        assert.equal(dataManager.load(),true);
        assert.equal(p.currentRoom,'penrose', 'legacy stale room labels must follow actual location');
        dataManager.applyData({player:{position:{x:0,y:30.2,z:10},
            rotation:{yaw:0,pitch:0,roll:0},currentRoom:'entrance',gravityDir:{x:0,y:1,z:0}}});
        assert.equal(p.position.y,8,'escaped older saves must recover inside their existing room');
        assert.ok(roomPicture(world.rooms.get('entrance')) > 0.5);
    """, r"""
        const originalExport = DataManager.prototype.export;
        DataManager.prototype.export = function() {
            const gravity = GAME_STATE.player.gravityDir;
            GAME_STATE.player.gravityDir = new Vector3(0,-1,0);
            try { originalExport.call(this); } finally { GAME_STATE.player.gravityDir = gravity; }
        };
    """, "export must preserve the active gravity direction"),
    "museum-invalid-import-is-atomic": ("museum", r"""
        makeMuseum();
        const invalid = [
            {gravityDir:{x:0,y:0,z:0}}, {gravityDir:{x:1,y:1,z:0}},
            {gravityDir:{x:0,y:-0.5,z:0}}, {gravityDir:null},
            {position:{x:'0',y:2,z:0}}, {rotation:{yaw:null,pitch:0}},
            {currentRoom:'missing'}
        ];
        for (const patch of invalid) {
            const player = {position:{x:1,y:4,z:2},rotation:{yaw:0,pitch:0,roll:0},
                gravityDir:{x:0,y:-1,z:0},currentRoom:'entrance',...patch};
            const before = playerSnapshot(), saved = [...storage];
            await assert.rejects(dataManager.import({content:JSON.stringify({
                version:'1.0.0',data:{player}})}), undefined, 'invalid imports must reject before changing state');
            assert.equal(playerSnapshot(),before);
            assert.deepEqual([...storage],saved);
        }
        for (const settings of [null, [], {mouseSensitivity:'fast'}, {renderDistance:-1}]) {
            const before = playerSnapshot(), configuration = JSON.stringify(WORLD_CONFIG);
            await assert.rejects(dataManager.import({content:JSON.stringify({
                version:'1.0.0',data:{player:{position:{x:0,y:5,z:0},rotation:{yaw:0,pitch:0}},settings}})}));
            assert.equal(playerSnapshot(),before);
            assert.equal(JSON.stringify(WORLD_CONFIG),configuration);
        }
    """, "DataManager.prototype.validateGravity = function() { return new Vector3(0,-1,0); };",
        "invalid imports must reject before changing state"),
    "instructions-match-actions": ("museum", r"""
        makeMuseum(); setupUI();
        emit(document,'keydown',{key:'r'});
        assert.deepEqual(components(GAME_STATE.player.gravityDir),[0,1,0]);
        const controls = html.match(/id="controls-info">([\s\S]*?)<\/div>/)[1];
        assert.ok(!/\b[TEP] - /.test(controls), 'instructions must not advertise missing T/P/E actions');
        assert.ok(/walk into.*portal/i.test(controls), 'portal instructions must describe proximity activation');
    """, "", "instructions must not advertise missing T/P/E actions"),
    "museum-menu-does-not-capture-pointer": ("museum", r"""
        let captures = 0;
        document.body.requestPointerLock = () => { captures++; };
        makeMuseum(); setupUI();
        emit(document,'click',{target:document.getElementById('export-btn')});
        emit(document,'click',{target:document.getElementById('import-btn')});
        assert.equal(captures,0,'menu controls must not request pointer lock');
        emit(document.getElementById('world-canvas'),'click');
        assert.equal(captures,1,'clicking the world must still enable mouse look');
        emit(document.getElementById('start-btn'),'click');
        assert.equal(captures,2);
    """, r"""
        const setup = InputHandler.prototype.setupEventListeners;
        InputHandler.prototype.setupEventListeners = function() {
            setup.call(this);
            document.addEventListener('click',() => this.requestPointerLock());
        };
    """, "menu controls must not request pointer lock"),
}

OUTPUT_MUTATIONS = {
    "solar-render-only-tracking-is-not-enough": ("solar-normal-and-render-agree", r"""
        const draw = SpaceStationApp.prototype.drawModule;
        SpaceStationApp.prototype.drawModule = function(...args) {
            const tracked = this.getModuleRotation;
            this.getModuleRotation = module => module.rot;
            try { draw.apply(this,args); } finally { this.getModuleRotation = tracked; }
        };
    """, "painted solar vertices must use the same tracked orientation as physics"),
    "invisible-room-colliders-are-not-enough": ("all-room-surfaces-and-rotations", r"""
        const create = MuseumWorld.prototype.createRoom;
        MuseumWorld.prototype.createRoom = function(name,...args) {
            create.call(this,name,...args);
            if (name !== 'entrance') {
                const room = this.rooms.get(name);
                delete room.floor; delete room.walls; delete room.ceiling;
            }
        };
    """, "every supporting room must emit visible surface geometry"),
    "world-axis-camera-is-not-gravity-relative": ("gravity-relative-movement-jump-view", r"""
        const camera = GameLoop.prototype.updateCamera;
        GameLoop.prototype.updateCamera = function() {
            camera.call(this);
            const p = GAME_STATE.player;
            GAME_STATE.camera.target.set(p.position.x+Math.sin(p.rotation.yaw)*Math.cos(p.rotation.pitch),
                p.position.y+Math.sin(p.rotation.pitch),p.position.z-Math.cos(p.rotation.yaw)*Math.cos(p.rotation.pitch));
        };
    """, "gravity-relative views must retain visible room output"),
    "export-without-import-restoration-is-not-enough": ("museum-gravity-json-reload-legacy",
        "DataManager.prototype.validateGravity = function() { return new Vector3(0,-1,0); };",
        "import must restore the exported gravity direction"),
    "import-without-reload-restoration-is-not-enough": ("museum-gravity-json-reload-legacy", r"""
        const load = DataManager.prototype.load;
        DataManager.prototype.load = function() {
            const loaded = load.call(this);
            GAME_STATE.player.gravityDir.set(0,-1,0);
            return loaded;
        };
    """, "reload must restore the stored gravity direction"),
}


def run_case(name, *, mutate=False, override_mutation=None):
    world, scenario, mutation, _ = CASES[name]
    html = PAGES[world].read_text(encoding="utf-8")
    if mutate and name == "instructions-match-actions":
        html = html.replace("R - Rotate Gravity", "T - Toggle Perspective | R - Rotate Gravity")
    source = re.search(r"<script>([\s\S]*?)</script>", html).group(1)
    result = subprocess.run(
        ["node", "-e", HARNESS],
        input=json.dumps({
            "source": source, "html": html, "scenario": scenario,
            "mutation": override_mutation if override_mutation is not None else mutation if mutate else "",
        }),
        text=True,
        capture_output=True,
        cwd=ROOT,
        timeout=20,
    )
    return result


@pytest.mark.parametrize("name", CASES)
def test_station_and_museum_regressions(name):
    result = run_case(name)
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("name", CASES)
def test_regression_gate_rejects_controlled_mutants(name):
    result = run_case(name, mutate=True)
    assert result.returncode != 0, f"Vacuous gate: {name} accepted its controlled mutant"
    assert CASES[name][3] in result.stderr, result.stdout + result.stderr


@pytest.mark.parametrize("name", OUTPUT_MUTATIONS)
def test_output_gates_reject_partial_repairs(name):
    case, mutation, message = OUTPUT_MUTATIONS[name]
    result = run_case(case, override_mutation=mutation)
    assert result.returncode != 0, f"Vacuous output gate: {name}"
    assert message in result.stderr, result.stdout + result.stderr
