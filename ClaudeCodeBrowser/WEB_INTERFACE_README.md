# Agent Browser - Web Interface

## 🌐 Complete Browser-Based Interface

A fully self-contained, browser-based interface for Agent Browser. **Everything runs locally in your browser** - no server required!

## ✨ Features

### 🎯 Core Functionality
- **Browser Control**: Navigate, back, forward, reload
- **Content Extraction**: Text, Markdown, JSON, Links, Images, Headings
- **Page Interaction**: Click, type, fill forms, scroll
- **Session Management**: Save and restore complete browsing sessions
- **Data Export/Import**: Full JSON export/import of all data

### 💾 Local Storage
- All data stored in browser's localStorage
- No server communication
- Complete privacy
- Persistent across sessions

### 📊 Features

#### 1. Browser Section
- URL navigation bar
- Back/Forward/Reload buttons
- Simulated browser frame (iframe)
- Screenshot capability
- Content extraction
- Real-time console output

#### 2. Extract Content
- **Plain Text** - Clean text extraction
- **Markdown** - Convert HTML to Markdown
- **Structured JSON** - Full page data extraction
- **Links** - All hyperlinks on page
- **Images** - All images with metadata
- **Headings** - Document structure
- **Custom Selector** - Extract specific elements by CSS selector

#### 3. Interact
- **Click Element** - Click any element by selector
- **Type Text** - Type into input fields
- **Fill Form** - Fill multiple form fields at once
- **Scroll** - Scroll to top/bottom or by viewport

#### 4. History
- Complete navigation history
- Timestamps for each visit
- Statistics dashboard
- Clear history option

#### 5. Sessions
- Save current browsing state
- Restore saved sessions
- Session metadata (URL, timestamp, extracted data)
- Delete sessions

#### 6. Settings
- Auto-save toggle
- History recording toggle
- Verbose logging
- Data management
- Export/Import all data

## 🚀 Quick Start

### Option 1: Open Directly
```bash
# Simply open index.html in your browser
open index.html
# or
firefox index.html
# or
chrome index.html
```

### Option 2: Local Server (Optional)
```bash
# Using Python
python -m http.server 8000

# Using Node.js
npx http-server

# Then visit http://localhost:8000/index.html
```

## 📖 Usage Guide

### Navigation
1. Enter URL in the navigation bar
2. Click "Go" or press Ctrl/Cmd+Enter
3. Use Back/Forward buttons
4. Click Reload to refresh

### Extracting Content
1. Navigate to a page
2. Go to "Extract Content" section
3. Choose extraction type
4. Click "Extract"
5. View results in Preview/Raw/JSON tabs
6. Copy or download extracted data

### Interacting with Pages
1. Navigate to target page
2. Go to "Interact" section
3. Enter CSS selector for element
4. Perform action (click, type, fill form)

### Saving Sessions
1. Browse to desired state
2. Go to "Sessions" section
3. Enter session name
4. Click "Save Session"

### Loading Sessions
1. Go to "Sessions" section
2. Find your session
3. Click "Load"

### Export/Import Data
```javascript
// Export all data
Click "Export All Data" button
// Saves complete state as JSON file

// Import data
Click "Import Data" button
// Select previously exported JSON file
```

## 🔧 Data Structure

### Complete State Object
```json
{
  "version": "1.0.0",
  "exportDate": "2024-01-15T10:30:00.000Z",
  "state": {
    "currentUrl": "https://example.com",
    "history": [
      {
        "url": "https://example.com",
        "timestamp": "2024-01-15T10:30:00.000Z",
        "title": "Example Domain"
      }
    ],
    "sessions": [
      {
        "name": "My Research Session",
        "url": "https://example.com",
        "history": [...],
        "extractedData": {...},
        "timestamp": "2024-01-15T10:30:00.000Z"
      }
    ],
    "extractedData": {
      "type": "json",
      "content": {...},
      "url": "https://example.com",
      "timestamp": "2024-01-15T10:30:00.000Z"
    },
    "statistics": {
      "pagesVisited": 10,
      "extractions": 5,
      "interactions": 3,
      "sessionsSaved": 2
    },
    "settings": {
      "autoSave": true,
      "recordHistory": true,
      "verboseLogging": false
    }
  }
}
```

## ⚠️ Important Notes

### Cross-Origin Restrictions
Due to browser security (CORS), the iframe cannot access content from different origins. This means:

