import { AgentBrowser } from '../src/browser.js';
import agentFormatter from '../src/agent-formatter.js';

/**
 * Example: Multi-page research workflow
 * Shows how an agent can gather information from multiple sources
 */

async function researchTopic(browser, url) {
  await browser.goto(url);
  const content = await browser.getStructuredContent();

  return {
    url: content.url,
    title: content.title,
    summary: content.content.text.substring(0, 500),
    keyPoints: content.structure.headings.slice(0, 5).map(h => h.text),
    sources: content.structure.links.slice(0, 10)
  };
}

async function main() {
  const browser = new AgentBrowser({ headless: true });
  await browser.init();

  console.log('🔬 Starting multi-page research on AI Safety...\n');

  const topics = [
    'https://en.wikipedia.org/wiki/AI_safety',
    'https://en.wikipedia.org/wiki/Artificial_general_intelligence',
    'https://en.wikipedia.org/wiki/Machine_learning'
  ];

  const research = [];

  for (const url of topics) {
    console.log(`📖 Researching: ${url}`);
    const data = await researchTopic(browser, url);
    research.push(data);

    console.log(`   ✓ ${data.title}`);
    console.log(`   Key points: ${data.keyPoints.length}`);
    console.log(`   Sources found: ${data.sources.length}\n`);
  }

  // Compile research report
  console.log('📝 Research Report:\n');
  console.log('='.repeat(60));

  research.forEach((item, i) => {
    console.log(`\n${i + 1}. ${item.title}`);
    console.log(`   URL: ${item.url}`);
    console.log('\n   Summary:');
    console.log(`   ${item.summary}...`);
    console.log('\n   Key Topics:');
    item.keyPoints.forEach(point => {
      console.log(`   - ${point}`);
    });
    console.log('');
  });

  console.log('='.repeat(60));
  console.log(`\nResearch complete! Analyzed ${research.length} pages`);

  await browser.close();
}

main().catch(console.error);
