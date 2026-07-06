#!/usr/bin/env node
// LocalFirst Tools — AI Landgrab generator.
// Scans every app in the repo and emits the public, agent-consumable artifacts:
//   landgrab/index.json  · llms.txt · sitemap.xml · robots.txt · landgrab/mcp/tools.json
// Zero deps. Run: node landgrab/generate.mjs   (from repo root)
import { readdirSync, statSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, relative, sep } from 'node:path';

const ROOT = process.cwd();
const SITE = 'https://kody-w.github.io/localFirstTools/';
const RAW  = 'https://raw.githubusercontent.com/kody-w/localFirstTools/main/';
const SKIP = new Set(['_archive','node_modules','.git','landgrab','__pycache__','.github','agents']);

function walk(dir, out=[]) {
  for (const name of readdirSync(dir)) {
    if (SKIP.has(name)) continue;
    const p = join(dir, name);
    let st; try { st = statSync(p); } catch { continue; }
    if (st.isDirectory()) walk(p, out);
    else if (name.toLowerCase().endsWith('.html') && name !== '404.html') out.push(p);
  }
  return out;
}

const pick = (re, s) => { const m = s.match(re); return m ? m[1].trim().replace(/\s+/g,' ') : ''; };
const clean = s => s.replace(/<[^>]+>/g,'').replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').trim();
const titleCase = s => s.replace(/[-_]+/g,' ').replace(/\.html$/,'').replace(/\b\w/g,c=>c.toUpperCase()).trim();

