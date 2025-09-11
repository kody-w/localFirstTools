#!/bin/bash

# Xbox Mouse & Keyboard Chrome/Edge Extension Setup Script
# This script creates a complete extension ready to import

echo "🎮 Xbox Mouse & Keyboard Extension Setup"
echo "======================================"

# Create extension directory
EXTENSION_DIR="xbox-mkb-extension"
echo "Creating extension directory: $EXTENSION_DIR"
mkdir -p "$EXTENSION_DIR"
cd "$EXTENSION_DIR"

# Create manifest.json
echo "Creating manifest.json..."
cat > manifest.json << 'EOF'
{
  "manifest_version": 3,
  "name": "Xbox Mouse & Keyboard Support",
  "version": "1.0.0",
  "description": "Adds mouse and keyboard support for Xbox Cloud Gaming",
  "permissions": [
    "storage",
    "activeTab"
  ],
  "host_permissions": [
    "https://www.xbox.com/*",
    "https://gamepass.com/*"
  ],
  "content_scripts": [
    {
      "matches": [
        "https://www.xbox.com/*/play*",
        "https://gamepass.com/*/play*"
      ],
      "js": ["content.js"],
      "run_at": "document_start"
    }
  ],
  "background": {
    "service_worker": "background.js"
  },
  "action": {
    "default_popup": "popup.html",
    "default_icon": {
      "16": "icon16.png",
      "48": "icon48.png",
      "128": "icon128.png"
    }
  }
}
EOF

