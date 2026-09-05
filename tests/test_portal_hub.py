import re
import subprocess
from pathlib import Path
from urllib.parse import urljoin

import pytest


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'apps/quantum-worlds/portal-hub.html'
SOURCE = PAGE.read_text(encoding='utf-8')
WORLDS = re.findall(r"id:\s*'([^']+)',\s*file:\s*'([^']+)'", SOURCE)


def test_all_ten_portals_have_unique_destinations():
    assert len(WORLDS) == 10
    assert len({world_id for world_id, _ in WORLDS}) == 10
    assert len({path for _, path in WORLDS}) == 10


@pytest.mark.parametrize('world_id,path', WORLDS)
def test_portal_points_to_a_real_world_under_both_host_roots(world_id, path):
    target = (PAGE.parent / path).resolve()
    assert target.is_relative_to(ROOT)
    assert target.is_file(), f'{world_id}: {path}'
    html = target.read_text(encoding='utf-8')
    assert '<script' in html
    assert 'http-equiv="refresh"' not in html
    relative = target.relative_to(ROOT).as_posix()
    for prefix in ('/', '/localFirstTools/'):
        base = f'https://example.test{prefix}apps/quantum-worlds/portal-hub.html'
        assert urljoin(base, path) == f'https://example.test{prefix}{relative}'


@pytest.mark.parametrize('world_id,path', WORLDS)
def test_world_javascript_parses_before_a_portal_opens_it(world_id, path):
    html = (PAGE.parent / path).read_text(encoding='utf-8')
    result = subprocess.run(
        ['node', '-e', r"""
            const vm = require('node:vm');
            const html = require('node:fs').readFileSync(0, 'utf8');
            for (const script of html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)) {
                new vm.Script(script[1]);
            }
        """],
        input=html,
        text=True,
        capture_output=True,
        timeout=15,
    )
    assert result.returncode == 0, f'{world_id}: {result.stderr}'


# Run the actual inline runtime with deterministic DOM, network, and timer boundaries.
# No browser, CDN, WebGL context, or multiplayer service is needed for these regressions.
HARNESS = r"""
const assert = require('node:assert/strict');
const vm = require('node:vm');
const html = require('node:fs').readFileSync(0, 'utf8');
const scripts = [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)];
const script = scripts.at(-1)[1];
new vm.Script(script);
const source = script.split('// -------- Boot ')[0];
const elements = new Map();
const timers = new Map();
const requests = [];
let now = 0, timerId = 0;

class Target {
    constructor() { this.listeners = new Map(); }
    addEventListener(name, callback) {
        if (!this.listeners.has(name)) this.listeners.set(name, []);
        this.listeners.get(name).push(callback);
    }
    emit(name, event = {}) {
        for (const callback of this.listeners.get(name) || []) callback(event);
    }
}
class Element extends Target {
    constructor(id) {
        super();
        this.id = id;
        this.attrs = {};
        this.style = {};
        this.dataset = {};
        this.hidden = false;
        this.open = false;
        this.textContent = '';
        this.classes = new Set();
        this.classList = {
            add: name => this.classes.add(name),
            remove: name => this.classes.delete(name),
            contains: name => this.classes.has(name),
        };
        this.src = 'about:blank';
    }
    set src(value) {
        this.attrs.src = value;
        this.contentDocument = new Target();
        this.contentDocument.URL = value;
        this.contentDocument.querySelector = selector => selector === 'canvas' ? {} : null;
        this.contentWindow = {
            performance: { getEntriesByType: () => [{ responseStatus: this.responseStatus ?? 200 }] },
        };
    }
    get src() { return this.attrs.src || 'about:blank'; }
    setAttribute(name, value) { this.attrs[name] = value; }
    removeAttribute(name) { delete this.attrs[name]; }
    cloneNode() { return new Element(this.id); }
    replaceWith(element) { elements.set(this.id, element); }
    focus() { document.activeElement = this; }
    closest() { return this.id === 'my-name' ? this : null; }
    showModal() { this.open = true; }
}
const document = new Target();
document.getElementById = id => {
    if (!elements.has(id)) elements.set(id, new Element(id));
    return elements.get(id);
};
document.querySelectorAll = () => [];
document.exitPointerLock = () => { document.pointerLockElement = null; };
const window = new Target();
window.location = new URL('https://example.test/localFirstTools/apps/quantum-worlds/portal-hub.html');
class Vector3 {
    constructor(x = 0, y = 0, z = 0) { this.set(x, y, z); }
    set(x, y, z) { this.x = x; this.y = y; this.z = z; return this; }
}
function tick(ms) {
    const end = now + ms;
    for (;;) {
        const next = [...timers].sort((a, b) => a[1].due - b[1].due)[0];
        if (!next || next[1].due > end) break;
        now = next[1].due;
        timers.delete(next[0]);
        next[1].callback();
    }
    now = end;
}
async function settle() {
    for (let i = 0; i < 5; i++) await Promise.resolve();
}
const context = {
    assert, document, window, Element, URL, AbortController, DOMException,
    console, timers, requests, tick, settle, THREE: { Vector3 },
    performance: { now: () => now },
    requestAnimationFrame: () => {},
    setTimeout: (callback, delay) => {
        timers.set(++timerId, { callback, due: now + delay });
        return timerId;
    },
    clearTimeout: id => timers.delete(id),
    fetch: (url, options) => new Promise((resolve, reject) => {
        requests.push({ url, resolve, reject });
        options.signal.addEventListener('abort', () => reject(new DOMException('Aborted', 'AbortError')));
    }),
};
const setup = `
    controller.position = new THREE.Vector3(22, 1.7, 0);
    controller.velocity = new THREE.Vector3();
    started = true;
    hubReady = true;
    portals.push({ world: WORLDS[0], group: { position: new THREE.Vector3(22, 0, 0) } });
`;
vm.runInNewContext(source + '\n(async () => {' + setup + process.argv[1] + '})()', context)
    .catch(error => { console.error(error); process.exitCode = 1; });
"""


