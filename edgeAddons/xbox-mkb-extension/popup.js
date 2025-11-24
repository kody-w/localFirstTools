document.addEventListener('DOMContentLoaded', () => {
  const sensitivitySlider = document.getElementById('sensitivity');
  const sensitivityValue = document.getElementById('sensitivityValue');
  const invertYCheckbox = document.getElementById('invertY');
  const keybindGrid = document.getElementById('keybindGrid');
  const saveBtn = document.getElementById('saveBtn');
  const resetBtn = document.getElementById('resetBtn');

  // Load current config
  chrome.storage.sync.get(['mkbConfig'], (result) => {
    if (result.mkbConfig) {
      sensitivitySlider.value = result.mkbConfig.sensitivity || 1.0;
      sensitivityValue.textContent = sensitivitySlider.value;
      invertYCheckbox.checked = result.mkbConfig.invertY || false;
      displayKeybindings(result.mkbConfig.keyBindings);
    }
  });

  // Update sensitivity display
  sensitivitySlider.addEventListener('input', () => {
    sensitivityValue.textContent = sensitivitySlider.value;
  });

  // Display keybindings
  function displayKeybindings(keyBindings) {
    keybindGrid.innerHTML = '';
    
    const friendlyNames = {
      'w': 'W',
      's': 'S',
      'a': 'A',
      'd': 'D',
      ' ': 'Space',
      'enter': 'Enter',
      'shift': 'Shift',
      'e': 'E',
      'r': 'R',
      'q': 'Q',
      'f': 'F',
      'c': 'C',
      'v': 'V',
      'mouse0': 'Left Click',
      'mouse2': 'Right Click',
      'arrowup': '↑',
      'arrowdown': '↓',
      'arrowleft': '←',
      'arrowright': '→',
      'escape': 'ESC',
      'tab': 'Tab'
    };
    
    const actionNames = {
      'LS_UP': 'Move Forward',
      'LS_DOWN': 'Move Backward',
      'LS_LEFT': 'Move Left',
      'LS_RIGHT': 'Move Right',
      'A': 'A Button (Select/Jump)',
      'B': 'B Button (Back/Crouch)',
      'X': 'X Button (Interact)',
      'Y': 'Y Button (Reload)',
      'RT': 'Right Trigger (Fire)',
      'LT': 'Left Trigger (Aim)',
      'RB': 'Right Bumper',
      'LB': 'Left Bumper',
      'DPAD_UP': 'D-Pad Up',
      'DPAD_DOWN': 'D-Pad Down',
      'DPAD_LEFT': 'D-Pad Left',
      'DPAD_RIGHT': 'D-Pad Right',
      'MENU': 'Menu',
      'VIEW': 'View',
      'LS': 'Left Stick Click',
      'RS': 'Right Stick Click'
    };
    
    for (const [key, action] of Object.entries(keyBindings)) {
      const item = document.createElement('div');
      item.className = 'keybind-item';
      item.innerHTML = `
        <span class="key">${friendlyNames[key] || key}</span>
        <span class="action">${actionNames[action] || action}</span>
      `;
      keybindGrid.appendChild(item);
    }
  }

  // Save settings
  saveBtn.addEventListener('click', async () => {
    const config = {
      sensitivity: parseFloat(sensitivitySlider.value),
      invertY: invertYCheckbox.checked,
      keyBindings: {} // This would be populated from current keybindings
    };
    
    // Get current keybindings
    const result = await chrome.storage.sync.get(['mkbConfig']);
    if (result.mkbConfig) {
      config.keyBindings = result.mkbConfig.keyBindings;
    }
    
    // Save to storage
    await chrome.storage.sync.set({ mkbConfig: config });
    
    // Notify content script
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab) {
      chrome.tabs.sendMessage(tab.id, { action: 'updateConfig', config });
    }
    
    // Visual feedback
    saveBtn.textContent = 'Saved!';
    setTimeout(() => {
      saveBtn.textContent = 'Save Settings';
    }, 2000);
  });

  // Reset to default
  resetBtn.addEventListener('click', async () => {
    const defaultConfig = {
      sensitivity: 1.0,
      invertY: false,
      keyBindings: {
        'w': 'LS_UP',
        's': 'LS_DOWN',
        'a': 'LS_LEFT',
        'd': 'LS_RIGHT',
        ' ': 'A',
        'enter': 'A',
        'shift': 'B',
        'e': 'X',
        'r': 'Y',
        'mouse0': 'RT',
        'mouse2': 'LT',
        'q': 'LB',
        'f': 'RB',
        'arrowup': 'DPAD_UP',
        'arrowdown': 'DPAD_DOWN',
        'arrowleft': 'DPAD_LEFT',
        'arrowright': 'DPAD_RIGHT',
        'escape': 'MENU',
        'tab': 'VIEW',
        'c': 'LS',
        'v': 'RS'
      }
    };
    
    await chrome.storage.sync.set({ mkbConfig: defaultConfig });
    
    // Update UI
    sensitivitySlider.value = defaultConfig.sensitivity;
    sensitivityValue.textContent = defaultConfig.sensitivity;
    invertYCheckbox.checked = defaultConfig.invertY;
    displayKeybindings(defaultConfig.keyBindings);
    
    // Notify content script
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab) {
      chrome.tabs.sendMessage(tab.id, { action: 'updateConfig', config: defaultConfig });
    }
    
    // Visual feedback
    resetBtn.textContent = 'Reset!';
    setTimeout(() => {
      resetBtn.textContent = 'Reset to Default';
    }, 2000);
  });
});