# Create content.js
echo "Creating content.js..."
cat > content.js << 'EOF'
(() => {
  let config = {
    sensitivity: 1.0,
    invertY: false,
    keyBindings: {
      // Movement
      'w': 'LS_UP',
      's': 'LS_DOWN',
      'a': 'LS_LEFT',
      'd': 'LS_RIGHT',
      
      // Actions
      ' ': 'A', // Space - Jump/Select
      'enter': 'A', // Enter - Also maps to A for menus
      'shift': 'B', // Shift - Crouch/Cancel
      'e': 'X', // E - Interact
      'r': 'Y', // R - Reload
      
      // Triggers & Bumpers
      'mouse0': 'RT', // Left Click - Fire
      'mouse2': 'LT', // Right Click - Aim
      'q': 'LB', // Q - Left Bumper
      'f': 'RB', // F - Right Bumper
      
      // D-Pad
      'arrowup': 'DPAD_UP',
      'arrowdown': 'DPAD_DOWN',
      'arrowleft': 'DPAD_LEFT',
      'arrowright': 'DPAD_RIGHT',
      
      // Menu
      'escape': 'MENU',
      'tab': 'VIEW',
      
      // Sticks
      'c': 'LS', // Left Stick Click
      'v': 'RS', // Right Stick Click
    }
  };

  // Virtual gamepad state
  const gamepadState = {
    buttons: new Array(17).fill(false),
    axes: [0, 0, 0, 0], // [LX, LY, RX, RY]
    timestamp: performance.now()
  };

  // Button mapping
  const buttonMap = {
    'A': 0,
    'B': 1,
    'X': 2,
    'Y': 3,
    'LB': 4,
    'RB': 5,
    'LT': 6,
    'RT': 7,
    'VIEW': 8,
    'MENU': 9,
    'LS': 10,
    'RS': 11,
    'DPAD_UP': 12,
    'DPAD_DOWN': 13,
    'DPAD_LEFT': 14,
    'DPAD_RIGHT': 15,
    'XBOX': 16
  };

  // Movement tracking
  const movement = {
    forward: false,
    backward: false,
    left: false,
    right: false
  };

  // Mouse tracking
  let mouseX = 0, mouseY = 0;
  let isPointerLocked = false;
  let isEnabled = false; // Track if extension is enabled

  // Load config from storage
  chrome.storage.sync.get(['mkbConfig'], (result) => {
    if (result.mkbConfig) {
      config = { ...config, ...result.mkbConfig };
    }
  });

  // Wait for page to be ready
  let gamepadOverrideApplied = false;
  
  function applyGamepadOverride() {
    if (gamepadOverrideApplied) return;
    
    const originalGetGamepads = navigator.getGamepads.bind(navigator);
    
    navigator.getGamepads = function() {
      const gamepads = originalGetGamepads();
      if (isEnabled) {
        // Create virtual gamepad
        const virtualGamepad = {
          id: 'Xbox Mouse & Keyboard Virtual Controller',
          index: 0,
          connected: true,
          timestamp: gamepadState.timestamp,
          mapping: 'standard',
          axes: [...gamepadState.axes],
          buttons: gamepadState.buttons.map(pressed => ({
            pressed,
            touched: pressed,
            value: pressed ? 1.0 : 0.0
          }))
        };
        
        // Replace first null/undefined gamepad or add as first
        if (gamepads.length === 0 || !gamepads[0]) {
          gamepads[0] = virtualGamepad;
        } else {
          // Find first empty slot
          for (let i = 0; i < 4; i++) {
            if (!gamepads[i]) {
              gamepads[i] = virtualGamepad;
              break;
            }
          }
        }
      }
      return gamepads;
    };
    
    gamepadOverrideApplied = true;
  }

  // Apply override immediately and on various page events
  applyGamepadOverride();
  document.addEventListener('DOMContentLoaded', applyGamepadOverride);
  window.addEventListener('load', applyGamepadOverride);

  // Also dispatch gamepad connected event
  function emitGamepadConnected() {
    if (isEnabled) {
      window.dispatchEvent(new Event('gamepadconnected'));
    }
  }

  // Handle keyboard input
  document.addEventListener('keydown', (e) => {
    if (!isEnabled) return;
    
    const key = e.key.toLowerCase();
    const binding = config.keyBindings[key];
    
    if (binding) {
      e.preventDefault();
      e.stopPropagation();
      
      // Handle movement keys
      if (binding === 'LS_UP') movement.forward = true;
      else if (binding === 'LS_DOWN') movement.backward = true;
      else if (binding === 'LS_LEFT') movement.left = true;
      else if (binding === 'LS_RIGHT') movement.right = true;
      else {
        // Handle button presses
        const buttonIndex = buttonMap[binding];
        if (buttonIndex !== undefined) {
          gamepadState.buttons[buttonIndex] = true;
        }
      }
      
      updateMovementAxes();
      gamepadState.timestamp = performance.now();
    }
  }, true); // Use capture phase

  document.addEventListener('keyup', (e) => {
    if (!isEnabled) return;
    
    const key = e.key.toLowerCase();
    const binding = config.keyBindings[key];
    
    if (binding) {
      e.preventDefault();
      e.stopPropagation();
      
      // Handle movement keys
      if (binding === 'LS_UP') movement.forward = false;
      else if (binding === 'LS_DOWN') movement.backward = false;
      else if (binding === 'LS_LEFT') movement.left = false;
      else if (binding === 'LS_RIGHT') movement.right = false;
      else {
        // Handle button releases
        const buttonIndex = buttonMap[binding];
        if (buttonIndex !== undefined) {
          gamepadState.buttons[buttonIndex] = false;
        }
      }
      
      updateMovementAxes();
      gamepadState.timestamp = performance.now();
    }
  }, true); // Use capture phase

  // Handle mouse input
  document.addEventListener('mousedown', (e) => {
    if (!isEnabled || !isPointerLocked) return;
    
    const binding = config.keyBindings[`mouse${e.button}`];
    if (binding) {
      e.preventDefault();
      const buttonIndex = buttonMap[binding];
      if (buttonIndex !== undefined) {
        gamepadState.buttons[buttonIndex] = true;
        gamepadState.timestamp = performance.now();
      }
    }
  });

  document.addEventListener('mouseup', (e) => {
    if (!isEnabled || !isPointerLocked) return;
    
    const binding = config.keyBindings[`mouse${e.button}`];
    if (binding) {
      e.preventDefault();
      const buttonIndex = buttonMap[binding];
      if (buttonIndex !== undefined) {
        gamepadState.buttons[buttonIndex] = false;
        gamepadState.timestamp = performance.now();
      }
    }
  });

  document.addEventListener('mousemove', (e) => {
    if (!isEnabled || !isPointerLocked) return;
    
    // Update right stick based on mouse movement
    mouseX += e.movementX * config.sensitivity * 0.01;
    mouseY += e.movementY * config.sensitivity * 0.01 * (config.invertY ? -1 : 1);
    
    // Clamp values
    mouseX = Math.max(-1, Math.min(1, mouseX));
    mouseY = Math.max(-1, Math.min(1, mouseY));
    
    // Apply to right stick
    gamepadState.axes[2] = mouseX;
    gamepadState.axes[3] = mouseY;
    
    // Decay over time for smooth camera movement
    setTimeout(() => {
      mouseX *= 0.8;
      mouseY *= 0.8;
      gamepadState.axes[2] = mouseX;
      gamepadState.axes[3] = mouseY;
    }, 50);
    
    gamepadState.timestamp = performance.now();
  });

  // Toggle extension with keyboard shortcut (Ctrl+Shift+X)
  document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && e.key === 'X') {
      isEnabled = !isEnabled;
      if (isEnabled) {
        emitGamepadConnected();
        showNotification('Mouse & Keyboard: Enabled');
      } else {
        showNotification('Mouse & Keyboard: Disabled');
        // Reset state
        gamepadState.buttons.fill(false);
        gamepadState.axes.fill(0);
        Object.keys(movement).forEach(key => movement[key] = false);
        mouseX = 0;
        mouseY = 0;
      }
      updateIndicator();
    }
  });

  // Pointer lock handling - only for mouse control
  document.addEventListener('click', async (e) => {
    if (!isEnabled) return;
    
    const gameCanvas = document.querySelector('canvas');
    if (gameCanvas && gameCanvas.contains(e.target)) {
      try {
        await gameCanvas.requestPointerLock();
      } catch (err) {
        console.error('Pointer lock failed:', err);
      }
    }
  });

  document.addEventListener('pointerlockchange', () => {
    isPointerLocked = document.pointerLockElement !== null;
    updateIndicator();
  });

  // Update movement axes based on WASD
  function updateMovementAxes() {
    let x = 0, y = 0;
    
    if (movement.left) x -= 1;
    if (movement.right) x += 1;
    if (movement.forward) y -= 1;
    if (movement.backward) y += 1;
    
    // Normalize diagonal movement
    if (x !== 0 && y !== 0) {
      const magnitude = Math.sqrt(x * x + y * y);
      x /= magnitude;
      y /= magnitude;
    }
    
    gamepadState.axes[0] = x;
    gamepadState.axes[1] = y;
  }

  // Listen for config updates
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'updateConfig') {
      config = { ...config, ...request.config };
      sendResponse({ success: true });
    }
  });

  // Inject CSS for visual feedback
  const style = document.createElement('style');
  style.textContent = `
    .mkb-indicator {
      position: fixed;
      top: 10px;
      right: 10px;
      background: rgba(0, 0, 0, 0.8);
      color: white;
      padding: 10px;
      border-radius: 5px;
      font-family: Arial, sans-serif;
      font-size: 14px;
      z-index: 10000;
      pointer-events: none;
    }
    .mkb-indicator.active {
      background: rgba(0, 200, 0, 0.8);
    }
    .mkb-indicator.disabled {
      background: rgba(100, 100, 100, 0.8);
    }
    .mkb-notification {
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: rgba(0, 0, 0, 0.9);
      color: white;
      padding: 20px;
      border-radius: 10px;
      font-family: Arial, sans-serif;
      font-size: 18px;
      z-index: 10001;
      pointer-events: none;
      animation: fadeInOut 2s ease-in-out;
    }
    @keyframes fadeInOut {
      0% { opacity: 0; }
      20% { opacity: 1; }
      80% { opacity: 1; }
      100% { opacity: 0; }
    }
  `;
  document.head.appendChild(style);

  // Add visual indicator
  const indicator = document.createElement('div');
  indicator.className = 'mkb-indicator disabled';
  indicator.textContent = 'M&K: Press Ctrl+Shift+X to enable';
  document.body.appendChild(indicator);

  // Update indicator
  function updateIndicator() {
    if (!isEnabled) {
      indicator.className = 'mkb-indicator disabled';
      indicator.textContent = 'M&K: Press Ctrl+Shift+X to enable';
    } else if (isPointerLocked) {
      indicator.className = 'mkb-indicator active';
      indicator.textContent = 'M&K: Active (ESC to release mouse)';
    } else {
      indicator.className = 'mkb-indicator';
      indicator.textContent = 'M&K: Enabled (Click game for mouse)';
    }
  }

  // Show notification
  function showNotification(text) {
    const notification = document.createElement('div');
    notification.className = 'mkb-notification';
    notification.textContent = text;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 2000);
  }

  // Initialize
  updateIndicator();

})();
EOF

