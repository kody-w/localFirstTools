(function () {
  var root = document.getElementById('frame-machine-app');
  var config = window.frameMachineConfig || {};
  var simulation = null;
  var liveOverlayState = { status: 'loading', data: null, error: '', sourceLabel: '' };
  var liquidDimensionState = { status: 'loading', data: null, error: '', sourceLabel: '' };
  var currentIndex = 0;
  var isPlaying = false;
  var playbackTimer = null;
  var runtimeLabel = 'Runtime projection';
  var frameIntervalMs = 1800;
  var endBehavior = 'stop';

  if (!root) {
    return;
  }

  function storageKey() {
    return 'frame-machine-bundle:' + (config.appId || 'frame-machine');
  }

  function escapeHtml(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function titleCase(value) {
    return String(value || '')
      .replace(/[-_]/g, ' ')
      .replace(/\b\w/g, function (char) { return char.toUpperCase(); });
  }

  function formatCurrency(value) {
    return '$' + Number(value || 0).toLocaleString('en-US');
  }

  function formatInterval(value) {
    return (Math.round((Number(value) / 100)) / 10).toLocaleString('en-US') + 's';
  }

  function loadImportedBundle() {
    try {
      var raw = window.localStorage ? window.localStorage.getItem(storageKey()) : null;
      return raw ? JSON.parse(raw) : null;
    } catch (error) {
      return null;
    }
  }

  function persistImportedBundle(bundle) {
    if (!window.localStorage) {
      return;
    }
    window.localStorage.setItem(storageKey(), JSON.stringify(bundle));
  }

  function clearImportedBundle() {
    if (!window.localStorage) {
      return;
    }
    window.localStorage.removeItem(storageKey());
  }

  function hasImportedBundle() {
    return !!loadImportedBundle();
  }

  function repoMetadata() {
    var repository = simulation && simulation.repository ? simulation.repository : {
      owner: 'kody-w',
      name: 'localFirstTools',
      branch: 'main',
      url: 'https://github.com/kody-w/localFirstTools',
      pagesUrl: 'https://kody-w.github.io/localFirstTools/'
    };
    var owner = repository.owner || '';
    var name = repository.name || '';
    var branch = repository.branch || 'main';
    var pagesUrl = repository.pagesUrl || '';
    var url = repository.url || '';

    if (window.location && /\.github\.io$/.test(window.location.hostname)) {
      owner = window.location.hostname.split('.')[0] || owner;
      name = window.location.pathname.replace(/^\/+/, '').split('/')[0] || name;
      pagesUrl = 'https://' + owner + '.github.io/' + name + '/';
      url = 'https://github.com/' + owner + '/' + name;
    }

    return {
      owner: owner,
      name: name,
      branch: branch,
      url: url,
      pagesUrl: pagesUrl
    };
  }

  function rawUrlFor(path) {
    var cleanPath = String(path || '').replace(/^\.?\//, '');
    var repository = repoMetadata();
    if (!cleanPath || !repository.owner || !repository.name) {
      return '';
    }
    return 'https://raw.githubusercontent.com/' + repository.owner + '/' + repository.name + '/' + repository.branch + '/' + cleanPath;
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

  function loadJson(path, primaryLabel, cacheLabel, onSuccess, onError) {
    var sources = [];
    var rawUrl = rawUrlFor(path);
    if (rawUrl) {
      sources.push({ url: rawUrl, label: primaryLabel || 'GitHub raw user data from the public repo' });
    }
    sources.push({ url: path, label: cacheLabel || 'checked-in cache' });

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

  function overlayCards(frame) {
    var frameData = liveOverlayState.data && liveOverlayState.data.frames ? liveOverlayState.data.frames[frame.id] : null;
    if (!frameData) {
      return [];
    }
    return frameData.cards || frameData.activeSystemData || [];
  }

  function liquidCards(frame) {
    var frameData = liquidDimensionState.data && liquidDimensionState.data.frames ? liquidDimensionState.data.frames[frame.id] : null;
    if (!frameData) {
      return [];
    }
    return frameData.cards || frameData.dimensionData || [];
  }

  function renderKeyValueCards(items) {
    return items.map(function (item) {
      return '<div class="frame-machine-state-item">' +
        '<span class="frame-machine-state-label">' + escapeHtml(item.label) + '</span>' +
        '<strong class="frame-machine-state-value">' + escapeHtml(item.value) + '</strong>' +
      '</div>';
    }).join('');
  }

  function renderMachineStates(machineState) {
    return renderKeyValueCards(Object.keys(machineState || {}).map(function (key) {
      return {
        label: titleCase(key),
        value: machineState[key]
      };
    }));
  }

  function renderTransitions(transitions) {
    return '<ul class="frame-machine-transition-list">' + (transitions || []).map(function (item) {
      return '<li><strong>' + escapeHtml(item.entity) + '</strong><span>' + escapeHtml(item.from) + ' -> ' + escapeHtml(item.to) + '</span><p>' + escapeHtml(item.note) + '</p></li>';
    }).join('') + '</ul>';
  }

  function renderList(items) {
    if (!items || items.length === 0) {
      return '<p class="frame-machine-empty">No items in this frame.</p>';
    }
    return '<ul class="frame-machine-list">' + items.map(function (item) {
      return '<li><strong>' + escapeHtml(item.primary || item.id || item.label || '') + '</strong>' +
        (item.secondary ? '<span>' + escapeHtml(item.secondary) + '</span>' : '') +
        (item.body ? '<p>' + escapeHtml(item.body) + '</p>' : '') +
        (item.meta ? '<em>' + escapeHtml(item.meta) + '</em>' : '') +
      '</li>';
    }).join('') + '</ul>';
  }

  function renderTable(title, rows, columns) {
    if (!rows || rows.length === 0) {
      return '<section class="frame-machine-panel"><h3>' + escapeHtml(title) + '</h3><p class="frame-machine-empty">No records in this frame.</p></section>';
    }
    var header = columns.map(function (column) { return '<th>' + escapeHtml(column.label) + '</th>'; }).join('');
    var body = rows.map(function (row) {
      return '<tr>' + columns.map(function (column) {
        var value = row[column.key];
        return '<td>' + escapeHtml(value == null ? '' : value) + '</td>';
      }).join('') + '</tr>';
    }).join('');
    return '<section class="frame-machine-panel"><h3>' + escapeHtml(title) + '</h3><div class="frame-machine-table-wrap"><table class="frame-machine-table"><thead><tr>' + header + '</tr></thead><tbody>' + body + '</tbody></table></div></section>';
  }

  function renderLineage(items) {
    if (!items || items.length === 0) {
      return '<p class="frame-machine-empty">This frame carries all required state directly.</p>';
    }
    return '<ul class="frame-machine-lineage-list">' + items.map(function (item) {
      return '<li><div class="frame-machine-lineage-head"><strong>' + escapeHtml(item.name) + '</strong><span class="frame-machine-lineage-chip is-' + escapeHtml(item.mode) + '">' + escapeHtml(item.mode) + '</span></div><span>' + escapeHtml(item.source) + '</span><p>' + escapeHtml(item.note) + '</p></li>';
    }).join('') + '</ul>';
  }

  function openPipeline(frame) {
    return (frame.entities.opportunities || []).reduce(function (total, opportunity) {
      return String(opportunity.stage || '').indexOf('Closed') === 0 ? total : total + Number(opportunity.amount || 0);
    }, 0);
  }

  function openCases(frame) {
    return (frame.entities.cases || []).filter(function (item) {
      return item.status !== 'Resolved' && item.status !== 'Closed';
    }).length;
  }

  function activeTasks(frame) {
    return (frame.entities.tasks || []).filter(function (item) {
      return item.status !== 'Done' && item.status !== 'Closed';
    }).length;
  }

  function activeAutomations(frame) {
    return (frame.automations || []).filter(function (item) {
      return item.status !== 'Complete';
    }).length;
  }

  function atRiskAccounts(frame) {
    return (frame.entities.accounts || []).filter(function (item) {
      return item.health === 'At Risk' || item.health === 'Watch';
    }).length;
  }

  function sourceMode(state, cards, fallbackReadyLabel, liveLabel, cacheLabel) {
    if (state.status === 'loading') {
      return { label: 'Hydrating', className: 'is-loading', detail: 'Trying public-repo GitHub raw first, then the checked-in cache.' };
    }
    if (state.status === 'error') {
      return { label: 'Offline', className: 'is-error', detail: state.error || 'Fetch failed.' };
    }
    if (state.status === 'ready' && state.sourceLabel === cacheLabel && cards.length > 0) {
      return { label: fallbackReadyLabel, className: 'is-cache', detail: 'Using the checked-in cache preserved in the repo.' };
    }
    if (state.status === 'ready') {
      return { label: liveLabel, className: 'is-live', detail: 'Using GitHub raw user data from the public repo as the active surface.' };
    }
    return { label: 'Disabled', className: 'is-disabled', detail: 'No runtime surface configured for this proof.' };
  }

  function renderSurfaceSummary(title, state, cards, cacheLabel, liveLabel, fallbackReadyLabel, emptyNote) {
    var mode = sourceMode(state, cards, fallbackReadyLabel, liveLabel, cacheLabel);
    var note = emptyNote;
    if (state.status === 'ready' && cards.length > 0) {
      note = 'Loaded from ' + state.sourceLabel + ' / ' + escapeHtml((state.data && state.data.lastUpdated) || 'unknown timestamp') + '.';
    } else if (state.status === 'loading') {
      note = 'Hydrating this surface from raw data in the public repo.';
    } else if (state.status === 'error') {
      note = state.error;
    }
    return '<div class="frame-machine-source-summary">' +
      '<div class="frame-machine-source-row"><span class="frame-machine-source-chip ' + mode.className + '">' + escapeHtml(mode.label) + '</span><strong>' + escapeHtml(title) + ': ' + escapeHtml(state.sourceLabel || 'None') + '</strong></div>' +
      '<div class="frame-machine-source-meta"><span><strong>Fields:</strong> ' + cards.length + '</span><span><strong>Mode:</strong> ' + escapeHtml(mode.detail) + '</span></div>' +
      '<p class="frame-machine-active-note' + (state.status === 'error' ? ' is-error' : '') + '">' + escapeHtml(note) + '</p>' +
    '</div>';
  }

  function renderResourceLinks() {
    var links = [
      { title: 'Live app URL', url: window.location.href, note: 'The rendered frame machine anyone can open in a browser.' },
      { title: 'Template repository', url: repoMetadata().url, note: 'Fork this public repo and swap the data surfaces while keeping the frame flow.' },
      { title: 'Machine ledger JSON', url: rawUrlFor(config.machinePath), note: 'Canonical frame-by-frame CRM state published from the public repo.' },
      { title: 'Active overlay JSON', url: rawUrlFor(config.overlayPath), note: 'Live edge data layered on top of the frame ledger from the public repo.' },
      { title: 'Liquid dimension JSON', url: rawUrlFor(config.liquidPath), note: 'Fork-aware alternative dimension flowing through the same machine.' }
    ].concat((simulation.relatedProofs || []).map(function (item) {
      return { title: item.title, url: item.url, note: item.note };
    })).filter(function (item) {
      return item.url;
    });

    return '<section class="frame-machine-panel"><h3>Portable state surfaces</h3><ul class="frame-machine-link-list">' + links.map(function (item) {
      return '<li><strong><a href="' + escapeHtml(item.url) + '">' + escapeHtml(item.title) + '</a></strong><span>' + escapeHtml(item.note) + '</span></li>';
    }).join('') + '</ul><p class="frame-machine-surface-note">' + escapeHtml(simulation.portabilityNote || '') + '</p></section>';
  }

  function bundleStatusText() {
    return hasImportedBundle()
      ? 'Imported bundle active. Fork edits are being replayed from local storage until you clear them.'
      : 'Published public-repo raw state is active. Export bundle to back it up or fork it locally.';
  }

  function renderBackupCard() {
    var importExport = simulation.importExport || { title: 'Fork backup and reimport', note: 'Export the machine bundle, edit it locally, and import it back.' };
    return '<section class="frame-machine-panel frame-machine-import-card"><h3>' + escapeHtml(importExport.title) + '</h3><p class="frame-machine-surface-note">' + escapeHtml(importExport.note) + '</p><div class="frame-machine-button-row"><button class="frame-machine-button" data-frame-machine-export>Export bundle</button><button class="frame-machine-button" data-frame-machine-import>Import bundle</button><button class="frame-machine-button" data-frame-machine-clear-import ' + (hasImportedBundle() ? '' : 'disabled') + '>Clear imported bundle</button></div><input class="frame-machine-hidden-input" type="file" accept="application/json" data-frame-machine-import-input><p class="frame-machine-status-note"><strong>Bundle status:</strong> ' + escapeHtml(bundleStatusText()) + '</p></section>';
  }

  function exportBundle() {
    downloadJson((config.appId || 'frame-machine') + '-bundle.json', {
      version: 1,
      exportedAt: new Date().toISOString(),
      appId: config.appId || 'frame-machine',
      machine: simulation,
      overlay: liveOverlayState.data,
      liquid: liquidDimensionState.data
    });
  }

  function applyImportedBundle(bundle) {
    simulation = bundle.machine;
    liveOverlayState = { status: bundle.overlay ? 'ready' : 'disabled', data: bundle.overlay || null, error: '', sourceLabel: 'imported bundle' };
    liquidDimensionState = { status: bundle.liquid ? 'ready' : 'disabled', data: bundle.liquid || null, error: '', sourceLabel: 'imported bundle' };
    runtimeLabel = simulation.runtime && simulation.runtime.label ? simulation.runtime.label : 'Runtime projection';
    frameIntervalMs = Math.max(500, Number(simulation.runtime && (simulation.runtime.frameIntervalMs || simulation.runtime.intervalMs) || 1800));
    endBehavior = simulation.runtime && simulation.runtime.endBehavior === 'loop' ? 'loop' : 'stop';
    currentIndex = 0;
    isPlaying = false;
    clearPlaybackTimer();
    renderFrame(currentIndex);
  }

  function importBundle(file) {
    var reader = new window.FileReader();
    reader.onload = function () {
      try {
        var bundle = JSON.parse(String(reader.result || '{}'));
        if (!bundle.machine || !bundle.machine.frames || !bundle.machine.frames.length) {
          throw new Error('Imported bundle is missing machine frames.');
        }
        persistImportedBundle(bundle);
        applyImportedBundle(bundle);
      } catch (error) {
        window.alert(error && error.message ? error.message : 'Import failed.');
      }
    };
    reader.readAsText(file);
  }

  function clearPlaybackTimer() {
    if (playbackTimer) {
      window.clearTimeout(playbackTimer);
      playbackTimer = null;
    }
  }

  function manualNavigate(nextIndex) {
    if (isPlaying) {
      isPlaying = false;
      clearPlaybackTimer();
    }
    currentIndex = Math.max(0, Math.min(simulation.frames.length - 1, nextIndex));
    renderFrame(currentIndex);
  }

  function stopPlayback(shouldRender) {
    isPlaying = false;
    clearPlaybackTimer();
    if (shouldRender) {
      renderFrame(currentIndex);
    }
  }

  function queueNextTick() {
    clearPlaybackTimer();
    if (!isPlaying) {
      return;
    }
    playbackTimer = window.setTimeout(function () {
      if (currentIndex >= simulation.frames.length - 1) {
        if (endBehavior === 'loop') {
          currentIndex = 0;
        } else {
          stopPlayback(true);
          return;
        }
      } else {
        currentIndex += 1;
      }
      renderFrame(currentIndex);
      queueNextTick();
    }, frameIntervalMs);
  }

  function startPlayback() {
    if (simulation.frames.length < 2) {
      return;
    }
    if (currentIndex >= simulation.frames.length - 1) {
      currentIndex = 0;
    }
    isPlaying = true;
    renderFrame(currentIndex);
    queueNextTick();
  }

  function renderProofPoints() {
    var intro = simulation.intro || {};
    return '<div class="frame-machine-proof-intro"><div class="frame-machine-proof-callout"><strong>Why this matters:</strong> ' + escapeHtml(intro.callout || '') + '</div><ul class="frame-machine-proof-points">' + (intro.points || []).map(function (item) { return '<li>' + escapeHtml(item) + '</li>'; }).join('') + '</ul></div>';
  }

  function renderFrame(index) {
    var frame = simulation.frames[index];
    var overlay = overlayCards(frame);
    var liquid = liquidCards(frame);
    var refreshOverlay = '<button class="frame-machine-button" data-frame-machine-refresh-overlay ' + (liveOverlayState.status === 'loading' ? 'disabled' : '') + '>' + (liveOverlayState.status === 'loading' ? 'Loading public-repo raw data...' : 'Refresh public-repo raw data') + '</button>';
    var refreshLiquid = '<button class="frame-machine-button" data-frame-machine-refresh-liquid ' + (liquidDimensionState.status === 'loading' ? 'disabled' : '') + '>' + (liquidDimensionState.status === 'loading' ? 'Loading liquid dimension...' : 'Refresh liquid dimension') + '</button>';

    root.innerHTML = '' +
      '<header class="frame-machine-page-header"><div class="frame-machine-kicker">' + escapeHtml(simulation.kicker || 'Universal frame machine') + '</div><h1 class="frame-machine-page-title">' + escapeHtml(simulation.title || 'Frame machine') + '</h1><p class="frame-machine-page-deck">' + escapeHtml(simulation.deck || '') + '</p></header>' +
      renderProofPoints() +
      '<div class="frame-machine-top-grid">' + renderResourceLinks() + renderBackupCard() + '</div>' +
      '<div class="frame-machine-shell">' +
        '<section class="frame-machine-hero"><h2>' + escapeHtml(frame.label) + '</h2><p class="frame-machine-summary">' + escapeHtml(frame.summary) + '</p><div class="frame-machine-runtime-row"><div class="frame-machine-runtime-pill ' + (isPlaying ? 'is-running' : 'is-paused') + '">' + escapeHtml(runtimeLabel) + ': ' + (isPlaying ? 'Running' : 'Paused') + '</div><div class="frame-machine-clock-detail">Static clock profile: ' + escapeHtml(formatInterval(frameIntervalMs)) + ' per frame / ' + escapeHtml(endBehavior) + ' at final frame</div></div><div class="frame-machine-controls"><div class="frame-machine-control-cluster"><button class="frame-machine-button" data-frame-machine-prev ' + (index === 0 ? 'disabled' : '') + '>Previous frame</button><button class="frame-machine-button frame-machine-button-primary" data-frame-machine-play aria-pressed="' + (isPlaying ? 'true' : 'false') + '">' + (isPlaying ? 'Pause frame time' : 'Play in frame time') + '</button>' + refreshOverlay + refreshLiquid + '<button class="frame-machine-button" data-frame-machine-next ' + (index === simulation.frames.length - 1 ? 'disabled' : '') + '>Next frame</button></div><input class="frame-machine-range" type="range" min="0" max="' + (simulation.frames.length - 1) + '" value="' + index + '" data-frame-machine-range></div><div class="frame-machine-meta"><span><strong>Clock:</strong> ' + escapeHtml(frame.clock) + '</span><span><strong>Frame:</strong> ' + escapeHtml((index + 1) + ' / ' + simulation.frames.length) + '</span></div><p class="frame-machine-note">' + escapeHtml(frame.note) + '</p></section>' +
        '<section class="frame-machine-stats"><div class="frame-machine-stat"><span>Open pipeline</span><strong>' + formatCurrency(openPipeline(frame)) + '</strong></div><div class="frame-machine-stat"><span>Open cases</span><strong>' + openCases(frame) + '</strong></div><div class="frame-machine-stat"><span>Active tasks</span><strong>' + activeTasks(frame) + '</strong></div><div class="frame-machine-stat"><span>Live automations</span><strong>' + activeAutomations(frame) + '</strong></div><div class="frame-machine-stat"><span>At-risk accounts</span><strong>' + atRiskAccounts(frame) + '</strong></div></section>' +
        '<div class="frame-machine-grid"><section class="frame-machine-panel"><h3>Machine state</h3><div class="frame-machine-state-grid">' + renderMachineStates(frame.machine) + '</div></section><section class="frame-machine-panel"><h3>Active system data</h3>' + renderSurfaceSummary('Hydration source', liveOverlayState, overlay, 'checked-in cache', 'Live raw', 'Cache fallback', 'The checked-in cache simulates the current running state when external fetches are unavailable.') + '<div class="frame-machine-state-grid">' + renderKeyValueCards(overlay) + '</div></section><section class="frame-machine-panel"><h3>Alternative dimensions</h3>' + renderSurfaceSummary('Dimension source', liquidDimensionState, liquid, 'checked-in liquid dimension', 'Live fork', 'Local fork', 'Forks can replace this file and still flow through the same state machine.') + '<div class="frame-machine-state-grid">' + renderKeyValueCards(liquid) + '</div><p class="frame-machine-dimension-note">' + escapeHtml((liquidDimensionState.data && liquidDimensionState.data.note) || 'Forks can replace the liquid dimension file and still flow through the same machine.') + '</p></section></div>' +
        '<div class="frame-machine-grid"><section class="frame-machine-panel"><h3>State transition log</h3>' + renderTransitions(frame.transitions) + '</section><section class="frame-machine-panel"><h3>Automations</h3>' + renderList((frame.automations || []).map(function (item) { return { primary: item.id, secondary: item.trigger, body: item.action, meta: item.status }; })) + '</section><section class="frame-machine-panel"><h3>State lineage</h3>' + renderLineage(frame.lineage) + '</section></div>' +
        '<div class="frame-machine-grid">' + renderTable('Accounts', frame.entities.accounts || [], [{ key: 'id', label: 'ID' }, { key: 'name', label: 'Name' }, { key: 'lifecycle', label: 'Lifecycle' }, { key: 'owner', label: 'Owner' }, { key: 'health', label: 'Health' }]) + renderTable('Leads', frame.entities.leads || [], [{ key: 'id', label: 'ID' }, { key: 'company', label: 'Company' }, { key: 'stage', label: 'Stage' }, { key: 'score', label: 'Score' }, { key: 'owner', label: 'Owner' }]) + '</div>' +
        '<div class="frame-machine-grid">' + renderTable('Opportunities', frame.entities.opportunities || [], [{ key: 'id', label: 'ID' }, { key: 'name', label: 'Name' }, { key: 'stage', label: 'Stage' }, { key: 'amount', label: 'Amount' }, { key: 'next', label: 'Next step' }]) + renderTable('Cases', frame.entities.cases || [], [{ key: 'id', label: 'ID' }, { key: 'title', label: 'Title' }, { key: 'severity', label: 'Severity' }, { key: 'status', label: 'Status' }, { key: 'owner', label: 'Owner' }]) + '</div>' +
        '<div class="frame-machine-grid">' + renderTable('Tasks', frame.entities.tasks || [], [{ key: 'id', label: 'ID' }, { key: 'queue', label: 'Queue' }, { key: 'title', label: 'Task' }, { key: 'status', label: 'Status' }]) + '</div>' +
      '</div>';

    bindControls();
  }

  function loadOverlay() {
    var imported = loadImportedBundle();
    if (imported && imported.overlay) {
      liveOverlayState = { status: 'ready', data: imported.overlay, error: '', sourceLabel: 'imported bundle' };
      renderFrame(currentIndex);
      return;
    }
    liveOverlayState.status = 'loading';
    renderFrame(currentIndex);
    loadJson(config.overlayPath, 'GitHub raw user data from the public repo', 'checked-in cache', function (data, label) {
      liveOverlayState = { status: 'ready', data: data, error: '', sourceLabel: label };
      renderFrame(currentIndex);
    }, function (error) {
      liveOverlayState = { status: 'error', data: null, error: error, sourceLabel: '' };
      renderFrame(currentIndex);
    });
  }

  function loadLiquid() {
    var imported = loadImportedBundle();
    if (imported && imported.liquid) {
      liquidDimensionState = { status: 'ready', data: imported.liquid, error: '', sourceLabel: 'imported bundle' };
      renderFrame(currentIndex);
      return;
    }
    liquidDimensionState.status = 'loading';
    renderFrame(currentIndex);
    loadJson(config.liquidPath, 'GitHub raw liquid dimension', 'checked-in liquid dimension', function (data, label) {
      liquidDimensionState = { status: 'ready', data: data, error: '', sourceLabel: label };
      renderFrame(currentIndex);
    }, function (error) {
      liquidDimensionState = { status: 'error', data: null, error: error, sourceLabel: '' };
      renderFrame(currentIndex);
    });
  }

  function bindControls() {
    var prev = root.querySelector('[data-frame-machine-prev]');
    var play = root.querySelector('[data-frame-machine-play]');
    var next = root.querySelector('[data-frame-machine-next]');
    var range = root.querySelector('[data-frame-machine-range]');
    var refreshOverlay = root.querySelector('[data-frame-machine-refresh-overlay]');
    var refreshLiquid = root.querySelector('[data-frame-machine-refresh-liquid]');
    var exportButton = root.querySelector('[data-frame-machine-export]');
    var importButton = root.querySelector('[data-frame-machine-import]');
    var clearImportButton = root.querySelector('[data-frame-machine-clear-import]');
    var importInput = root.querySelector('[data-frame-machine-import-input]');

    if (prev) {
      prev.addEventListener('click', function () { manualNavigate(currentIndex - 1); });
    }
    if (play) {
      play.addEventListener('click', function () {
        if (isPlaying) {
          stopPlayback(true);
          return;
        }
        startPlayback();
      });
    }
    if (next) {
      next.addEventListener('click', function () { manualNavigate(currentIndex + 1); });
    }
    if (range) {
      range.addEventListener('input', function () { manualNavigate(Number(this.value)); });
    }
    if (refreshOverlay) {
      refreshOverlay.addEventListener('click', function () { loadOverlay(); });
    }
    if (refreshLiquid) {
      refreshLiquid.addEventListener('click', function () { loadLiquid(); });
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
        clearImportedBundle();
        window.location.reload();
      });
    }
  }

  function initialize(machineData) {
    simulation = machineData;
    runtimeLabel = simulation.runtime && simulation.runtime.label ? simulation.runtime.label : 'Runtime projection';
    frameIntervalMs = Math.max(500, Number(simulation.runtime && (simulation.runtime.frameIntervalMs || simulation.runtime.intervalMs) || 1800));
    endBehavior = simulation.runtime && simulation.runtime.endBehavior === 'loop' ? 'loop' : 'stop';
    currentIndex = 0;
    renderFrame(currentIndex);
    loadOverlay();
    loadLiquid();
    if (simulation.runtime && simulation.runtime.autoPlay) {
      startPlayback();
    }
  }

  function renderLoadError(message) {
    root.innerHTML = '<section class="frame-machine-panel"><h1 class="frame-machine-page-title">Frame machine failed to load</h1><p class="frame-machine-active-note is-error frame-machine-load-error">' + escapeHtml(message) + '</p><p class="frame-machine-surface-note">The runtime expects a machine ledger at ' + escapeHtml(config.machinePath || 'data/frame-machines/dynamics365/machine.json') + '.</p></section>';
  }

  if (!window.fetch) {
    renderLoadError('This browser does not support fetch.');
    return;
  }

  var imported = loadImportedBundle();
  if (imported && imported.machine) {
    initialize(imported.machine);
    return;
  }

  loadJson(config.machinePath, 'GitHub raw machine', 'checked-in machine', function (data) {
    initialize(data);
  }, function (error) {
    renderLoadError(error);
  });
})();
