# WOWMON ACCESSIBILITY QUICK REFERENCE

**Quick guide for implementing accessible features in wowMon.html**

---

## KEYBOARD NAVIGATION PATTERNS

### Team Builder
```
Access: SELECT + START (hold 1s) or Menu > Team
Navigate: Arrow keys
Switch sections: Tab
Select slot: Enter
Swap creatures: S key
Sort: Q key
Filter: F key
Details: D key
Jump to slot: 1-6 keys
Exit: X or Escape
```

### Battle System
```
Main Menu: Arrow Up/Down
Select: Enter or Z
Cancel: X or Escape
Quick select: 1-4 keys

Switch Menu:
Navigate: Arrow Up/Down
Select: Enter
Quick slot: 1-6 keys
Cancel: X

Move Menu:
Navigate: Arrow keys (2x2 grid)
Select: Enter or Z
Cancel: X
```

---

## ESSENTIAL ARIA ATTRIBUTES

### Interactive Elements
```html
<button aria-label="Action button A - Confirm and interact">A</button>
<div role="menu" aria-label="Battle actions">...</div>
<div role="menuitem" tabindex="0">FIGHT</div>
<div role="status" aria-live="polite">HP: 20/20</div>
```

### Live Regions
```html
<!-- Polite (non-urgent) announcements -->
<div id="liveRegion" role="status" aria-live="polite" aria-atomic="true"></div>

<!-- Assertive (urgent) announcements -->
<div id="battleLog" role="log" aria-live="assertive"></div>
```

### Screen Reader Only Content
```html
<span class="sr-only">Creature has 20 of 20 HP, 100 percent, healthy</span>
```

---

## ANNOUNCEMENT TEMPLATES

### Team Builder
```javascript
// Opening
`Team Builder opened. ${partyCount} creatures in active party,
 ${storageCount} in storage. Use Tab to switch sections.`

// Slot selection
`Party slot ${index}: ${creature.name}, Level ${level},
 ${hp} of ${maxHp} HP, ${status}. Press Enter for options.`

// Creature swap
`Swapped ${creature1.name} with ${creature2.name}.`
```

### Battle
```javascript
// Turn start
`Turn ${turn}. Your ${player.name}: ${playerHP}% HP.
 Enemy ${enemy.name}: ${enemyHP}% HP. What will you do?`

// Attack result
`${attacker.name} used ${move.name}! ${effectiveness}
 ${defender.name} took ${damage} damage. ${hp} HP remaining, ${percent}%. ${status}`

// Switch
`${oldCreature.name} is switching out for ${newCreature.name}.`
```

### Status
```javascript
// Health status
const getHealthStatus = (creature) => {
  const percent = (creature.hp / creature.maxHp) * 100;
  if (percent === 0) return 'fainted';
  if (percent < 25) return 'critically injured';
  if (percent < 50) return 'heavily injured';
  if (percent < 75) return 'moderately injured';
  if (percent < 100) return 'slightly injured';
  return 'healthy';
};
```

---

## FOCUS MANAGEMENT

### Focus Styles (Already in wowMon.html)
```css
button:focus,
.menu-option:focus,
[tabindex]:focus {
  outline: 3px solid #ffcc00;
  outline-offset: 2px;
  z-index: 1000;
}
```

### Focus Trapping in Modals
```javascript
// Trap focus in team builder
trapFocus(container) {
  const focusable = container.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const first = focusable[0];
  const last = focusable[focusable.length - 1];

  container.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
  });
}
```

---

## VISUAL ALTERNATIVES

### HP Status (not just color)
```css
/* Add patterns for colorblind support */
.hp-fill {
  position: relative;
}

.hp-fill.high {
  background: green;
}

.hp-fill.low {
  background: repeating-linear-gradient(
    -45deg,
    red, red 4px,
    darkred 4px, darkred 8px
  );
  animation: pulse 1s infinite;
}

.hp-fill.critical {
  background: repeating-linear-gradient(
    90deg,
    red, red 2px,
    yellow 2px, yellow 4px
  );
  animation: flash 0.5s infinite;
}
```

### Type Indicators (beyond color)
```css
.type-badge {
  position: relative;
  padding: 4px 8px;
  border: 2px solid;
}

/* Different patterns for each type */
.type-warrior {
  background: linear-gradient(45deg, #8b4513 25%, transparent 25%);
  border-style: solid;
}

.type-spirit {
  background: radial-gradient(circle, rgba(255,255,255,0.2) 1px, transparent 1px);
  border-style: dotted;
}

.type-fire {
  background: repeating-linear-gradient(0deg, orange, red 10px);
  border-style: dashed;
}
```