# Create background.js
echo "Creating background.js..."
cat > background.js << 'EOF'
chrome.runtime.onInstalled.addListener(() => {
  // Set default config
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
  
  chrome.storage.sync.set({ mkbConfig: defaultConfig });
});
EOF

# Create popup.html
echo "Creating popup.html..."
cat > popup.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {
      width: 400px;
      padding: 15px;
      font-family: Arial, sans-serif;
    }
    h1 {
      font-size: 18px;
      margin-bottom: 15px;
    }
    .info-box {
      background: #f0f0f0;
      padding: 10px;
      border-radius: 5px;
      margin-bottom: 15px;
    }
    .info-box p {
      margin: 5px 0;
      font-size: 14px;
    }
    .control-group {
      margin-bottom: 15px;
    }
    label {
      display: block;
      margin-bottom: 5px;
      font-weight: bold;
    }
    input[type="range"] {
      width: 100%;
    }
    .sensitivity-value {
      display: inline-block;
      width: 40px;
      text-align: right;
    }
    button {
      background: #0078d4;
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 4px;
      cursor: pointer;
      font-size: 14px;
    }
    button:hover {
      background: #106ebe;
    }
    .keybind-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      max-height: 300px;
      overflow-y: auto;
      border: 1px solid #ddd;
      padding: 10px;
      border-radius: 4px;
    }
    .keybind-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 5px;
      background: #f5f5f5;
      border-radius: 3px;
    }
    .key {
      font-weight: bold;
      color: #0078d4;
    }
    .action {
      color: #666;
      font-size: 12px;
    }
    .shortcut {
      background: #0078d4;
      color: white;
      padding: 2px 6px;
      border-radius: 3px;
      font-family: monospace;
      font-size: 12px;
    }
  </style>
