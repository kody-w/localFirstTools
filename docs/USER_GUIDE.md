# Local First Tools - User Guide

Welcome to Local First Tools, a collection of 100+ self-contained interactive applications that work completely offline!

## Table of Contents

1. [Getting Started](#getting-started)
2. [Browsing the Gallery](#browsing-the-gallery)
3. [Using Applications](#using-applications)
4. [Xbox Controller Support](#xbox-controller-support)
5. [Offline Usage](#offline-usage)
6. [Data Import/Export](#data-importexport)
7. [Troubleshooting](#troubleshooting)

## Getting Started

### Quick Start

1. **Online Access**: Simply visit the gallery at your deployment URL
2. **Local Access**: Open `index.html` in any modern web browser
3. **No Installation Required**: Everything runs in your browser

### Browser Requirements

- **Recommended**: Chrome, Firefox, Edge, Safari (latest versions)
- **Mobile**: iOS Safari, Chrome for Android
- **Features**: JavaScript must be enabled

## Browsing the Gallery

### Gallery Organization

Applications are organized into 9 thematic categories:

#### Visual Art & Design
Interactive visual experiences, generative art, and design tools
- **Examples**: Rainbow SVG Path Designer, Terminal Viewer
- **Best For**: Creative expression, visual design

#### 3D & Immersive Worlds
Three-dimensional experiences and explorable virtual environments
- **Examples**: Minecraft Worm Game, Memory Palace, Sky Realms
- **Best For**: Immersive experiences, exploration

#### Audio & Music
Sound synthesis, music creation, and audio visualization
- **Examples**: 808s Production Suite, Holographic Camera
- **Best For**: Music creation, audio experimentation

#### Games & Puzzles
Interactive games and playful experiences
- **Examples**: Card Battle Arena, Poker Trainer, WoWmon
- **Best For**: Entertainment, skill building

#### Experimental & AI
AI-powered experiences and cutting-edge demos
- **Examples**: AI Companion Hub, Ghost Writer, Digital Twin Keeper
- **Best For**: Exploring AI interfaces, productivity

#### Creative Tools
Utilities for creative expression and productivity
- **Examples**: OmniWriter Pro, Prompt Library, Memory Palace
- **Best For**: Productivity, creative workflows

#### Generative Art
Algorithmic and procedural art generation
- **Examples**: Expansive Agents visualization
- **Best For**: Algorithmic art, procedural generation

#### Particle & Physics
Physics simulations and particle systems
- **Examples**: Physics Playground Laboratory
- **Best For**: Physics exploration, simulations

#### Educational Tools
Learning resources and tutorials
- **Examples**: Vibe Terminal, Claude Subagents Tutorial
- **Best For**: Learning, skill development

### Navigating the Gallery

1. **Browse by Category**: Click on category cards to filter applications
2. **Search**: Use the search bar to find specific tools
3. **Featured Apps**: Look for highlighted apps at the top
4. **Tags**: Click on tags to find similar applications
5. **Complexity Levels**:
   - Simple: Easy to use, straightforward
   - Intermediate: Some learning required
   - Advanced: Complex features, more learning curve

## Using Applications

### Opening an Application

1. Click on any application card in the gallery
2. The application opens in the same window
3. Use your browser's back button to return to the gallery

### Common Features

Most applications include:

- **Local Storage**: Your data is saved automatically in your browser
- **Import/Export**: Save your work as JSON files
- **Responsive Design**: Works on desktop and mobile
- **Offline Support**: Works without internet connection

### Best Practices

1. **Save Your Work**: Use export features to backup your data
2. **Browser Storage**: Be aware that clearing browser data will delete saved work
3. **Mobile Usage**: Some applications work better on desktop
4. **Performance**: Close other tabs for better performance with complex applications

## Xbox Controller Support

Many applications support Xbox controllers for enhanced gameplay:

### Setup

1. Connect your Xbox controller via USB or Bluetooth
2. The application will automatically detect the controller
3. On-screen prompts will show available controls

### Button Mapping

Standard mapping across supported games:
- **Left Stick**: Movement
- **Right Stick**: Camera/Aim
- **A Button**: Action/Select
- **B Button**: Back/Cancel
- **X Button**: Secondary action
- **Y Button**: Tertiary action
- **Triggers**: Fine control actions

### Browser Extension

For enhanced controller support:
- Install the Xbox Mouse & Keyboard Extension from `edgeAddons/xbox-mkb-extension`
- Provides system-wide controller support
- Works with any application

## Offline Usage

### Why Local First?

All applications follow the "local-first" philosophy:
- **Privacy**: No data sent to servers
- **Reliability**: Works without internet
- **Speed**: No network latency
- **Ownership**: Your data stays with you

### Using Offline

1. **First Visit**: Load the gallery while online
2. **Cache**: Browser caches all files automatically
3. **Offline Access**: Open cached `index.html` or bookmarked apps
4. **Updates**: Reconnect to internet to get new applications

### Downloading for Full Offline Use

```bash
# Clone the repository
git clone https://github.com/your-repo/localFirstTools3.git

# Open in browser
# Just open index.html in your browser
```

## Data Import/Export

### Exporting Your Data

Most applications support JSON export:

1. Look for "Export" or "Download" button
2. Choose JSON format (standard across all apps)
3. Save file to your computer
4. Filename typically includes timestamp

### Importing Data

1. Look for "Import" or "Load" button
2. Select your previously exported JSON file
3. Data is restored immediately
4. Your current work may be overwritten (check for warnings)

### Data Format

All applications use JSON format for maximum compatibility:

```json
{
  "version": "1.0",
  "timestamp": "2025-10-12T20:00:00Z",
  "data": {
    // Application-specific data
  }
}
```

### Sharing Your Work

1. Export your data as JSON
2. Share the JSON file with others
3. They can import it into the same application
4. Works across devices and platforms

## Troubleshooting

### Application Not Loading

**Problem**: Application shows blank page or error

**Solutions**:
- Refresh the page (Ctrl+R or Cmd+R)
- Clear browser cache
- Try a different browser
- Check browser console for errors (F12)

### Data Not Saving

**Problem**: Changes don't persist after closing

**Solutions**:
- Check browser storage permissions
- Ensure cookies/storage is not disabled
- Export your data manually as backup
- Check available storage space

### Controller Not Working

**Problem**: Xbox controller not detected

**Solutions**:
- Reconnect the controller
- Try a different USB port
- Update browser to latest version
- Check browser gamepad API support
- Try the browser extension

### Performance Issues

**Problem**: Application is slow or laggy

**Solutions**:
- Close other browser tabs
- Close other applications
- Update graphics drivers
- Use hardware acceleration (enable in browser settings)
- Try a simpler application first

### Mobile Issues

**Problem**: Application doesn't work well on mobile

**Solutions**:
- Rotate to landscape mode
- Use two-finger gestures for complex controls
- Some applications are desktop-only
- Check application description for mobile support

### Import/Export Problems

**Problem**: Can't import previously exported file

**Solutions**:
- Verify JSON file is valid (use JSON validator)
- Check file was exported from same application
- Ensure file is not corrupted
- Try exporting again from original device

## Getting Help

### Documentation

- **Developer Guide**: For technical details and contribution
- **Architecture Guide**: Understanding system design
- **Configuration Guide**: Customizing the gallery
- **FAQ**: Common questions and answers

### Community

- GitHub Issues: Report bugs or request features
- Discussions: Ask questions and share creations
- Pull Requests: Contribute your own applications

### Best Practices for Reporting Issues

1. Describe what you were trying to do
2. Include browser and OS information
3. Share error messages (from browser console)
4. Mention steps to reproduce the problem
5. Include screenshots if helpful

## Tips & Tricks

### Power User Tips

1. **Keyboard Shortcuts**: Most apps support common shortcuts (Ctrl+S, Ctrl+O, etc.)
2. **Bookmarking**: Bookmark individual apps for direct access
3. **Multiple Windows**: Open multiple apps simultaneously
4. **Developer Tools**: Use F12 to inspect and learn from applications
5. **Data Backup**: Regularly export your important work

### Creative Workflows

1. **Chaining Apps**: Export from one app, import to another
2. **Screen Recording**: Capture your creative process
3. **Sharing**: Share JSON files with collaborators
4. **Learning**: Study how applications work by viewing source
5. **Customization**: Fork and modify apps for your needs

### Mobile Optimization

1. **Portrait/Landscape**: Try both orientations
2. **Touch Gestures**: Learn app-specific gestures
3. **Zoom**: Use pinch-to-zoom where supported
4. **Rotation Lock**: Disable for better experience
5. **Full Screen**: Use browser full-screen mode

## What's Next?

### Exploring More

- Try applications from different categories
- Experiment with complexity levels
- Share your creations with others
- Learn by examining application code

### Contributing

- Create your own applications
- Submit them via pull requests
- Share feedback and suggestions
- Help improve documentation

### Stay Updated

- Watch the repository for updates
- Check for new applications regularly
- Follow development discussions
- Subscribe to release notifications

---

**Welcome to the local-first revolution! Create, explore, and own your digital tools.**
