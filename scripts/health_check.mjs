#!/usr/bin/env node
/**
 * Headless health check for every featured app.
 *
 * - Reads vibe_gallery_config.json
 * - Spins up a local static server
 * - For each featured app: opens in puppeteer, captures pageerror /
 *   console.error / 4xx responses / load timeouts
 * - Writes data/reports/health-check-latest.json
 * - Exits 1 if any new failures vs the last report (configurable)
 *
 * Designed to run in CI (GitHub Actions) and locally.
 *
 * Usage:
 *   node scripts/health_check.mjs                      # full run
 *   node scripts/health_check.mjs --limit 50           # quick run
 *   node scripts/health_check.mjs --concurrency 4      # parallel
 *   node scripts/health_check.mjs --all                # every registry app, not just featured
 *   node scripts/health_check.mjs --no-server          # don't start own server (use existing on :PORT)
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';
import puppeteer from 'puppeteer';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

// ---------- args ----------
const args = process.argv.slice(2);
const argv = {};
for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
        const key = args[i].slice(2);
        const next = args[i + 1];
        if (next && !next.startsWith('--')) {
            argv[key] = next; i++;
        } else {
            argv[key] = true;
        }
    }
}
const LIMIT = argv.limit ? parseInt(argv.limit, 10) : null;
const CONCURRENCY = argv.concurrency ? parseInt(argv.concurrency, 10) : 4;
const ALL = !!argv.all;
const PORT = argv.port ? parseInt(argv.port, 10) : 8765;
const NO_SERVER = !!argv['no-server'];
const TIMEOUT_MS = argv.timeout ? parseInt(argv.timeout, 10) * 1000 : 12000;
const SETTLE_MS = argv.settle ? parseInt(argv.settle, 10) : 1500;

// ---------- start static server (unless told not to) ----------
let serverProc = null;
async function startServer() {
    if (NO_SERVER) return;
    serverProc = spawn('python3', ['-m', 'http.server', String(PORT)], {
        cwd: ROOT,
        stdio: ['ignore', 'ignore', 'ignore'],
        detached: false,
    });
    // Wait for it to bind
    await new Promise(r => setTimeout(r, 1500));
}
function stopServer() {
    if (serverProc) {
        try { serverProc.kill('SIGTERM'); } catch (_) {}
    }
}

// ---------- load registry ----------
function loadApps() {
    const cfgPath = path.join(ROOT, 'vibe_gallery_config.json');
    if (!fs.existsSync(cfgPath)) {
        throw new Error('vibe_gallery_config.json not found');
    }
    const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf-8'));
    const apps = [];
    for (const [k, c] of Object.entries(cfg.vibeGallery?.categories ?? {})) {
        for (const app of (c.apps || [])) {
            if (!app.path) continue;
            if (!ALL && !app.featured) continue;
            apps.push({
                title: app.title || app.filename || app.path,
                path: app.path.replace(/^\.?\//, ''),
                category: app.category || k,
                featured: !!app.featured,
            });
        }
    }
    return apps;
}

// ---------- run one app ----------
async function checkApp(browser, app, baseUrl) {
    const errors = [];
    const warnings = [];
    let httpStatus = 200;
    const start = Date.now();
    const page = await browser.newPage();
    page.on('pageerror', e => errors.push({ kind: 'pageerror', msg: e.message }));
    page.on('console', msg => {
        if (msg.type() === 'error') errors.push({ kind: 'console.error', msg: msg.text().substring(0, 300) });
        else if (msg.type() === 'warning') warnings.push({ kind: 'console.warning', msg: msg.text().substring(0, 200) });
    });
    page.on('response', r => {
        if (r.status() >= 400) {
            // Don't count cross-origin API failures (CORS-affected, or third-party APIs)
            const url = r.url();
            const isOwnOrigin = url.startsWith(baseUrl);
            if (isOwnOrigin) {
                errors.push({ kind: `http_${r.status()}`, msg: url.replace(baseUrl, '') });
            }
        }
    });

    let timeoutMs = 0;
    try {
        await page.goto(baseUrl + app.path, { waitUntil: 'networkidle2', timeout: TIMEOUT_MS });
        await new Promise(r => setTimeout(r, SETTLE_MS));
    } catch (e) {
        if (e.message.includes('timeout')) {
            errors.push({ kind: 'load_timeout', msg: `${TIMEOUT_MS}ms` });
            timeoutMs = TIMEOUT_MS;
        } else {
            errors.push({ kind: 'navigation', msg: e.message });
        }
    }
    const elapsed = Date.now() - start;
    await page.close();

    const verdict = errors.length === 0 ? 'pass' : 'fail';
    return {
        path: app.path,
        title: app.title,
        category: app.category,
        featured: app.featured,
        verdict,
        ms: elapsed,
        errors,
        warnings: warnings.slice(0, 3), // cap to avoid bloat
        timestamp: new Date().toISOString(),
    };
}

// ---------- main ----------
async function main() {
    const apps = loadApps();
    if (LIMIT) apps.length = Math.min(apps.length, LIMIT);
    console.log(`health-check: targeting ${apps.length} apps (${ALL ? 'all' : 'featured'}); concurrency=${CONCURRENCY}`);

    if (!NO_SERVER) {
        console.log(`starting static server on port ${PORT}…`);
        await startServer();
    }
    const baseUrl = `http://localhost:${PORT}/`;
    const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox', '--disable-dev-shm-usage'] });

    const results = [];
    let nextIdx = 0;
    let completed = 0;
    const total = apps.length;
    const workers = Array.from({ length: CONCURRENCY }, async () => {
        while (true) {
            const i = nextIdx++;
            if (i >= apps.length) return;
            const r = await checkApp(browser, apps[i], baseUrl);
            results.push(r);
            completed++;
            const sym = r.verdict === 'pass' ? '✓' : '✗';
            const errSummary = r.errors.length ? ` [${r.errors[0].kind}]` : '';
            console.log(`  ${completed}/${total}  ${sym}  ${r.ms.toString().padStart(5)}ms  ${r.path}${errSummary}`);
        }
    });
    await Promise.all(workers);
    await browser.close();
    stopServer();

    // Sort results by category then title for stable output
    results.sort((a, b) => (a.category + a.title).localeCompare(b.category + b.title));

    const summary = {
        total: results.length,
        pass: results.filter(r => r.verdict === 'pass').length,
        fail: results.filter(r => r.verdict === 'fail').length,
        avgMs: Math.round(results.reduce((s, r) => s + r.ms, 0) / Math.max(1, results.length)),
        slowestN: results.slice().sort((a, b) => b.ms - a.ms).slice(0, 10).map(r => ({ path: r.path, ms: r.ms })),
    };

    const report = {
        format: 'localFirstTools-health-v1',
        generatedAt: new Date().toISOString(),
        scope: ALL ? 'all-registered' : 'featured',
        timeoutMs: TIMEOUT_MS,
        settleMs: SETTLE_MS,
        summary,
        results,
    };

    // Write report
    const outDir = path.join(ROOT, 'data', 'reports');
    fs.mkdirSync(outDir, { recursive: true });
    const outPath = path.join(outDir, 'health-check-latest.json');
    fs.writeFileSync(outPath, JSON.stringify(report, null, 2));

    // Also write a tiny markdown summary so users can scan it
    const mdLines = [
        '# Health Check Report',
        '',
        `_Generated: ${report.generatedAt}_`,
        '',
        `- **Total**: ${summary.total}`,
        `- **Pass**: ${summary.pass} (${((summary.pass / summary.total) * 100).toFixed(1)}%)`,
        `- **Fail**: ${summary.fail}`,
        `- **Avg load time**: ${summary.avgMs}ms`,
        '',
        '## Failing apps',
        '',
    ];
    const fails = results.filter(r => r.verdict === 'fail');
    if (fails.length === 0) {
        mdLines.push('_None — all featured apps load cleanly._ 🎉');
    } else {
        mdLines.push('| App | Errors |');
        mdLines.push('|---|---|');
        for (const r of fails.slice(0, 100)) {
            const errs = r.errors.slice(0, 2).map(e => `\`${e.kind}\` ${e.msg.substring(0, 80)}`).join('<br>');
            mdLines.push(`| [\`${r.path}\`](https://kody-w.github.io/localFirstTools/${r.path}) | ${errs} |`);
        }
    }
    mdLines.push('');
    mdLines.push('## 10 slowest loads');
    mdLines.push('');
    mdLines.push('| App | ms |');
    mdLines.push('|---|---|');
    for (const s of summary.slowestN) {
        mdLines.push(`| \`${s.path}\` | ${s.ms} |`);
    }
    fs.writeFileSync(path.join(outDir, 'health-check-latest.md'), mdLines.join('\n') + '\n');

    console.log('');
    console.log('=== SUMMARY ===');
    console.log(`  total: ${summary.total}`);
    console.log(`  pass:  ${summary.pass} (${((summary.pass / summary.total) * 100).toFixed(1)}%)`);
    console.log(`  fail:  ${summary.fail}`);
    console.log(`  avg:   ${summary.avgMs}ms`);
    console.log(`  → ${path.relative(ROOT, outPath)}`);

    // Exit code: 0 if all pass, 1 if any fail
    process.exit(summary.fail > 0 ? 1 : 0);
}

main().catch(e => {
    console.error('FATAL:', e);
    stopServer();
    process.exit(2);
});
