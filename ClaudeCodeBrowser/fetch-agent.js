#!/usr/bin/env node

/**
 * Fetch Agent - Downloads HTML and converts to JSON for the web interface
 * Bypasses CORS by fetching server-side and serving as JSON
 */

import https from 'https';
import http from 'http';
import { URL } from 'url';
import fs from 'fs/promises';
import path from 'path';

class FetchAgent {
    constructor() {
        this.userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36';
    }

    async fetchUrl(url) {
        console.log(`📥 Fetching: ${url}`);

        return new Promise((resolve, reject) => {
            const urlObj = new URL(url);
            const protocol = urlObj.protocol === 'https:' ? https : http;

            const options = {
                hostname: urlObj.hostname,
                port: urlObj.port,
                path: urlObj.pathname + urlObj.search,
                method: 'GET',
                headers: {
                    'User-Agent': this.userAgent,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                }
            };

            const req = protocol.request(options, (res) => {
                let data = '';

                res.on('data', (chunk) => {
                    data += chunk;
                });

                res.on('end', () => {
                    resolve({
                        statusCode: res.statusCode,
                        headers: res.headers,
                        body: data,
                        url: url
                    });
                });
            });

            req.on('error', (error) => {
                reject(error);
            });

            req.end();
        });
    }

    parseHtml(html, baseUrl) {
        console.log('🔍 Parsing HTML...');

        // Extract title
        const titleMatch = html.match(/<title[^>]*>(.*?)<\/title>/i);
        const title = titleMatch ? titleMatch[1].trim() : 'Untitled';

        // Extract meta tags
        const meta = {};
        const metaRegex = /<meta\s+([^>]*?)>/gi;
        let metaMatch;
        while ((metaMatch = metaRegex.exec(html)) !== null) {
            const attrs = metaMatch[1];
            const nameMatch = attrs.match(/(?:name|property)=["']([^"']+)["']/i);
            const contentMatch = attrs.match(/content=["']([^"']+)["']/i);
            if (nameMatch && contentMatch) {
                meta[nameMatch[1]] = contentMatch[1];
            }
        }

        // Extract headings
        const headings = [];
        const headingRegex = /<h([1-6])[^>]*>(.*?)<\/h\1>/gi;
        let headingMatch;
        while ((headingMatch = headingRegex.exec(html)) !== null) {
            headings.push({
                level: parseInt(headingMatch[1]),
                text: this.stripTags(headingMatch[2]).trim(),
                html: headingMatch[2]
            });
        }

        // Extract links
        const links = [];
        const linkRegex = /<a\s+([^>]*href=["']([^"']+)["'][^>]*)>(.*?)<\/a>/gi;
        let linkMatch;
        while ((linkMatch = linkRegex.exec(html)) !== null) {
            const href = linkMatch[2];
            const text = this.stripTags(linkMatch[3]).trim();
            const titleAttr = linkMatch[1].match(/title=["']([^"']+)["']/i);

            links.push({
                href: this.resolveUrl(href, baseUrl),
                text: text,
                title: titleAttr ? titleAttr[1] : null
            });
        }

        // Extract images
        const images = [];
        const imgRegex = /<img\s+([^>]*?)>/gi;
        let imgMatch;
        while ((imgMatch = imgRegex.exec(html)) !== null) {
            const attrs = imgMatch[1];
            const srcMatch = attrs.match(/src=["']([^"']+)["']/i);
            const altMatch = attrs.match(/alt=["']([^"']+)["']/i);
            const titleMatch = attrs.match(/title=["']([^"']+)["']/i);

            if (srcMatch) {
                images.push({
                    src: this.resolveUrl(srcMatch[1], baseUrl),
                    alt: altMatch ? altMatch[1] : null,
                    title: titleMatch ? titleMatch[1] : null
                });
            }
        }

        // Extract paragraphs
        const paragraphs = [];
        const pRegex = /<p[^>]*>(.*?)<\/p>/gi;
        let pMatch;
        while ((pMatch = pRegex.exec(html)) !== null) {
            const text = this.stripTags(pMatch[1]).trim();
            if (text.length > 0) {
                paragraphs.push(text);
            }
        }

        // Extract all text content
        const bodyMatch = html.match(/<body[^>]*>(.*?)<\/body>/is);
        let bodyText = '';
        if (bodyMatch) {
            bodyText = this.stripTags(bodyMatch[1])
                .replace(/\s+/g, ' ')
                .trim();
        }

        // Extract scripts (for interaction simulation)
        const scripts = [];
        const scriptRegex = /<script[^>]*>(.*?)<\/script>/gi;
        let scriptMatch;
        while ((scriptMatch = scriptRegex.exec(html)) !== null) {
            if (scriptMatch[1].trim()) {
                scripts.push(scriptMatch[1]);
            }
        }

        // Extract forms
        const forms = [];
        const formRegex = /<form([^>]*)>(.*?)<\/form>/gis;
        let formMatch;
        while ((formMatch = formRegex.exec(html)) !== null) {
            const formAttrs = formMatch[1];
            const formBody = formMatch[2];

            const actionMatch = formAttrs.match(/action=["']([^"']+)["']/i);
            const methodMatch = formAttrs.match(/method=["']([^"']+)["']/i);

            // Extract inputs
            const inputs = [];
            const inputRegex = /<(input|textarea|select)([^>]*)>/gi;
            let inputMatch;
            while ((inputMatch = inputRegex.exec(formBody)) !== null) {
                const inputAttrs = inputMatch[2];
                const typeMatch = inputAttrs.match(/type=["']([^"']+)["']/i);
                const nameMatch = inputAttrs.match(/name=["']([^"']+)["']/i);
                const idMatch = inputAttrs.match(/id=["']([^"']+)["']/i);
                const placeholderMatch = inputAttrs.match(/placeholder=["']([^"']+)["']/i);

                inputs.push({
                    type: typeMatch ? typeMatch[1] : 'text',
                    name: nameMatch ? nameMatch[1] : null,
                    id: idMatch ? idMatch[1] : null,
                    placeholder: placeholderMatch ? placeholderMatch[1] : null
                });
            }

            forms.push({
                action: actionMatch ? this.resolveUrl(actionMatch[1], baseUrl) : null,
                method: methodMatch ? methodMatch[1].toUpperCase() : 'GET',
                inputs: inputs
            });
        }

        return {
            title,
            meta,
            headings,
            links,
            images,
            paragraphs,
            bodyText,
            forms,
            rawHtml: html,
            hasScripts: scripts.length > 0
        };
    }

