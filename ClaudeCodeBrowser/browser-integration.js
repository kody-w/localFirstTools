/**
 * Browser Integration Script
 * Add this to index.html to enable proxy server integration
 *
 * INSERT THIS CODE INTO THE <script> SECTION OF index.html
 * BEFORE THE navigateToUrl() FUNCTION
 */

// ============================================
// PROXY SERVER INTEGRATION
// ============================================

// Configuration
const PROXY_CONFIG = {
    enabled: true, // Set to false to use iframe mode
    serverUrl: 'http://localhost:3000',
    useCache: true
};

// Current page data (loaded from JSON)
let currentPageData = null;

// Check if proxy server is available
async function checkProxyServer() {
    if (!PROXY_CONFIG.enabled) return false;

    try {
        const response = await fetch(`${PROXY_CONFIG.serverUrl}/api/health`, {
            method: 'GET',
            timeout: 2000
        });
        const data = await response.json();
        return data.status === 'ok';
    } catch (e) {
        return false;
    }
}

// Fetch page through proxy (bypasses CORS!)
async function fetchThroughProxy(url) {
    log(`Fetching through proxy: ${url}`, 'info');

    try {
        const response = await fetch(
            `${PROXY_CONFIG.serverUrl}/api/fetch?url=${encodeURIComponent(url)}`
        );

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const pageData = await response.json();
        return pageData;

    } catch (error) {
        throw new Error(`Proxy fetch failed: ${error.message}`);
    }
}

// Load page data (from proxy or JSON file)
async function loadPageData(url) {
    try {
        // Try proxy server first
        if (PROXY_CONFIG.enabled) {
            const isAvailable = await checkProxyServer();

            if (isAvailable) {
                const pageData = await fetchThroughProxy(url);
                return pageData;
            } else {
                log('Proxy server not available, using fallback mode', 'warning');
            }
        }

        // Fallback: try to load as iframe
        return null;

    } catch (error) {
        log(`Error loading page: ${error.message}`, 'error');
        throw error;
    }
}

// Render virtual page from JSON data
function renderVirtualPage(pageData) {
    currentPageData = pageData;

    const content = pageData.content;

    // Build HTML representation
    let html = `
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>${content.title}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2, h3 { color: #333; }
        a { color: #2563eb; }
        img { max-width: 100%; height: auto; }
        .meta { background: #f0f0f0; padding: 10px; margin-bottom: 20px; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="meta">
        <strong>Loaded from JSON:</strong> ${pageData.url}<br>
        <strong>Fetched:</strong> ${new Date(pageData.fetchedAt).toLocaleString()}<br>
        <strong>Title:</strong> ${content.title}
    </div>

    <h1>${content.title}</h1>
`;

    // Add paragraphs
    if (content.paragraphs && content.paragraphs.length > 0) {
        content.paragraphs.forEach(p => {
            html += `<p>${p}</p>\n`;
        });
    }

    // Add links section
    if (content.links && content.links.length > 0) {
        html += `<h2>Links (${content.links.length})</h2><ul>`;
        content.links.slice(0, 20).forEach(link => {
            html += `<li><a href="${link.href}">${link.text || link.href}</a></li>`;
        });
        if (content.links.length > 20) {
            html += `<li><em>... and ${content.links.length - 20} more links</em></li>`;
        }
        html += `</ul>`;
    }

    // Add images section
    if (content.images && content.images.length > 0) {
        html += `<h2>Images (${content.images.length})</h2>`;
        content.images.slice(0, 5).forEach(img => {
            html += `<img src="${img.src}" alt="${img.alt || ''}" style="max-width: 200px; margin: 10px;"><br>`;
        });
        if (content.images.length > 5) {
            html += `<p><em>... and ${content.images.length - 5} more images</em></p>`;
        }
    }

    html += `</body></html>`;

    // Load into iframe
    const iframe = document.getElementById('browserFrame');
    const doc = iframe.contentDocument || iframe.contentWindow.document;
    doc.open();
    doc.write(html);
    doc.close();

    log('Virtual page rendered from JSON data', 'success');
}

