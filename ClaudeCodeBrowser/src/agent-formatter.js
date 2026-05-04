import TurndownService from 'turndown';

/**
 * AgentFormatter - Converts web content to agent-friendly formats
 * Optimizes output for LLM consumption
 */
export class AgentFormatter {
  constructor() {
    this.turndown = new TurndownService({
      headingStyle: 'atx',
      codeBlockStyle: 'fenced',
      emDelimiter: '*',
      bulletListMarker: '-'
    });

    // Custom rules for better markdown conversion
    this.turndown.addRule('removeScripts', {
      filter: ['script', 'style', 'noscript'],
      replacement: () => ''
    });

    this.turndown.addRule('cleanNav', {
      filter: node => {
        return node.nodeName === 'NAV' ||
               (node.classList && (
                 node.classList.contains('navigation') ||
                 node.classList.contains('menu') ||
                 node.classList.contains('sidebar')
               ));
      },
      replacement: () => ''
    });
  }

  /**
   * Convert HTML to clean Markdown
   */
  htmlToMarkdown(html) {
    // Pre-process HTML
    let cleaned = this._cleanHtml(html);

    // Convert to markdown
    let markdown = this.turndown.turndown(cleaned);

    // Post-process markdown
    markdown = this._cleanMarkdown(markdown);

    return markdown;
  }

  /**
   * Clean HTML before conversion
   */
  _cleanHtml(html) {
    // Remove problematic elements
    const removed = [
      '<script[^>]*>.*?</script>',
      '<style[^>]*>.*?</style>',
      '<iframe[^>]*>.*?</iframe>',
      '<noscript[^>]*>.*?</noscript>',
      '<!--.*?-->'
    ];

    let cleaned = html;
    removed.forEach(pattern => {
      cleaned = cleaned.replace(new RegExp(pattern, 'gis'), '');
    });

    return cleaned;
  }

  /**
   * Clean markdown output
   */
  _cleanMarkdown(markdown) {
    // Remove excessive newlines
    markdown = markdown.replace(/\n{3,}/g, '\n\n');

    // Remove leading/trailing whitespace
    markdown = markdown.trim();

    // Clean up list formatting
    markdown = markdown.replace(/\n-\s*\n/g, '\n');

    return markdown;
  }

  /**
   * Format structured content for agent consumption
   */
  formatStructured(data, options = {}) {
    const format = options.format || 'json';

    switch (format) {
      case 'json':
        return JSON.stringify(data, null, options.pretty ? 2 : 0);

      case 'yaml':
        return this._toYaml(data);

      case 'text':
        return this._structuredToText(data);

      default:
        return JSON.stringify(data, null, 2);
    }
  }

  /**
   * Convert structured data to readable text
   */
  _structuredToText(data) {
    let output = [];

    if (data.title) {
      output.push(`TITLE: ${data.title}`);
      output.push('');
    }

    if (data.url) {
      output.push(`URL: ${data.url}`);
      output.push('');
    }

    if (data.metadata && Object.keys(data.metadata).length > 0) {
      output.push('METADATA:');
      Object.entries(data.metadata).forEach(([key, value]) => {
        output.push(`  ${key}: ${value}`);
      });
      output.push('');
    }

    if (data.structure) {
      if (data.structure.headings && data.structure.headings.length > 0) {
        output.push('HEADINGS:');
        data.structure.headings.forEach(h => {
          output.push(`  ${'#'.repeat(h.level)} ${h.text}`);
        });
        output.push('');
      }

      if (data.structure.links && data.structure.links.length > 0) {
        output.push(`LINKS (${data.structure.links.length}):`);
        data.structure.links.slice(0, 20).forEach(link => {
          output.push(`  - ${link.text} → ${link.href}`);
        });
        if (data.structure.links.length > 20) {
          output.push(`  ... and ${data.structure.links.length - 20} more`);
        }
        output.push('');
      }
    }

    if (data.content && data.content.text) {
      output.push('CONTENT:');
      output.push(data.content.text);
      output.push('');
    }

    return output.join('\n');
  }

