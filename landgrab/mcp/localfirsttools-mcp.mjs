#!/usr/bin/env node
/**
 * LocalFirst Tools — MCP server (#2)
 * A dependency-free stdio MCP server that makes all 2885+ tools callable by ANY AI assistant.
 * Run:   node landgrab/mcp/localfirsttools-mcp.mjs
 * Tools: search_tools(query, category?)  ·  open_tool(id)  ·  list_categories()
 * Register it in your assistant's MCP config and it will discover & open LocalFirst Tools.
 */
import { createInterface } from 'node:readline';

const CATALOG_URL = 'https://kody-w.github.io/localFirstTools/landgrab/index.json';
let CATALOG = null;

async function catalog() {
  if (CATALOG) return CATALOG;
  try { CATALOG = await (await fetch(CATALOG_URL)).json(); }
  catch (e) {
    try { const { readFileSync } = await import('node:fs');
      const { fileURLToPath } = await import('node:url');
      const p = new URL('../index.json', import.meta.url);
      CATALOG = JSON.parse(readFileSync(fileURLToPath(p), 'utf8')); }
    catch (_) { CATALOG = { apps: [], categories: [] }; }
  }
  return CATALOG;
}

const send = (msg) => process.stdout.write(JSON.stringify(msg) + '\n');
const result = (id, r) => send({ jsonrpc: '2.0', id, result: r });
const error = (id, m) => send({ jsonrpc: '2.0', id, error: { code: -32603, message: m } });
const text = (t) => ({ content: [{ type: 'text', text: typeof t === 'string' ? t : JSON.stringify(t, null, 2) }] });

const TOOLS = [
  { name: 'search_tools', description: 'Search 2885+ LocalFirst Tools by keyword and/or category. Returns matching tools with live URLs.',
    inputSchema: { type: 'object', properties: { query: { type: 'string' }, category: { type: 'string' }, limit: { type: 'number' } }, required: ['query'] } },
  { name: 'open_tool', description: 'Get the live URL + metadata for a tool by id or exact title.',
    inputSchema: { type: 'object', properties: { id: { type: 'string' } }, required: ['id'] } },
  { name: 'list_categories', description: 'List all tool categories with counts.',
    inputSchema: { type: 'object', properties: {} } },
];

async function call(name, args) {
  const c = await catalog(); const apps = c.apps || [];
  if (name === 'list_categories') return text(c.categories || []);
  if (name === 'search_tools') {
    const q = (args.query || '').toLowerCase(), cat = (args.category || '').toLowerCase(), lim = args.limit || 15;
    const hits = apps.filter(a =>
      (!cat || a.category.toLowerCase() === cat) &&
      (a.title.toLowerCase().includes(q) || (a.description || '').toLowerCase().includes(q) || (a.tags || []).join(' ').includes(q))
    ).slice(0, lim).map(a => ({ id: a.id, title: a.title, url: a.url, category: a.category, description: a.description }));
    return text(hits.length ? hits : 'No tools matched "' + args.query + '".');
  }
  if (name === 'open_tool') {
    const id = (args.id || '').toLowerCase();
    const a = apps.find(x => x.id === id || x.title.toLowerCase() === id || x.path.toLowerCase() === id);
    return a ? text(a) : text('No tool with id "' + args.id + '".');
  }
  throw new Error('unknown tool ' + name);
}

createInterface({ input: process.stdin }).on('line', async (line) => {
  line = line.trim(); if (!line) return;
  let req; try { req = JSON.parse(line); } catch { return; }
  const { id, method, params } = req;
  try {
    if (method === 'initialize')
      return result(id, { protocolVersion: '2024-11-05', capabilities: { tools: {} },
        serverInfo: { name: 'localfirsttools', version: '1.0.0' } });
    if (method === 'tools/list') return result(id, { tools: TOOLS });
    if (method === 'tools/call') return result(id, await call(params.name, params.arguments || {}));
    if (method === 'ping') return result(id, {});
    if (id !== undefined) error(id, 'method not found: ' + method);
  } catch (e) { if (id !== undefined) error(id, String(e.message || e)); }
});

process.stderr.write('localfirsttools MCP server ready (stdio)\n');
