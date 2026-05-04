# API Reference

Complete API documentation for Agent Browser.

## AgentBrowser Class

### Constructor

```javascript
new AgentBrowser(options)
```

**Options:**
- `headless` (boolean): Run in headless mode. Default: `true`
- `viewport` (object): Viewport size. Default: `{ width: 1280, height: 720 }`
- `timeout` (number): Default timeout in ms. Default: `30000`
- `userAgent` (string): User agent string. Default: `'AgentBrowser/1.0'`

### Methods

#### `init()`

Initialize the browser.

```javascript
await browser.init()
```

**Returns:** `this`

---

#### `goto(url, options)`

Navigate to a URL.

```javascript
await browser.goto('https://example.com', {
  waitUntil: 'networkidle2',
  timeout: 30000
})
```

**Parameters:**
- `url` (string): URL to navigate to
- `options` (object):
  - `waitUntil`: When to consider navigation complete. Options: `'load'`, `'domcontentloaded'`, `'networkidle0'`, `'networkidle2'`
  - `timeout`: Navigation timeout in ms

**Returns:**
```javascript
{
  url: string,
  status: number,
  ok: boolean,
  headers: object,
  timestamp: number
}
```

---

#### `getCurrentUrl()`

Get current page URL.

```javascript
const url = await browser.getCurrentUrl()
```

**Returns:** `string`

---

#### `getTitle()`

Get page title.

```javascript
const title = await browser.getTitle()
```

**Returns:** `string`

---

#### `getHtml()`

Get page HTML.

```javascript
const html = await browser.getHtml()
```

**Returns:** `string`

---

#### `getContent()`

Get main page content as clean text.

```javascript
const content = await browser.getContent()
```

**Returns:** `string` - Main content with scripts, styles, nav removed

---

#### `getStructuredContent()`

Get structured content optimized for agents.

```javascript
const content = await browser.getStructuredContent()
```

**Returns:**
```javascript
{
  title: string,
  url: string,
  content: {
    text: string,
    paragraphs: string[]
  },
  metadata: {
    description: string,
    keywords: string,
    // ... other meta tags
  },
  structure: {
    headings: [
      { level: number, text: string, id: string }
    ],
    links: [
      { text: string, href: string, title: string }
    ],
    images: [
      { src: string, alt: string, width: number, height: number }
    ]
  }
}
```

---

#### `getAccessibilityTree()`

Get simplified accessibility tree.

```javascript
const tree = await browser.getAccessibilityTree()
```

**Returns:**
```javascript
{
  role: string,
  name: string,
  value: string,
  children: [...]
}
```

---

#### `extract(selector, options)`

Extract elements by CSS selector.

```javascript
const elements = await browser.extract('.product', {
  includeHtml: true,
  includeAttributes: true,
  includeStyles: false
})
```

**Parameters:**
- `selector` (string): CSS selector
- `options` (object):
  - `includeHtml`: Include element HTML
  - `includeAttributes`: Include all attributes
  - `includeStyles`: Include computed styles

**Returns:**
```javascript
[
  {
    tagName: string,
    text: string,
    html: string,
    attributes: object,
    styles: object
  }
]
```

---

#### `click(selector)`

Click an element.

```javascript
await browser.click('button.submit')
```

**Parameters:**
- `selector` (string): CSS selector

**Returns:**
```javascript
{
  success: boolean,
  url: string
}
```

---

#### `type(selector, text, options)`

Type into an element.

```javascript
await browser.type('input#email', 'test@example.com', {
  clear: true,
  delay: 50
})
```

**Parameters:**
- `selector` (string): CSS selector
- `text` (string): Text to type
- `options` (object):
  - `clear`: Clear existing text first
  - `delay`: Delay between keystrokes in ms

**Returns:**
```javascript
{ success: boolean }
```

---

#### `fillForm(fields)`

Fill multiple form fields.

```javascript
await browser.fillForm({
  'input[name="email"]': 'test@example.com',
  'select[name="country"]': 'US',
  'textarea#message': 'Hello world'
})
```

**Parameters:**
- `fields` (object): Map of selector to value

**Returns:**
```javascript
[
  { selector: string, success: boolean, error: string }
]
```

---

#### `screenshot(options)`

Take a screenshot.

```javascript
await browser.screenshot({
  filename: 'page.png',
  fullPage: true,
  type: 'png'
})
```

**Parameters:**
- `options` (object):
  - `filename`: Output filename
  - `fullPage`: Capture full page
  - `type`: Image type (`'png'` or `'jpeg'`)

**Returns:**
```javascript
{ filename: string, path: string }
```

---

#### `pdf(options)`

Generate PDF.