    stripTags(html) {
        return html.replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"');
    }

    resolveUrl(href, baseUrl) {
        try {
            if (href.startsWith('http://') || href.startsWith('https://')) {
                return href;
            }
            if (href.startsWith('//')) {
                const baseUrlObj = new URL(baseUrl);
                return baseUrlObj.protocol + href;
            }
            if (href.startsWith('/')) {
                const baseUrlObj = new URL(baseUrl);
                return `${baseUrlObj.protocol}//${baseUrlObj.host}${href}`;
            }
            return new URL(href, baseUrl).href;
        } catch (e) {
            return href;
        }
    }

    async fetchAndConvert(url, outputPath = null) {
        try {
            const response = await this.fetchUrl(url);

            if (response.statusCode !== 200) {
                throw new Error(`HTTP ${response.statusCode}: ${url}`);
            }

            const parsed = this.parseHtml(response.body, url);

            const pageData = {
                url: url,
                fetchedAt: new Date().toISOString(),
                statusCode: response.statusCode,
                headers: response.headers,
                content: parsed,
                version: '1.0.0'
            };

            if (outputPath) {
                await fs.writeFile(outputPath, JSON.stringify(pageData, null, 2));
                console.log(`✅ Saved to: ${outputPath}`);
            }

            return pageData;

        } catch (error) {
            console.error(`❌ Error: ${error.message}`);
            throw error;
        }
    }

    async fetchBatch(urls, outputDir = './pages') {
        console.log(`📦 Fetching ${urls.length} URLs...\n`);

        // Create output directory
        try {
            await fs.mkdir(outputDir, { recursive: true });
        } catch (e) {
            // Directory exists
        }

        const results = [];

        for (let i = 0; i < urls.length; i++) {
            const url = urls[i];
            console.log(`\n[${i + 1}/${urls.length}] ${url}`);

            try {
                const filename = this.urlToFilename(url);
                const outputPath = path.join(outputDir, filename);

                const data = await this.fetchAndConvert(url, outputPath);
                results.push({ url, success: true, path: outputPath });

                // Rate limiting
                if (i < urls.length - 1) {
                    await new Promise(resolve => setTimeout(resolve, 1000));
                }

            } catch (error) {
                console.error(`Failed: ${error.message}`);
                results.push({ url, success: false, error: error.message });
            }
        }

        console.log(`\n✅ Complete! ${results.filter(r => r.success).length}/${urls.length} successful`);
        return results;
    }

    urlToFilename(url) {
        const urlObj = new URL(url);
        let filename = urlObj.hostname.replace(/\./g, '_');
        if (urlObj.pathname !== '/') {
            filename += '_' + urlObj.pathname.replace(/\//g, '_').replace(/[^a-z0-9_]/gi, '');
        }
        filename += '_' + Date.now();
        return filename + '.json';
    }
}

// CLI Interface
if (import.meta.url === `file://${process.argv[1]}`) {
    const args = process.argv.slice(2);

    if (args.length === 0) {
        console.log(`
🤖 Fetch Agent - Download HTML and convert to JSON

Usage:
  node fetch-agent.js <url>                    # Fetch single URL
  node fetch-agent.js <url> <output.json>      # Fetch and save to file
  node fetch-agent.js --batch urls.txt         # Fetch multiple URLs from file
  node fetch-agent.js --serve                  # Start proxy server

Examples:
  node fetch-agent.js https://example.com
  node fetch-agent.js https://example.com page.json
  node fetch-agent.js --batch urls.txt
  node fetch-agent.js --serve
        `);
        process.exit(0);
    }

    const agent = new FetchAgent();

    if (args[0] === '--batch') {
        // Batch mode
        const urlsFile = args[1];
        if (!urlsFile) {
            console.error('Error: Please provide URLs file');
            process.exit(1);
        }

        const content = await fs.readFile(urlsFile, 'utf-8');
        const urls = content.split('\n').filter(line => line.trim() && !line.startsWith('#'));

        await agent.fetchBatch(urls);

    } else if (args[0] === '--serve') {
        // Server mode - import and start
        const { startProxyServer } = await import('./proxy-server.js');
        startProxyServer(agent);

    } else {
        // Single URL mode
        const url = args[0];
        const output = args[1] || null;

        const data = await agent.fetchAndConvert(url, output);

        if (!output) {
            console.log('\n📄 Page Data:');
            console.log(JSON.stringify(data, null, 2));
        }
    }
}

export default FetchAgent;
