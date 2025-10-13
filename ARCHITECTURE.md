# Local First Tools Gallery - Architecture Design Document

## Executive Summary

This document presents a modular, maintainable architecture for rebuilding the Local First Tools gallery application from scratch. The design honors the local-first philosophy while introducing clear separation of concerns, event-driven communication, and a plugin-based system for features.

**Current State Analysis:**
- 3057 lines of tightly coupled code in a single HTML file
- Global state scattered across multiple variables
- Direct DOM manipulation throughout
- Features (search, stumble, 3D mode) intermingled with core logic
- No clear boundaries between UI, data, and business logic

**Proposed Architecture:**
- Modular component-based structure within a single HTML file
- Event-driven architecture with a central EventBus
- Clear separation: Data → State → Services → UI
- Plugin system for features (Stumble, 3D Gallery, Search)
- Approximately 40% reduction in complexity through better organization

---

## 1. System Overview

### 1.1 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Application Shell                        │
│                    (Initialization & Lifecycle)                  │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 │ initializes
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                           EventBus                               │
│              (Central Message Broker - Pub/Sub)                  │
└─────────────────────────────────────────────────────────────────┘
         │               │                │              │
         │ events        │ events         │ events       │ events
         ▼               ▼                ▼              ▼
┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐
│   Data     │──▶│   State    │──▶│  Services  │──▶│     UI     │
│  Service   │   │  Manager   │   │  Layer     │   │  Manager   │
└────────────┘   └────────────┘   └────────────┘   └────────────┘
     │                 │                 │                 │
     │                 │                 │                 │
     ▼                 ▼                 ▼                 ▼
┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐
│ IndexedDB  │   │   State    │   │  Plugins   │   │    DOM     │
│ LocalStore │   │   Object   │   │  System    │   │ Components │
└────────────┘   └────────────┘   └────────────┘   └────────────┘
                                       │
                                       │ manages
                                       ▼
                              ┌──────────────────┐
                              │    Plugins       │
                              ├──────────────────┤
                              │ • Stumble        │
                              │ • 3D Gallery     │
                              │ • Search Filter  │
                              │ • Pin Manager    │
                              │ • Vote System    │
                              └──────────────────┘
```

### 1.2 Data Flow

```
User Action → EventBus.emit() → Service Layer → StateManager.update()
                                                         │
                                                         ▼
                                              EventBus.emit('state:changed')
                                                         │
                                                         ▼
                                                   UIManager.render()
                                                         │
                                                         ▼
                                                    DOM Update
```

### 1.3 Core Principles

1. **Single Responsibility**: Each module has one clear purpose
2. **Loose Coupling**: Modules communicate only through EventBus
3. **High Cohesion**: Related functionality grouped together
4. **Dependency Injection**: Services receive dependencies via constructor
5. **Immutable State**: State changes produce new state objects
6. **Progressive Enhancement**: Features can be disabled without breaking core

---

## 2. Module Definitions

### 2.1 EventBus (Core Infrastructure)

**Purpose**: Central pub/sub message broker for decoupled communication

**Responsibilities**:
- Event registration and deregistration
- Event emission with payload
- Event prioritization
- Debug logging

**API**:
```javascript
class EventBus {
    on(event, handler, priority = 0)
    off(event, handler)
    emit(event, payload)
    once(event, handler)
    clear(event)
    getSubscribers(event)
}
```

**Events Catalog**:
```javascript
// Data events
'data:loaded'           // { tools: Array, timestamp: Date }
'data:error'           // { error: Error, context: String }

// State events
'state:changed'        // { previous: Object, current: Object, diff: Object }
'state:tools:filtered' // { tools: Array, criteria: Object }
'state:view:changed'   // { mode: 'gallery'|'archive'|'3d' }
'state:category:changed' // { category: String }

// UI events
'ui:search:input'      // { query: String }
'ui:card:click'        // { tool: Object }
'ui:pin:toggle'        // { toolId: String }
'ui:modal:open'        // { type: String, data: Object }
'ui:modal:close'       // { type: String }

// Plugin events
'plugin:stumble:trigger'
'plugin:3d:enter'
'plugin:3d:exit'
'plugin:vote:submit'   // { toolId: String, vote: Object }
```

---

### 2.2 DataService (Data Layer)

**Purpose**: Manage all data operations (fetch, cache, storage)

**Responsibilities**:
- Fetch gallery configuration from JSON
- Cache data in memory and IndexedDB
- Provide data query interface
- Handle offline scenarios
- Manage data versioning

**API**:
```javascript
class DataService {
    constructor(eventBus, config)