</head>
<body>
  <h1>Xbox Mouse & Keyboard Settings</h1>
  
  <div class="info-box">
    <p><strong>Toggle Extension:</strong> <span class="shortcut">Ctrl+Shift+X</span></p>
    <p>Press <strong>Space</strong> or <strong>Enter</strong> to start games</p>
  </div>
  
  <div class="control-group">
    <label>Mouse Sensitivity: <span class="sensitivity-value" id="sensitivityValue">1.0</span></label>
    <input type="range" id="sensitivity" min="0.1" max="3" step="0.1" value="1.0">
  </div>
  
  <div class="control-group">
    <label>
      <input type="checkbox" id="invertY"> Invert Y-axis
    </label>
  </div>
  
  <div class="control-group">
    <label>Key Bindings:</label>
    <div class="keybind-grid" id="keybindGrid"></div>
  </div>
  
  <button id="saveBtn">Save Settings</button>
  <button id="resetBtn">Reset to Default</button>
  
  <script src="popup.js"></script>
</body>
</html>
EOF

# Create popup.js
echo "Creating popup.js..."
cat > popup.js << 'EOF'
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
EOF

# Create icons using ImageMagick if available, otherwise create placeholder files
echo "Creating icons..."
if command -v convert &> /dev/null; then
    # Create icons with ImageMagick
    echo "ImageMagick found, creating proper icons..."
    
    # Create a simple gamepad icon
    convert -size 128x128 xc:transparent \
        -fill '#0078d4' \
        -draw "roundrectangle 20,40 108,88 10,10" \
        -fill '#106ebe' \
        -draw "circle 40,64 48,64" \
        -draw "circle 88,64 96,64" \
        -fill white \
        -draw "rectangle 36,60 44,68" \
        -draw "rectangle 40,56 40,72" \
        -draw "circle 88,58 90,58" \
        -draw "circle 94,64 96,64" \
        -draw "circle 88,70 90,70" \
        -draw "circle 82,64 84,64" \
        icon128.png
    
    # Resize for smaller versions
    convert icon128.png -resize 48x48 icon48.png
    convert icon128.png -resize 16x16 icon16.png
