import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
D365_PAGE = ROOT / 'dynamics365-frame-machine.html'
D365_LOCKSTEP_PAGE = ROOT / 'dynamics365-lockstep-twin.html'
HN_PAGE = ROOT / 'hacker-news-simulator.html'
FRAME_CSS = ROOT / 'frame-machines' / 'frame-machine.css'
D365_RUNTIME = ROOT / 'frame-machines' / 'dynamics365-runtime.js'
HN_RUNTIME = ROOT / 'frame-machines' / 'hacker-news-runtime.js'
LOCKSTEP_RUNTIME = ROOT / 'frame-machines' / 'lockstep-runtime.js'
D365_MACHINE = ROOT / 'data' / 'frame-machines' / 'dynamics365' / 'machine.json'
D365_OVERLAY = ROOT / 'data' / 'frame-machines' / 'dynamics365' / 'active-system-data.json'
D365_LIQUID = ROOT / 'data' / 'frame-machines' / 'dynamics365' / 'liquid-dimension.json'
D365_LOCKSTEP = ROOT / 'data' / 'frame-machines' / 'dynamics365' / 'lockstep.json'
HN_FLOW = ROOT / 'data' / 'frame-machines' / 'hacker-news' / 'frame-flow.json'
HN_LIQUID = ROOT / 'data' / 'frame-machines' / 'hacker-news' / 'liquid-dimension.json'
HN_FEED = ROOT / 'data' / 'content' / 'hacker-news-posts.json'
WORKFLOW = ROOT / '.github' / 'workflows' / 'nightly-hn-update.yml'
README = ROOT / 'README.md'
TOOLS_MANIFEST = ROOT / 'tools-manifest.json'


def test_dynamics_frame_machine_assets_exist():
    page = D365_PAGE.read_text(encoding='utf-8')
    machine = json.loads(D365_MACHINE.read_text(encoding='utf-8'))
    overlay = json.loads(D365_OVERLAY.read_text(encoding='utf-8'))
    liquid = json.loads(D365_LIQUID.read_text(encoding='utf-8'))

    assert 'frameMachineConfig' in page
    assert './frame-machines/dynamics365-runtime.js' in page
    assert './frame-machines/frame-machine.css' in page
    assert machine['repository']['name'] == 'localFirstTools'
    assert machine['relatedProofs'][0]['url'] == './dynamics365-lockstep-twin.html'
    assert 'public repo' in machine['liveOverlay']['label'].lower()
    frame_ids = [frame['id'] for frame in machine['frames']]
    assert set(frame_ids) == set(overlay['frames'].keys())
    assert set(frame_ids) == set(liquid['frames'].keys())
    assert 'Fork backup and reimport' in machine['importExport']['title']


def test_hacker_news_frame_machine_uses_feed_backup_flow():
    page = HN_PAGE.read_text(encoding='utf-8')
    flow = json.loads(HN_FLOW.read_text(encoding='utf-8'))
    liquid = json.loads(HN_LIQUID.read_text(encoding='utf-8'))
    feed = json.loads(HN_FEED.read_text(encoding='utf-8'))

    assert 'hnFrameMachineConfig' in page
    assert './frame-machines/hacker-news-runtime.js' in page
    assert flow['feedPath'] == 'data/content/hacker-news-posts.json'
    assert flow['frames'][-1]['id'] == 'backup-reimport'
    assert 'import it back' in flow['importExport']['note']
    frame_ids = [frame['id'] for frame in flow['frames']]
    assert set(frame_ids) == set(liquid['frames'].keys())
    assert len(feed['posts']) > 0


def test_runtimes_support_portable_import_export():
    d365_runtime = D365_RUNTIME.read_text(encoding='utf-8')
    hn_runtime = HN_RUNTIME.read_text(encoding='utf-8')
    lockstep_runtime = LOCKSTEP_RUNTIME.read_text(encoding='utf-8')
    css = FRAME_CSS.read_text(encoding='utf-8')

    assert 'raw.githubusercontent.com' in d365_runtime
    assert 'public repo' in d365_runtime.lower()
    assert 'Export bundle' in d365_runtime
    assert 'Import bundle' in d365_runtime
    assert 'clearImportedBundle' in d365_runtime
    assert 'Export bundle' in hn_runtime
    assert 'Import bundle' in hn_runtime
    assert 'buildCorrectionFrame' in lockstep_runtime
    assert 'Export twin bundle' in lockstep_runtime
    assert '.frame-machine-import-card' in css


def test_lockstep_page_and_data_support_correction_frames():
    page = D365_LOCKSTEP_PAGE.read_text(encoding='utf-8')
    data = json.loads(D365_LOCKSTEP.read_text(encoding='utf-8'))

    assert 'lockstepTwinConfig' in page
    assert './frame-machines/lockstep-runtime.js' in page
    assert data['actions'][3]['id'] == 'action-04'
    assert 'correctionPolicy' in data
    assert 'backupPolicy' in data
    assert 'forkDimensions' in data


def test_docs_and_workflow_reference_frame_machines():
    workflow = WORKFLOW.read_text(encoding='utf-8')
    readme = README.read_text(encoding='utf-8')
    manifest = TOOLS_MANIFEST.read_text(encoding='utf-8')

    assert 'update_hn_content.py' in workflow
    assert 'Frame machine surfaces' in readme
    assert 'backup and reimport' in readme.lower()
    assert 'public repo' in readme.lower()
    assert 'dynamics365-frame-machine.html' in manifest
    assert 'hacker-news-simulator.html' in manifest
