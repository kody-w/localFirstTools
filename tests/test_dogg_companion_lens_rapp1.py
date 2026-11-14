"""RAPP/1 rev-17 conformance of the DOGG Companion Lens (browser .js and terminal .py).

The two lenses must agree with the kody-w/rapp-1 reference (rapp.py @ f6bafe7): §4 strict JSON and RFC 8785
canonical form, §5 H with its own tags only, and the §7.5 consumer checklist.
"""
import importlib.util
import json
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
LENS_DIR = ROOT / 'apps' / 'quantum-worlds'
TERMINAL = LENS_DIR / 'dogg-companion-lens-terminal.py'
BROWSER = LENS_DIR / 'dogg-companion-lens.js'
BODY = 'rappid:@kody-w/dogg-world:' + 'ab' * 32
EMPTY_PARTICLE = '00d4ee8c3964f0e289ba07982ab8457a7b820056236640bda09572f0725a265b'


def load_terminal():
    spec = importlib.util.spec_from_file_location('dogg_companion_lens_terminal', TERMINAL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


M = load_terminal()


def make_frame(stream_id=BODY, seq=0, prev=None, payload=None):
    frame = {'spec': 'rapp/1', 'kind': 'body.pulse', 'stream_id': stream_id, 'seq': seq,
             'utc': '2026-09-28T10:40:53.256Z', 'payload': payload or {'tick': 1, 'price': '0.655'},
             'prev': prev, 'prev_wave': None, 'sig': None}
    frame['payload_hash'] = M.H('rapp/1:particle', frame['payload'])
    frame['frame_hash'] = M.H('rapp/1:wave', {k: v for k, v in frame.items() if k != 'sig'})
    return frame


GOOD = [b'{"b":0.1,"a":[1E2,-0,1e21,5e-7]}', '{"\ue000":1,"\U0001f600":2}'.encode(), b'{}', b' [true,null,"x"] ']
BAD = [b'{"a":1,"a":2}', b'\xef\xbb\xbf{}', b'["\\ud800"]', b'["\\ufdd0"]', b'{"n":9007199254740993}', b'[1e999]',
       b'[' * 65 + b']' * 65, b'{"a":1}x', b'\xff']


def test_canonical_is_rfc8785_over_the_rev17_domain():
    assert M.canonical(M._strict_json(GOOD[0])) == '{"a":[100,0,1e+21,5e-7],"b":0.1}'
    # member names sort by UTF-16 code units: U+1F600 (D83D DE00) before U+E000
    assert M.canonical(M._strict_json(GOOD[1])) == '{"\U0001f600":2,"\ue000":1}'


@pytest.mark.parametrize('octets', BAD)
def test_strict_json_refuses_what_section_4_refuses(octets):
    with pytest.raises(ValueError):
        M._strict_json(octets)


def test_H_takes_only_its_own_tags():
    assert M.H('rapp/1:particle', {}) == EMPTY_PARTICLE
    for tag in ('rapp/1:egg', 'rapp/1:seal', 'rapp/1:other', 'rapp/1:particle\n'):
        with pytest.raises(ValueError):
            M.H(tag, {})


def test_verify_frame_runs_the_section_7_5_checklist():
    genesis = make_frame()
    assert M.verify_frame(genesis, stream_id_of_record=BODY) == (True, None, 'ok')
    assert M.verify_frame(genesis, stream_id_of_record=BODY + ':x')[:2] == (False, '1a')
    later = make_frame(seq=1, prev=genesis['payload_hash'])
    assert M.verify_frame(later, stream_id_of_record=BODY)[:2] == (False, '4')
    assert M.verify_frame(later, head=genesis, stream_id_of_record=BODY) == (True, None, 'ok')
    tampered = dict(genesis, payload={'tick': 2})
    assert M.verify_frame(tampered)[:2] == (False, '2')
    # the live DOGG world stream id is not a §6.1.1 stream_id: a rev-17 consumer refuses it at step 1
    assert M.verify_frame(make_frame(stream_id='world:@kody-w/dogg'))[:2] == (False, '1')


JS_LOADER = r"""
const fs = require('fs'), vm = require('vm');
const src = fs.readFileSync(process.argv[1], 'utf8'), end = src.lastIndexOf('})();'), noop = () => {};
const ctx = { console, crypto: globalThis.crypto, TextEncoder, TextDecoder, AbortController, setTimeout, clearTimeout,
  URL, atob, btoa, performance: { now: () => 0 }, requestAnimationFrame: noop,
  localStorage: { getItem: () => null, setItem: noop }, location: { pathname: '/test' },
  document: { title: 'test', readyState: 'loading', addEventListener: noop }, window: { addEventListener: noop } };
vm.createContext(ctx);
vm.runInContext(src.slice(0, end) + ';globalThis.U = { parseStrict, canonical, H, verifyFrame };' + src.slice(end), ctx);
const U = ctx.U, job = JSON.parse(fs.readFileSync(0, 'utf8'));
(async () => {
  const values = [];
  for (const hex of job.values) {
    try {
      const v = U.parseStrict(Buffer.from(hex, 'hex'));
      values.push([U.canonical(v), await U.H('rapp/1:particle', v)]);
    } catch (e) { values.push(null); }
  }
  let tagRefused = false;
  try { await U.H('rapp/1:egg', {}); } catch (e) { tagRefused = true; }
  const frames = [];
  for (const [frameHex, headHex, record] of job.frames) {
    const frame = U.parseStrict(Buffer.from(frameHex, 'hex'));
    const head = headHex ? U.parseStrict(Buffer.from(headHex, 'hex')) : null;
    const r = await U.verifyFrame(frame, head, record);
    frames.push([r.ok, r.step]);
  }
  process.stdout.write(JSON.stringify({ values, tagRefused, frames }));
})();
"""


@pytest.mark.skipif(shutil.which('node') is None, reason='node is not installed')
def test_browser_lens_agrees_with_the_terminal_lens():
    genesis = make_frame()
    later = make_frame(seq=1, prev=genesis['payload_hash'])
    cases = [(genesis, None, BODY), (genesis, None, BODY + ':x'), (later, None, BODY), (later, genesis, BODY),
             (dict(genesis, payload={'tick': 2}), None, None), (make_frame(stream_id='world:@kody-w/dogg'), None, None)]
    hexed = lambda value: json.dumps(value).encode().hex()
    job = {'values': [o.hex() for o in GOOD + BAD],
           'frames': [[hexed(f), hexed(h) if h else None, r] for f, h, r in cases]}
    out = json.loads(subprocess.run(['node', '-e', JS_LOADER, str(BROWSER)], input=json.dumps(job),
                                    capture_output=True, text=True, check=True, timeout=60).stdout)
    expected = []
    for octets in GOOD + BAD:
        try:
            value = M._strict_json(octets)
            expected.append([M.canonical(value), M.H('rapp/1:particle', value)])
        except ValueError:
            expected.append(None)
    assert out['values'] == expected
    assert out['tagRefused'] is True
    assert out['frames'] == [list(M.verify_frame(f, head=h, stream_id_of_record=r)[:2]) for f, h, r in cases]
