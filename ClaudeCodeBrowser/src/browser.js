import puppeteer from 'puppeteer';

/**
 * AgentBrowser - Core browser controller optimized for AI agents
 * Wraps Puppeteer with agent-friendly methods and structured outputs
 */
export class AgentBrowser {
  constructor(options = {}) {
    this.browser = null;
    this.page = null;
    this.options = {
      headless: options.headless !== false,
      viewport: options.viewport || { width: 1280, height: 720 },
      timeout: options.timeout || 30000,
      userAgent: options.userAgent || 'AgentBrowser/1.0',
      ...options
    };
    this.history = [];
    this.networkLog = [];
  }

  /**
   * Initialize the browser
   */
  async init() {
    this.browser = await puppeteer.launch({
      headless: this.options.headless ? 'new' : false,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-web-security',
        '--disable-features=IsolateOrigins,site-per-process'
      ]
    });

    this.page = await this.browser.newPage();

    // Set viewport
    await this.page.setViewport(this.options.viewport);

    // Set user agent
    await this.page.setUserAgent(this.options.userAgent);

    // Set default timeout
    this.page.setDefaultTimeout(this.options.timeout);

    // Setup network monitoring
    this.page.on('request', request => {
      this.networkLog.push({
        type: 'request',
        method: request.method(),
        url: request.url(),
        resourceType: request.resourceType(),
        timestamp: Date.now()
      });
    });

    this.page.on('response', response => {
      this.networkLog.push({
        type: 'response',
        status: response.status(),
        url: response.url(),
        timestamp: Date.now()
      });
    });