- ✅ **Works**: Pages from the same origin
- ✅ **Works**: Local HTML files
- ❌ **Limited**: External websites (can navigate but can't extract content)

**Workarounds:**
1. Use the server.js backend for full functionality
2. Use browser extensions with proper permissions
3. Use a local proxy server

### Privacy & Security
- **All data stays local** - nothing sent to servers
- **localStorage limitations** - ~5-10MB per domain
- **No cookies from iframe** - Cross-origin restrictions apply
- **Safe to use** - No external dependencies loaded

## 🎨 Customization

### Adding Custom Extractors
```javascript
// In the extractContent() function, add new case:
case 'custom':
    const customData = extractCustomData(doc);
    extracted = customData;
    break;

function extractCustomData(doc) {
    // Your custom extraction logic
    return {
        // Custom data structure
    };
}
```

### Styling
All styles are in the `<style>` tag. CSS variables at the top:
```css
:root {
    --primary: #2563eb;        /* Change primary color */
    --success: #10b981;        /* Change success color */
    --danger: #ef4444;         /* Change danger color */
    /* etc. */
}
```

## 🔌 API Reference

### Main Functions

```javascript
// Navigation
navigateToUrl()              // Navigate to URL in input
goBack()                     // Go back in history
goForward()                  // Go forward in history
reload()                     // Reload current page

// Content Extraction
extractContent()             // Extract by selected type
extractBySelector()          // Extract by CSS selector
getPageTitle()               // Get page title
getPageContent()             // Get page content as text

// Interaction
clickElement()               // Click element by selector
typeInElement()              // Type text into element
fillForm()                   // Fill multiple form fields
scrollPage(direction)        // Scroll page (top/down/bottom)

// Session Management
saveSession()                // Save current session
loadSession(session)         // Load saved session
deleteSession(index)         // Delete session

// Data Management
exportData()                 // Export all data as JSON
importData()                 // Import JSON data
clearAllData()               // Clear all data

// Utility
log(message, type)           // Log to console
showAlert(message, type)     // Show alert
updateUI()                   // Update all UI elements
```

## 📱 Mobile Support

The interface is responsive and works on mobile devices, though some features may be limited due to mobile browser restrictions.

## 🐛 Troubleshooting

### Issue: Can't extract content from external sites
**Solution**: This is due to CORS restrictions. Use server.js backend for full access.

### Issue: Data not persisting
**Solution**: Check if localStorage is enabled in browser settings.

### Issue: iframe not loading page
**Solution**: Some sites prevent iframe embedding. This is normal security behavior.

### Issue: Out of storage space
**Solution**: Export and clear old data. localStorage has ~5-10MB limit.

## 🚀 Advanced Usage

### Automation Scripts
```javascript
// You can control the interface programmatically
// Open browser console and run:

// Navigate
document.getElementById('urlInput').value = 'https://example.com';
navigateToUrl();

// Wait for load, then extract
setTimeout(() => {
    document.getElementById('extractType').value = 'json';
    extractContent();
}, 3000);

// Save session
setTimeout(() => {
    document.getElementById('sessionName').value = 'Auto Session';
    saveSession();
}, 5000);
```

### Batch Operations
```javascript
// Extract from multiple pages
const urls = ['https://site1.com', 'https://site2.com', 'https://site3.com'];

async function batchExtract() {
    for (const url of urls) {
        document.getElementById('urlInput').value = url;
        navigateToUrl();
        await new Promise(r => setTimeout(r, 3000)); // Wait 3 sec
        extractContent();
        await new Promise(r => setTimeout(r, 1000)); // Wait 1 sec
    }
}

batchExtract();
```

## 📊 Statistics

The interface tracks:
- Pages visited
- Extractions performed
- Interactions (clicks, types, form fills)
- Sessions saved

View in History → Statistics section.

## 💡 Tips

1. **Use keyboard shortcuts**: Ctrl/Cmd+Enter to navigate, Ctrl/Cmd+S for sessions
2. **Auto-save is on by default**: Your work is continuously saved
3. **Export regularly**: Create backups of important sessions
4. **Use custom selectors**: More precise than generic extraction
5. **Check console output**: Debugging information appears there

## 🔄 Workflow Examples

### Research Workflow
1. Navigate to research topic
2. Extract as Markdown
3. Copy to clipboard
4. Paste into LLM/notes
5. Save session for later

### Data Collection Workflow
1. Navigate to data source
2. Extract as JSON
3. Download extracted data
4. Process with scripts
5. Save session

### Form Automation Workflow
1. Navigate to form page
2. Add form fields
3. Enter values
4. Click Fill Form
5. Submit (if needed)

## 🎓 Learning Path

1. **Start simple**: Navigate to a page, extract text
2. **Try selectors**: Extract specific elements
3. **Save sessions**: Preserve your work
4. **Batch operations**: Multiple extractions
5. **Export/Import**: Backup and restore

## 🌟 Best Practices

1. ✅ **Export data regularly** - Don't lose your work
2. ✅ **Use descriptive session names** - Easy to find later
3. ✅ **Clear old history** - Keep storage clean
4. ✅ **Test selectors first** - Verify before batch operations
5. ✅ **Check console** - Monitor for errors

## 📝 License

MIT License - Free to use, modify, and distribute.

## 🤝 Contributing

This is a self-contained file. To contribute:
1. Modify index.html
2. Test thoroughly
3. Share your improvements

## 🆘 Support

For issues or questions:
- Check browser console for errors
- Verify localStorage is enabled
- Test with different browsers
- Clear data and try again

---

**Enjoy building with Agent Browser!** 🚀
