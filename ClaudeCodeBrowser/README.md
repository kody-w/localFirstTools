# 🤖 Agent Browser - Complete End-to-End System

A fully functional browser interface designed for AI agents with **complete CORS bypass** capabilities. This system allows you to browse, extract, and interact with any website without cross-origin restrictions.

## 🌟 What Makes This Special

This is a complete, production-ready browser system that solves the #1 problem with web scraping and automation: **CORS restrictions**.

### How It Works

```
┌──────────────┐
│   Any URL    │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│  Fetch Agent         │  ← Server-side (No CORS!)
│  (Node.js)           │
└──────┬───────────────┘
       │
       │ Downloads HTML
       │ Parses content
       │ Converts to JSON
       │
       ▼
┌──────────────────────┐
│  Proxy Server        │  ← HTTP API Server
│  (Express)           │
└──────┬───────────────┘
       │
       │ Serves JSON
       │ Caches pages
       │
       ▼
┌──────────────────────┐
│  Web Interface       │  ← Browser UI
│  (index.html)        │
└──────┬───────────────┘
       │
       │ Renders pages
       │ Extracts data
       │ Full interaction
       │
       ▼
┌──────────────────────┐
│  Virtual Page        │  ← No CORS Issues!
└──────────────────────┘
```

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
npm install
```

### Step 2: Start the Proxy Server

```bash
node proxy-server.js
```

**Output:**
```
🚀 Agent Browser Proxy Server
📡 Running on http://localhost:3000
🌐 Open http://localhost:3000 to use the interface
```

### Step 3: Open Your Browser

Navigate to: **http://localhost:3000**

**That's it!** You can now browse any website without CORS restrictions.

## 📋 System Components

### 1. **fetch-agent.js** - Server-Side HTML Fetcher
- Downloads HTML from any URL (bypasses CORS server-side)
- Parses HTML into structured JSON
- Extracts: titles, headings, links, images, paragraphs, forms, metadata
- Batch processing support
- File persistence

**CLI Usage:**
```bash
# Fetch single URL
node fetch-agent.js https://example.com

# Save to file
node fetch-agent.js https://example.com output.json

# Batch fetch from file
node fetch-agent.js --batch urls.txt
```

### 2. **proxy-server.js** - API Server
- Express HTTP server on port 3000
- RESTful API endpoints
- In-memory caching (100 pages)
- Serves static files (index.html)
- CORS enabled

**API Endpoints:**
- `GET /api/fetch?url=<url>` - Fetch and convert URL
- `POST /api/fetch-batch` - Batch fetch multiple URLs
- `GET /api/cache` - List cached pages
- `GET /api/files` - List saved JSON files
- `GET /api/health` - Health check

### 3. **index.html** - Complete Web Interface
- Full browser UI with proxy integration
- Content extraction (Text, Markdown, JSON, Links, Images)
- Page interaction (Click, Type, Fill forms)
- Session management
- Import/Export capabilities
- localStorage persistence
- Automatic proxy detection

## 🎯 Features

### ✅ Complete CORS Bypass
- Fetch agent runs server-side (no browser restrictions)
- Works with **any** website
- Full page data access
- No iframe limitations

### ✅ Rich Data Extraction
- **Plain Text** - Clean text content
- **Markdown** - Formatted for LLMs
- **Structured JSON** - Full page metadata
- **Links** - All hyperlinks with context
- **Images** - All images with metadata
- **Headings** - Document structure
- **Forms** - Form fields and structure

### ✅ Persistent Storage
- Save pages as JSON files
- Load pages offline
- Build datasets
- Version control friendly

### ✅ Session Management
- Save browsing sessions
- Restore complete state
- Export/Import data
- History tracking

### ✅ Fast & Efficient
- In-memory caching
- No re-fetching
- Batch processing
- Rate limiting built-in

## 📖 Usage Examples

### Example 1: Browse a Website

1. Start the proxy server: `node proxy-server.js`
2. Open http://localhost:3000
3. Enter URL: `https://example.com`
4. Click "Go"
5. Page loads without CORS issues!

### Example 2: Extract Data

1. Navigate to a page
2. Go to "Extract Content" section
3. Choose extraction type (e.g., "Markdown")
4. Click "Extract"
5. View, copy, or download the extracted data

### Example 3: Batch Fetch Pages

Create `urls.txt`:
```
https://en.wikipedia.org/wiki/Artificial_intelligence
https://en.wikipedia.org/wiki/Machine_learning
https://en.wikipedia.org/wiki/Deep_learning
```

Run:
```bash
node fetch-agent.js --batch urls.txt
```

All pages saved to `./pages/` directory as JSON files.

### Example 4: Load Saved Pages

1. In the web interface, click "📂 Load Saved Pages"
2. Browse all previously fetched pages
3. Click "Load" to view offline
4. Extract data as needed

### Example 5: Build a Dataset

```bash
# Create URL list
cat > dataset-urls.txt << EOF
https://example.com/page1
https://example.com/page2
https://example.com/page3
EOF

# Fetch all pages
node fetch-agent.js --batch dataset-urls.txt

# Now you have a dataset of JSON files in ./pages/
```

## 🔧 Configuration

### Change Server Port

```bash
PORT=8080 node proxy-server.js
```

