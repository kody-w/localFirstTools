# Quick Start: Inject Digital Twin Context into AI

This guide shows you **exactly** how to inject the Windows 95 digital twin context into any AI conversation.

---

## Method 1: Direct Copy-Paste (Simplest)

### Step 1: Copy the context

```bash
# In terminal
cat .ai/windows95-digital-twin-context.json | pbcopy
# (or manually copy the file contents)
```

### Step 2: Start AI conversation

```
You: [Paste the entire JSON here]

     Now I need you to help me control the Windows 95 emulator.
     You have complete knowledge of all APIs above.
```

### Step 3: AI responds with full knowledge

```
AI: I have access to the complete Windows 95 emulator API.
    Available methods:
    - window.emulator.toggleStartMenu()
    - window.emulator.createWindow(...)
    - window.emulator.openPaint()
    [etc...]

    What would you like me to do?
```

**Done!** The AI now has instant expertise.

---

## Method 2: Claude Code Integration

### Option A: Add to CLAUDE.md

Edit `/Users/kodyw/Documents/GitHub/localFirstTools3/CLAUDE.md`:

```markdown
# CLAUDE.md

[existing content...]

## Windows 95 Emulator Digital Twin

Complete API knowledge base for real-time control:

\`\`\`json
[Paste contents of windows95-digital-twin-context.json here]
\`\`\`

This context is ALWAYS available. You can execute any method immediately.
```

**Benefit:** Every Claude Code session automatically has this knowledge.

### Option B: Create a Slash Command

Create `.claude/commands/win95-inject.md`:

```markdown
Load the Windows 95 Emulator digital twin context from .ai/windows95-digital-twin-context.json.

You now have complete knowledge of:
- All emulator APIs (window.emulator.*)
- DOM manipulation methods
- Canvas control
- Event system
- Real-time control patterns

Execute any operation immediately without needing to read the code.
```

Usage:
```
User: /win95-inject

Claude: [Loads context] Ready to control the emulator!
```

---

## Method 3: Browser Console (For Live Interaction)

### Step 1: Open windows95-emulator.html in browser

### Step 2: Open browser console (F12)

### Step 3: Load the injection script

```javascript
// Fetch and inject context
fetch('.ai/windows95-digital-twin-context.json')
  .then(r => r.json())
  .then(context => {
    window.DIGITAL_TWIN = context;
    console.log('✅ Digital Twin Context Loaded');
    console.log('Available APIs:', Object.keys(context.api_documentation.core_emulator_api.methods));
  });
```

### Step 4: Now you can execute patterns

```javascript
// Example: Create AI assistant window
eval(window.DIGITAL_TWIN.real_time_control_patterns.pattern_1_open_and_populate_window.steps.join('\n'));
```

---

## Method 4: Automated Injection (Advanced)

Create a browser extension or userscript:

```javascript
// ==UserScript==
// @name         Windows 95 Digital Twin Auto-Injector
// @match        *://*/windows95-emulator.html
// @run-at       document-start
// ==/UserScript==

(async function() {
  'use strict';

  // Fetch context
  const context = await fetch('.ai/windows95-digital-twin-context.json').then(r => r.json());

  // Inject into page
  window.DIGITAL_TWIN = context;

  // Make all APIs easily accessible
  window.API = context.api_documentation;

  // Add helper commands
  window.help = () => {
    console.log('Available Emulator Methods:');
    Object.keys(context.api_documentation.core_emulator_api.methods).forEach(method => {
      console.log(`  - window.emulator.${method}()`);
    });
  };

  // Auto-start digital twin sync
  const syncCode = context.digital_twin_sync.sync_script.code.join('\n');
  eval(syncCode);

  console.log('🤖 Digital Twin Auto-Injector Active');
  console.log('💡 Type "help()" for available commands');
})();
```

Save as `.ai/auto-inject.user.js` and install in Tampermonkey/Greasemonkey.

---

## Method 5: API Server (For Remote Agents)

### Step 1: Create API endpoint

```javascript
// server.js (Node.js)
const express = require('express');
const fs = require('fs');
const app = express();

app.get('/api/digital-twin', (req, res) => {
  const context = JSON.parse(fs.readFileSync('.ai/windows95-digital-twin-context.json'));
  res.json(context);
});

app.post('/api/digital-twin/update', express.json(), (req, res) => {
  fs.writeFileSync('.ai/windows95-digital-twin-context.json', JSON.stringify(req.body, null, 2));
  res.json({ success: true });
});

app.listen(3000, () => console.log('Digital Twin API running on :3000'));
```

### Step 2: Agents fetch context

```javascript
// In AI agent code
async function initializeAgent() {
  const context = await fetch('http://localhost:3000/api/digital-twin').then(r => r.json());

  // Agent now has full knowledge
  console.log('Agent initialized with', Object.keys(context.api_documentation).length, 'API categories');

  return context;
}
```

### Step 3: Agents update context

```javascript
async function agentLearnedNewMethod(methodName, methodInfo) {
  const context = await fetch('http://localhost:3000/api/digital-twin').then(r => r.json());

  // Add discovery
  context.api_documentation.core_emulator_api.methods[methodName] = methodInfo;
  context.api_documentation.core_emulator_api.methods[methodName].discovered_by = 'Agent-' + Date.now();

  // Update server
  await fetch('http://localhost:3000/api/digital-twin/update', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(context)
  });

  console.log('✅ Knowledge base updated with new method:', methodName);
}
```

