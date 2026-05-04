# Quick Start Guide

Get up and running with Agent Browser in 5 minutes.

## Installation

```bash
# Install dependencies
npm install

# Link CLI globally (optional)
npm link

# Or run directly
chmod +x src/cli.js
```

## 1. Your First Command

```bash
# Navigate to a page and extract content
node src/cli.js goto "https://example.com" --extract
```

Output:
```json
{
  "title": "Example Domain",
  "url": "https://example.com/",
  "content": {
    "text": "This domain is for use in illustrative examples...",
    "paragraphs": [...]
  },
  "structure": {
    "headings": [...],
    "links": [...],
    "images": [...]
  }
}
```

## 2. Interactive Mode

```bash
# Start interactive browser
node src/cli.js

# Or if linked:
agent-browser
```

Interactive commands:
```
agent-browser> goto "https://news.ycombinator.com"
agent-browser> links
agent-browser> markdown
agent-browser> screenshot hacker-news.png
agent-browser> exit
```

## 3. Programmatic Usage

Create a file `my-agent.js`:

```javascript
import { AgentBrowser } from './src/browser.js';

async function main() {
  const browser = new AgentBrowser({ headless: true });
  await browser.init();

  // Navigate and extract
  await browser.goto('https://example.com');
  const content = await browser.getStructuredContent();

  console.log('Page title:', content.title);
  console.log('Links found:', content.structure.links.length);

  await browser.close();
}

main().catch(console.error);
```

Run it:
```bash
node my-agent.js
```

## 4. Common Use Cases

### A. Web Research

```bash
# Get page as markdown (perfect for LLMs)
node src/cli.js content "https://en.wikipedia.org/wiki/AI" --format markdown > ai-info.md
```

### B. Extract Links

```bash
# Get all links from a page
node src/cli.js links "https://news.ycombinator.com" --format json > links.json
```

### C. Take Screenshots

```bash
# Capture a page
node src/cli.js screenshot "https://example.com" --output example.png
```

### D. Form Filling

```javascript
// In a script
await browser.goto('https://example.com/contact');

await browser.fillForm({
  'input[name="name"]': 'AI Agent',
  'input[name="email"]': 'agent@example.com',
  'textarea[name="message"]': 'Hello from Agent Browser!'
});

await browser.click('button[type="submit"]');
```

## 5. Running Examples

```bash
# Simple navigation
node examples/simple-navigation.js

# Form filling demo
node examples/form-filling.js

# Multi-page research
node examples/multi-page-research.js

# Complete agent workflow
node examples/agent-workflow.js "machine learning"
```

## 6. Agent Integration

### With Claude/ChatGPT

```javascript
// Extract content as markdown
const html = await browser.getHtml();
const markdown = agentFormatter.htmlToMarkdown(html);

// Send to LLM
const prompt = `
Summarize this web page:

${markdown}
`;

// Use with your LLM API
const response = await llm.complete(prompt);
```

### Structured Extraction

```javascript
// Get structured data
const content = await browser.getStructuredContent();

// Extract what you need
const summary = {
  title: content.title,
  mainPoints: content.structure.headings.map(h => h.text),
  sources: content.structure.links.slice(0, 5).map(l => l.href)
};

// Feed to your agent
await agent.process(summary);
```

## 7. Session Management

```bash
# Save a session
agent-browser> goto "https://example.com"
agent-browser> session-save my-work

# Load later
agent-browser> session-load my-work

# List sessions
agent-browser session-list
```

## 8. Tips

### For Faster Development

```javascript
// Use headless: false to see what's happening
const browser = new AgentBrowser({ headless: false });
```

### For Production

```javascript
// Use headless mode
const browser = new AgentBrowser({
  headless: true,
  timeout: 60000  // Longer timeout for slow sites
});
```

### For Debugging

```javascript
// Check network activity
const network = browser.getNetworkLog();
console.log('Requests:', network.filter(e => e.type === 'request').length);

// Take screenshot at each step
await browser.screenshot({ filename: 'step-1.png' });
```

## 9. Common Patterns

### Pattern: Research Multiple Topics

```javascript
const topics = ['AI', 'Machine Learning', 'Neural Networks'];

for (const topic of topics) {
  await browser.goto(`https://en.wikipedia.org/wiki/${topic}`);
  const content = await browser.getStructuredContent();

  // Save or process content
  console.log(`${topic}: ${content.content.text.substring(0, 200)}...`);
}
```

### Pattern: Monitor for Changes

```javascript
async function checkForChanges(url, selector) {
  await browser.goto(url);
  const current = await browser.extract(selector);

  // Compare with previous
  if (JSON.stringify(current) !== JSON.stringify(previous)) {
    console.log('Content changed!');
    // Send notification
  }
}
```

### Pattern: Batch Screenshots

```javascript
const urls = ['https://site1.com', 'https://site2.com'];

for (const url of urls) {
  await browser.goto(url);
  const filename = url.replace(/[^a-z0-9]/gi, '_') + '.png';
  await browser.screenshot({ filename });
}
```

## 10. Next Steps

- Read [AGENT_GUIDE.md](docs/AGENT_GUIDE.md) for advanced patterns
- Check [API.md](docs/API.md) for complete API reference
- Explore `examples/` directory for more use cases
- Build your own agents!

## Troubleshooting

### Browser won't start
```bash
# Install Chromium dependencies
# On Ubuntu/Debian:
sudo apt-get install -y libgbm1 libnss3 libxss1 libasound2

# On Mac:
# Should work out of the box
```

### Timeout errors
```javascript
// Increase timeout
const browser = new AgentBrowser({
  timeout: 120000  // 2 minutes
});

// Or per-command
await browser.goto(url, { timeout: 60000 });
```

### Memory issues
```javascript
// Close browser when done
await browser.close();

// Don't keep too many pages in history
// Create new browser instance for long-running tasks
```

## Help & Support

- Check documentation in `docs/`
- Review examples in `examples/`
- Open an issue on GitHub
- Read Puppeteer documentation for advanced features

---

🎉 **You're ready to build AI agents with Agent Browser!**
