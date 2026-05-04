#!/usr/bin/env node

/**
 * Agent Browser Demo
 * Shows all major features in one script
 */

import { AgentBrowser } from './src/browser.js';
import agentFormatter from './src/agent-formatter.js';
import sessionManager from './src/session-manager.js';

console.log('🤖 Agent Browser Demo\n');
console.log('This demo showcases all major features.\n');

async function demo() {
  // Initialize browser
  console.log('📦 Initializing browser...');
  const browser = new AgentBrowser({
    headless: true,
    timeout: 30000
  });
  await browser.init();
  console.log('✓ Browser ready\n');

  try {
    // Feature 1: Navigation
    console.log('1️⃣  Navigation');
    console.log('   Navigating to Example.com...');
    const navResult = await browser.goto('https://example.com');
    console.log(`   ✓ Loaded: ${navResult.url} (${navResult.status})\n`);

    // Feature 2: Get Title
    console.log('2️⃣  Get Page Title');
    const title = await browser.getTitle();
    console.log(`   Title: "${title}"\n`);

    // Feature 3: Extract Structured Content
    console.log('3️⃣  Extract Structured Content');
    const content = await browser.getStructuredContent();
    console.log(`   ✓ Extracted:`);
    console.log(`     - Title: ${content.title}`);
    console.log(`     - Headings: ${content.structure.headings.length}`);
    console.log(`     - Links: ${content.structure.links.length}`);
    console.log(`     - Images: ${content.structure.images.length}`);
    console.log(`     - Content length: ${content.content.text.length} chars\n`);

    // Feature 4: Content Preview
    console.log('4️⃣  Main Content Preview');
    const mainContent = content.content.text.substring(0, 200);
    console.log(`   "${mainContent}..."\n`);

    // Feature 5: Convert to Markdown
    console.log('5️⃣  Convert to Markdown (LLM-friendly)');
    const html = await browser.getHtml();
    const markdown = agentFormatter.htmlToMarkdown(html);
    console.log(`   ✓ Converted: ${markdown.length} chars`);
    console.log(`   Preview:\n`);
    console.log('   ' + markdown.substring(0, 300).split('\n').join('\n   '));
    console.log('   ...\n');

    // Feature 6: Accessibility Tree
    console.log('6️⃣  Accessibility Tree (Element Structure)');
    const a11y = await browser.getAccessibilityTree();
    const a11yText = agentFormatter.formatA11yTree(a11y, { format: 'text' });
    console.log(`   ✓ Generated tree with ${a11yText.split('\n').length} nodes`);
    console.log(`   Preview:\n`);
    console.log('   ' + a11yText.substring(0, 200).split('\n').join('\n   '));
    console.log('   ...\n');

    // Feature 7: Extract Specific Elements
    console.log('7️⃣  Extract Specific Elements');
    const links = await browser.extract('a', {
      includeAttributes: true
    });
    console.log(`   ✓ Found ${links.length} link elements`);
    if (links.length > 0) {
      console.log(`   First link: "${links[0].text}" → ${links[0].attributes?.href}\n`);
    }

    // Feature 8: Screenshot
    console.log('8️⃣  Take Screenshot');
    const screenshot = await browser.screenshot({
      filename: 'demo-screenshot.png',
      fullPage: true
    });
    console.log(`   ✓ Saved: ${screenshot.filename}\n`);

    // Feature 9: Network Log
    console.log('9️⃣  Network Activity');
    const network = browser.getNetworkLog({ clear: true });
    const requests = network.filter(e => e.type === 'request');
    const responses = network.filter(e => e.type === 'response');
    console.log(`   ✓ Captured: ${requests.length} requests, ${responses.length} responses\n`);

    // Feature 10: Session Management
    console.log('🔟 Session Management');
    const sessionResult = await sessionManager.createFromBrowser('demo-session', browser);
    console.log(`   ✓ Session saved: ${sessionResult.session.name}`);
    console.log(`   Saved at: ${sessionResult.session.savedAt}\n`);

    // Feature 11: Navigate to Another Page
    console.log('1️⃣1️⃣  Multi-Page Navigation');
    console.log('   Navigating to Wikipedia...');
    await browser.goto('https://en.wikipedia.org/wiki/Artificial_intelligence');
    const wikiContent = await browser.getStructuredContent();
    console.log(`   ✓ Loaded: ${wikiContent.title}`);
    console.log(`   Found ${wikiContent.structure.headings.length} headings\n`);

    // Feature 12: History
    console.log('1️⃣2️⃣  Navigation History');
    const history = browser.getHistory();
    console.log(`   ✓ Visited ${history.length} pages:`);
    history.forEach((url, i) => {
      console.log(`     ${i + 1}. ${url}`);
    });
    console.log('');

    // Feature 13: Go Back
    console.log('1️⃣3️⃣  Navigate Back');
    await browser.goBack();
    const backUrl = await browser.getCurrentUrl();
    console.log(`   ✓ Back to: ${backUrl}\n`);

    // Feature 14: List Sessions
    console.log('1️⃣4️⃣  List Saved Sessions');
    const sessions = await sessionManager.list();
    console.log(`   ✓ Found ${sessions.length} session(s):`);
    sessions.forEach(s => {
      console.log(`     - ${s.name} (${s.url})`);
    });
    console.log('');

    // Feature 15: Create LLM Summary
    console.log('1️⃣5️⃣  LLM-Optimized Summary');
    const summary = agentFormatter.createSummary(content);
    console.log(`   ✓ Generated summary (${summary.length} chars)`);
    console.log(`   Preview:\n`);
    console.log('   ' + summary.substring(0, 400).split('\n').join('\n   '));
    console.log('   ...\n');

    // Summary
    console.log('═══════════════════════════════════════════════════════');
    console.log('✅ Demo Complete!');
    console.log('═══════════════════════════════════════════════════════');
    console.log('');
    console.log('Features Demonstrated:');
    console.log('  ✓ Page navigation');
    console.log('  ✓ Content extraction');
    console.log('  ✓ Structured data');
    console.log('  ✓ Markdown conversion');
    console.log('  ✓ Accessibility tree');
    console.log('  ✓ Element extraction');
    console.log('  ✓ Screenshots');
    console.log('  ✓ Network monitoring');
    console.log('  ✓ Session management');
    console.log('  ✓ Multi-page workflows');
    console.log('  ✓ History tracking');
    console.log('  ✓ LLM-optimized output');
    console.log('');
    console.log('Generated Files:');
    console.log('  - demo-screenshot.png');
    console.log('  - sessions/demo-session.json');
    console.log('');
    console.log('Next Steps:');
    console.log('  - Read QUICKSTART.md for usage guide');
    console.log('  - Check examples/ for more patterns');
    console.log('  - Build your own agent!');
    console.log('');

  } catch (error) {
    console.error('❌ Error:', error.message);
    console.error(error.stack);
  } finally {
    console.log('🔒 Closing browser...');
    await browser.close();
    console.log('✓ Done!\n');
  }
}

// Run demo
demo().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