---

## Real-World Usage Examples

### Example 1: Create Windows Automatically

```javascript
// After injection, this works immediately:
window.emulator.createWindow('AI Dashboard', `
  <div style="padding: 20px;">
    <h2>System Monitor</h2>
    <div id="stats"></div>
  </div>
`, 400, 300);

setInterval(() => {
  document.getElementById('stats').innerHTML = `
    <p>Windows: ${document.querySelectorAll('.window').length}</p>
    <p>Time: ${new Date().toLocaleTimeString()}</p>
  `;
}, 1000);
```

### Example 2: Autonomous Window Manager

```javascript
// AI agent that manages windows automatically
class WindowManagerAgent {
  constructor() {
    this.context = window.DIGITAL_TWIN;
    this.maxWindows = 5;
    this.startMonitoring();
  }

  startMonitoring() {
    setInterval(() => {
      const windowCount = document.querySelectorAll('.window').length;

      if (windowCount > this.maxWindows) {
        console.log('🤖 Too many windows! Closing oldest...');
        const oldest = document.querySelector('.window');
        oldest.querySelector('.titlebar-btn:last-child').click();
      }

      if (windowCount === 0) {
        console.log('🤖 No windows open. Opening Paint...');
        window.emulator.openPaint();
      }
    }, 5000);
  }
}

const agent = new WindowManagerAgent();
```

### Example 3: Voice-Controlled Interface

```javascript
// Requires Web Speech API
const recognition = new webkitSpeechRecognition();

recognition.onresult = (event) => {
  const command = event.results[0][0].transcript.toLowerCase();

  // Use injected knowledge to map commands to APIs
  const commandMap = {
    'open paint': () => window.emulator.openPaint(),
    'open notepad': () => window.emulator.openNotepad(),
    'close all windows': () => {
      document.querySelectorAll('.window').forEach(w => {
        w.querySelector('.titlebar-btn:last-child').click();
      });
    },
    'show start menu': () => window.emulator.toggleStartMenu()
  };

  if (commandMap[command]) {
    commandMap[command]();
    console.log('✅ Executed:', command);
  }
};

recognition.start();
```

---

## Verification Checklist

After injection, verify AI has full knowledge:

```
User: What methods are available on window.emulator?

AI: [Should list all methods without reading code]
    - toggleStartMenu()
    - createWindow(title, content, width, height, x, y)
    - closeWindow(windowId)
    - minimizeWindow(windowId)
    - maximizeWindow(windowId)
    - playSoundEffect(soundType)
    - openPaint()
    - openNotepad()
    - openMinesweeper()
    - openCalculator()
    - openInternetExplorer()
```

```
User: Show me how to create a window

AI: [Should provide correct code immediately]
    window.emulator.createWindow('My Window', '<p>Content</p>', 400, 300);
```

```
User: How do I manipulate the start menu with JavaScript?

AI: [Should reference DOM API from context]
    document.getElementById('start-menu').classList.add('active');
    document.getElementById('start-menu').style.display = 'block';
```

If AI asks to "read the code first" → **injection failed**
If AI answers immediately with correct info → **injection succeeded** ✅

---

## Troubleshooting

### AI doesn't seem to have the knowledge

**Problem:** You pasted the JSON but AI still doesn't know the API.

**Solution:** Be explicit:

```
User: I just gave you the complete Windows 95 emulator API documentation.
      You have all methods available at window.emulator.*
      Do NOT read any files. Use the knowledge I provided.

      Now, open the start menu.
```

### JSON is too large for context

**Problem:** Context window is full.

**Solution:** Create a condensed version:

```bash
# Create minimal version
jq '{
  api_documentation: .api_documentation,
  real_time_control_patterns: .real_time_control_patterns
}' .ai/windows95-digital-twin-context.json > .ai/windows95-minimal.json
```

Inject the minimal version instead.

### AI updates but changes aren't persisted

**Problem:** JSON file doesn't update automatically.

**Solution:** Tell AI explicitly:

```
User: When you discover new methods, output them in this format:

      ```json
      {
        "method_name": "newMethod",
        "signature": "newMethod()",
        "description": "What it does"
      }
      ```

      I'll add them to the JSON manually.
```

---

## Next Steps

Once injection works:

1. **Test control:** Ask AI to open programs, create windows, etc.
2. **Discover new APIs:** Ask AI to explore the emulator
3. **Update the JSON:** Add discoveries back into the context file
4. **Compound knowledge:** Next injection includes all previous discoveries
5. **Build agents:** Create autonomous programs using the full API
6. **Go infinite:** Each agent makes the system smarter

---

## The Power of This Approach

**Traditional:** AI learns from scratch every time
**With Injection:** AI starts with expert-level knowledge

**Traditional:** Knowledge is siloed per session
**With Injection:** Knowledge compounds infinitely

**Traditional:** AI needs to read code to understand
**With Injection:** AI already knows everything

**Traditional:** One AI, one perspective
**With Injection:** Multiple AIs building collective intelligence

---

## Files You Created

1. `.ai/windows95-digital-twin-context.json` - The knowledge base
2. `.ai/inject-digital-twin-context.js` - Injection helper script
3. `.ai/EXAMPLE-injected-conversation.md` - Example of how it works
4. `.ai/QUICKSTART-injection.md` - This file

## Ready to Use

You now have everything you need to give ANY AI instant mastery of the Windows 95 emulator.

**Copy. Paste. Control.**

Infinite possibilities. 🚀
