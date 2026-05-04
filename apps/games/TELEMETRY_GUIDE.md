# LEVIATHAN: OMNIVERSE - Performance Telemetry Guide

## Overview
Version 8.95 introduces a comprehensive Performance Telemetry & Analytics System that tracks FPS, memory usage, feature utilization, crash points, and player progression bottlenecks in real-time.

## Toggle Debug Overlay
**Press the backtick key (`) to toggle the performance debug overlay**

## Features

### 🎯 Real-Time Metrics
- **FPS Tracking**: Live frames per second with visual graph
- **Frame Time**: Millisecond timing per frame (warning < 33ms, critical < 16ms)
- **Memory Usage**: JavaScript heap usage in MB with trend visualization
- **FPS History Chart**: 120-frame rolling history with 60 FPS reference line
- **Memory Chart**: Memory consumption over time

### 📊 System Health
- **Render Calls**: Number of Three.js render calls per frame
- **Triangles**: Total triangle count being rendered
- **Textures**: Active texture count in memory
- **Active Entities**: Total objects in the scene graph

### 🎮 Feature Utilization
- **Most Used Features**: Top 10 features by usage count
- **Automatic Tracking**: Tracks mode switches, ability usage, etc.
- **Feature Badges**: Visual indicators showing usage frequency

### 🎯 Player Progression
- **Current Level**: Player's current level
- **Playtime**: Total minutes played
- **Deaths**: Death counter
- **Bottleneck Detection**: Automatically identifies locations where players die repeatedly (3+ times)

### ⚠️ Crash Analysis
- **Error Logging**: Catches all JavaScript errors and unhandled promise rejections
- **Crash History**: Last 5 crashes with timestamps
- **Stack Traces**: Full error details for debugging
- **Console Tracking**: Monitors console.error() calls

### 📋 Session Statistics
- **Session Duration**: Minutes since game started
- **Average FPS**: Mean FPS over entire session
- **Frame Drops**: Count of frames below 30 FPS

## API Usage

### Track Custom Features
```javascript
PerformanceTelemetry.trackFeature('custom_feature_name');
```

### Track Death Locations
```javascript
PerformanceTelemetry.trackDeath('Boss Arena Level 5');
```

### Track Mode Time
```javascript
PerformanceTelemetry.trackModeTime('combat', durationInMs);
```

### Export Telemetry Data
```javascript
const data = PerformanceTelemetry.exportData();
console.log(JSON.stringify(data, null, 2));
```

## Visual Indicators

### Color Coding
- **Green (#00ff88)**: Normal/Good performance
- **Orange (#ffaa00)**: Warning threshold
- **Red (#ff4444)**: Critical threshold

### Performance Thresholds
- **FPS**: 
  - Normal: 60+ FPS
  - Warning: 30-60 FPS
  - Critical: < 30 FPS

- **Frame Time**:
  - Normal: < 16.67ms (60 FPS)
  - Warning: 16.67-33.33ms (30-60 FPS)
  - Critical: > 33.33ms (< 30 FPS)

## Automatic Integration

The telemetry system automatically hooks into:
- **Game Mode Changes**: Tracks time spent in each mode
- **Error Handler**: Captures all errors globally
- **Promise Rejections**: Logs unhandled async errors
- **Console Errors**: Records all console.error() calls

## Overlay Controls

- **Close Button**: Click the ✕ button in top-right corner
- **Backtick Key**: Press ` again to close
- **Scrollable**: Overlay scrolls if content exceeds viewport

## Performance Impact

The telemetry system is designed to have minimal performance impact:
- Monitoring runs on requestAnimationFrame
- Charts update only when overlay is visible
- History buffers limited to 120 frames
- Efficient canvas rendering

## Debug Tips

1. **Check FPS Graph**: Look for sudden drops or patterns
2. **Monitor Memory**: Watch for gradual increases (memory leaks)
3. **Review Bottlenecks**: See where players struggle most
4. **Analyze Crashes**: Review error patterns and frequencies
5. **Export Data**: Use exportData() for detailed analysis

## Example Integration

```javascript
// Track custom game event
function onPowerUpCollected(powerUpName) {
    PerformanceTelemetry.trackFeature(`powerup_${powerUpName}`);
}

// Track player death with location
function onPlayerDeath() {
    const location = getCurrentLocationName();
    PerformanceTelemetry.trackDeath(location);
}

// Track ability usage
function useAbility(abilityName) {
    PerformanceTelemetry.trackFeature(`ability_${abilityName}`);
    // ... ability logic
}
```

## Data Export Format

```json
{
  "session": {
    "start": 1703087123456,
    "duration": 600000,
    "avgFPS": 58,
    "frameDrops": 12
  },
  "performance": {
    "fpsHistory": [60, 59, 60, ...],
    "memoryHistory": [45.2, 45.5, 45.3, ...]
  },
  "features": {
    "mode_world": 45,
    "ability_powerStrike": 12,
    "mode_nexus": 8
  },
  "crashes": [
    {
      "type": "error",
      "message": "...",
      "timestamp": 1703087123456
    }
  ],
  "progression": {
    "deaths": 5,
    "bottlenecks": [
      {
        "location": "Boss Arena",
        "count": 3
      }
    ],
    "modeTime": {
      "world": 300000,
      "nexus": 180000
    }
  }
}
```

## Browser Compatibility

- **Chrome/Edge**: Full support including memory tracking
- **Firefox**: FPS and basic metrics (no performance.memory)
- **Safari**: FPS and basic metrics (no performance.memory)

## Notes

- Memory tracking requires Chromium-based browsers
- Overlay persists across game sessions
- All data resets on page reload
- Maximum 120 frames of history retained for charts
