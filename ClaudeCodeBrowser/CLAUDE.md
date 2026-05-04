# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Agent Browser is a dual-purpose system:
1. **Agent Browser Core**: A headless browser library (via Puppeteer) designed specifically for AI agents, with structured output formats (JSON, Markdown) and simplified DOM access
2. **CORS-Bypass Web Fetcher**: A server-side HTML fetching system that bypasses CORS restrictions for web scraping and browsing

The codebase contains two mostly independent subsystems that share a directory but serve different purposes.

## Key Commands

### Agent Browser (Puppeteer-based)
```bash
# Install dependencies
npm install

# Start interactive REPL
node src/cli.js

# Navigate and extract content (single command)
node src/cli.js goto "https://example.com" --extract

# Get page content as markdown
node src/cli.js content "https://example.com" --format markdown

# Take screenshot
node src/cli.js screenshot "https://example.com" --output page.png

# Run example scripts
node examples/simple-navigation.js
node examples/form-filling.js
node examples/multi-page-research.js
node examples/agent-workflow.js "machine learning"
```

### CORS-Bypass System
```bash
# Start the proxy server (serves both API and web interface)
node proxy-server.js

# Fetch single URL (CLI)
node fetch-agent.js https://example.com

# Fetch and save to file
node fetch-agent.js https://example.com output.json

# Batch fetch from file
node fetch-agent.js --batch urls.txt

# Start alternative server (web interface server)
node server.js
```

### Self-Improving Chat (React + Vite)
```bash
cd self-improving-chat
npm install
npm run dev      # Development server
npm run build    # Production build
```

## Architecture

### Agent Browser Core (src/)
- **browser.js**: Core `AgentBrowser` class wrapping Puppeteer with agent-friendly API
- **agent-formatter.js**: Converts HTML to Markdown, JSON, YAML, and plain text formats
- **session-manager.js**: Saves/loads browser sessions including cookies and state
- **cli.js**: Command-line interface with interactive REPL and single-command modes
- **index.js**: Main export file for programmatic use

Key design: Single browser instance, async/await throughout, structured return values, timeout protection.

### CORS-Bypass System (root level)
- **fetch-agent.js**: Server-side HTML fetcher using native `fetch`, parses HTML with JSDOM
- **proxy-server.js**: Express server providing REST API + static file serving
  - API endpoint: `GET /api/fetch?url=<url>` - Returns structured JSON
  - Caches 100 pages in memory (LRU)
  - Serves index.html at root
- **index.html**: Complete browser UI with extraction tools, session management, proxy integration
- **browser-integration.js**: Standalone script demonstrating browser UI integration

Data flow: URL → fetch-agent.js (server-side) → JSON → proxy-server.js → index.html (browser)

### Supporting Files
- **server.js**: Alternative web server for dynamic documents
- **demo.js**: Demo script for dynamic document features
- **living-strategic-document.html**: Original inspiration/reference
- **dynamic-living-document.html**: Interactive document viewer
- **standalone-browser.html**: Standalone browser UI (no proxy)
- **iframe-demo.html**: Demonstration of iframe integration

### Examples Directory
Shows complete agent workflows:
- **simple-navigation.js**: Basic navigation and content extraction
- **form-filling.js**: Form automation patterns
- **multi-page-research.js**: Multi-page data gathering
- **agent-workflow.js**: Complete research agent implementation

## Core Design Patterns

### Agent-First Output
All browser operations return structured data optimized for programmatic consumption:
```javascript
const content = await browser.getStructuredContent();
// Returns: { title, url, content: { text, paragraphs }, metadata, structure: { headings, links, images } }
```

### Content Extraction Strategy
1. Remove clutter (scripts, styles, nav, footer)
2. Identify main content area (main, article, [role=main])
3. Extract structured data (headings, links, images)
4. Clean and normalize text
5. Return in agent-friendly format (JSON or Markdown)

### Markdown Conversion for LLMs
HTML → Remove scripts/styles → TurndownService → Clean markdown
This is the preferred format for feeding page content to LLMs.

### Session Persistence
Sessions store: current URL, cookies, navigation history, viewport settings, custom metadata.
Files saved to `./sessions/` directory (created on first use).

### CORS Bypass Architecture
The fetch-agent.js runs server-side (Node.js), so it bypasses all browser CORS restrictions. The proxy-server.js serves as a bridge, allowing the browser-based UI to access any website's content as JSON.

## Common Development Workflows

### Building an Agent with Puppeteer
1. Import `AgentBrowser` from `./src/browser.js`
2. Initialize: `await browser.init()`
3. Navigate: `await browser.goto(url)`
4. Extract: `await browser.getStructuredContent()` or `await browser.getHtml()` then convert to markdown
5. Interact: `await browser.click()`, `await browser.fillForm()`, etc.
6. Close: `await browser.close()` (always in finally block)

### Building a CORS-Bypass Scraper
1. Start proxy-server.js
2. Either:
   - Use web UI at http://localhost:3000
   - Make API calls to http://localhost:3000/api/fetch?url=...
   - Use fetch-agent.js CLI directly for batch operations
3. Process returned JSON data

### Extending Output Formats
Add custom formatters in agent-formatter.js by adding methods to the AgentFormatter class.

### Custom Page Extraction
Use `browser.evaluate()` to run custom JavaScript in page context for domain-specific data extraction.

## File Naming and Conventions

- Session files: `./sessions/*.json`
- Screenshot output: `./screenshots/*.png`
- PDF output: `./pdfs/*.pdf`
- Fetched pages: `./pages/*.json` (for CORS-bypass system)
- These directories are auto-created on first use

## Important Implementation Details

### Puppeteer Configuration
- Default headless mode for production
- Set `headless: false` for debugging/development
- Default timeout: 30 seconds (configurable per browser instance)
- Waits for `networkidle2` by default on navigation

### Fetch Agent Configuration
- User agent is customizable in fetch-agent.js
- Default: 'Mozilla/5.0 (compatible; AgentBot/1.0)'
- Rate limiting: Single-threaded, no built-in delays (add manually for politeness)
- Caching: In-memory LRU cache (100 entries) in proxy-server.js

### Performance Considerations
- Single Puppeteer browser: ~20-30 pages/minute
- Multiple parallel browsers scale linearly
- Headless mode is significantly faster than visual mode
- Extract only needed data using specific selectors for best performance
- Memory: ~100-200MB per browser instance
- CORS-bypass system: ~1-3 seconds per page fetch

### Security Model
- Puppeteer runs Chromium with sandboxing enabled
- No access to file system from browser context by default
- URL validation before navigation
- Timeout protection on all operations
- CORS-bypass system runs server-side on localhost (not exposed to internet by default)

## Integration Points

### LLM Integration Pattern
```javascript
const html = await browser.getHtml();
const markdown = agentFormatter.htmlToMarkdown(html);
// Feed markdown to LLM context window
```

### REST API Integration (CORS-Bypass)
```bash
curl "http://localhost:3000/api/fetch?url=https://example.com"
# Returns full structured JSON
```

### Programmatic Import
```javascript
import { AgentBrowser, AgentFormatter, SessionManager } from './src/index.js';
```

## Project-Specific Notes

- This is NOT a git repository (per inspection)
- The self-improving-chat subdirectory is a separate React+Vite application (appears to be a template, not customized)
- The "living strategic document" HTML files are reference/inspiration materials, not active code
- No test suite currently exists (package.json has placeholder test script)
- No cursor rules or copilot instructions defined
- The codebase uses ES modules (type: "module" in package.json)
- All core source files use .js extension but are ESM, not CommonJS