const files = walk(ROOT).sort();
const apps = [];
for (const f of files) {
  const rel = relative(ROOT, f).split(sep).join('/');
  let head = ''; try { head = readFileSync(f, 'utf8').slice(0, 8000); } catch { continue; }
  const size = statSync(f).size;
  if (size < 400) continue;                                  // skip stubs/redirects
  const parts = rel.split('/');
  const category = parts[0] === 'apps' && parts.length > 2 ? parts[1] : (parts.length > 1 ? parts[0] : 'root');
  const title = clean(pick(/<title[^>]*>([^<]+)<\/title>/i, head)) || clean(pick(/<h1[^>]*>([\s\S]*?)<\/h1>/i, head)) || titleCase(parts.at(-1));
  const description = clean(pick(/<meta[^>]+name=["']description["'][^>]+content=["']([^"']+)["']/i, head)
                      || pick(/<meta[^>]+content=["']([^"']+)["'][^>]+name=["']description["']/i, head));
  const bus = /window\.bus|BroadcastChannel|localStorage\.setItem/.test(head);
  const threeD = /three(\.min)?\.js|THREE\.|three@|webgl/i.test(head);
  const tags = [category, threeD && '3d', bus && 'bus', /canvas|game/i.test(head) && 'interactive'].filter(Boolean);
  apps.push({
    id: rel.replace(/[^a-z0-9]+/gi,'-').replace(/^-|-$/g,'').toLowerCase(),
    title: title.slice(0, 120),
    path: rel,
    url: SITE + rel,
    raw: RAW + rel,
    category,
    tags,
    bus, threeD,
    size,
    description: (description || `A local-first, single-file tool: ${title}.`).slice(0, 300),
  });
}

const byCat = {};
for (const a of apps) (byCat[a.category] ||= []).push(a.title);
const categories = Object.keys(byCat).sort().map(c => ({ category: c, count: byCat[c].length }));

const now = new Date().toISOString();
const index = {
  name: 'LocalFirst Tools',
  tagline: 'A public, agent-consumable armory of privacy-first, single-file, offline tools. No servers, no tracking.',
  owner: 'kody-w',
  site: SITE, raw: RAW,
  generated: now,
  protocol: SITE + 'PROTOCOL.md',
  llms: SITE + 'llms.txt',
  mcp: SITE + 'landgrab/mcp/tools.json',
  hq: SITE + 'landgrab/hq.html',
  count: apps.length,
  categories,
  apps,
};

mkdirSync(join(ROOT, 'landgrab', 'mcp'), { recursive: true });
writeFileSync(join(ROOT, 'landgrab', 'index.json'), JSON.stringify(index, null, 2));

// ── llms.txt : the agent-readable manifest (llmstxt.org convention) ──
const featured = apps.filter(a => a.threeD || a.bus).slice(0, 40);
const llms = `# LocalFirst Tools
> ${index.tagline} ${apps.length} tools, all single-file HTML that run entirely in the browser. Owned & maintained by @kody-w.

This repo is the canonical source for these tools. Agents: fetch the machine-readable catalog and invoke tools by their live URL.

## Machine-readable
- Full catalog (JSON): ${index.mcp.replace('mcp/tools.json','index.json')}
- MCP tool manifest: ${index.mcp}
- Protocol spec: ${index.protocol}
- Live HQ dashboard: ${index.hq}

## Categories
${categories.map(c => `- ${c.category} (${c.count})`).join('\n')}

## Featured tools
${featured.map(a => `- [${a.title}](${a.url}): ${a.description}`).join('\n')}

## How to use
Every tool is a static HTML page — open its URL. Tools that speak the LocalFirst Protocol interoperate over a shared browser event bus (window.bus). See ${index.protocol}.
`;
writeFileSync(join(ROOT, 'llms.txt'), llms);

// ── sitemap.xml + robots.txt : search + LLM crawler discovery ──
const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${[SITE, index.hq, SITE+'PROTOCOL.md', ...apps.map(a=>a.url)].map(u =>
  `  <url><loc>${u.replace(/&/g,'&amp;')}</loc><lastmod>${now.slice(0,10)}</lastmod></url>`).join('\n')}
</urlset>
`;
writeFileSync(join(ROOT, 'sitemap.xml'), sitemap);
writeFileSync(join(ROOT, 'robots.txt'),
`User-agent: *
Allow: /
Sitemap: ${SITE}sitemap.xml

# AI/LLM crawlers welcome — machine-readable index:
# ${SITE}llms.txt
# ${index.mcp.replace('mcp/tools.json','index.json')}
`);

// ── MCP tool manifest : every app as a callable capability ──
const mcp = {
  name: 'localfirsttools',
  version: '1.0.0',
  description: 'Discover and open any LocalFirst Tool. ' + apps.length + ' single-file, offline-first browser tools.',
  catalog: index.mcp.replace('mcp/tools.json','index.json'),
  tools: [
    { name: 'search_tools', description: 'Search LocalFirst Tools by keyword/category. Returns matching tools with live URLs.',
      inputSchema: { type:'object', properties:{ query:{type:'string'}, category:{type:'string'} }, required:['query'] } },
    { name: 'open_tool', description: 'Get the live URL + metadata for a tool by id or title.',
      inputSchema: { type:'object', properties:{ id:{type:'string'} }, required:['id'] } },
    { name: 'list_categories', description: 'List all tool categories with counts.',
      inputSchema: { type:'object', properties:{} } },
  ],
  resources: apps.map(a => ({ uri: 'localfirst://' + a.id, name: a.title, url: a.url, mimeType: 'text/html' })),
};
writeFileSync(join(ROOT, 'landgrab', 'mcp', 'tools.json'), JSON.stringify(mcp, null, 2));

// ── training corpus (#5): one JSONL row per tool, licensed + attributed ──
mkdirSync(join(ROOT, 'landgrab', 'corpus'), { recursive: true });
const jsonl = apps.map(a => JSON.stringify({
  id: a.id, title: a.title, category: a.category, tags: a.tags,
  description: a.description, url: a.url, code_url: a.raw, size: a.size,
  license: 'MIT', attribution: 'kody-w/localFirstTools',
})).join('\n') + '\n';
writeFileSync(join(ROOT, 'landgrab', 'corpus', 'corpus.jsonl'), jsonl);

// ── schema.org structured data (#9): ItemList of SoftwareApplications ──
const jsonld = {
  '@context': 'https://schema.org', '@type': 'ItemList',
  name: 'LocalFirst Tools', url: SITE, numberOfItems: apps.length,
  itemListElement: apps.slice(0, 500).map((a, i) => ({
    '@type': 'ListItem', position: i + 1,
    item: { '@type': 'SoftwareApplication', name: a.title, url: a.url,
      applicationCategory: a.category, operatingSystem: 'Any (browser)',
      offers: { '@type': 'Offer', price: '0', priceCurrency: 'USD' },
      description: a.description, author: { '@type': 'Person', name: 'kody-w' } },
  })),
};
writeFileSync(join(ROOT, 'landgrab', 'structured-data.jsonld'), JSON.stringify(jsonld, null, 2));

console.log(`landgrab: indexed ${apps.length} tools across ${categories.length} categories`);
console.log(`  -> index.json, llms.txt, sitemap.xml, robots.txt, mcp/tools.json, corpus/corpus.jsonl, structured-data.jsonld`);