else
    echo "ImageMagick not found, creating placeholder icons..."
    # Create simple placeholder files
    echo "PNG" > icon16.png
    echo "PNG" > icon48.png
    echo "PNG" > icon128.png
fi

# Create README
echo "Creating README.md..."
cat > README.md << 'EOF'
# Xbox Mouse & Keyboard Support Extension

This extension adds mouse and keyboard support for Xbox Cloud Gaming on PC.

## Installation

1. Open Microsoft Edge
2. Navigate to `edge://extensions/`
3. Enable "Developer mode"
4. Click "Load unpacked"
5. Select this folder

## Usage

1. Go to Xbox Cloud Gaming (xbox.com/play)
2. Press **Ctrl+Shift+X** to enable the extension
3. For game menus: Use keyboard (Space/Enter to select)
4. For gameplay: Click on the game canvas to enable mouse control
5. Press ESC to release mouse control

## Important Notes

- **Enable First**: Press Ctrl+Shift+X to toggle the extension on/off
- **Menu Navigation**: Space and Enter both work as the A button
- **Mouse Control**: Only activates after clicking the game canvas

## Default Controls

- **Movement**: WASD
- **Camera**: Mouse (when pointer locked)
- **Select/Jump**: Space or Enter
- **Back/Crouch**: Shift
- **Interact**: E
- **Reload**: R
- **Fire**: Left Click
- **Aim**: Right Click
- **D-Pad**: Arrow Keys
- **Menu**: ESC
- **View**: Tab

## Settings

Click the extension icon to adjust:
- Mouse sensitivity
- Y-axis inversion
- View all key bindings

## Troubleshooting

If controls aren't working:
1. Make sure the extension is enabled (Ctrl+Shift+X)
2. For menus, just press keys - no mouse lock needed
3. For gameplay, click the game canvas first
EOF

# Final message
cd ..
echo ""
echo "✅ Extension created successfully!"
echo ""
echo "📁 Extension location: $(pwd)/$EXTENSION_DIR"
echo ""
echo "To install in Microsoft Edge:"
echo "1. Open Edge and go to: edge://extensions/"
echo "2. Turn ON 'Developer mode'"
echo "3. Click 'Load unpacked'"
echo "4. Select the folder: $EXTENSION_DIR"
echo ""
echo "⚡ IMPORTANT: Press Ctrl+Shift+X to enable/disable the extension!"
echo ""
echo "🎮 Happy gaming with mouse and keyboard!"
EOF

chmod +x create-xbox-mkb-extension.sh