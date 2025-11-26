# Cursor Tarot System - Step-by-Step Integration Guide

## Quick Start

1. Open `recursive-self-portrait.html` in your code editor
2. Open `TAROT_SYSTEM_ADDITION.html` in another window
3. Follow the steps below (copy-paste 4 sections)
4. Save and test

Total time: **5 minutes**

---

## Step 1: Add CSS Styles

### Location
Find line **6454** in `recursive-self-portrait.html`

It looks like this:
```css
        body.cosmic-horror-active .recursion-layer {
            border-color: rgba(100, 255, 150, 0.5);
            box-shadow:
                0 0 30px rgba(100, 255, 150, 0.2),
                inset 0 0 40px rgba(100, 255, 150, 0.08);
        }

        </style>  ← LINE 6454
```

### What to do
1. In `TAROT_SYSTEM_ADDITION.html`, find the section marked:
   ```html
   <!-- ========== CSS SECTION - ADD TO <style> BEFORE </style> TAG ========== -->
   ```

2. Copy everything from that marker down to (but not including):
   ```html
   <!-- ========== HTML SECTION - ADD TO SIDEBAR AFTER AKASHIC PANEL ========== -->
   ```

3. Paste it **ABOVE** the `</style>` tag at line 6454

### Result
Line 6454 should now look like:
```css
        }

        /* ===== CURSOR TAROT/ORACLE SYSTEM ===== */
        .tarot-panel {
            background: rgba(30, 30, 50, 0.5);
            ...
        }

        </style>  ← Still line 6454 (now with more CSS above it)
```

---

## Step 2: Add Sidebar Panel HTML

### Location
Find **around line 9030** in `recursive-self-portrait.html`

Look for the end of the Akashic panel:
```html
            <!-- ===== AKASHIC RECORDS PANEL ===== -->
            <div class="akashic-panel">
                ...
            </div>

            ← INSERT HERE (around line 9030)

            <!-- Replay Tab Content -->
            <div class="tab-content" id="replayTab">
```

### What to do
1. In `TAROT_SYSTEM_ADDITION.html`, find:
   ```html
   <!-- ========== HTML SECTION - ADD TO SIDEBAR AFTER AKASHIC PANEL ========== -->
   ```

2. Copy everything from there until (but not including):
   ```html
   <!-- ========== TAROT OVERLAY - ADD TO END OF BODY ========== -->
   ```

3. Paste it after the Akashic panel `</div>` closing tag

### Result
```html
            </div>  ← End of Akashic panel

            <!-- ===== CURSOR TAROT/ORACLE SYSTEM ===== -->
            <div class="tarot-panel">
                <h3>🔮 Cursor Tarot & Oracle</h3>
                ...
            </div>

            <!-- Replay Tab Content -->
```

---

## Step 3: Add Overlay HTML

### Location
Find **line 23249** (near the very end of the file)

It looks like:
```html
    </div>

</body>  ← LINE 23249
</html>
```

### What to do
1. In `TAROT_SYSTEM_ADDITION.html`, find:
   ```html
   <!-- ========== TAROT OVERLAY - ADD TO END OF BODY ========== -->
   ```

2. Copy everything from there until (but not including):
   ```html
   <!-- ========== JAVASCRIPT SECTION - ADD BEFORE CLOSING </script> TAG ========== -->
   ```

3. Paste it **ABOVE** the `</body>` tag

### Result
```html
    </div>

    <!-- Tarot Reading Overlay -->
    <div class="tarot-overlay" id="tarotOverlay">
        ...
    </div>

</body>  ← LINE 23249 (now with overlay above it)
</html>
```

---

## Step 4: Add JavaScript Code

### Location
Find the **closing `</script>` tag** near the end of the file

Use your editor's Find function (Ctrl+F or Cmd+F) to search for:
```javascript
        </script>
```

There should be a `<script>` tag that contains all the app's JavaScript. Find where it ends.

### What to do
1. In `TAROT_SYSTEM_ADDITION.html`, find:
   ```html
   <!-- ========== JAVASCRIPT SECTION - ADD BEFORE CLOSING </script> TAG ========== -->
   ```

2. Copy everything after that marker (all the JavaScript code)

3. Paste it **ABOVE** the `</script>` closing tag

### Result
```javascript
        // ... existing JavaScript code ...

        // ===== CURSOR TAROT/ORACLE SYSTEM =====

        const MAJOR_ARCANA = [
            { name: 'The Fool', symbol: '🃏', ...
        ...

        </script>  ← Closing script tag
```

---

## Verification Checklist

After integration, verify:

- [ ] **CSS added**: Search for `.tarot-panel {` - should find it
- [ ] **HTML panel added**: Search for `Cursor Tarot & Oracle` - should find it
- [ ] **Overlay added**: Search for `tarotOverlay` - should find it
- [ ] **JavaScript added**: Search for `MAJOR_ARCANA` - should find it
- [ ] **No syntax errors**: File should still be valid HTML

---

## Testing

1. Open `recursive-self-portrait.html` in a web browser
2. Look in the sidebar - you should see a new panel titled **"🔮 Cursor Tarot & Oracle"**
3. Move your cursor around for a few seconds
4. You might see a "Card of the Session" appear
5. Try clicking the mode buttons: **Tarot**, **I-Ching**, **Runes**
6. Click **"Draw Reading"**
7. A full-screen overlay should appear with your reading
8. Check the browser console (F12) for any errors

---

## Troubleshooting

### "I don't see the panel"
- Check that you pasted the HTML in the sidebar section
- Look for `<div class="tarot-panel">` in your code
- Make sure it's inside `<div class="sidebar">`

### "Buttons don't work"
- Check that you pasted the JavaScript
- Open browser console (F12) and look for errors
- Search for `function drawTarotReading()` in your code

### "Styling looks wrong"
- Check that you pasted the CSS before `</style>`
- Search for `.tarot-panel {` in your CSS section

### "Daily card doesn't appear"
- This is normal - it only appears after ~5 movements
- Try moving your cursor more
- Wait a few seconds after the page loads

### "Reading says 'not enough data'"
- Move your cursor around more (need at least 10 movements)
- The system analyzes your actual movement patterns

---

## File Organization

After integration, your file structure should be:

```
recursive-self-portrait.html
├── <style>
│   ├── ... existing styles ...
│   ├── /* ===== CURSOR TAROT/ORACLE SYSTEM ===== */  ← NEW
│   └── </style>
├── <body>
│   ├── <div class="sidebar">
│   │   ├── ... existing panels ...
│   │   ├── <div class="akashic-panel">...</div>
│   │   ├── <div class="tarot-panel">...</div>  ← NEW
│   │   └── ...
│   ├── ... existing content ...
│   ├── <div class="tarot-overlay">...</div>  ← NEW
│   └── </body>
├── <script>
│   ├── ... existing JavaScript ...
│   ├── // ===== CURSOR TAROT/ORACLE SYSTEM =====  ← NEW
│   └── </script>
└── </html>
```

---

## What You're Adding

| Section | Lines | Purpose |
|---------|-------|---------|
| **CSS** | ~350 | Styling for cards, overlays, animations |
| **HTML Panel** | ~70 | Sidebar controls and display |
| **HTML Overlay** | ~30 | Full-screen reading display |
| **JavaScript** | ~650 | Divination logic and behavior analysis |
| **TOTAL** | ~1,100 | Complete feature |

---

## Quick Copy-Paste Checklist

Use this checklist as you work:

- [ ] **1. CSS**: Find line 6454 → Paste before `</style>`
- [ ] **2. HTML Panel**: Find line ~9030 → Paste after Akashic panel
- [ ] **3. Overlay**: Find line 23249 → Paste before `</body>`
- [ ] **4. JavaScript**: Find `</script>` → Paste before closing tag
- [ ] **5. Save** the file
- [ ] **6. Open** in browser
- [ ] **7. Test** the Draw Reading button

---

## Visual Guide

### Before Integration:
```
recursive-self-portrait.html (23,250 lines)
└── Existing features only
```

### After Integration:
```
recursive-self-portrait.html (~24,350 lines)
├── Existing features (unchanged)
└── NEW: Cursor Tarot/Oracle System
    ├── 3 divination modes
    ├── Movement analysis
    ├── Reading generation
    ├── Prophetic commentary
    └── History tracking
```

---

## Support

If you run into issues:

1. **Check the browser console** (F12) for error messages
2. **Compare your code** to `TAROT_SYSTEM_ADDITION.html`
3. **Make sure** all 4 sections were copied
4. **Verify** proper nesting (HTML tags closed correctly)
5. **Try the demo** (`TAROT_DEMO.html`) to see expected behavior

---

## Next Steps After Integration

Once working:

1. **Move your cursor** to build up movement data
2. **Draw readings** in all three modes (Tarot, I-Ching, Runes)
3. **Check accuracy** - readings update as you use the app
4. **Export data** - readings are saved in your session export
5. **Observe patterns** - watch how readings adapt to your behavior

---

## Remember

The system **reads your actual behavior**, so:
- More chaotic movements → Different cards (Tower, Moon)
- Smooth movements → Different cards (Chariot, Sun)
- Slow movements → Different cards (Hermit, Hanged Man)
- Circular patterns → Wheel of Fortune
- Linear patterns → The Chariot

**The divination is real behavioral analysis dressed as mysticism.**

That's the magic. 🔮✨