def run_scenario(scenario):
    result = subprocess.run(
        ['node', '-e', HARNESS, scenario],
        input=SOURCE,
        text=True,
        capture_output=True,
        cwd=ROOT,
        timeout=15,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_return_clears_movement_and_pushes_away_before_resuming():
    run_scenario(r"""
        keys.KeyW = true;
        controller.velocity.set(2, 3, 4);
        enterWorld(WORLDS[0]);
        assert.equal(Object.keys(keys).length, 0);
        exitWorld();
        assert.equal(activeWorld, null);
        assert.equal(nearestPortal, null);
        assert.ok(Math.hypot(controller.position.x - 22, controller.position.z) >= 4.5);
        assert.equal(controller.velocity.y, 0);
        assert.equal(document.getElementById('world-iframe').src, 'about:blank');
        await settle();
        tick(5000);
        assert.equal(document.getElementById('world-overlay').classList.contains('active'), false);
        assert.equal(timers.size, 0);
    """)


def test_cancelled_load_cannot_replace_the_next_world():
    run_scenario(r"""
        enterWorld(WORLDS[0]);
        const oldFrame = document.getElementById('world-iframe');
        exitWorld();
        enterWorld(WORLDS[1]);
        requests[0].resolve({ ok: true });
        await settle();
        oldFrame.emit('load');
        assert.equal(document.getElementById('world-overlay').dataset.state, 'loading');
        requests[1].resolve({ ok: true });
        await settle();
        const frame = document.getElementById('world-iframe');
        assert.equal(frame.src, new URL(WORLDS[1].file, window.location).href);
        frame.emit('load');
        assert.equal(document.getElementById('world-overlay').dataset.state, 'ready');
        exitWorld();
        frame.emit('load');
        assert.equal(document.getElementById('world-overlay').dataset.state, 'idle');
    """)


def test_http_errors_are_retryable_and_stale_frames_stay_cancelled():
    run_scenario(r"""
        enterWorld(WORLDS[0]);
        const failedFrame = document.getElementById('world-iframe');
        requests[0].resolve({ ok: false, status: 404 });
        await settle();
        assert.equal(document.getElementById('world-overlay').dataset.state, 'error');
        assert.match(document.getElementById('world-status-detail').textContent, /404/);
        assert.equal(document.getElementById('retry-world').hidden, false);
        assert.equal(timers.size, 0);
        loadWorld(activeWorld);
        failedFrame.emit('load');
        assert.equal(document.getElementById('world-overlay').dataset.state, 'loading');
        requests[1].resolve({ ok: true });
        await settle();
        const frame = document.getElementById('world-iframe');
        frame.emit('load');
        assert.equal(document.getElementById('world-overlay').dataset.state, 'ready');
        assert.equal(frame.hidden, false);
        assert.equal(frame.inert, false);
        exitWorld();
    """)


def test_slow_loads_time_out_without_late_reopening():
    run_scenario(r"""
        enterWorld(WORLDS[0]);
        tick(20000);
        await settle();
        assert.equal(document.getElementById('world-overlay').dataset.state, 'error');
        assert.match(document.getElementById('world-status-detail').textContent, /too long/);
        requests[0].resolve({ ok: true });
        await settle();
        assert.equal(document.getElementById('world-iframe').src, 'about:blank');
        exitWorld();
        assert.equal(activeWorld, null);
    """)


def test_network_failure_is_visible_and_return_still_works():
    run_scenario(r"""
        enterWorld(WORLDS[0]);
        requests[0].reject(new TypeError('Network unavailable'));
        await settle();
        assert.equal(document.getElementById('world-overlay').dataset.state, 'error');
        assert.match(document.getElementById('world-status-detail').textContent, /connection/);
        exitWorld();
        assert.equal(document.getElementById('world-overlay').dataset.state, 'idle');
    """)


def test_escape_is_rebound_after_iframe_navigation():
    run_scenario(r"""
        enterWorld(WORLDS[0]);
        requests[0].resolve({ ok: true });
        await settle();
        const frame = document.getElementById('world-iframe');
        frame.emit('load');
        frame.src = 'https://example.test/localFirstTools/another-world.html';
        frame.emit('load');
        frame.contentDocument.emit('keydown', { code: 'Escape', preventDefault() {} });
        assert.equal(activeWorld, null);
    """)


def test_typing_focus_loss_and_picker_do_not_leave_movement_stuck():
    run_scenario(r"""
        initControls();
        const event = { code: 'KeyW', target: document.getElementById('my-name'), preventDefault() {} };
        document.emit('keydown', event);
        assert.equal(keys.KeyW, undefined);
        event.target = document.getElementById('scene-canvas');
        document.emit('keydown', event);
        assert.equal(keys.KeyW, true);
        window.emit('blur');
        assert.equal(keys.KeyW, undefined);
        document.emit('keydown', event);
        document.emit('pointerlockchange');
        assert.equal(keys.KeyW, undefined);
        openWorldPicker();
        document.emit('keydown', event);
        assert.equal(keys.KeyW, undefined);
    """)


def test_hidden_hub_does_not_render_behind_active_world():
    run_scenario(r"""
        activeWorld = WORLDS[0];
        started = false;
        portals.length = 0;
        clock = { getDelta: () => 0.016, getElapsedTime: () => 1 };
        renderer = { render() { assert.fail('Hidden hub rendered'); } };
        animate();
    """)


def test_return_releases_pointer_lock_owned_by_the_child_document():
    run_scenario(r"""
        enterWorld(WORLDS[0]);
        const child = document.getElementById('world-iframe').contentDocument;
        child.pointerLockElement = {};
        let released = false;
        child.exitPointerLock = () => { released = true; };
        exitWorld();
        assert.equal(released, true);
        await settle();
    """)


def test_failed_get_after_successful_head_keeps_retry_and_escape_available():
    run_scenario(r"""
        initControls();
        enterWorld(WORLDS[0]);
        requests[0].resolve({ ok: true });
        await settle();
        const frame = document.getElementById('world-iframe');
        frame.contentDocument = null;
        frame.emit('load');
        assert.equal(document.getElementById('world-overlay').dataset.state, 'error');
        assert.equal(document.getElementById('retry-world').hidden, false);
        assert.equal(document.activeElement.id, 'retry-world');
        document.emit('keydown', { code: 'Escape', target: document.activeElement });
        assert.equal(activeWorld, null);
        assert.equal(document.getElementById('world-overlay').dataset.state, 'idle');
    """)


def test_actual_get_status_is_checked_even_when_the_error_document_contains_a_canvas():
    run_scenario(r"""
        enterWorld(WORLDS[0]);
        requests[0].resolve({ ok: true });
        await settle();
        const frame = document.getElementById('world-iframe');
        frame.responseStatus = 503;
        frame.emit('load');
        assert.equal(document.getElementById('world-overlay').dataset.state, 'error');
        assert.match(document.getElementById('world-status-detail').textContent, /503/);
    """)


def test_loaded_non_world_html_is_not_promoted_to_ready():
    run_scenario(r"""
        enterWorld(WORLDS[0]);
        requests[0].resolve({ ok: true });
        await settle();
        const frame = document.getElementById('world-iframe');
        frame.contentDocument.querySelector = () => null;
        frame.emit('load');
        assert.equal(document.getElementById('world-overlay').dataset.state, 'error');
        assert.equal(document.getElementById('world-status').hidden, false);
    """)