### Text Status Indicators
```html
<span class="health-status" data-status="Healthy">
  HP: 20/20
</span>

<style>
.health-status::before {
  content: "[" attr(data-status) "] ";
  font-weight: bold;
}
</style>
```

---

## ACCESSIBILITY SETTINGS API

### Initialize Settings
```javascript
accessibilitySettings: {
  highContrast: false,
  reducedMotion: false,
  largeText: false,
  textSize: 120,
  uiScale: 100,
  screenReaderMode: false,
  verboseMode: false,
  textSpeed: 3,
  autoAdvanceText: false,
  showTypeEffectiveness: true,
  colorblindMode: false,
  colorblindType: 'deuteranopia',
  soundEffectCues: true,
  creatureTypeSounds: false,
  announceMenuPosition: true
}
```

### Apply Settings
```javascript
applyAccessibilitySettings() {
  const body = document.body;

  // High contrast
  body.classList.toggle('high-contrast', this.settings.highContrast);

  // Reduced motion
  body.classList.toggle('reduced-motion', this.settings.reducedMotion);

  // Large text
  body.style.fontSize = `${this.settings.textSize}%`;

  // UI scale
  const container = document.querySelector('.game-container');
  container.style.transform = `scale(${this.settings.uiScale / 100})`;

  // Colorblind mode
  body.classList.toggle('colorblind-mode', this.settings.colorblindMode);
  body.setAttribute('data-colorblind-type', this.settings.colorblindType);
}
```

### Save/Load Settings
```javascript
saveAccessibilitySettings() {
  localStorage.setItem('wowmon_a11y_settings',
    JSON.stringify(this.accessibilitySettings)
  );
  this.announce('Accessibility settings saved.', 'polite');
}

loadAccessibilitySettings() {
  const saved = localStorage.getItem('wowmon_a11y_settings');
  if (saved) {
    this.accessibilitySettings = { ...this.accessibilitySettings, ...JSON.parse(saved) };
    this.applyAccessibilitySettings();
  }
}
```

---

## TESTING CHECKLIST

### Keyboard Navigation
- [ ] Can navigate entire game without mouse
- [ ] Tab order is logical
- [ ] All interactive elements are reachable
- [ ] Focus is visible at all times
- [ ] Can escape from all modals
- [ ] Shortcuts don't conflict
- [ ] Number keys work for quick selection

### Screen Reader
- [ ] All images have alt text or aria-label
- [ ] Form inputs have associated labels
- [ ] Live regions announce updates
- [ ] Menu structure is clear
- [ ] Role attributes are appropriate
- [ ] ARIA labels are descriptive
- [ ] No unnecessary announcements

### Visual
- [ ] Works in high contrast mode
- [ ] Text is readable at 200% zoom
- [ ] No information conveyed by color alone
- [ ] Focus indicators are visible
- [ ] Patterns distinguish types
- [ ] Text overlays have sufficient contrast

### Motor/Input
- [ ] No time limits on inputs
- [ ] Can pause at any time
- [ ] No rapid button mashing required
- [ ] Controls can be remapped
- [ ] Touch targets are 44px minimum
- [ ] Double-tap protection (optional)

---

## COMMON PATTERNS

### Menu Navigation with Announcement
```javascript
handleMenuInput(key) {
  const options = this.getMenuOptions();

  switch(key) {
    case 'ArrowUp':
      this.menuIndex = Math.max(0, this.menuIndex - 1);
      this.updateMenuFocus();
      this.announceMenuOption(options[this.menuIndex]);
      break;

    case 'ArrowDown':
      this.menuIndex = Math.min(options.length - 1, this.menuIndex + 1);
      this.updateMenuFocus();
      this.announceMenuOption(options[this.menuIndex]);
      break;

    case 'Enter':
    case 'z':
      this.selectMenuOption(this.menuIndex);
      break;
  }
}

announceMenuOption(option) {
  const position = this.settings.announceMenuPosition
    ? ` Item ${this.menuIndex + 1} of ${options.length}.`
    : '';
  this.announce(`${option.text}. ${option.description}${position}`, 'polite');
}
```

