# Chromium Browser - Quick Start Guide

## 🚀 How to Launch

### Method 1: Desktop Icon
1. Start the Windows 95 Desktop Simulator
2. Look for the **"Chromium"** icon at coordinates (180, 90)
3. Double-click the icon
4. Browser opens with the New Tab page

### Method 2: Start Menu
1. Click the **Start** button (bottom-left)
2. Look for **"🌐 Chromium Browser ⭐"** (highlighted entry)
3. Click to launch
4. Browser opens immediately

## 🌐 Browsing the Web

### Enter a URL
1. Click in the **omnibox** (address bar)
2. Type a URL: `example.com` or `https://example.com`
3. Press **Enter** or click **Go**

### Search the Web
1. Click in the omnibox
2. Type a search query: `cats`
3. Press **Enter**
4. Searches via DuckDuckGo

### Navigation Buttons
- **◀ Back**: Go to previous page
- **▶ Forward**: Go to next page
- **🔄 Reload**: Refresh current page
- **🏠 Home**: Return to New Tab page

## 📑 Tab Management

### Open New Tab
- Click the **+** button next to existing tabs
- Opens a new tab with the New Tab page

### Switch Tabs
- Click on any tab to switch to it
- Active tab is highlighted in white

### Close Tab
- Click the **×** button on the tab
- Browser closes if last tab is closed

## ⭐ Bookmarks

### Add Bookmark
1. Navigate to a page
2. Click the **⭐** star icon in omnibox
3. Bookmark is saved automatically
4. Toast notification confirms

### View Bookmarks
- Visit `chrome://bookmarks`
- Or see them on New Tab page
- Click any bookmark to navigate

### Remove Bookmark
- Go to `chrome://bookmarks`
- Click **Remove** button next to bookmark

## 🔧 Developer Tools

### Open DevTools
- Click the **🔧** button in toolbar
- Or press **F12** (if supported)

### DevTools Panels

#### 1. Elements Panel
- View DOM tree structure
- Inspect HTML elements
- See syntax-highlighted code

#### 2. Console Panel
- **Execute JavaScript**: Type code and press Enter
- **Real REPL**: Uses native `eval()`
- Example: `console.log('Hello!')` or `2 + 2`
- View error/warning messages

#### 3. Sources Panel
- View page resources
- Click files to inspect source
- HTML, CSS, JS files

#### 4. Network Panel
- **Real-time monitoring**: See all fetch requests
- View HTTP status, method, URL
- Check timing and size
- Color-coded status (green = 200 OK)

#### 5. Performance Panel
- See FPS, paint time, layout time
- Monitor script execution time
- Click **Record** to capture timeline

#### 6. Application Panel
- **localStorage**: View actual browser storage
- **sessionStorage**: See session data
- **Cookies**: Inspect cookie values

### Close DevTools
- Click **🔧** button again
- Or click close button on DevTools panel

## 🛠️ Special Chrome Pages

### chrome://newtab
- Default new tab page
- Search bar at top
- Quick links to common pages
- Bookmarks preview

### chrome://settings
- **Search engine**: Choose default search
- **Appearance**: UI customization
- **Privacy**: Cookie settings
- **Performance**: Hardware acceleration

### chrome://history
- View all browsing history
- Click entries to revisit
- Search history
- **Clear browsing data** button

### chrome://bookmarks
- Manage all bookmarks
- Click to navigate
- Remove unwanted bookmarks

### chrome://downloads
- See download history
- Progress bars for active downloads
- Open or cancel downloads

### chrome://extensions
- View installed extensions
- Sample extensions shown:
  - uBlock Origin (ad blocker)
  - Dark Reader (dark mode)
  - JSON Formatter
  - ColorZilla (color picker)
- Toggle extensions on/off

### chrome://flags
- **⚠️ Experimental features**
- Smooth scrolling
- Parallel downloading
- GPU rasterization
- QUIC protocol
- Tab hover cards

### chrome://version
- Browser version information
- JavaScript engine (V8)
- Rendering engine (Blink)
- User agent string
- Platform details

### chrome://internals
- **Browser process**: Main UI process
- **GPU process**: Graphics acceleration
- **Network process**: Network requests
- **Renderer processes**: Per-tab processes
- **Performance metrics**: FPS, paint, layout, script times
- **Network activity**: Recent requests log

## 🎨 Chrome UI Features

### Omnibox (Address Bar)
- 🔒 Lock icon shows security
- Type URLs or search queries
- Auto-completion of protocols
- ⭐ Star for bookmarking

### Tab Bar
- Rounded Material Design tabs
- Tab title and favicon
- Close button (×) per tab
- **+** button for new tab
- Horizontal scrolling for many tabs

### Status Bar (Bottom)
- Loading status text
- Process count
- Memory usage (MB)
- FPS (frames per second)

### Toolbar Buttons
- **🧩 Extensions**: Open extensions page
- **🔧 DevTools**: Toggle developer tools
- **⋮ Menu**: Chrome menu (coming soon)
- **⚙️ Settings**: Quick settings access

## 🚫 CORS Handling

### If a Site Won't Load

The browser will show one of these:

#### 1. Direct Load (Success)
- Site loads in iframe
- Full interactivity
- Status: "Done"

