/*!
 * LocalFirst Protocol — v1  ·  kody-w/localFirstTools
 * One tiny, dependency-free, server-free runtime that gives ANY single-file app:
 *   • a shared cross-app/cross-tab event bus       (LocalFirst.bus)
 *   • a portable public identity                   (LocalFirst.identity)
 *   • cross-app achievements + a global profile     (LocalFirst.achievements)
 *   • append-only telemetry you can harvest as data (LocalFirst.telemetry)
 * Drop-in:  <script src="https://kody-w.github.io/localFirstTools/landgrab/lib/localfirst.js"></script>
 * Everything is local-first: it works offline and never phones a server.
 */
(function (global) {
  'use strict';
  var NS = 'localfirst', VER = 1;
  var LS = { get: function (k, d) { try { return JSON.parse(localStorage.getItem(NS + ':' + k)) ?? d; } catch (_) { return d; } },
             set: function (k, v) { try { localStorage.setItem(NS + ':' + k, JSON.stringify(v)); } catch (_) {} } };

  // ── bus: BroadcastChannel across tabs + localStorage mirror for history ──
  function Bus() {
    var subs = {}, hist = {}, CAP = 200, bc = null;
    try { bc = new BroadcastChannel(NS); } catch (_) {}
    function dispatch(m) {
      (hist[m.channel] = hist[m.channel] || []).push(m);
      if (hist[m.channel].length > CAP) hist[m.channel].shift();
      (subs[m.channel] || []).forEach(function (fn) { try { fn(m.payload, m); } catch (_) {} });
      (subs['*'] || []).forEach(function (fn) { try { fn(m.payload, m); } catch (_) {} });
    }
    if (bc) bc.onmessage = function (e) { if (e.data && e.data.__lf) dispatch(e.data); };
    return {
      publish: function (channel, payload) {
        var m = { __lf: VER, channel: channel, payload: payload, ts: Date.now(), from: identity.id };
        dispatch(m); if (bc) try { bc.postMessage(m); } catch (_) {} return m;
      },
      subscribe: function (channel, fn) { (subs[channel] = subs[channel] || []).push(fn);
        return function () { subs[channel] = (subs[channel] || []).filter(function (f) { return f !== fn; }); }; },
      history: function (channel, n) { var h = hist[channel] || []; return n ? h.slice(-n) : h.slice(); }
    };
  }

  // ── identity: a portable public profile, generated once, yours forever ──
  var identity = (function () {
    var id = LS.get('id');
    if (!id) { id = 'lf-' + Math.random().toString(36).slice(2, 8) + Date.now().toString(36); LS.set('id', id); }
    var handle = LS.get('handle', 'anon-' + id.slice(3, 7));
    return { id: id, handle: handle,
      setHandle: function (h) { handle = String(h).slice(0, 24); LS.set('handle', handle); this.handle = handle; return handle; } };
  })();

  var bus = Bus();

  // ── achievements: unlock once, broadcast, persist, show off across apps ──
  var achievements = {
    all: function () { return LS.get('badges', {}); },
    has: function (id) { return !!this.all()[id]; },
    unlock: function (id, meta) {
      var b = this.all(); if (b[id]) return false;
      b[id] = { at: Date.now(), app: (document.title || location.pathname), meta: meta || null };
      LS.set('badges', b); bus.publish('achievement', { id: id, by: identity.id, handle: identity.handle, meta: meta || null });
      telemetry.record('achievement', { id: id }); return true;
    }
  };

  // ── telemetry: append-only local log → export as a harvestable dataset ──
  var telemetry = {
    record: function (type, data) {
      var log = LS.get('telemetry', []); log.push({ t: type, d: data || {}, app: location.pathname, ts: Date.now(), who: identity.id });
      if (log.length > 1000) log = log.slice(-1000); LS.set('telemetry', log);
      bus.publish('telemetry', { type: type, data: data || {} });
    },
    export: function () { return { owner: identity.id, handle: identity.handle, generated: new Date().toISOString(), events: LS.get('telemetry', []) }; },
    download: function () {
      var blob = new Blob([JSON.stringify(this.export(), null, 2)], { type: 'application/json' });
      var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'localfirst-telemetry.json'; a.click();
    }
  };

  // ── score: the shared leaderboard convention (matches snake4) ──
  function score(game, value, extra) {
    telemetry.record('score', Object.assign({ game: game, score: value }, extra || {}));
    return bus.publish('score', Object.assign({ game: game, score: Number(value) || 0, client: identity.id, handle: identity.handle, ts: Date.now() }, extra || {}));
  }

  var LocalFirst = { version: VER, bus: bus, identity: identity, achievements: achievements, telemetry: telemetry, score: score,
    catalog: function () { return fetch('https://kody-w.github.io/localFirstTools/landgrab/index.json').then(function (r) { return r.json(); }); } };
  global.LocalFirst = LocalFirst;
  try { global.bus = global.bus || bus; } catch (_) {}   // back-compat with apps using window.bus
})(typeof window !== 'undefined' ? window : this);
