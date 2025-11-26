#!/usr/bin/env node

import { Command } from 'commander';
import chalk from 'chalk';
import ora from 'ora';
import readline from 'readline';
import { AgentBrowser } from './browser.js';
import agentFormatter from './agent-formatter.js';
import sessionManager from './session-manager.js';

const program = new Command();
let browser = null;
let spinner = null;

// Global error handler
process.on('unhandledRejection', (error) => {
  console.error(chalk.red('Error:'), error.message);
  if (browser) {
    browser.close().then(() => process.exit(1));
  } else {
    process.exit(1);
  }
});

/**
 * Initialize browser if not already initialized
 */
async function ensureBrowser(options = {}) {
  if (!browser) {
    spinner = ora('Initializing browser...').start();
    browser = new AgentBrowser(options);
    await browser.init();
    spinner.succeed('Browser ready');
  }
  return browser;
}

/**
 * Interactive REPL mode
 */
async function interactiveMode() {
  console.log(chalk.blue.bold('\n🤖 Agent Browser - Interactive Mode'));
  console.log(chalk.gray('Type "help" for commands, "exit" to quit\n'));

  await ensureBrowser({ headless: false });

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    prompt: chalk.green('agent-browser> ')
  });

  rl.prompt();

  rl.on('line', async (line) => {
    const input = line.trim();

    if (!input) {
      rl.prompt();
      return;
    }

    if (input === 'exit' || input === 'quit') {
      console.log(chalk.yellow('\nClosing browser...'));
      await browser.close();
      process.exit(0);
    }

    try {
      await processCommand(input);
    } catch (error) {
      console.error(chalk.red('Error:'), error.message);
    }

    rl.prompt();
  });

  rl.on('close', async () => {
    console.log(chalk.yellow('\nClosing browser...'));
    await browser.close();
    process.exit(0);
  });
}

/**
 * Process a command (for REPL mode)
 */