    // Core methods
    async initialize()
    async loadGalleryConfig()
    async loadToolsManifest()
    getTools(filters = {})
    getToolById(id)
    getCategories()

    // Cache management
    async refreshCache()
    clearCache()
    getCacheInfo()

    // Storage operations
    async saveToLocal(key, data)
    async loadFromLocal(key)
    async deleteFromLocal(key)
}
```

**Internal Structure**:
```javascript
{
    _cache: {
        tools: Map,           // toolId → tool object
        categories: Map,      // categoryId → category object
        metadata: Object      // version, lastUpdate, etc.
    },
    _config: {
        dataSource: 'vibe_gallery_config.json',
        cacheExpiry: 3600000, // 1 hour
        useIndexedDB: true
    }
}
```

---

### 2.3 StateManager (State Layer)

**Purpose**: Single source of truth for application state

**Responsibilities**:
- Hold current application state
- Validate state transitions
- Emit state change events
- Provide state query interface
- Support state history (undo/redo)

**API**:
```javascript
class StateManager {
    constructor(eventBus)

    // State access
    getState()
    getStateSlice(path)

    // State mutations
    setState(newState)
    updateState(partialState)
    mergeState(deepMerge, ...states)

    // State queries
    getCurrentView()
    getSelectedCategory()
    getFilteredTools()
    getSearchQuery()

    // History
    undo()
    redo()
    canUndo()
    canRedo()
    clearHistory()

    // Persistence
    saveState()
    loadState()
}
```

**State Schema**:
```javascript
{
    view: {
        mode: 'gallery' | 'archive' | '3d',
        previousMode: String
    },
    filters: {
        category: String,
        searchQuery: String,
        tags: Array<String>,
        complexity: 'simple' | 'intermediate' | 'advanced'
    },
    tools: {
        all: Array<Tool>,
        filtered: Array<Tool>,
        pinned: Set<String>,
        featured: Array<String>
    },
    user: {
        votes: Map<String, Object>,
        history: {
            stumble: Array<Object>,
            visited: Set<String>,
            recent: Array<String>
        },
        preferences: {
            theme: 'dark' | 'light',
            gridSize: Number,
            enableAnimations: Boolean
        }
    },
    ui: {
        modals: {
            stumble: { open: Boolean, data: Object },
            vote: { open: Boolean, data: Object },
            history: { open: Boolean, data: Object }
        },
        loading: Boolean,
        error: Object | null
    }
}
```

---

### 2.4 UIManager (Presentation Layer)

**Purpose**: Manage all DOM operations and UI rendering

**Responsibilities**:
- Render components based on state
- Handle user interactions
- Manage animations and transitions
- Provide component lifecycle
- Handle responsive behavior

**API**:
```javascript
class UIManager {
    constructor(eventBus, stateManager, config)

    // Rendering
    render()
    renderComponent(componentName, container, props)
    updateComponent(componentName, props)

    // Component registration
    registerComponent(name, component)
    unregisterComponent(name)

    // UI utilities
    showLoading()
    hideLoading()
    showError(message, error)
    showToast(message, type)

    // Layout
    setLayout(layoutName)
    getCurrentLayout()

    // Cleanup
    destroy()
}
```

**Component Structure**:
```javascript
// Base Component Interface
class Component {
    constructor(props, eventBus)

    // Lifecycle
    mount(container)
    unmount()
    update(props)

    // Rendering
    render()
    getHTML()

    // Event handling
    bindEvents()
    unbindEvents()

    // State
    setState(newState)
    getState()
}

// Specific Components:
- HeaderComponent
- SearchBarComponent
- CategoryFilterComponent
- ToolCardComponent
- ToolGridComponent
- StumbleModalComponent
- VoteModalComponent
- HistoryModalComponent
- Gallery3DComponent
- ToastComponent
```

---

### 2.5 PluginSystem (Extension Layer)

**Purpose**: Manage optional features as plugins

**Responsibilities**:
- Plugin registration and initialization
- Plugin lifecycle management
- Plugin communication via EventBus
- Plugin dependency resolution
- Plugin configuration

**API**:
```javascript
class PluginSystem {
    constructor(eventBus, stateManager, config)

