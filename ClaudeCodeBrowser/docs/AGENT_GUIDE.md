# Agent Developer Guide

## Building AI Agents with Agent Browser

This guide shows you how to build effective web-browsing AI agents using Agent Browser.

## Core Concepts

### 1. Agent-First Design

Agent Browser is designed for programmatic control:
- **Structured Outputs**: All data returned in JSON, making it easy to parse and use
- **Markdown Conversion**: Perfect for feeding into LLM context windows
- **Simplified DOM**: Accessibility tree provides clean element structure
- **Stateless Operations**: Each command is independent and composable

### 2. Content Extraction

Extract content optimized for agent consumption:

```javascript
import { AgentBrowser } from './src/browser.js';

const browser = new AgentBrowser({ headless: true });
await browser.init();

// Navigate to page
await browser.goto('https://example.com');

// Get structured content
const content = await browser.getStructuredContent();
// Returns: { title, url, content, metadata, structure }

// Get as clean text
const text = await browser.getContent();

// Get as markdown (best for LLMs)
const html = await browser.getHtml();
const markdown = agentFormatter.htmlToMarkdown(html);
```

### 3. Element Interaction

Interact with page elements programmatically:

```javascript
// Click elements
await browser.click('button.submit');

// Fill forms
await browser.fillForm({
  'input[name="email"]': 'agent@example.com',
  'input[name="password"]': 'secure-pass',
  'select[name="country"]': 'US'
});

// Type text
await browser.type('#search', 'query text', { clear: true });

// Extract specific elements
const products = await browser.extract('.product-card', {
  includeAttributes: true,
  includeStyles: false
});
```

### 4. Accessibility Tree

Use the accessibility tree for intelligent element selection:

```javascript
const a11y = await browser.getAccessibilityTree();

// Tree structure shows:
// - role (button, link, textbox, etc.)
// - name (visible label)
// - value (current value)
// - children (nested elements)

// Perfect for agents to understand page structure
// and decide which elements to interact with
```

## Agent Patterns

### Pattern 1: Research Agent

Gather information from multiple sources:

```javascript
async function researchAgent(topic) {
  const browser = new AgentBrowser({ headless: true });
  await browser.init();

  const findings = [];

  // Search
  await browser.goto(`https://duckduckgo.com?q=${encodeURIComponent(topic)}`);
  const results = await browser.getStructuredContent();

  // Visit top results
  const topLinks = results.structure.links.slice(0, 5);
  for (const link of topLinks) {
    await browser.goto(link.href);
    const content = await browser.getStructuredContent();

    findings.push({
      url: content.url,
      title: content.title,
      summary: content.content.text.substring(0, 500)
    });
  }

  await browser.close();
  return findings;
}
```

### Pattern 2: Form Automation Agent

Fill out forms automatically:

```javascript
async function formAgent(formData) {
  const browser = new AgentBrowser({ headless: true });
  await browser.init();

  await browser.goto(formData.url);

  // Fill form fields
  await browser.fillForm(formData.fields);

  // Submit
  await browser.click(formData.submitButton);

  // Wait for response
  await browser.waitForNavigation();

  // Extract confirmation
  const confirmation = await browser.getStructuredContent();

  await browser.close();
  return confirmation;
}
```

### Pattern 3: Monitoring Agent

Check websites for changes:

```javascript
async function monitorAgent(url, selector) {
  const browser = new AgentBrowser({ headless: true });
  await browser.init();

  await browser.goto(url);

  // Extract target content
  const elements = await browser.extract(selector);

  // Take screenshot for visual record
  await browser.screenshot({ filename: `monitor-${Date.now()}.png` });

  await browser.close();

  return {
    timestamp: new Date(),
    url,
    content: elements,
    hash: hashContent(elements) // Your hash function
  };
}
```

### Pattern 4: Data Collection Agent

Scrape structured data:

```javascript
async function scrapeAgent(url, selectors) {
  const browser = new AgentBrowser({ headless: true });
  await browser.init();

  await browser.goto(url);

  const data = {};

  // Extract each field
  for (const [field, selector] of Object.entries(selectors)) {
    const elements = await browser.extract(selector);
    data[field] = elements.map(el => el.text);
  }

  await browser.close();
  return data;
}

// Usage
const productData = await scrapeAgent('https://shop.example.com/product', {
  title: 'h1.product-title',
  price: '.price',
  description: '.description',
  reviews: '.review-text'
});
```

## LLM Integration

### Preparing Content for LLMs

Agent Browser outputs are optimized for LLM consumption:

```javascript
// Get page as markdown
const html = await browser.getHtml();
const markdown = agentFormatter.htmlToMarkdown(html);