// Override navigateToUrl function to use proxy
const originalNavigateToUrl = window.navigateToUrl;
window.navigateToUrl = async function() {
    const url = document.getElementById('urlInput').value.trim();

    if (!url) {
        showAlert('Please enter a URL', 'warning');
        return;
    }

    // Validate URL
    let finalUrl = url;
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
        finalUrl = 'https://' + url;
    }

    try {
        new URL(finalUrl); // Validate

        appState.currentUrl = finalUrl;
        document.getElementById('currentUrl').textContent = finalUrl;

        // Show loading
        log(`Loading: ${finalUrl}`, 'info');
        const iframe = document.getElementById('browserFrame');
        iframe.srcdoc = '<div style="padding: 20px; text-align: center;">Loading...</div>';

        // Try to load through proxy
        const pageData = await loadPageData(finalUrl);

        if (pageData) {
            // Success! Render virtual page
            renderVirtualPage(pageData);

            // Add to history
            if (appState.settings.recordHistory) {
                appState.history.unshift({
                    url: finalUrl,
                    timestamp: new Date().toISOString(),
                    title: pageData.content.title
                });
                appState.statistics.pagesVisited++;
            }

            // Store page data for extraction
            appState.currentPageData = pageData;

            updateUI();
            saveStateToLocalStorage();

        } else {
            // Fallback to iframe
            log('Falling back to iframe mode', 'warning');
            iframe.src = finalUrl;

            if (appState.settings.recordHistory) {
                appState.history.unshift({
                    url: finalUrl,
                    timestamp: new Date().toISOString(),
                    title: 'Loading...'
                });
                appState.statistics.pagesVisited++;
            }

            iframe.onload = function() {
                try {
                    const title = iframe.contentDocument.title || finalUrl;
                    if (appState.history[0]) {
                        appState.history[0].title = title;
                    }
                    log(`Loaded via iframe: ${finalUrl}`, 'success');
                } catch (e) {
                    log(`Loaded: ${finalUrl} (cross-origin, limited access)`, 'warning');
                }
                updateUI();
                saveStateToLocalStorage();
            };
        }

    } catch (e) {
        showAlert('Invalid URL format', 'danger');
        log(`Invalid URL: ${url}`, 'error');
    }
};

// Override extraction functions to work with JSON data
const originalExtractContent = window.extractContent;
window.extractContent = function() {
    const type = document.getElementById('extractType').value;

    // If we have JSON page data, extract from that
    if (currentPageData && currentPageData.content) {
        const content = currentPageData.content;
        let extracted = null;

        switch(type) {
            case 'text':
                extracted = content.bodyText;
                break;

            case 'markdown':
                extracted = convertPageDataToMarkdown(content);
                break;

            case 'json':
                extracted = content;
                break;

            case 'links':
                extracted = content.links;
                break;

            case 'images':
                extracted = content.images;
                break;

            case 'headings':
                extracted = content.headings;
                break;
        }

        appState.extractedData = {
            type: type,
            content: extracted,
            url: currentPageData.url,
            timestamp: new Date().toISOString()
        };

        displayExtractedContent(extracted, type);
        appState.statistics.extractions++;
        saveStateToLocalStorage();
        log(`Extracted ${type} from JSON data`, 'success');

        return;
    }

    // Fallback to original iframe extraction
    if (originalExtractContent) {
        originalExtractContent();
    }
};