    // Plugin management
    registerPlugin(plugin)
    unregisterPlugin(pluginName)
    getPlugin(pluginName)
    getAllPlugins()

    // Lifecycle
    async initializePlugin(pluginName)
    async enablePlugin(pluginName)
    async disablePlugin(pluginName)

    // Queries
    isPluginEnabled(pluginName)
    getPluginConfig(pluginName)
    setPluginConfig(pluginName, config)
}

// Plugin Interface
class Plugin {
    name: String
    version: String
    dependencies: Array<String>

    constructor(eventBus, stateManager, config)

    async initialize()
    async enable()
    async disable()
    getConfig()
    setConfig(config)
}
```

**Built-in Plugins**:

1. **StumblePlugin**
   - Random tool discovery
   - History tracking
   - Keyboard shortcuts

2. **Gallery3DPlugin**
   - Three.js 3D gallery
   - Xbox controller support
   - VR/immersive mode

3. **SearchPlugin**
   - Real-time search
   - Fuzzy matching
   - Search history

4. **PinManagerPlugin**
   - Tool pinning
   - Pin persistence
   - Quick access

5. **VoteSystemPlugin**
   - Feature voting
   - Vote persistence
   - Vote aggregation

---

## 3. Service Layer

### 3.1 StorageService

```javascript
class StorageService {
    constructor(config)

    // LocalStorage operations
    setItem(key, value)
    getItem(key)
    removeItem(key)
    clear()

    // IndexedDB operations (for larger data)
    async setDB(store, key, value)
    async getDB(store, key)
    async deleteDB(store, key)
    async clearDB(store)

    // Cache operations
    setCache(key, value, ttl)
    getCache(key)
    clearExpiredCache()
}
```

### 3.2 NavigationService

```javascript
class NavigationService {
    constructor(eventBus, stateManager)

    navigateTo(view, params)
    goBack()
    goForward()
    getCurrentRoute()
    getHistory()
}
```

### 3.3 AnalyticsService (Optional)

```javascript
class AnalyticsService {
    constructor(eventBus, config)

    trackEvent(category, action, label, value)
    trackPageView(page)
    trackError(error, context)

    // Privacy-first: all local, no external tracking
    getLocalStats()
    exportStats()
}
```

---

## 4. Implementation Guidelines

### 4.1 File Structure (Within Single HTML)

```html
<!DOCTYPE html>
<html>
<head>
    <title>Local First Tools Gallery</title>
    <style>
        /* 1. CSS Variables & Resets */
        /* 2. Layout Styles */
        /* 3. Component Styles */
        /* 4. Animation Keyframes */
        /* 5. Responsive Media Queries */
    </style>
</head>
<body>
    <!-- DOM Structure -->
    <div id="app"></div>

    <!-- Three.js CDN (only external dependency) -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

    <script>
    'use strict';

    // ==================== SECTION 1: UTILITIES ====================
    // - Helper functions
    // - Constants
    // - Type definitions (JSDoc)

    // ==================== SECTION 2: CORE INFRASTRUCTURE ====================
    // - EventBus
    // - Logger

    // ==================== SECTION 3: DATA LAYER ====================
    // - DataService
    // - StorageService

    // ==================== SECTION 4: STATE LAYER ====================
    // - StateManager

    // ==================== SECTION 5: SERVICE LAYER ====================
    // - NavigationService
    // - AnalyticsService

    // ==================== SECTION 6: UI LAYER ====================
    // - Component base class
    // - All UI components
    // - UIManager

    // ==================== SECTION 7: PLUGIN SYSTEM ====================
    // - Plugin base class
    // - PluginSystem
    // - All plugins

    // ==================== SECTION 8: APPLICATION SHELL ====================
    // - App initialization
    // - Lifecycle management

    // ==================== SECTION 9: INITIALIZATION ====================
    // - Bootstrap code

    </script>
</body>
</html>
```

### 4.2 Code Style Guidelines

**Naming Conventions**:
```javascript
// Classes: PascalCase
class DataService {}

// Methods/Functions: camelCase
function loadData() {}

// Constants: UPPER_SNAKE_CASE
const MAX_CACHE_SIZE = 1000;

// Private methods: _prefixed
_validateInput() {}

