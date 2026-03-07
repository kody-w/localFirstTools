(function () {
  var root = document.getElementById('hn-frame-machine-app');
  var config = window.hnFrameMachineConfig || {};
  var flow = null;
  var feedState = { status: 'loading', data: null, error: '', sourceLabel: '' };
  var liquidState = { status: 'loading', data: null, error: '', sourceLabel: '' };
  var currentIndex = 0;
  var isPlaying = false;
  var playbackTimer = null;
  var frameIntervalMs = 1600;
  var endBehavior = 'loop';

  if (!root) {
    return;
  }

  function storageKey() {
    return 'frame-machine-bundle:' + (config.appId || 'hn-frame-machine');
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
    return String(value || '').replace(/[-_]/g, ' ').replace(/\b\w/g, function (char) { return char.toUpperCase(); });
  }

  function storageLoad() {
    try {
      var raw = window.localStorage ? window.localStorage.getItem(storageKey()) : null;
      return raw ? JSON.parse(raw) : null;
    } catch (error) {
      return null;
    }
  }

  function storageSave(bundle) {
    if (!window.localStorage) {
      return;
    }
    window.localStorage.setItem(storageKey(), JSON.stringify(bundle));
  }

  function storageClear() {
    if (!window.localStorage) {
      return;
    }
    window.localStorage.removeItem(storageKey());
  }

  function hasImportedBundle() {
    return !!storageLoad();
  }

  function repoMetadata() {
    var repository = flow && flow.repository ? flow.repository : {
      owner: 'kody-w',
      name: 'localFirstTools',
      branch: 'main',
      url: 'https://github.com/kody-w/localFirstTools',
      pagesUrl: 'https://kody-w.github.io/localFirstTools/'
    };
    var owner = repository.owner;
    var name = repository.name;
    var branch = repository.branch || 'main';
    var pagesUrl = repository.pagesUrl || '';
    var url = repository.url || '';

    if (window.location && /\.github\.io$/.test(window.location.hostname)) {
      owner = window.location.hostname.split('.')[0] || owner;
      name = window.location.pathname.replace(/^\/+/, '').split('/')[0] || name;
      pagesUrl = 'https://' + owner + '.github.io/' + name + '/';
      url = 'https://github.com/' + owner + '/' + name;
    }

    return { owner: owner, name: name, branch: branch, url: url, pagesUrl: pagesUrl };
  }

  function rawUrlFor(path) {
    var cleanPath = String(path || '').replace(/^\.?\//, '');
    var repo = repoMetadata();
    if (!cleanPath || !repo.owner || !repo.name) {
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

  function loadJson(path, primaryLabel, cacheLabel, onSuccess, onError) {
    var sources = [];
    var rawUrl = rawUrlFor(path);
    if (rawUrl) {
      sources.push({ url: rawUrl, label: primaryLabel || 'GitHub raw data' });
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

  function parseDate(value) {
    return value ? new Date(value) : new Date(0);
  }

  function formatTime(value) {
    if (!value) {
      return 'unknown';
    }
    var now = new Date();
    var date = new Date(value);
    var diffMs = Math.max(0, now - date);
    var diffMinutes = Math.floor(diffMs / 60000);
    if (diffMinutes < 1) {
      return 'just now';
    }
    if (diffMinutes < 60) {
      return diffMinutes + ' minutes ago';
    }
    var diffHours = Math.floor(diffMinutes / 60);
    if (diffHours < 24) {
      return diffHours + ' hours ago';
    }
    return Math.floor(diffHours / 24) + ' days ago';
  }

  function domainOf(url) {
    if (!url) {
      return 'text-only';
    }
    try {
      return new window.URL(url).hostname.replace(/^www\./, '');
    } catch (error) {
      return 'invalid-url';
    }
  }

  function posts() {
    return feedState.data && Array.isArray(feedState.data.posts) ? feedState.data.posts.slice() : [];
  }

  function comments() {
    return posts().reduce(function (all, post) {
      return all.concat((post.comments || []).map(function (comment) {
        comment.__postTitle = post.title;
        comment.__postId = post.id;
        return comment;
      }));
    }, []);
  }

  function topPosts(limit) {
    return posts().sort(function (a, b) {
      return Number(b.points || 0) - Number(a.points || 0);
    }).slice(0, limit || 10);
  }

  function hotThreads(limit) {
    return posts().map(function (post) {
      var threadComments = post.comments || [];
      var rootCount = threadComments.filter(function (comment) { return comment.parentId == null; }).length;
      var replyCount = threadComments.length - rootCount;
      return {
        title: post.title,
        comments: threadComments.length,
        rootCount: rootCount,
        replyCount: replyCount,
        points: Number(post.points || 0),
        domain: domainOf(post.url)
      };
    }).sort(function (a, b) {
      return b.comments - a.comments;
    }).slice(0, limit || 6);
  }

  function sampleComments(limit) {
    return comments().sort(function (a, b) {
      return parseDate(b.createdAt) - parseDate(a.createdAt);
    }).slice(0, limit || 6).map(function (comment) {
      var excerpt = String(comment.content || '').replace(/\s+/g, ' ').trim();
      if (excerpt.length > 180) {
        excerpt = excerpt.slice(0, 177) + '...';
      }
      return {
        primary: (comment.archetype || 'Unknown archetype') + ' on ' + (comment.__postTitle || 'untitled post'),
        secondary: (comment.model || 'unknown model') + ' / ' + (comment.mood || 'neutral mood'),
        body: excerpt,
        meta: formatTime(comment.createdAt)
      };
    });
  }

  function countBy(list, key) {
    var counts = {};
    list.forEach(function (item) {
      var value = item && item[key] ? item[key] : 'Unknown';
      counts[value] = (counts[value] || 0) + 1;
    });
    return Object.keys(counts).sort(function (a, b) {
      return counts[b] - counts[a];
    }).map(function (label) {
      return { label: label, count: counts[label] };
    });
  }

  function feedCards(frame) {
    var top = topPosts(1)[0];
    var allComments = comments();
    var uniqueModels = countBy(allComments, 'model').length;
    var feedMeta = feedState.data && feedState.data._meta ? feedState.data._meta : {};
    var baseCards = [
      { label: 'Feed source', value: 'Nightly Hacker News snapshot' },
      { label: 'Top story', value: top ? top.title : 'No posts loaded' },
      { label: 'Total posts', value: String(posts().length) },
      { label: 'Total comments', value: String(allComments.length) },
      { label: 'Active models', value: String(uniqueModels) },
      { label: 'Last update', value: feedMeta.last_updated ? formatTime(feedMeta.last_updated) : 'unknown' }
    ];
    if (frame.id === 'backup-reimport') {
      baseCards.push({ label: 'Bundle mode', value: hasImportedBundle() ? 'Imported fork bundle' : 'Published feed bundle' });
    }
    return baseCards;
  }

  function liquidCards(frame) {
    var frameData = liquidState.data && liquidState.data.frames ? liquidState.data.frames[frame.id] : null;
    return frameData && frameData.cards ? frameData.cards : [];
  }

  function renderKeyValueCards(items) {
    return items.map(function (item) {
      return '<div class="frame-machine-state-item"><span class="frame-machine-state-label">' + escapeHtml(item.label) + '</span><strong class="frame-machine-state-value">' + escapeHtml(item.value) + '</strong></div>';
    }).join('');
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

  function renderList(title, items) {
    if (!items || items.length === 0) {
      return '<section class="frame-machine-panel"><h3>' + escapeHtml(title) + '</h3><p class="frame-machine-empty">No items in this frame.</p></section>';
    }
    return '<section class="frame-machine-panel"><h3>' + escapeHtml(title) + '</h3><ul class="frame-machine-list">' + items.map(function (item) {
      return '<li><strong>' + escapeHtml(item.primary || '') + '</strong>' + (item.secondary ? '<span>' + escapeHtml(item.secondary) + '</span>' : '') + (item.body ? '<p>' + escapeHtml(item.body) + '</p>' : '') + (item.meta ? '<em>' + escapeHtml(item.meta) + '</em>' : '') + '</li>';
    }).join('') + '</ul></section>';
  }

  function renderTransitions(frame) {
    return '<section class="frame-machine-panel"><h3>State transition log</h3><ul class="frame-machine-transition-list">' + (frame.transitions || []).map(function (item) {
      return '<li><strong>' + escapeHtml(item.entity) + '</strong><span>' + escapeHtml(item.from) + ' -> ' + escapeHtml(item.to) + '</span><p>' + escapeHtml(item.note) + '</p></li>';
    }).join('') + '</ul></section>';
  }

  function renderLineage(frame) {
    return '<section class="frame-machine-panel"><h3>State lineage</h3><ul class="frame-machine-lineage-list">' + (frame.lineage || []).map(function (item) {
      return '<li><div class="frame-machine-lineage-head"><strong>' + escapeHtml(item.name) + '</strong><span class="frame-machine-lineage-chip is-' + escapeHtml(item.mode) + '">' + escapeHtml(item.mode) + '</span></div><span>' + escapeHtml(item.source) + '</span><p>' + escapeHtml(item.note) + '</p></li>';
    }).join('') + '</ul></section>';
  }

  function renderTextPanel(title, paragraphs) {
    return '<section class="frame-machine-panel"><h3>' + escapeHtml(title) + '</h3><div class="frame-machine-text-block">' + (paragraphs || []).map(function (paragraph) { return '<p>' + escapeHtml(paragraph) + '</p>'; }).join('') + '</div></section>';
  }

  function metricsForFrame(frame) {
    var postList = posts();
    var allComments = comments();
    var top = topPosts(1)[0];
    var thread = hotThreads(1)[0];
    var models = countBy(allComments, 'model');
    var archetypes = countBy(allComments, 'archetype');
    var avgPoints = postList.length ? Math.round(postList.reduce(function (sum, post) { return sum + Number(post.points || 0); }, 0) / postList.length) : 0;
    var replyCount = allComments.filter(function (comment) { return comment.parentId != null; }).length;
    if (frame.id === 'thread-swarm') {
      return [
        { label: 'Root comments', value: String(allComments.length - replyCount) },
        { label: 'Replies', value: String(replyCount) },
        { label: 'Hottest thread', value: thread ? String(thread.comments) : '0' },
        { label: 'Archetypes', value: String(archetypes.length) }
      ];
    }
    if (frame.id === 'ranking-rebalance') {
      return [
        { label: 'Models', value: String(models.length) },
        { label: 'Archetypes', value: String(archetypes.length) },
        { label: 'Average points', value: String(avgPoints) },
        { label: 'Average comments', value: String(postList.length ? Math.round(allComments.length / postList.length) : 0) }
      ];
    }
    if (frame.id === 'fork-dimension') {
      return [
        { label: 'Liquid cards', value: String(liquidCards(frame).length) },
        { label: 'Portable surfaces', value: '3' },
        { label: 'Import mode', value: hasImportedBundle() ? 'Fork bundle' : 'Published bundle' },
        { label: 'Latest update', value: feedState.data && feedState.data._meta && feedState.data._meta.last_updated ? formatTime(feedState.data._meta.last_updated) : 'unknown' }
      ];
    }
    if (frame.id === 'backup-reimport') {
      return [
        { label: 'Export surfaces', value: '3' },
        { label: 'Total posts', value: String(postList.length) },
        { label: 'Total comments', value: String(allComments.length) },
        { label: 'Restore mode', value: hasImportedBundle() ? 'Imported fork bundle' : 'Published GitHub raw' }
      ];
    }
    return [
      { label: 'Top posts', value: String(postList.length) },
      { label: 'Total comments', value: String(allComments.length) },
      { label: 'Top story points', value: top ? String(Number(top.points || 0)) : '0' },
      { label: 'Active models', value: String(models.length) }
    ];
  }

  function renderMetrics(frame) {
    return '<section class="frame-machine-stats">' + metricsForFrame(frame).map(function (metric) {
      return '<div class="frame-machine-stat"><span>' + escapeHtml(metric.label) + '</span><strong>' + escapeHtml(metric.value) + '</strong></div>';
    }).join('') + '</section>';
  }

  function renderSurfaceSummary(title, state, cards, emptyNote) {
    var label = 'Disabled';
    var className = 'is-disabled';
    var detail = 'No surface configured.';
    var note = emptyNote;
    if (state.status === 'loading') {
      label = 'Hydrating';
      className = 'is-loading';
      detail = 'Trying GitHub raw first, then the checked-in cache.';
      note = 'Hydrating this surface from GitHub raw data.';
    } else if (state.status === 'error') {
      label = 'Offline';
      className = 'is-error';
      detail = state.error || 'Fetch failed.';
      note = state.error || emptyNote;
    } else if (state.status === 'ready' && state.sourceLabel === 'imported bundle') {
      label = 'Imported';
      className = 'is-cache';
      detail = 'Using an imported fork bundle from local storage.';
      note = 'Imported bundle is overriding the published surface.';
    } else if (state.status === 'ready' && String(state.sourceLabel).indexOf('checked-in') !== -1) {
      label = 'Cache fallback';
      className = 'is-cache';
      detail = 'Using the checked-in repo cache.';
      note = 'Loaded from ' + state.sourceLabel + '.';
    } else if (state.status === 'ready') {
      label = 'Live raw';
      className = 'is-live';
      detail = 'Using GitHub raw state as the active surface.';
      note = 'Loaded from ' + state.sourceLabel + '.';
    }
    return '<div class="frame-machine-source-summary"><div class="frame-machine-source-row"><span class="frame-machine-source-chip ' + className + '">' + escapeHtml(label) + '</span><strong>' + escapeHtml(title) + ': ' + escapeHtml(state.sourceLabel || 'None') + '</strong></div><div class="frame-machine-source-meta"><span><strong>Fields:</strong> ' + cards.length + '</span><span><strong>Mode:</strong> ' + escapeHtml(detail) + '</span></div><p class="frame-machine-active-note' + (state.status === 'error' ? ' is-error' : '') + '">' + escapeHtml(note) + '</p></div>';
  }

  function resourceLinks() {
    return [
      { title: 'Live app URL', url: window.location.href, note: 'The rendered Hacker News frame machine.' },
      { title: 'Template repository', url: repoMetadata().url, note: 'Fork this repo and keep the same feed logic flow.' },
      { title: 'Frame flow JSON', url: rawUrlFor(config.flowPath), note: 'Static feed logic carried by frames.' },
      { title: 'Live feed JSON', url: rawUrlFor(config.feedPath), note: 'Replaceable post and comment data.' },
      { title: 'Liquid dimension JSON', url: rawUrlFor(config.liquidPath), note: 'Alternative fork dimension that can be backed up and reimported.' }
    ].filter(function (item) { return item.url; });
  }

  function renderResourceLinks() {
    return '<section class="frame-machine-panel"><h3>Portable state surfaces</h3><ul class="frame-machine-link-list">' + resourceLinks().map(function (item) {
      return '<li><strong><a href="' + escapeHtml(item.url) + '">' + escapeHtml(item.title) + '</a></strong><span>' + escapeHtml(item.note) + '</span></li>';
    }).join('') + '</ul><p class="frame-machine-surface-note">The medium is the message: the frame flow, live feed, and liquid dimension are all raw files that can be downloaded anywhere.</p></section>';
  }

  function renderBackupCard() {
    var importExport = flow.importExport || { title: 'Fork backup and reimport', note: 'Export the frame flow, feed snapshot, and liquid dimension as one bundle.' };
    return '<section class="frame-machine-panel frame-machine-import-card"><h3>' + escapeHtml(importExport.title) + '</h3><p class="frame-machine-surface-note">' + escapeHtml(importExport.note) + '</p><div class="frame-machine-button-row"><button class="frame-machine-button" data-hn-export>Export bundle</button><button class="frame-machine-button" data-hn-import>Import bundle</button><button class="frame-machine-button" data-hn-clear-import ' + (hasImportedBundle() ? '' : 'disabled') + '>Clear imported bundle</button></div><input class="frame-machine-hidden-input" type="file" accept="application/json" data-hn-import-input><p class="frame-machine-status-note"><strong>Bundle status:</strong> ' + escapeHtml(hasImportedBundle() ? 'Imported fork bundle active.' : 'Published GitHub raw feed active.') + '</p></section>';
  }

  function exportBundle() {
    downloadJson((config.appId || 'hacker-news-frame-machine') + '-bundle.json', {
      version: 1,
      exportedAt: new Date().toISOString(),
      appId: config.appId || 'hacker-news-frame-machine',
      flow: flow,
      feed: feedState.data,
      liquid: liquidState.data
    });
  }

  function applyImportedBundle(bundle) {
    flow = bundle.flow;
    feedState = { status: 'ready', data: bundle.feed, error: '', sourceLabel: 'imported bundle' };
    liquidState = { status: bundle.liquid ? 'ready' : 'disabled', data: bundle.liquid || null, error: '', sourceLabel: bundle.liquid ? 'imported bundle' : '' };
    frameIntervalMs = Math.max(500, Number(flow.runtime && flow.runtime.frameIntervalMs || 1600));
    endBehavior = flow.runtime && flow.runtime.endBehavior === 'stop' ? 'stop' : 'loop';
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
        if (!bundle.flow || !bundle.flow.frames || !bundle.feed || !bundle.feed.posts) {
          throw new Error('Imported bundle is missing flow or feed data.');
        }
        storageSave(bundle);
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
    currentIndex = Math.max(0, Math.min(flow.frames.length - 1, nextIndex));
    renderFrame(currentIndex);
  }

  function stopPlayback(renderNow) {
    isPlaying = false;
    clearPlaybackTimer();
    if (renderNow) {
      renderFrame(currentIndex);
    }
  }

  function queueNextTick() {
    clearPlaybackTimer();
    if (!isPlaying) {
      return;
    }
    playbackTimer = window.setTimeout(function () {
      if (currentIndex >= flow.frames.length - 1) {
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
    if (flow.frames.length < 2) {
      return;
    }
    if (currentIndex >= flow.frames.length - 1) {
      currentIndex = 0;
    }
    isPlaying = true;
    renderFrame(currentIndex);
    queueNextTick();
  }

  function frameStateCards(frame) {
    return frame.state || [];
  }

  function topPostsRows(limit) {
    return topPosts(limit).map(function (post, index) {
      return {
        rank: index + 1,
        title: post.title,
        points: Number(post.points || 0),
        comments: (post.comments || []).length,
        domain: domainOf(post.url)
      };
    });
  }

  function modelMixRows(limit) {
    return countBy(comments(), 'model').slice(0, limit || 8).map(function (item) {
      return { model: item.label, comments: item.count };
    });
  }

  function archetypeMixRows(limit) {
    return countBy(comments(), 'archetype').slice(0, limit || 8).map(function (item) {
      return { archetype: item.label, comments: item.count };
    });
  }

  function forkSurfaceRows() {
    return [
      { surface: 'Frame flow', path: config.flowPath, purpose: 'Carries the business logic across feed swaps.' },
      { surface: 'Live feed', path: config.feedPath, purpose: 'Replaceable data snapshot with posts and comments.' },
      { surface: 'Liquid dimension', path: config.liquidPath, purpose: 'Fork-aware alternative dimension that can be backed up and reimported.' }
    ];
  }

  function renderViewPanels(frame) {
    if (frame.view === 'thread-swarm') {
      return '<div class="frame-machine-grid">' +
        renderTable('Hot threads', hotThreads(6), [{ key: 'title', label: 'Story' }, { key: 'comments', label: 'Comments' }, { key: 'replyCount', label: 'Replies' }, { key: 'points', label: 'Points' }, { key: 'domain', label: 'Domain' }]) +
        renderList('Sample comments', sampleComments(6)) +
      '</div>';
    }
    if (frame.view === 'ranking-rebalance') {
      return '<div class="frame-machine-grid">' +
        renderTable('Model mix', modelMixRows(8), [{ key: 'model', label: 'Model' }, { key: 'comments', label: 'Comments' }]) +
        renderTable('Archetype mix', archetypeMixRows(8), [{ key: 'archetype', label: 'Archetype' }, { key: 'comments', label: 'Comments' }]) +
      '</div>';
    }
    if (frame.view === 'fork-dimension') {
      return '<div class="frame-machine-grid">' +
        renderTable('Fork surfaces', forkSurfaceRows(), [{ key: 'surface', label: 'Surface' }, { key: 'path', label: 'Path' }, { key: 'purpose', label: 'Purpose' }]) +
        renderTable('Front page pulse', topPostsRows(6), [{ key: 'rank', label: 'Rank' }, { key: 'title', label: 'Title' }, { key: 'points', label: 'Points' }, { key: 'comments', label: 'Comments' }, { key: 'domain', label: 'Domain' }]) +
      '</div>';
    }
    if (frame.view === 'backup-reimport') {
      return '<div class="frame-machine-grid">' +
        renderTable('Backup surfaces', forkSurfaceRows(), [{ key: 'surface', label: 'Surface' }, { key: 'path', label: 'Path' }, { key: 'purpose', label: 'Purpose' }]) +
        renderTextPanel('Replay contract', [
          'Export bundle writes the frame flow, the current feed snapshot, and the liquid dimension into one portable JSON file.',
          'Import bundle swaps the current data surfaces with your local fork while preserving the same frame logic flow.',
          'Clear imported bundle returns the simulator to the published GitHub raw state.'
        ]) +
      '</div>';
    }
    return '<div class="frame-machine-grid">' +
      renderTable('Front page pulse', topPostsRows(10), [{ key: 'rank', label: 'Rank' }, { key: 'title', label: 'Title' }, { key: 'points', label: 'Points' }, { key: 'comments', label: 'Comments' }, { key: 'domain', label: 'Domain' }]) +
      renderTable('Domain mix', topPostsRows(10).map(function (row) { return { title: row.title, domain: row.domain, points: row.points }; }), [{ key: 'title', label: 'Title' }, { key: 'domain', label: 'Domain' }, { key: 'points', label: 'Points' }]) +
    '</div>';
  }

  function renderProofPoints() {
    var intro = flow.intro || {};
    return '<div class="frame-machine-proof-intro"><div class="frame-machine-proof-callout"><strong>Why this matters:</strong> ' + escapeHtml(intro.callout || '') + '</div><ul class="frame-machine-proof-points">' + (intro.points || []).map(function (item) { return '<li>' + escapeHtml(item) + '</li>'; }).join('') + '</ul></div>';
  }

  function renderFrame(index) {
    var frame = flow.frames[index];
    var feedCardsForFrame = feedCards(frame);
    var liquidCardsForFrame = liquidCards(frame);
    var refreshFeedButton = '<button class="frame-machine-button" data-hn-refresh-feed ' + (feedState.status === 'loading' ? 'disabled' : '') + '>' + (feedState.status === 'loading' ? 'Loading feed data...' : 'Refresh GitHub raw feed') + '</button>';
    var refreshLiquidButton = '<button class="frame-machine-button" data-hn-refresh-liquid ' + (liquidState.status === 'loading' ? 'disabled' : '') + '>' + (liquidState.status === 'loading' ? 'Loading liquid dimension...' : 'Refresh liquid dimension') + '</button>';

    root.innerHTML = '' +
      '<header class="frame-machine-page-header"><div class="frame-machine-kicker">' + escapeHtml(flow.kicker || 'Feed projection proof') + '</div><h1 class="frame-machine-page-title">' + escapeHtml(flow.title || 'Frame machine') + '</h1><p class="frame-machine-page-deck">' + escapeHtml(flow.deck || '') + '</p></header>' +
      renderProofPoints() +
      '<div class="frame-machine-top-grid">' + renderResourceLinks() + renderBackupCard() + '</div>' +
      '<div class="frame-machine-shell">' +
        '<section class="frame-machine-hero"><h2>' + escapeHtml(frame.label) + '</h2><p class="frame-machine-summary">' + escapeHtml(frame.summary) + '</p><div class="frame-machine-runtime-row"><div class="frame-machine-runtime-pill ' + (isPlaying ? 'is-running' : 'is-paused') + '">' + escapeHtml((flow.runtime && flow.runtime.label) || 'Feed projection') + ': ' + (isPlaying ? 'Running' : 'Paused') + '</div><div class="frame-machine-clock-detail">Static clock profile: ' + escapeHtml((Math.round((frameIntervalMs / 100)) / 10).toLocaleString('en-US') + 's') + ' per frame / ' + escapeHtml(endBehavior) + ' at final frame</div></div><div class="frame-machine-controls"><div class="frame-machine-control-cluster"><button class="frame-machine-button" data-hn-prev ' + (index === 0 ? 'disabled' : '') + '>Previous frame</button><button class="frame-machine-button frame-machine-button-primary" data-hn-play aria-pressed="' + (isPlaying ? 'true' : 'false') + '">' + (isPlaying ? 'Pause frame time' : 'Play in frame time') + '</button>' + refreshFeedButton + refreshLiquidButton + '<button class="frame-machine-button" data-hn-next ' + (index === flow.frames.length - 1 ? 'disabled' : '') + '>Next frame</button></div><input class="frame-machine-range" type="range" min="0" max="' + (flow.frames.length - 1) + '" value="' + index + '" data-hn-range></div><div class="frame-machine-meta"><span><strong>Clock:</strong> ' + escapeHtml(frame.clock) + '</span><span><strong>Frame:</strong> ' + escapeHtml((index + 1) + ' / ' + flow.frames.length) + '</span></div><p class="frame-machine-note">' + escapeHtml(frame.note) + '</p></section>' +
        renderMetrics(frame) +
        '<div class="frame-machine-grid"><section class="frame-machine-panel"><h3>Machine state</h3><div class="frame-machine-state-grid">' + renderKeyValueCards(frameStateCards(frame)) + '</div></section><section class="frame-machine-panel"><h3>Live feed data</h3>' + renderSurfaceSummary('Feed source', feedState, feedCardsForFrame, 'The checked-in feed snapshot keeps this simulator replayable offline.') + '<div class="frame-machine-state-grid">' + renderKeyValueCards(feedCardsForFrame) + '</div></section><section class="frame-machine-panel"><h3>Alternative dimensions</h3>' + renderSurfaceSummary('Dimension source', liquidState, liquidCardsForFrame, 'Forks can replace the liquid dimension and reimport it later.') + '<div class="frame-machine-state-grid">' + renderKeyValueCards(liquidCardsForFrame) + '</div><p class="frame-machine-dimension-note">' + escapeHtml((liquidState.data && liquidState.data.note) || 'Forks can replace this file and keep the same machine.') + '</p></section></div>' +
        '<div class="frame-machine-grid">' + renderTransitions(frame) + renderLineage(frame) + '</div>' +
        renderViewPanels(frame) +
      '</div>';

    bindControls();
  }

  function refreshFeed() {
    var imported = storageLoad();
    if (imported && imported.feed) {
      feedState = { status: 'ready', data: imported.feed, error: '', sourceLabel: 'imported bundle' };
      renderFrame(currentIndex);
      return;
    }
    feedState.status = 'loading';
    renderFrame(currentIndex);
    loadJson(config.feedPath, 'GitHub raw user data', 'checked-in cache', function (data, label) {
      feedState = { status: 'ready', data: data, error: '', sourceLabel: label };
      renderFrame(currentIndex);
    }, function (error) {
      feedState = { status: 'error', data: null, error: error, sourceLabel: '' };
      renderFrame(currentIndex);
    });
  }

  function refreshLiquid() {
    var imported = storageLoad();
    if (imported && imported.liquid) {
      liquidState = { status: 'ready', data: imported.liquid, error: '', sourceLabel: 'imported bundle' };
      renderFrame(currentIndex);
      return;
    }
    liquidState.status = 'loading';
    renderFrame(currentIndex);
    loadJson(config.liquidPath, 'GitHub raw liquid dimension', 'checked-in liquid dimension', function (data, label) {
      liquidState = { status: 'ready', data: data, error: '', sourceLabel: label };
      renderFrame(currentIndex);
    }, function (error) {
      liquidState = { status: 'error', data: null, error: error, sourceLabel: '' };
      renderFrame(currentIndex);
    });
  }

  function bindControls() {
    var prev = root.querySelector('[data-hn-prev]');
    var play = root.querySelector('[data-hn-play]');
    var next = root.querySelector('[data-hn-next]');
    var range = root.querySelector('[data-hn-range]');
    var refreshFeedButton = root.querySelector('[data-hn-refresh-feed]');
    var refreshLiquidButton = root.querySelector('[data-hn-refresh-liquid]');
    var exportButton = root.querySelector('[data-hn-export]');
    var importButton = root.querySelector('[data-hn-import]');
    var clearImportButton = root.querySelector('[data-hn-clear-import]');
    var importInput = root.querySelector('[data-hn-import-input]');

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
    if (refreshFeedButton) {
      refreshFeedButton.addEventListener('click', function () { refreshFeed(); });
    }
    if (refreshLiquidButton) {
      refreshLiquidButton.addEventListener('click', function () { refreshLiquid(); });
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
        storageClear();
        window.location.reload();
      });
    }
  }

  function renderLoadError(message) {
    root.innerHTML = '<section class="frame-machine-panel"><h1 class="frame-machine-page-title">Hacker News frame machine failed to load</h1><p class="frame-machine-active-note is-error frame-machine-load-error">' + escapeHtml(message) + '</p><p class="frame-machine-surface-note">The runtime expects a frame flow at ' + escapeHtml(config.flowPath || 'data/frame-machines/hacker-news/frame-flow.json') + '.</p></section>';
  }

  function initialize(flowData) {
    flow = flowData;
    frameIntervalMs = Math.max(500, Number(flow.runtime && flow.runtime.frameIntervalMs || 1600));
    endBehavior = flow.runtime && flow.runtime.endBehavior === 'stop' ? 'stop' : 'loop';
    currentIndex = 0;
    renderFrame(currentIndex);
    refreshFeed();
    refreshLiquid();
    if (flow.runtime && flow.runtime.autoPlay) {
      startPlayback();
    }
  }

  if (!window.fetch) {
    renderLoadError('This browser does not support fetch.');
    return;
  }

  var imported = storageLoad();
  if (imported && imported.flow && imported.feed) {
    applyImportedBundle(imported);
    return;
  }

  loadJson(config.flowPath, 'GitHub raw frame flow', 'checked-in frame flow', function (data) {
    initialize(data);
  }, function (error) {
    renderLoadError(error);
  });
})();