    return this;
  }

  /**
   * Navigate to a URL
   */
  async goto(url, options = {}) {
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      url = 'https://' + url;
    }

    const response = await this.page.goto(url, {
      waitUntil: options.waitUntil || 'networkidle2',
      timeout: options.timeout || this.options.timeout
    });

    this.history.push(url);

    return {
      url: this.page.url(),
      status: response.status(),
      ok: response.ok(),
      headers: response.headers(),
      timestamp: Date.now()
    };
  }

  /**
   * Get current URL
   */
  async getCurrentUrl() {
    return this.page.url();
  }

  /**
   * Get page title
   */
  async getTitle() {
    return await this.page.title();
  }

  /**
   * Get page HTML
   */
  async getHtml() {
    return await this.page.content();
  }

  /**
   * Get main page content (text only, cleaned)
   */
  async getContent() {
    return await this.page.evaluate(() => {
      // Remove unwanted elements
      const unwanted = ['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe'];
      unwanted.forEach(tag => {
        document.querySelectorAll(tag).forEach(el => el.remove());
      });

      // Get main content
      const main = document.querySelector('main') ||
                   document.querySelector('article') ||
                   document.querySelector('[role="main"]') ||
                   document.body;

      return main.innerText.trim();
    });
  }

  /**
   * Get structured content optimized for agents
   */
  async getStructuredContent() {
    return await this.page.evaluate(() => {
      const result = {
        title: document.title,
        url: window.location.href,
        content: {},
        metadata: {},
        structure: {}
      };

      // Extract metadata
      const metaTags = document.querySelectorAll('meta');
      metaTags.forEach(meta => {
        const name = meta.getAttribute('name') || meta.getAttribute('property');
        const content = meta.getAttribute('content');
        if (name && content) {
          result.metadata[name] = content;
        }
      });

      // Extract headings
      result.structure.headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'))
        .map(h => ({
          level: parseInt(h.tagName[1]),
          text: h.innerText.trim(),
          id: h.id || null
        }));

      // Extract links
      result.structure.links = Array.from(document.querySelectorAll('a[href]'))
        .map(a => ({
          text: a.innerText.trim(),
          href: a.href,
          title: a.title || null
        }))
        .filter(link => link.text.length > 0);

      // Extract images
      result.structure.images = Array.from(document.querySelectorAll('img[src]'))
        .map(img => ({
          src: img.src,
          alt: img.alt || null,
          title: img.title || null,
          width: img.naturalWidth,
          height: img.naturalHeight
        }));

      // Extract main content
      const unwanted = ['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe'];
      const clone = document.body.cloneNode(true);
      unwanted.forEach(tag => {
        clone.querySelectorAll(tag).forEach(el => el.remove());
      });

      const main = clone.querySelector('main') ||
                   clone.querySelector('article') ||
                   clone.querySelector('[role="main"]') ||
                   clone;

      result.content.text = main.innerText.trim();
      result.content.paragraphs = Array.from(main.querySelectorAll('p'))
        .map(p => p.innerText.trim())
        .filter(text => text.length > 0);

      return result;
    });
  }

  /**
   * Get accessibility tree (simplified DOM for agents)
   */
  async getAccessibilityTree() {
    const snapshot = await this.page.accessibility.snapshot();
    return this._simplifyA11yTree(snapshot);
  }

  _simplifyA11yTree(node, depth = 0, maxDepth = 5) {
    if (!node || depth > maxDepth) return null;

    const simplified = {
      role: node.role,
      name: node.name || null,
    };

    if (node.value) simplified.value = node.value;
    if (node.description) simplified.description = node.description;
    if (node.keyshortcuts) simplified.keyshortcuts = node.keyshortcuts;
    if (node.roledescription) simplified.roledescription = node.roledescription;
    if (node.valuetext) simplified.valuetext = node.valuetext;

    if (node.children && node.children.length > 0) {
      simplified.children = node.children
        .map(child => this._simplifyA11yTree(child, depth + 1, maxDepth))
        .filter(child => child !== null);
    }

    return simplified;
  }

  /**
   * Extract elements by selector
   */
  async extract(selector, options = {}) {
    return await this.page.evaluate((sel, opts) => {
      const elements = Array.from(document.querySelectorAll(sel));

      return elements.map(el => {
        const data = {
          tagName: el.tagName.toLowerCase(),
          text: el.innerText ? el.innerText.trim() : null,
          html: opts.includeHtml ? el.innerHTML : null
        };

        // Get attributes
        if (opts.includeAttributes) {
          data.attributes = {};
          Array.from(el.attributes).forEach(attr => {
            data.attributes[attr.name] = attr.value;
          });
        }

        // Get computed styles
        if (opts.includeStyles) {
          const styles = window.getComputedStyle(el);
          data.styles = {
            display: styles.display,
            visibility: styles.visibility,
            position: styles.position
          };
        }

        return data;
      });
    }, selector, options);
  }

  /**
   * Click an element
   */
  async click(selector) {
    await this.page.waitForSelector(selector, { visible: true });
    await this.page.click(selector);
    await this.page.waitForTimeout(500); // Brief wait for any resulting changes

    return {
      success: true,
      url: this.page.url()
    };
  }

  /**
   * Type into an element
   */
  async type(selector, text, options = {}) {
    await this.page.waitForSelector(selector, { visible: true });

    if (options.clear) {
      await this.page.click(selector, { clickCount: 3 });
    }

    await this.page.type(selector, text, {
      delay: options.delay || 50
    });

    return { success: true };
  }

  /**
   * Fill a form with multiple fields
   */
  async fillForm(fields) {
    const results = [];

    for (const [selector, value] of Object.entries(fields)) {
      try {
        await this.page.waitForSelector(selector, { visible: true, timeout: 5000 });

        const elementType = await this.page.evaluate(sel => {
          const el = document.querySelector(sel);
          return el ? el.tagName.toLowerCase() : null;
        }, selector);

        if (elementType === 'select') {
          await this.page.select(selector, value);
        } else if (elementType === 'input' || elementType === 'textarea') {
          await this.page.click(selector, { clickCount: 3 });
          await this.page.type(selector, value);
        }

        results.push({ selector, success: true });
      } catch (error) {
        results.push({ selector, success: false, error: error.message });
      }
    }

    return results;
  }

  /**
   * Take a screenshot
   */
  async screenshot(options = {}) {
    const filename = options.filename || `screenshot-${Date.now()}.png`;

    await this.page.screenshot({
      path: filename,
      fullPage: options.fullPage !== false,
      type: options.type || 'png'
    });

    return { filename, path: filename };
  }

  /**
   * Generate PDF
   */
  async pdf(options = {}) {
    const filename = options.filename || `page-${Date.now()}.pdf`;

    await this.page.pdf({
      path: filename,
      format: options.format || 'A4',
      printBackground: options.printBackground !== false,
      margin: options.margin || { top: '1cm', right: '1cm', bottom: '1cm', left: '1cm' }
    });

    return { filename, path: filename };
  }

  /**
   * Execute JavaScript in page context
   */
  async evaluate(script) {
    return await this.page.evaluate(script);
  }

  /**
   * Wait for selector
   */
  async waitForSelector(selector, options = {}) {
    await this.page.waitForSelector(selector, {
      visible: options.visible !== false,
      timeout: options.timeout || this.options.timeout
    });
    return { success: true };
  }

  /**
   * Wait for navigation
   */
  async waitForNavigation(options = {}) {
    await this.page.waitForNavigation({
      waitUntil: options.waitUntil || 'networkidle2',
      timeout: options.timeout || this.options.timeout
    });
    return { url: this.page.url() };
  }

  /**
   * Go back
   */
  async goBack() {
    await this.page.goBack({ waitUntil: 'networkidle2' });
    return { url: this.page.url() };
  }

  /**
   * Go forward
   */
  async goForward() {
    await this.page.goForward({ waitUntil: 'networkidle2' });
    return { url: this.page.url() };
  }

  /**
   * Reload page
   */
  async reload() {
    await this.page.reload({ waitUntil: 'networkidle2' });
    return { url: this.page.url() };
  }

  /**
   * Get cookies
   */
  async getCookies() {
    return await this.page.cookies();
  }

  /**
   * Set cookie
   */
  async setCookie(cookie) {
    await this.page.setCookie(cookie);
    return { success: true };
  }

  /**
   * Clear cookies
   */
  async clearCookies() {
    const cookies = await this.page.cookies();
    await this.page.deleteCookie(...cookies);
    return { success: true, cleared: cookies.length };
  }

  /**
   * Set viewport
   */
  async setViewport(width, height) {
    await this.page.setViewport({ width, height });
    return { width, height };
  }

  /**
   * Scroll page
   */
  async scroll(direction) {
    await this.page.evaluate((dir) => {
      const scrollAmount = window.innerHeight * 0.8;

      switch(dir) {
        case 'down':
          window.scrollBy(0, scrollAmount);
          break;
        case 'up':
          window.scrollBy(0, -scrollAmount);
          break;
        case 'top':
          window.scrollTo(0, 0);
          break;
        case 'bottom':
          window.scrollTo(0, document.body.scrollHeight);
          break;
      }
    }, direction);

    return { success: true };
  }

  /**
   * Get network activity
   */
  getNetworkLog(options = {}) {
    const log = this.networkLog;

    if (options.clear) {
      this.networkLog = [];
    }

    if (options.type) {
      return log.filter(entry => entry.type === options.type);
    }

    return log;
  }

  /**
   * Get browser history
   */
  getHistory() {
    return this.history;
  }

  /**
   * Close the browser
   */
  async close() {
    if (this.browser) {
      await this.browser.close();
      this.browser = null;
      this.page = null;
    }
  }
}