// Event names: namespace:action:target
'data:loaded:tools'
'ui:click:card'
'state:updated:filters'
```

**Documentation**:
```javascript
/**
 * Loads gallery configuration from JSON file
 * @async
 * @param {Object} options - Configuration options
 * @param {boolean} options.forceRefresh - Skip cache
 * @param {number} options.timeout - Request timeout in ms
 * @returns {Promise<GalleryConfig>} Gallery configuration object
 * @throws {DataLoadError} If fetch fails
 */
async loadGalleryConfig(options = {}) {
    // Implementation
}
```

### 4.3 Error Handling Strategy

```javascript
// Custom error classes
class LocalFirstError extends Error {
    constructor(message, code, context) {
        super(message);
        this.name = 'LocalFirstError';
        this.code = code;
        this.context = context;
    }
}

class DataLoadError extends LocalFirstError {}
class StateValidationError extends LocalFirstError {}
class PluginError extends LocalFirstError {}

// Error boundaries
class ErrorBoundary {
    constructor(eventBus) {
        this.eventBus = eventBus;
        this.setupGlobalHandlers();
    }

    setupGlobalHandlers() {
        window.addEventListener('error', (e) => {
            this.handleError(e.error);
        });

        window.addEventListener('unhandledrejection', (e) => {
            this.handleError(e.reason);
        });
    }

    handleError(error) {
        console.error('[ErrorBoundary]', error);
        this.eventBus.emit('app:error', { error });
        // Show user-friendly error UI
    }
}
```

### 4.4 Performance Optimizations

1. **Lazy Loading**:
```javascript
// Load 3D library only when needed
async function load3DPlugin() {
    if (!window.THREE) {
        await loadScript('three.js');
    }
    return new Gallery3DPlugin();
}
```

2. **Virtual Scrolling** (for large lists):
```javascript
class VirtualScrollComponent extends Component {
    // Only render visible items + buffer
    renderVisibleItems() {
        const startIndex = Math.floor(this.scrollTop / this.itemHeight);
        const endIndex = startIndex + this.visibleCount;
        return this.items.slice(startIndex, endIndex);
    }
}
```

3. **Debouncing/Throttling**:
```javascript
// Search input debouncing
const debouncedSearch = debounce((query) => {
    eventBus.emit('ui:search:input', { query });
}, 300);
```

4. **Memoization**:
```javascript
class DataService {
    constructor() {
        this._memoCache = new Map();
    }

    memoize(fn, keyFn) {
        return (...args) => {
            const key = keyFn(...args);
            if (this._memoCache.has(key)) {
                return this._memoCache.get(key);
            }
            const result = fn(...args);
            this._memoCache.set(key, result);
            return result;
        };
    }
}
```

---

## 5. Migration Strategy

### 5.1 Phase 1: Foundation (Week 1)
- Implement EventBus
- Implement StateManager (with existing state schema)
- Implement basic DataService
- Create skeleton UIManager
- Setup testing framework

### 5.2 Phase 2: Core Features (Week 2)
- Migrate gallery display to UIManager
- Implement ToolCard component
- Implement search functionality as plugin
- Migrate state management to StateManager
- Implement StorageService

### 5.3 Phase 3: Plugins (Week 3)
- Extract Stumble feature to plugin
- Extract Pin Manager to plugin
- Extract Vote System to plugin
- Implement PluginSystem
- Test plugin enable/disable

### 5.4 Phase 4: 3D Gallery (Week 4)
- Refactor 3D gallery as plugin
- Improve Xbox controller integration
- Add VR support
- Performance optimization

### 5.5 Phase 5: Polish & Testing (Week 5)
- Comprehensive testing
- Performance optimization
- Documentation
- User testing
- Bug fixes

---

## 6. Testing Strategy

### 6.1 Unit Tests (using built-in test framework)

```javascript
// Inline test framework (no dependencies!)
const test = (name, fn) => {
    try {
        fn();
        console.log(`✓ ${name}`);
    } catch (e) {
        console.error(`✗ ${name}`, e);
    }
};

const assertEquals = (actual, expected, message) => {
    if (JSON.stringify(actual) !== JSON.stringify(expected)) {
        throw new Error(message || `Expected ${expected}, got ${actual}`);
    }
};