#### 2. Proxy Load (Fallback)
- Loads via CORS proxy
- Some features may be limited
- Status: "Done (via proxy)"

#### 3. CORS Error (Blocked)
- Shows error page with 🔒 icon
- Explains why (X-Frame-Options)
- Offers solutions:
  - **Open in New Window**: Opens in browser tab
  - **Try Proxy Load**: Attempts proxy fallback

### Sites That Usually Work
- Wikipedia
- MDN Web Docs
- Many GitHub pages
- Simple HTML sites
- CORS-friendly APIs

### Sites That May Not Work
- Google, Facebook, Twitter (X-Frame-Options)
- Banking sites (security policies)
- Most social media (embedding blocked)
- Many commercial sites

### Workarounds
1. Click **"Open in New Window"** button
2. Use **"Try Proxy Load"** button
3. Visit CORS-friendly alternative sites

## 💡 Tips & Tricks

### Multiple Tabs
- Open many tabs for multitasking
- Each tab has independent history
- Back/forward works per-tab
- Tabs remember their state

### Bookmarks on New Tab
- Frequently visited sites appear
- Up to 6 bookmarks shown
- Click Quick Links for more

### Search vs URL Detection
- Contains `.` → Treated as URL
- No `.` → Searches via DuckDuckGo
- `chrome://` → Special Chrome page

### Console Commands
Try these in DevTools Console:
```javascript
// Basic math
2 + 2

// Access DOM
document.title

// View current URL
location.href

// Log messages
console.log('Testing console!')

// Inspect variables
navigator.userAgent
```

### History Navigation
- Back/forward buttons update per tab
- History persists between sessions
- Visit `chrome://history` to search

### Performance Monitoring
- Status bar shows real-time FPS
- Memory usage updates every second
- Check `chrome://internals` for details

## 🐛 Troubleshooting

### Browser Won't Open
- Ensure Windows 95 emulator is running
- Try Start Menu instead of desktop icon
- Check browser console for errors

### Page Won't Load
- Check if site blocks iframes
- Try "Open in New Window" button
- Use "Try Proxy Load" fallback
- Visit CORS-friendly alternative

### DevTools Not Working
- Ensure panel is open (click 🔧)
- Try switching between panels
- Check Console panel for errors

### Tabs Not Switching
- Click directly on tab
- Check if tab is hidden (scroll tab bar)
- Try closing and reopening tab

### Bookmarks Not Saving
- Check localStorage is enabled
- Try clearing browser cache
- Re-add bookmark manually

### Performance Issues
- Close unused tabs
- Check `chrome://internals` for metrics
- Restart browser window

## 📚 Learning Resources

### Study the Code
- File: `windows95-emulator.html`
- Class: `ChromiumBrowserEngine`
- Lines: ~1,600 lines of code
- Methods: 50+ functions

### Explore Browser Internals
1. Visit `chrome://internals`
2. See multi-process architecture
3. Monitor performance metrics
4. Track network requests

### Use DevTools
1. Open any page
2. Toggle DevTools (F12)
3. Explore all 6 panels
4. Execute JavaScript in Console

### Read Documentation
- `CHROMIUM-BROWSER-ENGINE.md` - Full technical docs
- Code comments explain concepts
- Study browser architecture patterns

## 🎓 Educational Use

### For Students
- Learn browser architecture
- Understand multi-process design
- Study network protocols (CORS, HTTP)
- Practice JavaScript in Console

### For Developers
- See DevTools implementation
- Study network interception
- Learn DOM manipulation
- Understand browser storage APIs

### For Teachers
- Demonstrate browser concepts
- Show real-world CORS issues
- Teach performance monitoring
- Explain multi-process benefits

## ⚡ Quick Reference

| Action | Method |
|--------|--------|
| Open Chromium | Desktop icon or Start menu |
| New Tab | Click + button |
| Close Tab | Click × on tab |
| Navigate | Enter URL in omnibox |
| Search Web | Type query in omnibox |
| Back/Forward | Use ◀ ▶ buttons |
| Reload | Click 🔄 button |
| Bookmark | Click ⭐ star |
| DevTools | Click 🔧 button |
| Settings | chrome://settings |
| History | chrome://history |
| Bookmarks | chrome://bookmarks |
| Internals | chrome://internals |

## 🌟 Pro Tips

1. **Bookmark chrome:// pages** for quick access
2. **Use Console for quick calculations** instead of Calculator app
3. **Check Network panel** to debug loading issues
4. **Monitor Performance panel** for slow pages
5. **Visit chrome://internals** to see browser architecture
6. **Try multiple tabs** to test multi-process system
7. **Use history search** to find previously visited pages
8. **Explore all DevTools panels** to understand browser capabilities

## 🎉 Have Fun!

Chromium Browser is a **real, working browser** built entirely in JavaScript within the Windows 95 emulator. It demonstrates actual browser engine concepts and provides a fully functional web browsing experience (within CORS constraints).

Explore, experiment, and learn how modern browsers work under the hood!

---

**Version**: 1.0.0  
**Last Updated**: 2025-10-14  
**File**: `windows95-emulator.html`  
**Documentation**: `CHROMIUM-BROWSER-ENGINE.md`