// Feed to LLM
const llmContext = `
Page: ${content.title}
URL: ${content.url}

Content:
${markdown}

Task: Summarize the key points from this page.
`;

// Send to your LLM API
const summary = await llm.complete(llmContext);
```

### Structured Prompts

Use structured content for precise prompts:

```javascript
const content = await browser.getStructuredContent();

const llmPrompt = {
  role: "system",
  content: "You are analyzing a web page."
};

const userPrompt = {
  role: "user",
  content: `
Page Title: ${content.title}
Headings: ${content.structure.headings.map(h => h.text).join(', ')}
Links: ${content.structure.links.length}

Question: What is the main topic of this page?
`
};
```

## Best Practices

### 1. Error Handling

Always handle navigation and extraction errors:

```javascript
try {
  await browser.goto(url);
  const content = await browser.getStructuredContent();
} catch (error) {
  if (error.message.includes('timeout')) {
    // Handle timeout
  } else if (error.message.includes('net::ERR')) {
    // Handle network error
  }
}
```

### 2. Rate Limiting

Be respectful of servers:

```javascript
async function politeAgent(urls) {
  for (const url of urls) {
    await browser.goto(url);
    // ... extract content ...

    // Wait between requests
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
}
```

### 3. Session Management

Save and restore sessions for complex workflows:

```javascript
// Save session at checkpoints
await sessionManager.createFromBrowser('checkpoint-1', browser);

// Later, restore
const session = await sessionManager.load('checkpoint-1');
// Apply cookies, navigate to saved URL
```

### 4. Content Validation

Validate extracted content:

```javascript
const content = await browser.getStructuredContent();

if (!content.title || content.content.text.length < 100) {
  // Page might not have loaded correctly
  await browser.reload();
  content = await browser.getStructuredContent();
}
```

### 5. Memory Management

Close browser when done:

```javascript
const browser = new AgentBrowser();
await browser.init();

try {
  // ... do work ...
} finally {
  await browser.close(); // Always close
}
```

## Advanced Techniques

### JavaScript Execution

Execute custom JavaScript in page context:

```javascript
// Extract computed values
const metrics = await browser.evaluate(() => {
  return {
    scrollHeight: document.body.scrollHeight,
    viewportHeight: window.innerHeight,
    images: document.images.length,
    scripts: document.scripts.length
  };
});
```

### Network Monitoring

Track network requests:

```javascript
const network = browser.getNetworkLog();

// Filter for specific resources
const apiCalls = network.filter(entry =>
  entry.url.includes('/api/') && entry.type === 'request'
);

// Analyze performance
const slowRequests = network.filter(entry => {
  if (entry.type === 'response' && entry.duration) {
    return entry.duration > 1000; // > 1 second
  }
});
```

### Dynamic Content

Handle dynamically loaded content:

```javascript
// Wait for specific element
await browser.waitForSelector('.dynamic-content');

// Or wait for network to be idle
await browser.goto(url, { waitUntil: 'networkidle0' });

// Or wait a specific time
await browser.evaluate(() => {
  return new Promise(resolve => setTimeout(resolve, 2000));
});
```

## CLI Integration

Use CLI commands in agent scripts:

```bash
#!/bin/bash

# Research script
agent-browser goto "https://example.com" --extract > data.json

# Process with jq
cat data.json | jq '.structure.links[] | .href' > links.txt

# Visit each link
while read url; do
  agent-browser content "$url" --format markdown >> research.md
done < links.txt
```

## Performance Tips

1. **Use headless mode**: Faster than visual mode
2. **Limit image loading**: Set `args: ['--blink-settings=imagesEnabled=false']`
3. **Disable unnecessary features**: No need for audio, video, etc.
4. **Reuse browser instance**: Don't create new browser for each page
5. **Extract only what you need**: Use specific selectors

## Security Considerations

1. **Validate URLs**: Ensure URLs are safe before navigating
2. **Sandbox execution**: Run in isolated environment
3. **Limit permissions**: Don't grant unnecessary file access
4. **Monitor resource usage**: Prevent resource exhaustion
5. **Handle user data securely**: Encrypt sensitive session data

## Next Steps

- See `examples/` directory for complete agent implementations
- Read API documentation for detailed method reference
- Join community to share agent patterns
- Contribute your own agent recipes
