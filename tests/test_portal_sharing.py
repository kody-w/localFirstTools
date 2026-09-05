"""Sharing/state regressions against the actual inline Portal Hub runtime."""

import json
import re
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "apps/quantum-worlds/portal-hub.html"

HARNESS = r"""
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const vm = require('node:vm');
const html = require('node:fs').readFileSync(0, 'utf8');
const script = [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].at(-1)[1];
const source = script.split('// -------- Boot ')[0];
const elements = new Map(), warnings = [], storageData = new Map(), downloads = [];
const storage = {readError: null, writeError: null};
const canvasPixels = () => elements.get('qr-canvas').pixels;

class Element {
    constructor(id = '') {
        this.id = id;
        this.value = '';
        this.textContent = '';
        this.hidden = false;
        this.disabled = false;
        this.listeners = {};
        this.attrs = {};
        this.children = [];
        this.style = {setProperty() {}};
        this.classList = {add() {}, remove() {}};
        this.width = this.height = 120;
        this.dataset = {};
    }
    set id(id) { this._id = id; if (id) elements.set(id, this); }
    get id() { return this._id; }
    addEventListener(name, callback) { this.listeners[name] = callback; }
    emit(name, event = {target: this}) { return this.listeners[name]?.(event); }
    setAttribute(name, value) { this.attrs[name] = value; }
    append(...children) { this.children.push(...children); }
    appendChild(child) { this.append(child); }
    insertAdjacentElement(_where, child) { this.append(child); }
    closest() { return this; }
    get parentElement() { return this; }
    focus() { document.activeElement = this; }
    select() { this.selected = true; }
    click() {
        if (this.download) downloads.push(this);
        return this.onclick?.() || this.emit('click');
    }
    getContext() {
        const canvas = this;
        return {
            fillStyle: '#fff',
            fillRect(x, y, w, h) {
                if (canvas.pixels?.length !== canvas.width * canvas.height)
                    canvas.pixels = new Uint8Array(canvas.width * canvas.height);
                const value = this.fillStyle === '#fff' ? 255 : 0;
                for (let row = y; row < y + h; row++)
                    canvas.pixels.fill(value, row * canvas.width + x, row * canvas.width + x + w);
            },
        };
    }
}
for (const [, id] of html.matchAll(/\bid="([^"]+)"/g)) new Element(id);
const document = {
    getElementById: id => elements.get(id) || null,
    createElement: () => new Element(),
    querySelectorAll: () => [],
};
const navigator = {};
const window = {location: new URL('https://example.test/localFirstTools/apps/quantum-worlds/portal-hub.html?old=1#old')};
class Reader {
    readAsText(file) {
        if (file.error) { this.onerror?.(); return; }
        this.result = file.text;
        this.onload?.({target: this});
    }
}
const localStorage = {
    getItem(key) { if (storage.readError) throw storage.readError; return storageData.get(key) ?? null; },
    setItem(key, value) { if (storage.writeError) throw storage.writeError; storageData.set(key, value); },
};
let exportedBlob;
class TestURL extends URL {
    static createObjectURL(blob) { exportedBlob = blob; return 'blob:avatar'; }
    static revokeObjectURL() {}
}
const context = {
    assert, crypto, document, window, navigator, Blob, URL: TestURL, FileReader: Reader,
    localStorage, storage, storageData, warnings, downloads, elements, canvasPixels,
    exportedText: () => exportedBlob.text(),
    console: {warn: (...args) => warnings.push(args), error: (...args) => warnings.push(args)},
    setTimeout: () => 1, clearTimeout() {},
    alert: message => { throw new Error('Unexpected blocking alert: ' + message); },
};
const setup = `
    loadAvatar();
    const importText = text => importAvatarData({target: {files: [{text, size: text.length}], value: 'avatar.json'}});
    const importObject = obj => importText(JSON.stringify(obj));
    const fieldsEqual = avatar => {
        for (const prefix of ['start', 'my']) {
            assert.equal(document.getElementById(prefix + '-name').value, avatar.name);
            assert.equal(document.getElementById(prefix + '-color').value, avatar.color);
        }
    };
`;
vm.runInNewContext(source + '\n(async () => {' + setup + process.argv[1] + '})()', context)
    .catch(error => { console.error(error); process.exitCode = 1; });
"""


