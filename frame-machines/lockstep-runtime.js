(function () {
  var root = document.getElementById('lockstep-twin-app');
  var config = window.lockstepTwinConfig || {};
  var simulation = null;
  var actions = [];
  var executedCount = 0;
  var currentActionIndex = -1;
  var status = 'ready';
  var autorunTimer = null;
  var isRunningAll = false;
  var autoPlayDelayMs = 900;

  if (!root) {
    return;
  }

  function storageKey() {
    return 'lockstep-bundle:' + (config.appId || 'lockstep-twin');
  }

  function escapeHtml(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function loadStoredBundle() {
    try {
      var raw = window.localStorage ? window.localStorage.getItem(storageKey()) : null;
      return raw ? JSON.parse(raw) : null;
    } catch (error) {
      return null;
    }
  }

  function saveStoredBundle(bundle) {
    if (!window.localStorage) {
      return;
    }
    window.localStorage.setItem(storageKey(), JSON.stringify(bundle));
  }

  function clearStoredBundle() {
    if (!window.localStorage) {
      return;
    }
    window.localStorage.removeItem(storageKey());
  }

  function hasStoredBundle() {
    return !!loadStoredBundle();
  }

  function repoMetadata() {
    var owner = 'kody-w';
    var name = 'localFirstTools';
    var branch = 'main';
    var url = 'https://github.com/kody-w/localFirstTools';
    if (window.location && /\.github\.io$/.test(window.location.hostname)) {
      owner = window.location.hostname.split('.')[0] || owner;
      name = window.location.pathname.replace(/^\/+/, '').split('/')[0] || name;
      url = 'https://github.com/' + owner + '/' + name;
    }
    return { owner: owner, name: name, branch: branch, url: url };
  }

  function rawUrlFor(path) {
    var cleanPath = String(path || '').replace(/^\.?\//, '');
    var repo = repoMetadata();
    if (!cleanPath) {
      return '';
    }
    return 'https://raw.githubusercontent.com/' + repo.owner + '/' + repo.name + '/' + repo.branch + '/' + cleanPath;
  }

  function downloadJson(filename, data) {
    var blob = new window.Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    var url = window.URL.createObjectURL(blob);
    var link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  }

  function loadJson(path, onSuccess, onError) {
    var sources = [];
    var raw = rawUrlFor(path);
    if (raw) {
      sources.push({ url: raw, label: 'GitHub raw user data' });
    }
    sources.push({ url: path, label: 'checked-in cache' });

    function trySource(index, lastError) {
      if (index >= sources.length) {
        onError(lastError || 'No sources responded.');
        return;
      }
      window.fetch(sources[index].url, { cache: 'no-store' })
        .then(function (response) {
          if (!response.ok) {
            throw new Error('HTTP ' + response.status);
          }
          return response.json();
        })
        .then(function (data) {
          onSuccess(data, sources[index].label);
        })
        .catch(function (error) {
          trySource(index + 1, error && error.message ? error.message : 'Unknown fetch failure');
        });
    }

    trySource(0, 'Unknown fetch failure');
  }

  function stateSignature(state) {
    return Object.keys(state || {}).sort().map(function (key) {
      return key + '=' + String(state[key]);
    }).join('|');
  }

  function simpleHash(value) {
    var hash = 0;
    var index;
    for (index = 0; index < value.length; index += 1) {
      hash = ((hash << 5) - hash) + value.charCodeAt(index);
      hash |= 0;
    }
    return 'hx-' + Math.abs(hash).toString(16);
  }

  function hashState(state) {
    return simpleHash(stateSignature(state));
  }

  function diffStates(twinState, liveState) {
    var keys = {};
    var diffs = [];
    Object.keys(twinState || {}).forEach(function (key) { keys[key] = true; });
    Object.keys(liveState || {}).forEach(function (key) { keys[key] = true; });
    Object.keys(keys).sort().forEach(function (key) {
      var twinValue = twinState && twinState[key] != null ? String(twinState[key]) : 'n/a';
      var liveValue = liveState && liveState[key] != null ? String(liveState[key]) : 'n/a';
      if (twinValue !== liveValue) {
        diffs.push({ field: key, twin: twinValue, live: liveValue });
      }
    });
    return diffs;
  }

  function buildCorrectionFrame(action) {
    if (!action || !action.diffs || action.diffs.length === 0) {
      return null;
    }
    return {
      id: 'correction-' + action.id,
      title: 'Correction frame / ' + action.label,
      summary: 'Drift was detected, so the runtime re-slushes intent and truth into a correction frame before the next action can continue.',
      twinHash: action.twinHash,
      liveHash: action.liveHash,
      corrections: action.diffs.map(function (diff) {
        return { field: diff.field, expected: diff.twin, observed: diff.live, corrected: diff.twin };
      })
    };
  }

  function clearAutorun() {
    if (autorunTimer) {
      window.clearTimeout(autorunTimer);
      autorunTimer = null;
    }
    isRunningAll = false;
  }

  function actionStatus(index) {
    if (index < executedCount) {
      if (status === 'drift' && index === currentActionIndex) {
        return 'drift';
      }
      return 'applied';
    }
    if (status === 'drift' && index > currentActionIndex) {
      return 'blocked';
    }
    if (index === executedCount) {
      return 'next';
    }
    return 'queued';
  }

  function currentAction() {
    if (currentActionIndex >= 0) {
      return actions[currentActionIndex];
    }
    return actions[0];
  }

  function renderBanner(action) {
    if (status === 'ready') {
      return '<div class="lockstep-banner is-ready">Ready. The next accepted action will be mirrored into both systems.</div>';
    }
    if (status === 'drift') {
      return '<div class="lockstep-banner is-drift">Drift detected on ' + escapeHtml(action.label) + '. Execution halted and a correction frame was minted.</div>';
    }
    if (status === 'complete') {
      return '<div class="lockstep-banner is-complete">All actions landed without drift. The twin stayed valid.</div>';
    }
    if (isRunningAll) {
      return '<div class="lockstep-banner is-running">Auto-running until drift. Lockstep still holds through ' + escapeHtml(action.label) + '.</div>';
    }
    return '<div class="lockstep-banner is-healthy">Lockstep maintained through ' + escapeHtml(action.label) + '.</div>';
  }

  function renderRules() {
    return '<ul class="lockstep-rule-list">' + (simulation.rules || []).map(function (rule) { return '<li>' + escapeHtml(rule) + '</li>'; }).join('') + '</ul>';
  }

  function renderRequest(action) {
    return '<div class="lockstep-request"><div><span>Operation</span><strong>' + escapeHtml(action.request.operation) + '</strong></div><div><span>Target</span><strong>' + escapeHtml(action.request.target) + '</strong></div><div><span>Payload</span><strong>' + escapeHtml(action.request.payload) + '</strong></div><p>' + escapeHtml(action.note) + '</p></div>';
  }

  function renderInputs(items) {
    return '<ul class="lockstep-input-list">' + (items || []).map(function (item) {
      return '<li><div class="lockstep-input-head"><strong>' + escapeHtml(item.name) + '</strong><span class="lockstep-input-chip is-' + escapeHtml(item.mode) + '">' + escapeHtml(item.mode) + '</span></div><span>' + escapeHtml(item.source) + '</span><p>' + escapeHtml(item.note) + '</p></li>';
    }).join('') + '</ul>';
  }

  function renderQueue() {
    return '<ol class="lockstep-queue">' + actions.map(function (action, index) {
      var state = actionStatus(index);
      var label = state.charAt(0).toUpperCase() + state.slice(1);
      return '<li class="lockstep-queue-item is-' + state + '"><div class="lockstep-queue-head"><strong>' + escapeHtml(action.label) + '</strong><span class="lockstep-chip is-' + state + '">' + escapeHtml(label) + '</span></div><span>' + escapeHtml(action.clock) + '</span><p>' + escapeHtml(action.note) + '</p></li>';
    }).join('') + '</ol>';
  }

  function renderStateComparison(action) {
    var keys = {};
    Object.keys(action.twinState || {}).forEach(function (key) { keys[key] = true; });
    Object.keys(action.liveState || {}).forEach(function (key) { keys[key] = true; });
    return '<div class="lockstep-table-wrap"><table class="lockstep-state-table"><thead><tr><th>Field</th><th>Twin</th><th>Live</th></tr></thead><tbody>' + Object.keys(keys).sort().map(function (key) {
      var twinValue = action.twinState[key];
      var liveValue = action.liveState[key];
      var different = String(twinValue) !== String(liveValue);
      return '<tr class="lockstep-state-row ' + (different ? 'is-different' : 'is-matching') + '"><td>' + escapeHtml(key) + '</td><td>' + escapeHtml(twinValue) + '</td><td>' + escapeHtml(liveValue) + '</td></tr>';
    }).join('') + '</tbody></table></div>';
  }

  function renderDiffs(action) {
    if (!action || action.diffs.length === 0) {
      return '<p class="lockstep-empty">No drift detected in the current action.</p>';
    }
    return '<ul class="lockstep-diff-list">' + action.diffs.map(function (diff) {
      return '<li><strong>' + escapeHtml(diff.field) + '</strong><span>Twin: ' + escapeHtml(diff.twin) + '</span><span>Live: ' + escapeHtml(diff.live) + '</span></li>';
    }).join('') + '</ul>';
  }

  function renderCorrectionFrame(action) {
    var correctionFrame = buildCorrectionFrame(action);
    if (!correctionFrame) {
      return '<p class="lockstep-empty">No correction frame is needed while lockstep holds.</p>';
    }
    return '<div class="lockstep-correction-card"><div class="lockstep-correction-head"><h4>' + escapeHtml(correctionFrame.title) + '</h4><span>' + escapeHtml(correctionFrame.id) + '</span></div><p>' + escapeHtml(correctionFrame.summary) + '</p><div class="lockstep-correction-grid"><div><strong>Expected twin hash</strong><span>' + escapeHtml(correctionFrame.twinHash) + '</span></div><div><strong>Observed live hash</strong><span>' + escapeHtml(correctionFrame.liveHash) + '</span></div></div><ul class="lockstep-correction-list">' + correctionFrame.corrections.map(function (diff) {
      return '<li><strong>' + escapeHtml(diff.field) + '</strong><span>Expected: ' + escapeHtml(diff.expected) + '</span><span>Observed: ' + escapeHtml(diff.observed) + '</span><span>Correction target: ' + escapeHtml(diff.corrected) + '</span></li>';
    }).join('') + '</ul></div>';
  }

  function renderPolicy() {
    var correction = simulation.correctionPolicy || {};
    var backup = simulation.backupPolicy || {};
    return '<div class="lockstep-request"><div><span>Correction policy</span><strong>' + escapeHtml(correction.title || 'Correction frames') + '</strong></div><p>' + escapeHtml(correction.summary || '') + '</p><div><span>Backup policy</span><strong>' + escapeHtml(backup.title || 'Fork backup and reimport') + '</strong></div><p>' + escapeHtml(backup.summary || 'Export and reimport the twin JSON without losing the drift logic.') + '</p></div>';
  }

  function renderLinks() {
    var links = [
      { title: 'Live console URL', url: window.location.href, note: 'The rendered lockstep twin console.' },
      { title: 'Template repository', url: repoMetadata().url, note: 'Fork this repo and keep the correction-frame logic.' },
      { title: 'Twin JSON', url: rawUrlFor(config.dataPath), note: 'Twin projection, live adapter response, and correction policy.' },
      { title: 'Back to frame machine', url: config.backLink, note: 'Return to the Dynamics frame machine.' }
    ].filter(function (item) { return item.url; });
    return '<section class="frame-machine-panel"><h3>Portable twin surfaces</h3><ul class="frame-machine-link-list">' + links.map(function (item) {
      return '<li><strong><a href="' + escapeHtml(item.url) + '">' + escapeHtml(item.title) + '</a></strong><span>' + escapeHtml(item.note) + '</span></li>';
    }).join('') + '</ul><p class="frame-machine-surface-note">The twin JSON is exportable, forkable, and reimportable just like the base frame machine.</p></section>';
  }

  function renderBackupCard() {
    return '<section class="frame-machine-panel lockstep-import-card"><h3>Fork backup and reimport</h3><p class="frame-machine-surface-note">Export twin bundle to back up the current action stream, edit it locally, and import it back without losing correction-frame behavior.</p><div class="lockstep-button-row"><button class="lockstep-button" data-lockstep-export>Export twin bundle</button><button class="lockstep-button" data-lockstep-import>Import twin bundle</button><button class="lockstep-button" data-lockstep-clear-import ' + (hasStoredBundle() ? '' : 'disabled') + '>Clear imported twin</button></div><input class="lockstep-hidden-input" type="file" accept="application/json" data-lockstep-import-input><p class="lockstep-status-note"><strong>Twin bundle status:</strong> ' + escapeHtml(hasStoredBundle() ? 'Imported fork bundle active.' : 'Published GitHub raw twin active.') + '</p></section>';
  }

  function exportBundle() {
    downloadJson((config.appId || 'lockstep-twin') + '-bundle.json', {
      version: 1,
      exportedAt: new Date().toISOString(),
      appId: config.appId || 'lockstep-twin',
      simulation: simulation
    });
  }

  function applySimulation(data) {
    simulation = data;
    actions = (simulation.actions || []).map(function (action) {
      action.diffs = diffStates(action.twinState, action.liveState);
      action.matches = action.diffs.length === 0;
      action.twinHash = hashState(action.twinState);
      action.liveHash = hashState(action.liveState);
      return action;
    });
    autoPlayDelayMs = Math.max(400, Number(simulation.runtime && simulation.runtime.autoPlayDelayMs || 900));
    executedCount = 0;
    currentActionIndex = -1;
    status = 'ready';
    clearAutorun();
    render();
  }

  function importBundle(file) {
    var reader = new window.FileReader();
    reader.onload = function () {
      try {
        var bundle = JSON.parse(String(reader.result || '{}'));
        var nextSimulation = bundle.simulation || bundle;
        if (!nextSimulation.actions || !nextSimulation.actions.length) {
          throw new Error('Imported bundle is missing action data.');
        }
        saveStoredBundle({ simulation: nextSimulation });
        applySimulation(nextSimulation);
      } catch (error) {
        window.alert(error && error.message ? error.message : 'Import failed.');
      }
    };
    reader.readAsText(file);
  }

  function runNextAction() {
    var action;
    if (status === 'drift' || status === 'complete' || executedCount >= actions.length) {
      clearAutorun();
      return;
    }
    action = actions[executedCount];
    currentActionIndex = executedCount;
    executedCount += 1;
    if (action.matches) {
      status = executedCount >= actions.length ? 'complete' : 'healthy';
    } else {
      status = 'drift';
      clearAutorun();
    }
    render();
  }

  function scheduleAutorun() {
    window.clearTimeout(autorunTimer);
    if (!isRunningAll || status === 'drift' || status === 'complete') {
      return;
    }
    autorunTimer = window.setTimeout(function () {
      runNextAction();
      if (status !== 'drift' && status !== 'complete') {
        scheduleAutorun();
      }
    }, autoPlayDelayMs);
  }

  function runUntilDrift() {
    if (status === 'drift' || status === 'complete') {
      return;
    }
    isRunningAll = true;
    runNextAction();
    if (status !== 'drift' && status !== 'complete') {
      scheduleAutorun();
    }
  }

  function resetSimulation() {
    clearAutorun();
    executedCount = 0;
    currentActionIndex = -1;
    status = 'ready';
    render();
  }

  function bindControls() {
    var nextButton = root.querySelector('[data-lockstep-next]');
    var autoButton = root.querySelector('[data-lockstep-auto]');
    var resetButton = root.querySelector('[data-lockstep-reset]');
    var exportButton = root.querySelector('[data-lockstep-export]');
    var importButton = root.querySelector('[data-lockstep-import]');
    var clearImportButton = root.querySelector('[data-lockstep-clear-import]');
    var importInput = root.querySelector('[data-lockstep-import-input]');

    if (nextButton) {
      nextButton.addEventListener('click', function () {
        clearAutorun();
        runNextAction();
      });
    }
    if (autoButton) {
      autoButton.addEventListener('click', function () { runUntilDrift(); });
    }
    if (resetButton) {
      resetButton.addEventListener('click', function () { resetSimulation(); });
    }
    if (exportButton) {
      exportButton.addEventListener('click', function () { exportBundle(); });
    }
    if (importButton && importInput) {
      importButton.addEventListener('click', function () { importInput.click(); });
      importInput.addEventListener('change', function () {
        if (this.files && this.files[0]) {
          importBundle(this.files[0]);
          this.value = '';
        }
      });
    }
    if (clearImportButton) {
      clearImportButton.addEventListener('click', function () {
        clearStoredBundle();
        window.location.reload();
      });
    }
  }

  function render() {
    var action = currentAction();
    var driftCount = action && action.diffs ? action.diffs.length : 0;
    var nextDisabled = status === 'drift' || status === 'complete' || executedCount >= actions.length;
    var autoDisabled = nextDisabled || isRunningAll;

    root.innerHTML = '' +
      '<div class="frame-machine-top-grid">' + renderLinks() + renderBackupCard() + '</div>' +
      '<div class="lockstep-shell">' +
        '<section class="lockstep-hero"><div class="lockstep-kicker">Executable mirror proof</div><h2>' + escapeHtml(simulation.title) + '</h2><p class="lockstep-summary">' + escapeHtml(simulation.subtitle) + '</p>' + renderBanner(action) + '<div class="lockstep-controls"><button class="lockstep-button lockstep-button-primary" data-lockstep-next ' + (nextDisabled ? 'disabled' : '') + '>Run next action</button><button class="lockstep-button" data-lockstep-auto ' + (autoDisabled ? 'disabled' : '') + '>' + (isRunningAll ? 'Running until drift...' : 'Run until drift') + '</button><button class="lockstep-button" data-lockstep-reset>Reset twin</button></div><div class="lockstep-meta"><span><strong>Twin:</strong> ' + escapeHtml(simulation.targets.twin) + '</span><span><strong>Live:</strong> ' + escapeHtml(simulation.targets.live) + '</span><span><strong>Executed:</strong> ' + escapeHtml(executedCount + ' / ' + actions.length) + '</span></div></section>' +
        '<section class="lockstep-stats"><div class="lockstep-stat"><span>Current twin hash</span><strong>' + escapeHtml(action ? action.twinHash : '--') + '</strong></div><div class="lockstep-stat"><span>Current live hash</span><strong>' + escapeHtml(action ? action.liveHash : '--') + '</strong></div><div class="lockstep-stat"><span>Drift fields</span><strong>' + driftCount + '</strong></div><div class="lockstep-stat"><span>Auto-run delay</span><strong>' + escapeHtml(String(autoPlayDelayMs)) + 'ms</strong></div></section>' +
        '<div class="lockstep-grid"><section class="lockstep-panel"><h3>Lockstep rules</h3>' + renderRules() + renderPolicy() + '</section><section class="lockstep-panel"><h3>' + escapeHtml(currentActionIndex >= 0 ? 'Current action' : 'Next action') + '</h3>' + renderRequest(action) + '</section></div>' +
        '<div class="lockstep-grid"><section class="lockstep-panel"><h3>Action queue</h3>' + renderQueue() + '</section><section class="lockstep-panel"><h3>Action inputs</h3>' + renderInputs(action.inputs) + '<h3>Fork dimensions</h3>' + renderInputs(simulation.forkDimensions || []) + '</section></div>' +
        '<div class="lockstep-grid"><section class="lockstep-panel"><h3>State comparison</h3>' + renderStateComparison(action) + '</section><section class="lockstep-panel"><h3>Drift ledger</h3>' + renderDiffs(action) + '</section></div>' +
        '<div class="lockstep-grid"><section class="lockstep-panel"><h3>Correction frame</h3>' + renderCorrectionFrame(action) + '</section></div>' +
      '</div>';

    bindControls();
  }

  function renderLoadError(message) {
    root.innerHTML = '<section class="frame-machine-panel"><h2>Lockstep twin failed to load</h2><p class="lockstep-empty">' + escapeHtml(message) + '</p></section>';
  }

  if (!window.fetch) {
    renderLoadError('This browser does not support fetch.');
    return;
  }

  var stored = loadStoredBundle();
  if (stored && stored.simulation) {
    applySimulation(stored.simulation);
    return;
  }

  loadJson(config.dataPath, function (data) {
    applySimulation(data);
  }, function (error) {
    renderLoadError(error);
  });
})();