  /**
   * Convert to simple YAML-like format
   */
  _toYaml(obj, indent = 0) {
    const spaces = '  '.repeat(indent);
    let output = [];

    for (const [key, value] of Object.entries(obj)) {
      if (value === null || value === undefined) {
        output.push(`${spaces}${key}: null`);
      } else if (typeof value === 'object' && !Array.isArray(value)) {
        output.push(`${spaces}${key}:`);
        output.push(this._toYaml(value, indent + 1));
      } else if (Array.isArray(value)) {
        output.push(`${spaces}${key}:`);
        value.forEach(item => {
          if (typeof item === 'object') {
            output.push(`${spaces}  -`);
            const itemYaml = this._toYaml(item, indent + 2);
            output.push(itemYaml.replace(/^  /, ''));
          } else {
            output.push(`${spaces}  - ${item}`);
          }
        });
      } else if (typeof value === 'string' && value.includes('\n')) {
        output.push(`${spaces}${key}: |`);
        value.split('\n').forEach(line => {
          output.push(`${spaces}  ${line}`);
        });
      } else {
        output.push(`${spaces}${key}: ${value}`);
      }
    }

    return output.join('\n');
  }

  /**
   * Format accessibility tree
   */
  formatA11yTree(tree, options = {}) {
    const format = options.format || 'json';

    if (format === 'json') {
      return JSON.stringify(tree, null, options.pretty ? 2 : 0);
    }

    if (format === 'text') {
      return this._a11yTreeToText(tree);
    }

    return tree;
  }

  /**
   * Convert accessibility tree to readable text
   */
  _a11yTreeToText(node, depth = 0) {
    if (!node) return '';

    const indent = '  '.repeat(depth);
    let output = [];

    const parts = [node.role];
    if (node.name) parts.push(`"${node.name}"`);
    if (node.value) parts.push(`= ${node.value}`);

    output.push(`${indent}${parts.join(' ')}`);

    if (node.children) {
      node.children.forEach(child => {
        output.push(this._a11yTreeToText(child, depth + 1));
      });
    }

    return output.join('\n');
  }

  /**
   * Format elements array
   */
  formatElements(elements, options = {}) {
    const format = options.format || 'json';

    if (format === 'json') {
      return JSON.stringify(elements, null, options.pretty ? 2 : 0);
    }

    if (format === 'text') {
      return elements.map((el, i) => {
        const parts = [`[${i}]`, el.tagName.toUpperCase()];
        if (el.text) parts.push(`"${el.text.substring(0, 50)}..."`);
        if (el.attributes && el.attributes.href) parts.push(`→ ${el.attributes.href}`);
        return parts.join(' ');
      }).join('\n');
    }

    return elements;
  }

  /**
   * Create summary for LLM context
   */
  createSummary(data) {
    const parts = [];

    parts.push(`# ${data.title || 'Untitled Page'}`);
    parts.push('');
    parts.push(`URL: ${data.url || 'unknown'}`);
    parts.push('');

    if (data.metadata && data.metadata.description) {
      parts.push(`Description: ${data.metadata.description}`);
      parts.push('');
    }

    if (data.structure && data.structure.headings) {
      parts.push('## Page Structure');
      data.structure.headings.forEach(h => {
        parts.push(`${'#'.repeat(h.level + 2)} ${h.text}`);
      });
      parts.push('');
    }

    if (data.content && data.content.text) {
      parts.push('## Main Content');
      const preview = data.content.text.substring(0, 500);
      parts.push(preview + (data.content.text.length > 500 ? '...' : ''));
      parts.push('');
    }

    if (data.structure && data.structure.links) {
      parts.push(`## Links (${data.structure.links.length} total)`);
      data.structure.links.slice(0, 10).forEach(link => {
        parts.push(`- [${link.text}](${link.href})`);
      });
      if (data.structure.links.length > 10) {
        parts.push(`- ... and ${data.structure.links.length - 10} more links`);
      }
      parts.push('');
    }

    return parts.join('\n');
  }
}

export default new AgentFormatter();
