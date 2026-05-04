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
