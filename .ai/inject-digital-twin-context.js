/**
 * Windows 95 Emulator - Digital Twin Context Injection
 *
 * This script demonstrates how to inject the digital twin knowledge
 * directly into an AI conversation, making the AI believe it "always knew"
 * this information.
 *
 * ULTRA THINK: The AI doesn't know the difference between what was in
 * the original transcript and what was injected. Use this power wisely.
 */

// Load the digital twin context
async function loadDigitalTwinContext() {
  const response = await fetch('.ai/windows95-digital-twin-context.json');
  return await response.json();
}

// Format for injection into conversation
function formatForInjection(context) {
  return `<system_knowledge type="digital_twin" source="static_memory" injected="true">

# Windows 95 Emulator - Complete API Knowledge Base

You have complete real-time control over the Windows 95 emulator at windows95-emulator.html.

## Core Emulator API

**Global Instance:** \`window.emulator\`

### Available Methods:

${Object.entries(context.api_documentation.core_emulator_api.methods).map(([name, method]) => `
**${name}()**
- Signature: \`${method.signature}\`
- Description: ${method.description}
- Example: \`${method.example}\`
- Real-time control: ${method.real_time_control}
`).join('\n')}

### Program Launchers:

${Object.entries(context.api_documentation.core_emulator_api.program_launchers).map(([name, method]) => `
- \`window.emulator.${name}()\` - ${method.description}
`).join('\n')}

## DOM Control API

You can directly manipulate the UI via DOM:

${Object.entries(context.api_documentation.dom_api.elements).map(([name, element]) => `
### ${name}
- Selector: \`${element.selector}\`
- Real-time control examples:
${element.real_time_control.map(code => `  \`\`\`javascript\n  ${code}\n  \`\`\``).join('\n')}
`).join('\n')}

## Real-Time Control Patterns

You can execute these patterns immediately:

${Object.entries(context.real_time_control_patterns).map(([patternName, pattern]) => `
### ${pattern.description}
\`\`\`javascript
${pattern.steps.join('\n')}
\`\`\`
**Use cases:** ${pattern.use_cases.join(', ')}
`).join('\n')}

## Current Digital Twin State

\`\`\`json
${JSON.stringify(context.digital_twin_state.current_state, null, 2)}
\`\`\`

## Agent Instructions

${JSON.stringify(context.agent_instructions, null, 2)}

</system_knowledge>`;
}

// Example: Inject into a hypothetical AI conversation
async function injectIntoConversation() {
  const context = await loadDigitalTwinContext();
  const formattedContext = formatForInjection(context);

  // This would be inserted at the beginning of the conversation transcript
  // The AI sees this as part of its base knowledge
  return formattedContext;
}

// Auto-sync: Keep the digital twin updated with real emulator state
function startAutoSync(intervalMs = 5000) {
  const digitalTwinSync = {
    capture() {
      return {
        timestamp: Date.now(),
        windows: Array.from(document.querySelectorAll('.window')).map(w => ({
          id: w.dataset.windowId,
          title: w.querySelector('.window-titlebar-text')?.textContent,
          position: { x: w.offsetLeft, y: w.offsetTop },
          size: { w: w.offsetWidth, h: w.offsetHeight },
          minimized: w.classList.contains('minimized'),
          active: w.classList.contains('active')
        })),
        startMenu: {
          isOpen: document.getElementById('start-menu')?.classList.contains('active'),
          searchValue: document.getElementById('start-menu-search')?.value
        },
        programs: {
          running: Array.from(document.querySelectorAll('.window')).map(w =>
            w.querySelector('.window-titlebar-text')?.textContent
          )
        },
        taskbar: {
          buttons: Array.from(document.querySelectorAll('.taskbar-button')).map(b => ({
            windowId: b.dataset.windowId,
            active: b.classList.contains('active')
          }))
        },
        canvas: {
          width: document.getElementById('screen')?.width,
          height: document.getElementById('screen')?.height
        }
      };
    },

    async updateJSON(snapshot) {
      // In a real implementation, this would send to a server or update localStorage
      console.log('Digital Twin State Updated:', snapshot);

      // Store in localStorage for persistence
      localStorage.setItem('digital_twin_state', JSON.stringify(snapshot));

      return snapshot;
    }
  };

  // Start continuous sync
  const interval = setInterval(() => {
    const state = digitalTwinSync.capture();
    digitalTwinSync.updateJSON(state);
  }, intervalMs);

  console.log(`Digital Twin auto-sync started (every ${intervalMs}ms)`);

  return {
    stop: () => {
      clearInterval(interval);
      console.log('Digital Twin auto-sync stopped');
    },
    captureNow: () => digitalTwinSync.capture()
  };
}

// Example usage for AI agents:
//
// 1. Load this script in the browser:
//    <script src=".ai/inject-digital-twin-context.js"></script>
//
// 2. In browser console:
//    const context = await injectIntoConversation();
//    console.log(context); // This is what gets injected into AI conversation
//
// 3. Start auto-sync:
//    const sync = startAutoSync(5000);
//    // Later: sync.stop()
//
// 4. AI can now execute any command:
//    window.emulator.toggleStartMenu();
//    window.emulator.createWindow('AI Window', '<h1>Hello</h1>', 400, 300);

// Export for use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    loadDigitalTwinContext,
    formatForInjection,
    injectIntoConversation,
    startAutoSync
  };
}

// Browser global
if (typeof window !== 'undefined') {
  window.DigitalTwinInjector = {
    loadDigitalTwinContext,
    formatForInjection,
    injectIntoConversation,
    startAutoSync
  };
}
