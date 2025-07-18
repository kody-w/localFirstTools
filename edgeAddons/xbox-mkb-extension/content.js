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
      ' ': 'A', // Space - Jump
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

  // Load config from storage
  chrome.storage.sync.get(['mkbConfig'], (result) => {
    if (result.mkbConfig) {
      config = { ...config, ...result.mkbConfig };
    }
  });

  // Override gamepad API
  const originalGetGamepads = navigator.getGamepads.bind(navigator);
  
  navigator.getGamepads = function() {
    const gamepads = originalGetGamepads();
    if (isPointerLocked) {
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
      
      // Replace first null/undefined gamepad
      for (let i = 0; i < 4; i++) {
        if (!gamepads[i]) {
          gamepads[i] = virtualGamepad;
          break;
        }
      }
    }
    return gamepads;
  };

  // Handle keyboard input
  document.addEventListener('keydown', (e) => {
    if (!isPointerLocked) return;
    
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
  });

  document.addEventListener('keyup', (e) => {
    if (!isPointerLocked) return;
    
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
  });

  // Handle mouse input
  document.addEventListener('mousedown', (e) => {
    if (!isPointerLocked) return;
    
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
    if (!isPointerLocked) return;
    
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
    if (!isPointerLocked) return;
    
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

  // Pointer lock handling
  document.addEventListener('click', async (e) => {
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
    if (!isPointerLocked) {
      // Reset state when pointer lock is released
      gamepadState.buttons.fill(false);
      gamepadState.axes.fill(0);
      Object.keys(movement).forEach(key => movement[key] = false);
      mouseX = 0;
      mouseY = 0;
    }
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
  `;
  document.head.appendChild(style);

  // Add visual indicator
  const indicator = document.createElement('div');
  indicator.className = 'mkb-indicator';
  indicator.textContent = 'Mouse & Keyboard: Click game to activate';
  document.body.appendChild(indicator);

  // Update indicator based on pointer lock state
  setInterval(() => {
    if (isPointerLocked) {
      indicator.className = 'mkb-indicator active';
      indicator.textContent = 'Mouse & Keyboard: Active (ESC to release)';
    } else {
      indicator.className = 'mkb-indicator';
      indicator.textContent = 'Mouse & Keyboard: Click game to activate';
    }
  }, 100);

})();