async function processCommand(input) {
  const parts = input.match(/(?:[^\s"]+|"[^"]*")+/g) || [];
  const command = parts[0];
  const args = parts.slice(1).map(arg => arg.replace(/^"|"$/g, ''));

  switch (command) {
    case 'help':
      showHelp();
      break;

    case 'goto':
      if (!args[0]) {
        console.log(chalk.red('Usage: goto <url>'));
        return;
      }
      spinner = ora('Navigating...').start();
      const navResult = await browser.goto(args[0]);
      spinner.succeed(`Loaded: ${chalk.cyan(navResult.url)} (${navResult.status})`);
      break;

    case 'url':
      console.log(chalk.cyan(await browser.getCurrentUrl()));
      break;

    case 'title':
      console.log(await browser.getTitle());
      break;

    case 'content':
      const content = await browser.getContent();
      console.log(content);
      break;

    case 'markdown':
      spinner = ora('Converting to markdown...').start();
      const html = await browser.getHtml();
      const markdown = agentFormatter.htmlToMarkdown(html);
      spinner.stop();
      console.log(markdown);
      break;

    case 'extract':
      const structured = await browser.getStructuredContent();
      console.log(JSON.stringify(structured, null, 2));
      break;

    case 'screenshot':
      spinner = ora('Taking screenshot...').start();
      const screenshot = await browser.screenshot({ filename: args[0] });
      spinner.succeed(`Screenshot saved: ${chalk.cyan(screenshot.filename)}`);
      break;

    case 'click':
      if (!args[0]) {
        console.log(chalk.red('Usage: click <selector>'));
        return;
      }
      await browser.click(args[0]);
      console.log(chalk.green('Clicked'));
      break;

    case 'type':
      if (args.length < 2) {
        console.log(chalk.red('Usage: type <selector> <text>'));
        return;
      }
      await browser.type(args[0], args.slice(1).join(' '));
      console.log(chalk.green('Typed'));
      break;

    case 'back':
      await browser.goBack();
      console.log(chalk.green('Went back'));
      break;

    case 'forward':
      await browser.goForward();
      console.log(chalk.green('Went forward'));
      break;

    case 'reload':
      await browser.reload();
      console.log(chalk.green('Reloaded'));
      break;

    case 'links':
      const data = await browser.getStructuredContent();
      console.log(chalk.bold(`\nFound ${data.structure.links.length} links:\n`));
      data.structure.links.forEach((link, i) => {
        console.log(`${i + 1}. ${link.text} → ${chalk.cyan(link.href)}`);
      });
      break;

    case 'accessibility':
      const a11y = await browser.getAccessibilityTree();
      console.log(agentFormatter.formatA11yTree(a11y, { format: 'text' }));
      break;

    case 'cookies':
      const cookies = await browser.getCookies();
      console.log(JSON.stringify(cookies, null, 2));
      break;

    case 'network':
      const network = browser.getNetworkLog({ clear: true });
      console.log(`${network.length} network requests`);
      network.slice(-20).forEach(entry => {
        const color = entry.type === 'request' ? chalk.blue : chalk.green;
        console.log(color(`${entry.type}: ${entry.url}`));
      });
      break;

    case 'scroll':
      await browser.scroll(args[0] || 'down');
      console.log(chalk.green(`Scrolled ${args[0] || 'down'}`));
      break;

    default:
      console.log(chalk.red(`Unknown command: ${command}`));
      console.log('Type "help" for available commands');
  }
}

/**
 * Show help
 */
function showHelp() {
  console.log(chalk.bold('\nAvailable Commands:\n'));
  console.log(chalk.cyan('Navigation:'));
  console.log('  goto <url>           Navigate to URL');
  console.log('  back                 Go back');
  console.log('  forward              Go forward');
  console.log('  reload               Reload page');
  console.log('');
  console.log(chalk.cyan('Content:'));
  console.log('  content              Get main content');
  console.log('  markdown             Convert to markdown');
  console.log('  extract              Get structured content');
  console.log('  links                List all links');
  console.log('  accessibility        Get accessibility tree');
  console.log('');
  console.log(chalk.cyan('Interaction:'));
  console.log('  click <selector>     Click element');
  console.log('  type <sel> <text>    Type into element');
  console.log('  scroll <direction>   Scroll (up/down/top/bottom)');
  console.log('');
  console.log(chalk.cyan('Information:'));
  console.log('  url                  Get current URL');
  console.log('  title                Get page title');
  console.log('  screenshot [file]    Take screenshot');
  console.log('  cookies              Show cookies');
  console.log('  network              Show network log');
  console.log('');
  console.log(chalk.cyan('Other:'));
  console.log('  help                 Show this help');
  console.log('  exit                 Exit browser\n');
}

// ============================================
// CLI COMMANDS
// ============================================

program
  .name('agent-browser')
  .description('A headless browser for AI agents')
  .version('1.0.0');

// Interactive mode (default)
program
  .command('interactive', { isDefault: true })
  .description('Start interactive mode')
  .action(async () => {
    await interactiveMode();
  });

// Goto command
program
  .command('goto <url>')
  .description('Navigate to a URL')
  .option('-e, --extract', 'Extract structured content')
  .option('-m, --markdown', 'Convert to markdown')
  .option('-s, --screenshot <filename>', 'Take screenshot')
  .option('-f, --format <format>', 'Output format (json|text|markdown)', 'json')
  .action(async (url, options) => {
    await ensureBrowser();

    spinner = ora('Navigating...').start();
    await browser.goto(url);
    spinner.succeed(`Loaded: ${chalk.cyan(url)}`);

    if (options.extract) {
      const data = await browser.getStructuredContent();
      console.log(JSON.stringify(data, null, 2));
    }

    if (options.markdown) {
      const html = await browser.getHtml();
      const markdown = agentFormatter.htmlToMarkdown(html);
      console.log(markdown);
    }

    if (options.screenshot) {
      await browser.screenshot({ filename: options.screenshot });
      console.log(chalk.green(`Screenshot saved: ${options.screenshot}`));
    }

    await browser.close();
  });

// Content command
program
  .command('content <url>')
  .description('Get page content')
  .option('-f, --format <format>', 'Output format (text|markdown|json)', 'text')
  .action(async (url, options) => {
    await ensureBrowser();

    await browser.goto(url);

    if (options.format === 'markdown') {
      const html = await browser.getHtml();
      console.log(agentFormatter.htmlToMarkdown(html));
    } else if (options.format === 'json') {
      const data = await browser.getStructuredContent();
      console.log(JSON.stringify(data, null, 2));
    } else {
      const content = await browser.getContent();
      console.log(content);
    }

    await browser.close();
  });

// Extract command
program
  .command('extract <url>')
  .description('Extract structured content from a page')
  .option('-s, --selector <selector>', 'CSS selector to extract')
  .option('-f, --format <format>', 'Output format (json|text)', 'json')
  .action(async (url, options) => {
    await ensureBrowser();

    await browser.goto(url);

    if (options.selector) {
      const elements = await browser.extract(options.selector, {
        includeAttributes: true
      });
      console.log(JSON.stringify(elements, null, 2));
    } else {
      const data = await browser.getStructuredContent();
      console.log(JSON.stringify(data, null, 2));
    }

    await browser.close();
  });

// Screenshot command
program
  .command('screenshot <url>')
  .description('Take a screenshot')
  .option('-o, --output <filename>', 'Output filename')
  .option('-f, --fullpage', 'Full page screenshot', true)
  .action(async (url, options) => {
    await ensureBrowser();

    await browser.goto(url);

    const result = await browser.screenshot({
      filename: options.output,
      fullPage: options.fullpage
    });

    console.log(chalk.green(`Screenshot saved: ${result.filename}`));

    await browser.close();
  });

// Links command
program
  .command('links <url>')
  .description('Extract all links from a page')
  .option('-f, --format <format>', 'Output format (json|text)', 'text')
  .action(async (url, options) => {
    await ensureBrowser();

    await browser.goto(url);
    const data = await browser.getStructuredContent();

    if (options.format === 'json') {
      console.log(JSON.stringify(data.structure.links, null, 2));
    } else {
      data.structure.links.forEach((link, i) => {
        console.log(`${i + 1}. ${link.text} → ${link.href}`);
      });
    }

    await browser.close();
  });

// Session commands
program
  .command('session')
  .description('Session management')
  .action(() => {
    console.log('Use: session <save|load|list|delete> [name]');
  });

program
  .command('session-save <name>')
  .description('Save current session')
  .action(async (name) => {
    if (!browser) {
      console.log(chalk.red('No active browser session'));
      return;
    }

    const result = await sessionManager.createFromBrowser(name, browser);
    console.log(chalk.green(`Session saved: ${name}`));
  });

program
  .command('session-load <name>')
  .description('Load a saved session')
  .action(async (name) => {
    await ensureBrowser();

    const session = await sessionManager.load(name);

    // Apply session
    if (session.cookies) {
      for (const cookie of session.cookies) {
        await browser.setCookie(cookie);
      }
    }

    if (session.url) {
      await browser.goto(session.url);
    }

    console.log(chalk.green(`Session loaded: ${name}`));
  });

program
  .command('session-list')
  .description('List all saved sessions')
  .action(async () => {
    const sessions = await sessionManager.list();

    if (sessions.length === 0) {
      console.log('No saved sessions');
      return;
    }

    console.log(chalk.bold('\nSaved Sessions:\n'));
    sessions.forEach(s => {
      console.log(`  ${chalk.cyan(s.name)} - ${s.url} (${s.savedAt})`);
    });
    console.log('');
  });

// If no command specified, run interactive mode
if (process.argv.length === 2) {
  interactiveMode();
} else {
  program.parse();
}