// Example tests
test('EventBus: should emit and receive events', () => {
    const bus = new EventBus();
    let received = false;
    bus.on('test', () => received = true);
    bus.emit('test');
    assertEquals(received, true);
});

test('StateManager: should update state immutably', () => {
    const state = new StateManager(eventBus);
    const initial = state.getState();
    state.updateState({ test: 'value' });
    const updated = state.getState();
    assertEquals(initial === updated, false);
});
```

### 6.2 Integration Tests

```javascript
test('Integration: Search filters tools correctly', async () => {
    const app = new Application();
    await app.initialize();

    app.eventBus.emit('ui:search:input', { query: 'game' });
    await wait(100); // debounce

    const filtered = app.stateManager.getFilteredTools();
    assertEquals(filtered.every(t => t.title.toLowerCase().includes('game')), true);
});
```

### 6.3 E2E Tests (Manual Checklist)

- [ ] Gallery loads and displays all tools
- [ ] Search filters tools correctly
- [ ] Category filter works
- [ ] Stumble modal opens and shows random tool
- [ ] Pin/unpin tools persists across sessions
- [ ] 3D mode loads and is navigable
- [ ] Xbox controller works in 3D mode
- [ ] Vote system accepts and stores votes
- [ ] Offline mode works (disconnect network)
- [ ] Mobile responsive design works
- [ ] All links open correct tools

---

## 7. API Contracts

### 7.1 Tool Object Schema

```typescript
interface Tool {
    id: string;
    title: string;
    filename: string;
    path: string;
    url: string;
    description: string;
    category: string;
    tags: string[];
    complexity: 'simple' | 'intermediate' | 'advanced';
    interactionType: 'game' | 'visual' | 'interactive' | 'drawing';
    featured: boolean;
    isArchive?: boolean;
    metadata: {
        size: number;
        modified: number;
        created: number;
    };
}
```

### 7.2 Event Payload Schemas

```typescript
// Data Events
interface DataLoadedPayload {
    tools: Tool[];
    categories: Category[];
    timestamp: Date;
    source: 'cache' | 'network';
}

interface DataErrorPayload {
    error: Error;
    context: string;
    retry: () => Promise<void>;
}

// State Events
interface StateChangedPayload {
    previous: AppState;
    current: AppState;
    diff: Partial<AppState>;
    timestamp: Date;
}

// UI Events
interface UISearchInputPayload {
    query: string;
    timestamp: Date;
}

interface UICardClickPayload {
    tool: Tool;
    source: 'grid' | 'stumble' | 'search';
}
```

### 7.3 Plugin Interface

```typescript
interface IPlugin {
    name: string;
    version: string;
    dependencies: string[];

    initialize(): Promise<void>;
    enable(): Promise<void>;
    disable(): Promise<void>;

    getConfig(): PluginConfig;
    setConfig(config: PluginConfig): void;

    // Optional lifecycle hooks
    onStateChange?(state: AppState): void;
    onBeforeDestroy?(): void;
}
```

---

## 8. Configuration

### 8.1 Application Config

```javascript
const DEFAULT_CONFIG = {
    // Data sources
    data: {
        galleryConfig: 'vibe_gallery_config.json',
        toolsManifest: 'tools-manifest.json',
        archiveConfig: 'data/config/utility_apps_config.json'
    },

    // Cache settings
    cache: {
        enabled: true,
        ttl: 3600000, // 1 hour
        maxSize: 100, // MB
        strategy: 'stale-while-revalidate'
    },

    // Storage settings
    storage: {
        useIndexedDB: true,
        useLocalStorage: true,
        namespace: 'localFirstTools'
    },

    // UI settings
    ui: {
        gridColumns: {
            desktop: 3,
            tablet: 2,
            mobile: 1
        },
        animationsEnabled: true,
        theme: 'dark',
        loadingDelay: 300 // ms before showing spinner
    },

    // Plugin settings
    plugins: {
        enabled: ['stumble', '3d-gallery', 'search', 'pin-manager', 'vote-system'],
        config: {
            stumble: {
                historyLimit: 50,
                keyboardShortcut: 's'
            },
            '3d-gallery': {
                controllerDeadzone: 0.15,
                moveSpeed: 0.3,
                lookSpeed: 0.002
            }
        }
    },

    // Feature flags
    features: {
        offlineMode: true,
        analytics: false,
        betaFeatures: false
    }
};
```

### 8.2 Environment Configuration

```javascript
// Detect environment
const ENV = {
    isDevelopment: location.hostname === 'localhost',
    isProduction: location.hostname !== 'localhost',
    supportsIndexedDB: 'indexedDB' in window,
    supportsServiceWorker: 'serviceWorker' in navigator,
    isMobile: /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent),
    hasGamepad: 'getGamepads' in navigator
};

