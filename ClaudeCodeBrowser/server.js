#!/usr/bin/env node

/**
 * Agent Browser Web Server
 * Exposes Agent Browser functionality via HTTP API
 */

import express from 'express';
import cors from 'cors';
import { AgentBrowser } from './src/browser.js';
import agentFormatter from './src/agent-formatter.js';
import sessionManager from './src/session-manager.js';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.static(__dirname));

// Browser instance
let browser = null;
let browserState = {
  initialized: false,
  currentUrl: null,
  history: [],
  cookies: [],
  sessions: [],
  screenshots: [],
  networkLog: []
};

// Initialize browser
async function ensureBrowser() {
  if (!browser) {
    browser = new AgentBrowser({ headless: true });
    await browser.init();
    browserState.initialized = true;
  }
  return browser;
}

// Update state
async function updateState() {
  if (browser) {
    try {
      browserState.currentUrl = await browser.getCurrentUrl();
      browserState.history = browser.getHistory();
      browserState.cookies = await browser.getCookies();
      browserState.networkLog = browser.getNetworkLog();
      browserState.sessions = await sessionManager.list();
    } catch (error) {
      console.error('Error updating state:', error.message);
    }
  }
}

// API Routes

// Health check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    browserInitialized: browserState.initialized,
    currentUrl: browserState.currentUrl
  });
});

// Initialize browser
app.post('/api/init', async (req, res) => {
  try {
    await ensureBrowser();
    await updateState();
    res.json({ success: true, state: browserState });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Navigate
app.post('/api/goto', async (req, res) => {
  try {
    const { url, waitUntil } = req.body;
    const b = await ensureBrowser();
    const result = await b.goto(url, { waitUntil });
    await updateState();
    res.json({ success: true, result, state: browserState });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get current URL
app.get('/api/url', async (req, res) => {
  try {
    const b = await ensureBrowser();
    const url = await b.getCurrentUrl();
    res.json({ url });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get title
app.get('/api/title', async (req, res) => {
  try {
    const b = await ensureBrowser();
    const title = await b.getTitle();
    res.json({ title });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get content
app.get('/api/content', async (req, res) => {
  try {
    const b = await ensureBrowser();
    const content = await b.getContent();
    res.json({ content });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get structured content
app.get('/api/structured', async (req, res) => {
  try {
    const b = await ensureBrowser();
    const content = await b.getStructuredContent();
    res.json(content);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get markdown
app.get('/api/markdown', async (req, res) => {
  try {
    const b = await ensureBrowser();
    const html = await b.getHtml();
    const markdown = agentFormatter.htmlToMarkdown(html);
    res.json({ markdown });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get accessibility tree
app.get('/api/accessibility', async (req, res) => {
  try {
    const b = await ensureBrowser();
    const tree = await b.getAccessibilityTree();
    res.json({ tree });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Extract elements
app.post('/api/extract', async (req, res) => {
  try {
    const { selector, options } = req.body;
    const b = await ensureBrowser();
    const elements = await b.extract(selector, options);
    res.json({ elements });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Click element
app.post('/api/click', async (req, res) => {
  try {
    const { selector } = req.body;
    const b = await ensureBrowser();
    const result = await b.click(selector);
    await updateState();
    res.json({ success: true, result, state: browserState });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Type text
app.post('/api/type', async (req, res) => {
  try {
    const { selector, text, options } = req.body;
    const b = await ensureBrowser();
    const result = await b.type(selector, text, options);
    res.json({ success: true, result });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Fill form
app.post('/api/fill-form', async (req, res) => {
  try {
    const { fields } = req.body;
    const b = await ensureBrowser();
    const results = await b.fillForm(fields);
    res.json({ success: true, results });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Screenshot
app.post('/api/screenshot', async (req, res) => {
  try {
    const { filename, fullPage } = req.body;
    const b = await ensureBrowser();
    const result = await b.screenshot({ filename, fullPage });
    browserState.screenshots.push(result);
    res.json({ success: true, result });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Navigation controls
app.post('/api/back', async (req, res) => {
  try {
    const b = await ensureBrowser();
    await b.goBack();
    await updateState();
    res.json({ success: true, state: browserState });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/forward', async (req, res) => {
  try {
    const b = await ensureBrowser();
    await b.goForward();
    await updateState();
    res.json({ success: true, state: browserState });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/reload', async (req, res) => {
  try {
    const b = await ensureBrowser();
    await b.reload();
    await updateState();
    res.json({ success: true, state: browserState });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get state
app.get('/api/state', async (req, res) => {
  try {
    await updateState();
    res.json(browserState);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Export state
app.get('/api/export', async (req, res) => {
  try {
    await updateState();
    const exportData = {
      browserState,
      sessions: await sessionManager.list(),
      timestamp: new Date().toISOString(),
      version: '1.0.0'
    };
    res.json(exportData);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Import state
app.post('/api/import', async (req, res) => {
  try {
    const { data } = req.body;

    // Restore browser state
    if (data.browserState) {
      const b = await ensureBrowser();

      // Restore cookies
      if (data.browserState.cookies) {
        for (const cookie of data.browserState.cookies) {
          try {
            await b.setCookie(cookie);
          } catch (e) {
            console.error('Error setting cookie:', e.message);
          }
        }
      }

      // Navigate to last URL
      if (data.browserState.currentUrl) {
        await b.goto(data.browserState.currentUrl);
      }
    }

    await updateState();
    res.json({ success: true, state: browserState });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Session management
app.get('/api/sessions', async (req, res) => {
  try {
    const sessions = await sessionManager.list();
    res.json({ sessions });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/session/save', async (req, res) => {
  try {
    const { name } = req.body;
    const b = await ensureBrowser();
    const result = await sessionManager.createFromBrowser(name, b);
    await updateState();
    res.json({ success: true, session: result.session });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/session/load', async (req, res) => {
  try {
    const { name } = req.body;
    const session = await sessionManager.load(name);

    const b = await ensureBrowser();

    // Apply cookies
    if (session.cookies) {
      for (const cookie of session.cookies) {
        await b.setCookie(cookie);
      }
    }

    // Navigate to URL
    if (session.url) {
      await b.goto(session.url);
    }

    await updateState();
    res.json({ success: true, session, state: browserState });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Cleanup on exit
process.on('SIGINT', async () => {
  console.log('\nShutting down...');
  if (browser) {
    await browser.close();
  }
  process.exit(0);
});

// Start server
app.listen(PORT, () => {
  console.log(`🤖 Agent Browser Server running on http://localhost:${PORT}`);
  console.log(`📊 API available at http://localhost:${PORT}/api/*`);
  console.log(`🌐 Open http://localhost:${PORT}/index.html in your browser`);
});
