import { AgentBrowser } from '../src/browser.js';
import agentFormatter from '../src/agent-formatter.js';

/**
 * Example: Simple navigation and content extraction
 * Perfect for agent-driven web research
 */

async function main() {
  const browser = new AgentBrowser({ headless: true });
  await browser.init();

  try {
    // Navigate to a page
    console.log('Navigating to Wikipedia...');
    await browser.goto('https://en.wikipedia.org/wiki/Artificial_intelligence');

    // Get structured content
    console.log('\n📊 Extracting structured content...\n');
    const content = await browser.getStructuredContent();

    // Display title
    console.log('Title:', content.title);
    console.log('URL:', content.url);

    // Display headings structure
    console.log('\n📋 Page Structure:');
    content.structure.headings.slice(0, 10).forEach(h => {
      console.log(`${'  '.repeat(h.level - 1)}${h.text}`);
    });

    // Get as markdown (perfect for LLM context)
    console.log('\n📝 Converting to Markdown...\n');
    const html = await browser.getHtml();
    const markdown = agentFormatter.htmlToMarkdown(html);

    // Show first 500 chars of markdown
    console.log(markdown.substring(0, 500) + '...\n');

    // Get accessibility tree (for element interaction)
    console.log('🌳 Accessibility Tree:\n');
    const a11y = await browser.getAccessibilityTree();
    console.log(agentFormatter.formatA11yTree(a11y, { format: 'text' }).substring(0, 500) + '...\n');

    // Extract all links
    console.log(`🔗 Found ${content.structure.links.length} links`);
    console.log('\nTop 5 links:');
    content.structure.links.slice(0, 5).forEach(link => {
      console.log(`  - ${link.text} → ${link.href}`);
    });

  } finally {
    await browser.close();
  }
}

main().catch(console.error);