// Convert page data to markdown
function convertPageDataToMarkdown(content) {
    let md = `# ${content.title}\n\n`;

    if (content.meta && content.meta.description) {
        md += `> ${content.meta.description}\n\n`;
    }

    if (content.headings && content.headings.length > 0) {
        md += `## Headings\n\n`;
        content.headings.forEach(h => {
            md += `${'#'.repeat(h.level)} ${h.text}\n`;
        });
        md += '\n';
    }

    if (content.paragraphs && content.paragraphs.length > 0) {
        md += `## Content\n\n`;
        content.paragraphs.forEach(p => {
            md += `${p}\n\n`;
        });
    }

    if (content.links && content.links.length > 0) {
        md += `## Links\n\n`;
        content.links.slice(0, 50).forEach(link => {
            md += `- [${link.text || 'Link'}](${link.href})\n`;
        });
    }

    return md;
}

// Load saved page files from server
async function loadSavedFiles() {
    try {
        const response = await fetch(`${PROXY_CONFIG.serverUrl}/api/files`);
        const data = await response.json();

        if (data.files && data.files.length > 0) {
            const modal = document.getElementById('modal');
            const modalTitle = document.getElementById('modalTitle');
            const modalBody = document.getElementById('modalBody');

            modalTitle.textContent = 'Saved Page Files';

            let html = `<p>Found ${data.files.length} saved pages:</p><ul style="list-style: none; padding: 0;">`;

            data.files.forEach(file => {
                html += `
                    <li style="margin-bottom: 1rem; padding: 1rem; background: var(--gray-50); border-radius: 6px;">
                        <strong>${file.url}</strong><br>
                        <small>Fetched: ${new Date(file.fetchedAt).toLocaleString()}</small><br>
                        <small>Size: ${(file.size / 1024).toFixed(1)} KB</small><br>
                        <button class="btn btn-primary" style="margin-top: 0.5rem;" onclick="loadFileFromServer('${file.path}')">Load</button>
                    </li>
                `;
            });

            html += `</ul>`;
            modalBody.innerHTML = html;
            modal.classList.add('active');
        } else {
            showAlert('No saved files found. Fetch some pages first!', 'info');
        }

    } catch (error) {
        showAlert('Could not connect to proxy server', 'warning');
        log('Proxy server not available', 'error');
    }
}

// Load specific file from server
async function loadFileFromServer(filePath) {
    try {
        const response = await fetch(
            `${PROXY_CONFIG.serverUrl}/api/load-file?path=${encodeURIComponent(filePath)}`
        );
        const pageData = await response.json();

        renderVirtualPage(pageData);
        currentPageData = pageData;
        appState.currentUrl = pageData.url;
        document.getElementById('currentUrl').textContent = pageData.url;
        document.getElementById('urlInput').value = pageData.url;

        closeModal();
        log(`Loaded file: ${filePath}`, 'success');

    } catch (error) {
        showAlert('Error loading file: ' + error.message, 'danger');
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', async function() {
    // Check proxy server
    const available = await checkProxyServer();

    if (available) {
        log('✅ Proxy server connected - CORS bypass enabled!', 'success');
        document.getElementById('statusIndicator').classList.add('connected');
        document.getElementById('statusText').textContent = 'Proxy Connected';

        // Add "Load Files" button to sidebar
        const sidebar = document.querySelector('.sidebar');
        const divider = document.createElement('div');
        divider.style.cssText = 'margin-top: 1rem; padding-top: 1rem; border-top: 2px solid var(--gray-200);';
        divider.innerHTML = `
            <button class="btn btn-success" style="width: 100%; margin-bottom: 0.5rem;" onclick="loadSavedFiles()">📂 Load Saved Pages</button>
        `;
        sidebar.appendChild(divider);

    } else {
        log('⚠️ Proxy server not available - Limited to same-origin pages', 'warning');
        log('💡 Start proxy: node proxy-server.js', 'info');
        document.getElementById('statusIndicator').classList.add('disconnected');
        document.getElementById('statusText').textContent = 'Proxy Disconnected';
    }
});

console.log('🤖 Agent Browser - Proxy Integration Loaded');
console.log('📡 Proxy Server:', PROXY_CONFIG.enabled ? PROXY_CONFIG.serverUrl : 'Disabled');
