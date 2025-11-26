import { AgentBrowser } from '../src/browser.js';
import agentFormatter from '../src/agent-formatter.js';
import sessionManager from '../src/session-manager.js';

/**
 * Example: Complete agent workflow
 * Demonstrates a full agent task: research, extract, summarize, save session
 */

async function agentTask(topic) {
  const browser = new AgentBrowser({
    headless: true,
    userAgent: 'ResearchAgent/1.0'
  });

  await browser.init();

  console.log(`🤖 Agent Task: Research "${topic}"\n`);

  try {
    // Step 1: Search
    console.log('Step 1: Searching...');
    await browser.goto('https://duckduckgo.com');
    await browser.type('input[name="q"]', topic, { clear: true });
    await browser.evaluate(() => {
      document.querySelector('input[name="q"]').form.submit();
    });

    await new Promise(resolve => setTimeout(resolve, 2000));

    // Step 2: Extract search results
    console.log('Step 2: Extracting results...');
    const searchResults = await browser.getStructuredContent();
    const topLinks = searchResults.structure.links
      .filter(link => link.href.startsWith('http'))
      .slice(0, 3);

    console.log(`   Found ${topLinks.length} relevant links\n`);

    // Step 3: Visit top results
    console.log('Step 3: Analyzing top results...');
    const analyses = [];

    for (let i = 0; i < Math.min(2, topLinks.length); i++) {
      const link = topLinks[i];
      console.log(`   Visiting: ${link.text}`);

      try {
        await browser.goto(link.href);
        const content = await browser.getStructuredContent();

        // Get markdown for LLM processing
        const html = await browser.getHtml();
        const markdown = agentFormatter.htmlToMarkdown(html);

        analyses.push({
          url: content.url,
          title: content.title,
          markdown: markdown.substring(0, 1000), // First 1000 chars
          headings: content.structure.headings.map(h => h.text),
          linkCount: content.structure.links.length
        });

        // Take screenshot
        await browser.screenshot({
          filename: `research-${i + 1}.png`
        });

      } catch (error) {
        console.log(`   ⚠️  Skipped (error): ${error.message}`);
      }
    }

    // Step 4: Generate report
    console.log('\nStep 4: Generating report...\n');

    const report = {
      topic,
      timestamp: new Date().toISOString(),
      searchResults: topLinks.length,
      analyzed: analyses.length,
      findings: analyses
    };

    // Pretty print report
    console.log('📊 RESEARCH REPORT');
    console.log('='.repeat(60));
    console.log(`Topic: ${topic}`);
    console.log(`Date: ${new Date().toLocaleString()}`);
    console.log(`Pages Analyzed: ${analyses.length}`);
    console.log('');

    analyses.forEach((analysis, i) => {
      console.log(`\n${i + 1}. ${analysis.title}`);
      console.log(`   URL: ${analysis.url}`);
      console.log(`   Headings: ${analysis.headings.slice(0, 3).join(', ')}`);
      console.log(`   Links Found: ${analysis.linkCount}`);
      console.log(`   \n   Preview:\n   ${analysis.markdown.substring(0, 200)}...\n`);
    });

    console.log('='.repeat(60));

    // Step 5: Save session
    console.log('\nStep 5: Saving session...');
    await sessionManager.createFromBrowser('research-session', browser);
    console.log('   ✓ Session saved\n');

    // Step 6: Export report
    const reportJson = JSON.stringify(report, null, 2);
    console.log('Step 6: Report ready for export');
    console.log(`   Report size: ${reportJson.length} chars\n`);

    return report;

  } finally {
    await browser.close();
    console.log('✓ Browser closed');
  }
}

// Run the agent
const topic = process.argv[2] || 'artificial intelligence';
agentTask(topic)
  .then(report => {
    console.log('\n✅ Agent task completed successfully!');
  })
  .catch(error => {
    console.error('\n❌ Agent task failed:', error.message);
    process.exit(1);
  });