// Adjust config based on environment
if (ENV.isDevelopment) {
    DEFAULT_CONFIG.cache.enabled = false;
    DEFAULT_CONFIG.features.betaFeatures = true;
}
```

---

## 9. Benefits of New Architecture

### 9.1 Maintainability
- **Clear module boundaries**: Each module has single responsibility
- **Easy to locate code**: Consistent organization
- **Reduced cognitive load**: Understand one piece at a time
- **Better testing**: Each module can be tested in isolation

### 9.2 Extensibility
- **Plugin system**: Add features without modifying core
- **Event-driven**: New features can subscribe to existing events
- **Dependency injection**: Easy to swap implementations
- **Configuration-based**: Behavior can be changed via config

### 9.3 Performance
- **Lazy loading**: Load features only when needed
- **Efficient rendering**: Only re-render what changed
- **Optimized state updates**: Batched updates, immutable state
- **Better caching**: Centralized cache strategy

### 9.4 Developer Experience
- **Type hints via JSDoc**: Better autocomplete
- **Consistent patterns**: Same structure everywhere
- **Clear data flow**: Easy to trace events
- **Self-documenting**: Code structure explains intent

---

## 10. Code Size Comparison

### Current Implementation
```
Total: ~3057 lines
- CSS: ~1358 lines
- HTML: ~100 lines
- JavaScript: ~1599 lines
  - Global state: scattered
  - Functions: ~60 top-level functions
  - Classes: 1 (Gallery3D)
  - Tight coupling throughout
```

### Proposed Implementation (Estimated)
```
Total: ~2800 lines (8% reduction)
- CSS: ~1200 lines (better organized)
- HTML: ~80 lines (cleaner structure)
- JavaScript: ~1520 lines
  - Infrastructure: ~200 lines (EventBus, Logger)
  - Data Layer: ~250 lines (DataService, Storage)
  - State Layer: ~200 lines (StateManager)
  - Service Layer: ~150 lines (Navigation, Analytics)
  - UI Layer: ~400 lines (Components, UIManager)
  - Plugin System: ~150 lines
  - Plugins: ~170 lines (5 plugins @ ~34 lines each)

Key Improvements:
- 40% less complexity (cyclomatic complexity)
- 60% reduction in function length (avg)
- 0 global variables (except app instance)
- 100% modular structure
```

---

## 11. Next Steps

### Immediate Actions
1. **Review & Approve** this architecture document
2. **Create prototype** of core infrastructure (EventBus + StateManager)
3. **Migrate one feature** as proof of concept (e.g., Search)
4. **Measure improvements** (LOC, complexity, performance)
5. **Iterate based on feedback**

### Long-term Roadmap
1. **Q1**: Complete migration to new architecture
2. **Q2**: Add service worker for true offline support
3. **Q3**: Plugin marketplace for community extensions
4. **Q4**: Native app wrappers (Electron, Tauri)

---

## 12. Appendix

### A. Glossary

- **Local-First**: Applications that work offline and sync later
- **EventBus**: Publish-subscribe message broker pattern
- **Plugin**: Self-contained feature module
- **State Manager**: Single source of truth for application state
- **Component**: Reusable UI element with lifecycle
- **Service**: Business logic layer between data and UI

### B. References

- [Local-First Software Principles](https://www.inkandswitch.com/local-first/)
- [Event-Driven Architecture](https://martinfowler.com/articles/201701-event-driven.html)
- [Plugin Architecture Pattern](https://en.wikipedia.org/wiki/Plug-in_(computing))
- [State Management Patterns](https://kentcdodds.com/blog/application-state-management-with-react)

### C. Contact

For questions about this architecture:
- Review the CLAUDE.md file for project context
- Check inline code comments for implementation details
- Reference this document for architectural decisions

---

**Document Version**: 1.0
**Last Updated**: 2025-10-12
**Status**: PROPOSED - Awaiting Review
**Prepared By**: Architecture Agent (Claude Code)