Then update `index.html`:
```javascript
const PROXY_CONFIG = {
    enabled: true,
    serverUrl: 'http://localhost:8080',  // Changed port
    useCache: true
};
```

### Custom User Agent

Edit `fetch-agent.js`:
```javascript
this.userAgent = 'MyCustomBot/1.0';
```

### Disable Proxy (Standalone Mode)

In `index.html`, set:
```javascript
const PROXY_CONFIG = {
    enabled: false,  // Disable proxy
    serverUrl: 'http://localhost:3000',
    useCache: true
};
```

## 📊 JSON Page Format

Pages are stored/transmitted as structured JSON:

```json
{
  "url": "https://example.com",
  "fetchedAt": "2024-01-15T10:30:00.000Z",
  "statusCode": 200,
  "headers": { ... },
  "content": {
    "title": "Example Domain",
    "meta": {
      "description": "Example description",
      "keywords": "example, domain"
    },
    "headings": [
      { "level": 1, "text": "Example Domain" }
    ],
    "links": [
      { "href": "https://...", "text": "More info" }
    ],
    "images": [
      { "src": "https://...", "alt": "Image" }
    ],
    "paragraphs": ["First paragraph", "Second paragraph"],
    "bodyText": "Full page text...",
    "forms": [
      {
        "action": "/submit",
        "method": "POST",
        "inputs": [...]
      }
    ],
    "rawHtml": "<html>...</html>",
    "hasScripts": true
  },
  "version": "1.0.0"
}
```

## 🛠️ Advanced Usage

### API Usage (cURL)

```bash
# Fetch a URL
curl "http://localhost:3000/api/fetch?url=https://example.com"

# List cached pages
curl "http://localhost:3000/api/cache"

# List saved files
curl "http://localhost:3000/api/files"

# Batch fetch
curl -X POST http://localhost:3000/api/fetch-batch \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.com", "https://github.com"]}'
```

### Programmatic Usage

```javascript
// Using fetch in your code
const response = await fetch('http://localhost:3000/api/fetch?url=https://example.com');
const pageData = await response.json();

console.log('Title:', pageData.content.title);
console.log('Paragraphs:', pageData.content.paragraphs);
console.log('Links:', pageData.content.links.length);
```

### Integration with Other Tools

```bash
# Extract specific data with jq
curl -s "http://localhost:3000/api/fetch?url=https://example.com" | \
  jq '.content.links[] | .href'

# Save to file
curl "http://localhost:3000/api/fetch?url=https://example.com" > page.json

# Process with Node.js
node -e "
const data = require('./page.json');
console.log('Found', data.content.links.length, 'links');
"
```

## 🔐 Security & Privacy

- All fetching happens server-side on your machine
- No external services or APIs
- All data stays local
- No cookies sent by default
- Respects standard HTTP headers
- User agent is customizable

## 📁 File Structure

```
ClaudeCodeBrowser/
├── index.html              # Complete web interface (with proxy integration)
├── fetch-agent.js          # Server-side HTML fetcher
├── proxy-server.js         # Express API server
├── package.json            # Dependencies
├── pages/                  # Saved JSON pages (auto-created)
│   ├── example_com_123.json
│   └── github_com_456.json
├── README.md               # This file
├── COMPLETE_SETUP.md       # Detailed setup guide
└── WEB_INTERFACE_README.md # Web interface docs
```

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or use different port
PORT=8080 node proxy-server.js
```

### Proxy Not Connecting

1. Check proxy server is running
2. Check console for errors
3. Verify port configuration
4. Check firewall settings

### Can't Fetch HTTPS Sites

- The fetch agent handles HTTPS automatically
- No additional configuration needed
- SSL certificates are validated

### Rate Limiting Issues

Add delays in batch mode or reduce concurrent requests.

## 📊 Performance

- **Fetch Speed**: ~1-3 seconds per page
- **JSON Size**: ~10-50KB per page (vs 100-500KB HTML)
- **Cache**: 100 pages in memory
- **Batch**: Can process 1000s of pages
- **Concurrent**: Single-threaded with rate limiting

## 🎓 Complete Workflows

### Research Workflow
1. Batch fetch research URLs
2. Load pages in web interface
3. Extract as Markdown
4. Feed to LLM/notes
5. Save session for later

### Data Collection Workflow
1. Fetch target pages
2. Extract as JSON
3. Process with scripts
4. Build datasets
5. Version control JSON files

### Monitoring Workflow
1. Periodically fetch pages
2. Compare changes
3. Track updates
4. Alert on changes

## 💡 Pro Tips

1. **Batch Process**: Fetch everything upfront, process offline
2. **Version Control**: JSON files work great with Git
3. **Cache Everything**: Let the proxy cache frequently accessed pages
4. **Export Regularly**: Create backups of important sessions
5. **Use Markdown**: Best format for LLM context windows

## 🚀 Next Steps

1. ✅ Start the proxy server
2. ✅ Open the web interface
3. ✅ Fetch your first page
4. ✅ Extract some data
5. ✅ Save a session
6. ✅ Build a dataset

## 📝 License

MIT License - Free to use, modify, and distribute.

## 🤝 Support

Questions? Issues?
- Check the console output for debugging info
- Review COMPLETE_SETUP.md for detailed setup
- Review WEB_INTERFACE_README.md for UI docs

---

**Built for AI agents. Built to work.** 🤖✨