```javascript
await browser.pdf({
  filename: 'page.pdf',
  format: 'A4',
  printBackground: true
})
```

**Parameters:**
- `options` (object):
  - `filename`: Output filename
  - `format`: Paper format
  - `printBackground`: Include backgrounds
  - `margin`: Page margins

**Returns:**
```javascript
{ filename: string, path: string }
```

---

#### `evaluate(script)`

Execute JavaScript in page context.

```javascript
const result = await browser.evaluate(() => {
  return document.body.scrollHeight
})
```

**Parameters:**
- `script` (function): JavaScript to execute

**Returns:** Any - Result of script execution

---

#### `waitForSelector(selector, options)`

Wait for element to appear.

```javascript
await browser.waitForSelector('.dynamic-content', {
  visible: true,
  timeout: 5000
})
```

**Parameters:**
- `selector` (string): CSS selector
- `options` (object):
  - `visible`: Wait for visibility
  - `timeout`: Wait timeout

**Returns:**
```javascript
{ success: boolean }
```

---

#### `goBack()`

Navigate back in history.

```javascript
await browser.goBack()
```

**Returns:**
```javascript
{ url: string }
```

---

#### `goForward()`

Navigate forward in history.

```javascript
await browser.goForward()
```

**Returns:**
```javascript
{ url: string }
```

---

#### `reload()`

Reload current page.

```javascript
await browser.reload()
```

**Returns:**
```javascript
{ url: string }
```

---

#### `getCookies()`

Get all cookies.

```javascript
const cookies = await browser.getCookies()
```

**Returns:** `Array` - Array of cookie objects

---

#### `setCookie(cookie)`

Set a cookie.

```javascript
await browser.setCookie({
  name: 'session',
  value: 'abc123',
  domain: 'example.com'
})
```

**Returns:**
```javascript
{ success: boolean }
```

---

#### `clearCookies()`

Clear all cookies.

```javascript
await browser.clearCookies()
```

**Returns:**
```javascript
{ success: boolean, cleared: number }
```

---

#### `setViewport(width, height)`

Set viewport size.

```javascript
await browser.setViewport(1920, 1080)
```

**Returns:**
```javascript
{ width: number, height: number }
```

---

#### `scroll(direction)`

Scroll the page.

```javascript
await browser.scroll('down') // 'up', 'down', 'top', 'bottom'
```

**Returns:**
```javascript
{ success: boolean }
```

---

#### `getNetworkLog(options)`

Get network activity log.

```javascript
const log = browser.getNetworkLog({
  clear: true,
  type: 'request'
})
```

**Parameters:**
- `options` (object):
  - `clear`: Clear log after retrieving
  - `type`: Filter by type (`'request'` or `'response'`)

**Returns:**
```javascript
[
  {
    type: 'request' | 'response',
    method: string,
    url: string,
    status: number,
    timestamp: number
  }
]
```

---

#### `getHistory()`

Get navigation history.

```javascript
const history = browser.getHistory()
```

**Returns:** `Array<string>` - Array of URLs

---

#### `close()`

Close the browser.

```javascript
await browser.close()
```

**Returns:** `void`

---

## AgentFormatter Class

### Methods

#### `htmlToMarkdown(html)`

Convert HTML to Markdown.

```javascript
const markdown = agentFormatter.htmlToMarkdown(html)
```

---

#### `formatStructured(data, options)`

Format structured data.

```javascript
const output = agentFormatter.formatStructured(data, {
  format: 'json', // 'json', 'yaml', 'text'
  pretty: true
})
```

---

#### `formatA11yTree(tree, options)`

Format accessibility tree.

```javascript
const output = agentFormatter.formatA11yTree(tree, {
  format: 'text'
})
```

---

#### `createSummary(data)`

Create LLM-friendly summary.

```javascript
const summary = agentFormatter.createSummary(structuredContent)
```

---

## SessionManager Class

### Methods

#### `save(name, data)`

Save a session.

```javascript
await sessionManager.save('my-session', {
  url: 'https://example.com',
  cookies: [...],
  history: [...],
  viewport: { width: 1280, height: 720 }
})
```

---

#### `load(name)`

Load a session.

```javascript
const session = await sessionManager.load('my-session')
```

---

#### `list()`

List all sessions.

```javascript
const sessions = await sessionManager.list()
```

---

#### `delete(name)`

Delete a session.

```javascript
await sessionManager.delete('my-session')
```

---

#### `createFromBrowser(name, browser)`

Create session from browser state.

```javascript
await sessionManager.createFromBrowser('checkpoint', browser)
```

---

## CLI Commands

See README.md for complete CLI documentation.
