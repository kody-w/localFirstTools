/*!
 * LocalFirst Tools — embed widget (#8)
 * Put any of 2885 tools on ANY website with one line:
 *   <script src="https://kody-w.github.io/localFirstTools/landgrab/embed.js"
 *           data-tool="apps/games/snake4.html" data-height="640"></script>
 * Renders a framed, branded, offline-capable tool that links back to the showcase.
 */
(function () {
  var SITE = 'https://kody-w.github.io/localFirstTools/';
  var s = document.currentScript;
  if (!s) return;
  var tool = s.getAttribute('data-tool') || '';
  var height = s.getAttribute('data-height') || '600';
  var title = s.getAttribute('data-title') || tool.split('/').pop().replace(/\.html$/, '').replace(/[-_]/g, ' ');
  var url = /^https?:/.test(tool) ? tool : SITE + tool.replace(/^\//, '');

  var wrap = document.createElement('div');
  wrap.style.cssText = 'max-width:100%;border:1px solid #2a2a3a;border-radius:12px;overflow:hidden;font-family:system-ui,sans-serif;box-shadow:0 8px 30px rgba(0,0,0,.25);background:#0e0e16';
  var bar = document.createElement('div');
  bar.style.cssText = 'display:flex;align-items:center;gap:8px;padding:7px 12px;background:#14141f;color:#cfe;font-size:13px;font-weight:600';
  bar.innerHTML = '<span style="color:#7ec87e">◆</span><span style="flex:1">' + title.replace(/</g, '&lt;') +
    '</span><a href="' + url + '" target="_blank" rel="noopener" style="color:#8fd0ff;text-decoration:none;font-size:12px">open ↗</a>';
  var frame = document.createElement('iframe');
  frame.src = url; frame.loading = 'lazy';
  frame.style.cssText = 'width:100%;height:' + height + 'px;border:0;display:block;background:#000';
  frame.setAttribute('title', title);
  var foot = document.createElement('div');
  foot.style.cssText = 'padding:5px 12px;background:#14141f;color:#667;font-size:11px;text-align:right';
  foot.innerHTML = 'powered by <a href="' + SITE + 'landgrab/hq.html" target="_blank" rel="noopener" style="color:#8fd0ff;text-decoration:none">LocalFirst Tools</a> · offline-first · no tracking';

  wrap.appendChild(bar); wrap.appendChild(frame); wrap.appendChild(foot);
  s.parentNode.insertBefore(wrap, s.nextSibling);

  // best-effort embed telemetry via the shared bus (local-first, no server)
  try { new BroadcastChannel('localfirst').postMessage({ __lf: 1, channel: 'embed', payload: { tool: tool, host: location.host }, ts: Date.now() }); } catch (e) {}
})();
