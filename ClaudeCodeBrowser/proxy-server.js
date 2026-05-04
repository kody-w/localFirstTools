#!/usr/bin/env node

/**
 * Proxy Server - Serves fetched page data to web interface
 * Bypasses CORS by fetching server-side and serving as JSON
 */

import express from 'express';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs/promises';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export function startProxyServer(fetchAgent) {
    const app = express();
    const PORT = process.env.PORT || 3000;

    // Middleware
    app.use(cors());
    app.use(express.json());
    app.use(express.static(__dirname));

    // Cache for fetched pages
    const pageCache = new Map();

    // Serve index.html
    app.get('/', (req, res) => {
        res.sendFile(path.join(__dirname, 'index.html'));
    });

    // Health check
    app.get('/api/health', (req, res) => {
        res.json({
            status: 'ok',
            service: 'Agent Browser Proxy',
            version: '1.0.0',
            cached: pageCache.size
        });
    });

    // Fetch and convert URL to JSON
    app.get('/api/fetch', async (req, res) => {
        try {
            const { url } = req.query;

            if (!url) {
                return res.status(400).json({ error: 'URL parameter required' });
            }

            console.log(`📥 Fetching: ${url}`);

            // Check cache
            if (pageCache.has(url)) {
                console.log(`💾 Serving from cache`);
                return res.json(pageCache.get(url));
            }

            // Fetch and convert
            const pageData = await fetchAgent.fetchAndConvert(url);

            // Cache it
            pageCache.set(url, pageData);

            // Set cache limit
            if (pageCache.size > 100) {
                const firstKey = pageCache.keys().next().value;
                pageCache.delete(firstKey);
            }

            res.json(pageData);

        } catch (error) {
            console.error(`❌ Error: ${error.message}`);
            res.status(500).json({
                error: error.message,
                stack: error.stack
            });
        }
    });

    // Batch fetch multiple URLs
    app.post('/api/fetch-batch', async (req, res) => {
        try {
            const { urls } = req.body;

            if (!Array.isArray(urls)) {
                return res.status(400).json({ error: 'URLs array required' });
            }

            console.log(`📦 Batch fetching ${urls.length} URLs`);

            const results = [];

            for (const url of urls) {
                try {
                    let pageData;

                    if (pageCache.has(url)) {
                        pageData = pageCache.get(url);
                    } else {
                        pageData = await fetchAgent.fetchAndConvert(url);
                        pageCache.set(url, pageData);
                    }

                    results.push({
                        url,
                        success: true,
                        data: pageData
                    });

                } catch (error) {
                    results.push({
                        url,
                        success: false,
                        error: error.message
                    });
                }

                // Rate limiting
                await new Promise(resolve => setTimeout(resolve, 500));
            }

            res.json({
                total: urls.length,
                successful: results.filter(r => r.success).length,
                results
            });

        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    });

    // Get cached page
    app.get('/api/cache/:url', (req, res) => {
        const url = decodeURIComponent(req.params.url);

        if (pageCache.has(url)) {
            res.json(pageCache.get(url));
        } else {
            res.status(404).json({ error: 'Page not in cache' });
        }
    });

    // List cached pages
    app.get('/api/cache', (req, res) => {
        const cached = Array.from(pageCache.keys()).map(url => ({
            url,
            fetchedAt: pageCache.get(url).fetchedAt
        }));

        res.json({
            count: cached.length,
            pages: cached
        });
    });

    // Clear cache
    app.delete('/api/cache', (req, res) => {
        const count = pageCache.size;
        pageCache.clear();
        res.json({
            message: 'Cache cleared',
            cleared: count
        });
    });

    // Load page from file
    app.get('/api/load-file', async (req, res) => {
        try {
            const { path: filePath } = req.query;

            if (!filePath) {
                return res.status(400).json({ error: 'Path parameter required' });
            }

            const content = await fs.readFile(filePath, 'utf-8');
            const pageData = JSON.parse(content);

            res.json(pageData);

        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    });

    // List available page files
    app.get('/api/files', async (req, res) => {
        try {
            const pagesDir = path.join(__dirname, 'pages');

            try {
                const files = await fs.readdir(pagesDir);
                const jsonFiles = files.filter(f => f.endsWith('.json'));

                const fileList = await Promise.all(
                    jsonFiles.map(async (file) => {
                        const filePath = path.join(pagesDir, file);
                        const stats = await fs.stat(filePath);
                        const content = await fs.readFile(filePath, 'utf-8');
                        const data = JSON.parse(content);

                        return {
                            filename: file,
                            path: filePath,
                            url: data.url,
                            fetchedAt: data.fetchedAt,
                            size: stats.size,
                            modified: stats.mtime
                        };
                    })
                );

                res.json({
                    directory: pagesDir,
                    count: fileList.length,
                    files: fileList
                });

            } catch (e) {
                res.json({
                    directory: pagesDir,
                    count: 0,
                    files: [],
                    note: 'Directory does not exist or is empty'
                });
            }

        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    });

    // CORS Proxy endpoint (for browser-based fetching)
    app.get('/api/proxy', async (req, res) => {
        try {
            const { url } = req.query;

            if (!url) {
                return res.status(400).json({ error: 'URL parameter required' });
            }

            const pageData = await fetchAgent.fetchAndConvert(url);

            // Return with CORS headers
            res.header('Access-Control-Allow-Origin', '*');
            res.header('Access-Control-Allow-Methods', 'GET');
            res.json(pageData);

        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    });

    // Start server
    app.listen(PORT, () => {
        console.log(`\n🚀 Agent Browser Proxy Server`);
        console.log(`📡 Running on http://localhost:${PORT}`);
        console.log(`🌐 Open http://localhost:${PORT} to use the interface`);
        console.log(`\nEndpoints:`);
        console.log(`  GET  /api/fetch?url=<url>           - Fetch and convert URL`);
        console.log(`  POST /api/fetch-batch               - Batch fetch URLs`);
        console.log(`  GET  /api/cache                     - List cached pages`);
        console.log(`  GET  /api/files                     - List saved page files`);
        console.log(`  GET  /api/proxy?url=<url>           - CORS proxy`);
        console.log(`\nExamples:`);
        console.log(`  http://localhost:${PORT}/api/fetch?url=https://example.com`);
        console.log(`  http://localhost:${PORT}/api/files`);
        console.log(``);
    });

    return app;
}

// CLI mode
if (import.meta.url === `file://${process.argv[1]}`) {
    const FetchAgent = (await import('./fetch-agent.js')).default;
    const agent = new FetchAgent();
    startProxyServer(agent);
}