### Grid Navigation (2x2 move menu)
```javascript
handleGridInput(key) {
  const columns = 2;
  const rows = 2;
  const total = columns * rows;

  switch(key) {
    case 'ArrowUp':
      if (this.selectedIndex >= columns) {
        this.selectedIndex -= columns;
      }
      break;

    case 'ArrowDown':
      if (this.selectedIndex < total - columns) {
        this.selectedIndex += columns;
      }
      break;

    case 'ArrowLeft':
      if (this.selectedIndex % columns !== 0) {
        this.selectedIndex--;
      }
      break;

    case 'ArrowRight':
      if (this.selectedIndex % columns !== columns - 1) {
        this.selectedIndex++;
      }
      break;
  }

  this.updateGridFocus();
  this.announceGridSelection();
}
```

### Creature Selection with Details
```javascript
announceCreatureSelection(creature, index, total) {
  // Basic info
  const name = creature.name;
  const level = creature.level;
  const types = creature.types ? creature.types.join(' and ') : 'Normal';

  // HP status
  const hp = creature.hp;
  const maxHp = creature.maxHp;
  const hpPercent = Math.round((hp / maxHp) * 100);
  const status = this.getHealthStatus(creature);

  // Verbose mode adds more details
  let announcement = `${name}, ${types} type, Level ${level},
                      ${hp} of ${maxHp} HP, ${hpPercent} percent, ${status}.`;

  if (this.settings.verboseMode) {
    announcement += ` Attack ${creature.attack}, Defense ${creature.defense},
                      Speed ${creature.speed}. Knows ${creature.moves.length} moves.`;
  }

  if (this.settings.announceMenuPosition) {
    announcement += ` Item ${index + 1} of ${total}.`;
  }

  this.announce(announcement, 'polite');
}
```

---

## INTEGRATION STEPS

### 1. Add Team Builder to wowMon.html
```javascript
// In GameEngine class
this.teamBuilder = new TeamBuilder(this);

// Add to handleInput
if (key === 'SELECT' && this.keys['START']) {
  // Both held for 1 second
  if (this.selectStartHoldTime > 1000) {
    this.teamBuilder.open();
  }
}
```

### 2. Enhance Battle System
```javascript
// In battle menu
selectBattleOption(index) {
  switch(index) {
    case 0: // FIGHT
      this.showMoveSelection();
      break;
    case 1: // SWITCH (NEW)
      this.battleSystem.openSwitchMenu();
      break;
    case 2: // BAG
      // existing code
      break;
    case 3: // RUN
      // existing code
      break;
  }
}
```

### 3. Add Accessibility Panel Trigger
```javascript
// Global keyboard listener
document.addEventListener('keydown', (e) => {
  // Alt + A opens accessibility settings
  if (e.altKey && e.key === 'a') {
    game.toggleAccessibilityPanel();
  }

  // Ctrl + S reads status
  if (e.ctrlKey && e.key === 's') {
    e.preventDefault();
    game.readGameStatus();
  }

  // Ctrl + R repeats announcement
  if (e.ctrlKey && e.key === 'r') {
    e.preventDefault();
    game.repeatLastAnnouncement();
  }

  // H toggles help
  if (e.key === 'h' || e.key === 'H') {
    game.toggleKeyboardHelp();
  }
});
```

---

## RESOURCES

### Screen Readers for Testing
- **NVDA** (Windows, free): https://www.nvaccess.org/
- **JAWS** (Windows, trial): https://www.freedomscientific.com/
- **VoiceOver** (Mac/iOS, built-in): Cmd + F5
- **TalkBack** (Android, built-in): Settings > Accessibility

### Accessibility Guidelines
- **WCAG 2.1 Level AA**: https://www.w3.org/WAI/WCAG21/quickref/
- **ARIA Authoring Practices**: https://www.w3.org/WAI/ARIA/apg/
- **Game Accessibility Guidelines**: https://gameaccessibilityguidelines.com/

### Testing Tools
- **axe DevTools** (browser extension)
- **WAVE** (web accessibility evaluation tool)
- **Keyboard Navigation Tester** (F12 > Accessibility tab in Chrome)

---

## CONTACT & SUPPORT

For questions about implementing these accessibility features:
1. Review the full design document: `ACCESSIBILITY_FIRST_FEATURE_DESIGN.md`
2. Test with actual screen readers and keyboard-only navigation
3. Consult WCAG 2.1 guidelines for specific requirements
4. Prioritize user testing with people who rely on assistive technologies

**Remember:** Accessibility is not a checklist, it's a mindset. Design for everyone from the start.
