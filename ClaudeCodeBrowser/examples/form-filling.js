import { AgentBrowser } from '../src/browser.js';

/**
 * Example: Form filling and submission
 * Shows how agents can interact with web forms
 */

async function main() {
  const browser = new AgentBrowser({ headless: false }); // Visual mode to see it work
  await browser.init();

  try {
    // Navigate to a form (using DuckDuckGo as example)
    console.log('Navigating to DuckDuckGo...');
    await browser.goto('https://duckduckgo.com');

    // Wait a moment for page to load
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Type in search box
    console.log('Typing search query...');
    await browser.type('input[name="q"]', 'AI agents and web automation', { clear: true });

    // Take screenshot before submission
    console.log('Taking screenshot...');
    await browser.screenshot({ filename: 'before-search.png' });

    // Submit form (press Enter)
    console.log('Submitting form...');
    await browser.evaluate(() => {
      document.querySelector('input[name="q"]').form.submit();
    });

    // Wait for navigation
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Get results
    console.log('\n📊 Search Results:');
    const content = await browser.getStructuredContent();

    // Take screenshot of results
    await browser.screenshot({ filename: 'search-results.png' });

    console.log(`\nTitle: ${content.title}`);
    console.log(`URL: ${content.url}`);
    console.log(`\nFound ${content.structure.links.length} links in results`);

    // Show first 10 result links
    console.log('\nTop 10 Results:');
    content.structure.links.slice(0, 10).forEach((link, i) => {
      console.log(`${i + 1}. ${link.text}`);
      console.log(`   ${link.href}`);
    });

  } finally {
    await browser.close();
  }
}

main().catch(console.error);