def run_scenario(scenario, source=None):
    result = subprocess.run(
        ["node", "-e", HARNESS, scenario],
        input=source if source is not None else PAGE.read_text(encoding="utf-8"),
        text=True,
        capture_output=True,
        cwd=ROOT,
        timeout=20,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_versioned_and_legacy_exports_round_trip_before_start():
    run_scenario(r"""
        const avatar = {name: '星 Wanderer', color: '#abcdef'};
        importObject({app: APP_NAME, version: 1, avatar});
        fieldsEqual(avatar);
        assert.equal(myAvatar.name, avatar.name);
        assert.equal(myAvatar.color, avatar.color);
        exportAvatarData();
        const exported = JSON.parse(await exportedText());
        assert.equal(exported.app, APP_NAME);
        assert.equal(exported.version, 1);
        assert.equal(exported.avatar.name, avatar.name);
        assert.equal(downloads.length, 1);
        assert.match(downloads[0].download, /^portal-hub-data-\d{4}-\d{2}-\d{2}\.json$/);
        importObject({name: 'Legacy', color: '#123456'});
        fieldsEqual(myAvatar);
        importObject(exported);
        fieldsEqual(avatar);
        startHub(false);
        fieldsEqual(avatar);
        assert.equal(myAvatar.name, avatar.name);
        assert.equal(myAvatar.color, avatar.color);
        assert.equal(JSON.parse(storageData.get(STORAGE_KEY)).name, avatar.name);
    """)


def test_start_uses_previous_name_for_blank_input_and_keeps_the_forms_in_sync():
    run_scenario(r"""
        importObject({name: 'Previous', color: '#112233'});
        document.getElementById('start-name').value = ' \t ';
        document.getElementById('start-color').value = '#abcdef';
        startHub(false);
        assert.equal(started, true);
        assert.equal(myAvatar.name, 'Previous');
        assert.equal(myAvatar.color, '#abcdef');
        fieldsEqual(myAvatar);
        assert.equal(JSON.parse(storageData.get(STORAGE_KEY)).name, 'Previous');
    """)


def test_invalid_start_fields_keep_the_previous_avatar_with_visible_feedback():
    run_scenario(r"""
        importObject({name: 'Previous', color: '#112233'});
        document.getElementById('start-name').value = '\u0000bad';
        document.getElementById('start-color').value = '#abcdef';
        startHub(false);
        assert.equal(started, true);
        assert.equal(myAvatar.name, 'Previous');
        assert.equal(myAvatar.color, '#112233');
        fieldsEqual(myAvatar);
        assert.match(document.getElementById('avatar-feedback').textContent, /Previous avatar kept/);
    """)


@pytest.mark.parametrize("invalid", [
    "{",
    "null",
    "[]",
    "42",
    '"avatar"',
    "{}",
    '{"name":null,"color":"#123456"}',
    '{"name":42,"color":"#123456"}',
    '{"name":{},"color":"#123456"}',
    '{"name":"","color":"#123456"}',
    '{"name":"too-long-avatar-name","color":"#123456"}',
    '{"name":"New","color":42}',
    '{"name":"New","color":"red"}',
    '{"name":"New","color":"#xyzxyz"}',
    '{"name":"New","color":"#123"}',
    '{"app":"other-app","version":1,"avatar":{"name":"New","color":"#123456"}}',
    '{"app":"portal-hub","version":"1","avatar":{"name":"New","color":"#123456"}}',
    '{"app":"portal-hub","version":2,"avatar":{"name":"New","color":"#123456"}}',
    '{"app":"portal-hub","version":1,"avatar":null}',
    '{"app":"portal-hub","version":1,"avatar":[]}',
])
def test_rejected_import_preserves_last_good_avatar_and_storage(invalid):
    run_scenario(r"""
        importObject({name: 'Last good', color: '#12abcd'});
        const before = JSON.stringify(myAvatar);
        const saved = storageData.get(STORAGE_KEY);
        importText(INVALID);
        assert.equal(JSON.stringify(myAvatar), before);
        assert.equal(storageData.get(STORAGE_KEY), saved);
        fieldsEqual(myAvatar);
        assert.match(document.getElementById('avatar-feedback').textContent, /Import failed/i);
        assert.match(document.getElementById('avatar-feedback').textContent, /kept/i);
        assert.equal(document.getElementById('avatar-feedback').hidden, false);
    """.replace("INVALID", json.dumps(invalid)))


def test_read_failure_preserves_avatar_and_file_input_can_be_reused():
    run_scenario(r"""
        importObject({name: 'Good', color: '#102030'});
        const input = {files: [{error: true, size: 1}], value: 'bad.json'};
        importAvatarData({target: input});
        assert.equal(myAvatar.name, 'Good');
        assert.equal(input.value, '');
        assert.match(document.getElementById('avatar-feedback').textContent, /read/i);
        assert.match(document.getElementById('avatar-feedback').textContent, /kept/i);
    """)


def test_valid_name_spacing_round_trips_and_hex_color_is_canonicalized():
    run_scenario(r"""
        importObject({name: '  Explorer  ', color: '#ABCDEF'});
        fieldsEqual({name: '  Explorer  ', color: '#abcdef'});
        exportAvatarData();
        importObject(JSON.parse(await exportedText()));
        startHub(false);
        fieldsEqual({name: '  Explorer  ', color: '#abcdef'});
    """)


def test_oversized_and_superseded_imports_cannot_overwrite_the_latest_avatar():
    run_scenario(r"""
        importObject({name: 'Good', color: '#123456'});
        importAvatarData({target: {files: [{size: 65537, text: '{}'}], value: 'huge.json'}});
        assert.equal(myAvatar.name, 'Good');
        assert.match(document.getElementById('avatar-feedback').textContent, /64 KB/);
        const readers = [];
        FileReader.prototype.readAsText = function(file) {
            this.result = file.text;
            readers.push(this);
        };
        importObject({name: 'Older', color: '#111111'});
        importObject({name: 'Newest', color: '#222222'});
        readers[1].onload();
        readers[0].onload();
        fieldsEqual({name: 'Newest', color: '#222222'});
        assert.equal(JSON.parse(storageData.get(STORAGE_KEY)).name, 'Newest');
    """)


@pytest.mark.parametrize("raw", [
    "{",
    "null",
    "[]",
    '{"name":{},"color":"garbage"}',
])
def test_corrupt_saved_avatar_is_not_applied(raw):
    run_scenario(r"""
        const good = {...myAvatar};
        storageData.set(STORAGE_KEY, RAW);
        loadAvatar();
        assert.equal(myAvatar.name, good.name);
        assert.equal(myAvatar.color, good.color);
        fieldsEqual(good);
        assert.equal(storageData.get(STORAGE_KEY), RAW);
        assert.ok(warnings.length > 0);
        assert.match(document.getElementById('start-avatar-feedback').textContent, /saved avatar/i);
        assert.match(document.getElementById('start-avatar-feedback').textContent, /temporary/i);
    """.replace("RAW", json.dumps(raw)))


def test_denied_storage_is_visible_without_blocking_import_or_start():
    run_scenario(r"""
        storage.readError = new Error('SecurityError');
        storage.writeError = new Error('QuotaExceededError');
        loadAvatar();
        importObject({name: 'Temporary', color: '#123456'});
        startHub(false);
        assert.equal(started, true);
        fieldsEqual({name: 'Temporary', color: '#123456'});
        assert.ok(warnings.length >= 2);
        assert.match(document.getElementById('avatar-feedback').textContent, /temporary|only in this tab/i);
        assert.match(document.getElementById('start-avatar-feedback').textContent, /storage/i);
        assert.equal(storageData.size, 0);
        exportAvatarData();
        assert.equal(JSON.parse(await exportedText()).avatar.name, 'Temporary');
    """)


def test_avatar_listeners_keep_both_forms_in_sync_and_import_is_keyboard_native():
    source = PAGE.read_text(encoding="utf-8")
    assert re.search(r'<button\b[^>]*id="import-avatar-btn"', source)
    run_scenario(r"""
        bindUI();
        const name = document.getElementById('my-name');
        name.value = 'Edited';
        name.emit('change');
        const color = document.getElementById('my-color');
        color.value = '#123456';
        color.emit('change');
        fieldsEqual({name: 'Edited', color: '#123456'});
        name.value = '';
        name.emit('change');
        fieldsEqual({name: 'Edited', color: '#123456'});
        let opened = false;
        document.getElementById('import-avatar').click = () => { opened = true; };
        document.getElementById('import-avatar-btn').click();
        assert.equal(opened, true);
    """)


@pytest.mark.parametrize("clipboard", [
    "undefined",
    "{}",
    "{writeText: async () => { throw new Error('denied'); }}",
    "{writeText: () => { throw new Error('blocked'); }}",
])
def test_clipboard_failure_exposes_a_selected_read_only_room_link(clipboard):
    run_scenario(r"""
        navigator.clipboard = CLIPBOARD;
        myPeerId = 'peer&with?reserved=characters#too';
        updateShareLink();
        const button = document.getElementById('copy-link');
        assert.equal(button.disabled, false);
        await button.onclick();
        const field = document.getElementById('share-link');
        assert.equal(field.hidden, false);
        assert.equal(field.readOnly, true);
        assert.equal(field.selected, true);
        const link = new URL(field.value);
        assert.equal(link.searchParams.get('room'), myPeerId);
        assert.equal(link.searchParams.has('old'), false);
        assert.equal(link.hash, '');
        assert.match(document.getElementById('hub-hint').textContent, /copy/i);
        assert.ok(warnings.length > 0);
    """.replace("CLIPBOARD", clipboard))


def test_clipboard_success_and_no_room_does_not_publish_a_null_invite():
    run_scenario(r"""
        let copied;
        navigator.clipboard = {writeText: async text => { copied = text; }};
        updateShareLink();
        assert.equal(document.getElementById('copy-link').disabled, true);
        myPeerId = 'real-room-id';
        updateShareLink();
        await document.getElementById('copy-link').onclick();
        assert.equal(new URL(copied).searchParams.get('room'), myPeerId);
        assert.equal(document.getElementById('copy-link').textContent, 'Copied ✓');
    """)


def test_qr_failure_hides_stale_pixels_and_keeps_a_copyable_link():
    run_scenario(r"""
        myPeerId = 'good-room';
        updateShareLink();
        assert.equal(document.getElementById('qr-wrap').style.display, 'inline-block');
        myPeerId = 'a'.repeat(5000);
        updateShareLink();
        assert.equal(document.getElementById('qr-wrap').style.display, 'none');
        assert.equal(document.getElementById('share-link').hidden, false);
        assert.equal(new URL(document.getElementById('share-link').value).searchParams.get('room'), myPeerId);
        assert.match(document.getElementById('hub-hint').textContent, /QR/i);
    """)


# Computed with licensed upstream Nayuki qrcodegen, then decoded from the app's
# real Chrome canvas PNGs with both BarcodeDetector and independent jsQR 1.4.0.
# These fixed vectors keep the ordinary regression suite network/browser-free.
QR_VECTORS = [
    (
        "https://example.test/?room=one",
        "f5d6600ae4443e0fbc1c92618f91798ee5cdd459145d873ffedbaffd8988a05c",
        "46d031dc9bc181e0fcbbf0496fb082f4cb7f41d0a10ed449355d41690db42c62",
        148,
    ),
    (
        "https://kody-w.github.io/localFirstTools/apps/quantum-worlds/portal-hub.html"
        "?room=5cb69c15-8805-46f8-81c9-615c6fb592b0",
        "e851f9723f086883f794ca65f05b59d2917cc95ba1b8593bb69e0f3f4dd058c5",
        "6b065b758abbcaced3579cd119b2ed4da509a39e294ecf83b30b11719278b1d9",
        212,
    ),
    (
        "https://example.test/" + "long-section/" * 26 + "?room=longer-room-1234",
        "05b4d288d91d50ca50a0c860868051104fada70da3f7cec32570740ab7ff9200",
        "33fb5262b6196e3ee73c6f00d7b4f4f2845d0d0150de1610b65c41e11e601618",
        170,
    ),
    (
        "https://example.test/世界?room=光-🌀",
        "e18cca994844becedcf9e74cc1b2eb3e88025ce576abb35c2f3d60b18f913a4c",
        "a19b46cc524878d4e95360e2d8028a1d70ac23cdd0f7ff625092b4d09c8d5686",
        148,
    ),
    (
        "01234567890123456789",
        "d7954d5c236d5cf2fae234cf890280f49b2711be87544f5f17ab0e3a75753c09",
        "dd7dd3b5c26e08c2903bb9f39eedba2ca60dc64c2f1821f9a6f94145e7c8f7c5",
        116,
    ),
    (
        "HELLO WORLD",
        "7cb519f187a1f6d6294385b11fd9d65487509b897a600c9c5e6398297cd45222",
        "c8507e5dca4b21eb36ebacc215955c2424797662abc8bdad9fa48aa94d9c411e",
        116,
    ),
]


@pytest.mark.parametrize("text,module_hash,pixel_hash,size", QR_VECTORS)
def test_qr_matches_independently_decoded_matrix_and_pixel_vectors(text, module_hash, pixel_hash, size):
    run_scenario(r"""
        const [text, moduleHash, pixelHash, size] = VECTOR;
        const qr = qrcodegen.QrCode.encodeText(text, qrcodegen.Ecc.MEDIUM);
        const matrix = qr.modules.map(row => row.map(bit => bit ? '1' : '0').join('')).join('\n');
        assert.equal(crypto.createHash('sha256').update(matrix).digest('hex'), moduleHash);
        assert.equal(drawQR(text), true);
        assert.equal(document.getElementById('qr-canvas').width, size);
        assert.equal(crypto.createHash('sha256').update(canvasPixels()).digest('hex'), pixelHash);
    """.replace("VECTOR", json.dumps([text, module_hash, pixel_hash, size])))


def test_qr_rejects_capacity_and_parameter_errors_instead_of_looping():
    run_scenario(r"""
        const {QrCode, QrSegment, Ecc} = qrcodegen;
        assert.throws(() => QrCode.encodeText('a'.repeat(5000), Ecc.MEDIUM), /too long/i);
        assert.throws(() => QrCode.encodeSegments([], Ecc.MEDIUM, 0), /parameters/i);
        assert.throws(() => QrCode.encodeSegments([], Ecc.MEDIUM, 1, 41), /parameters/i);
        assert.throws(() => QrCode.encodeSegments([], Ecc.MEDIUM, 2, 1), /parameters/i);
        assert.throws(() => QrCode.encodeSegments([], Ecc.MEDIUM, 1, 40, 8), /parameters/i);
        const segments = QrSegment.makeSegments('https://example.test');
        const qr = QrCode.encodeSegments(segments, Ecc.MEDIUM, 1, 40, 0);
        assert.equal(qr.mask, 0);
        assert.throws(() => QrSegment.makeAlphanumeric('lowercase'), /alphanumeric/i);
    """)


@pytest.mark.parametrize("before,after,scenario", [
    (
        "function syncAvatarFields() {",
        "function syncAvatarFields() { return;",
        "importObject({name: 'Imported', color: '#123456'}); fieldsEqual(myAvatar);",
    ),
    (
        "if (typeof avatar.color !== 'string' || !/^#[0-9a-f]{6}$/i.test(avatar.color))",
        "if (false)",
        """
        importObject({name: 'Good', color: '#123456'});
        importObject({name: 'Bad', color: 'red'});
        assert.equal(myAvatar.color, '#123456');
        """,
    ),
    (
        "feedback.textContent = text;",
        "feedback.textContent = '';",
        """
        storage.writeError = new Error('Storage unavailable');
        saveAvatar();
        assert.match(document.getElementById('avatar-feedback').textContent, /storage/i);
        """,
    ),
    (
        "field.hidden = false;",
        "field.hidden = true;",
        """
        myPeerId = 'room-id';
        updateShareLink();
        await document.getElementById('copy-link').onclick();
        assert.equal(document.getElementById('share-link').hidden, false);
        """,
    ),
    (
        "if (qr.modules[y][x])",
        "if (false)",
        """
        drawQR('https://example.test/?room=one');
        assert.equal(crypto.createHash('sha256').update(canvasPixels()).digest('hex'),
            '46d031dc9bc181e0fcbbf0496fb082f4cb7f41d0a10ed449355d41690db42c62');
        """,
    ),
    (
        "appendBits(seg.mode.modeBits, 4, bb);",
        "appendBits(0, 4, bb);",
        """
        const qr = qrcodegen.QrCode.encodeText('https://example.test/?room=one', qrcodegen.Ecc.MEDIUM);
        const matrix = qr.modules.map(row => row.map(bit => bit ? '1' : '0').join('')).join('\\n');
        assert.equal(crypto.createHash('sha256').update(matrix).digest('hex'),
            'f5d6600ae4443e0fbc1c92618f91798ee5cdd459145d873ffedbaffd8988a05c');
        """,
    ),
])
def test_sharing_assertions_reject_controlled_in_memory_mutations(before, after, scenario):
    source = PAGE.read_text(encoding="utf-8")
    assert source.count(before) == 1, "Mutation must target exactly one invariant"
    run_scenario(scenario, source)
    with pytest.raises(AssertionError, match="ERR_ASSERTION"):
        run_scenario(scenario, source.replace(before, after, 1))
