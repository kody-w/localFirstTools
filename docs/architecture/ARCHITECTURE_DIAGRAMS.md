# Local First Tools Gallery - Architecture Diagrams

## 1. High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                          SINGLE HTML FILE                               │
│                    (No External Dependencies)                           │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                                                                   │ │
│  │                     APPLICATION SHELL                             │ │
│  │              (Bootstrap, Lifecycle, Error Handling)               │ │
│  │                                                                   │ │
│  └────────────────────────┬──────────────────────────────────────────┘ │
│                           │                                            │
│                           │ initializes                                │
│                           ▼                                            │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                                                                   │ │
│  │                         EVENT BUS                                 │ │
│  │                  (Pub/Sub Message Broker)                         │ │
│  │                                                                   │ │
│  └─────────┬──────────┬──────────┬──────────┬──────────┬────────────┘ │
│            │          │          │          │          │              │
│    ┌───────┴─────┐ ┌──┴────┐ ┌──┴────┐ ┌──┴────┐ ┌───┴──────┐       │
│    │             │ │       │ │       │ │       │ │          │       │
│    │    DATA     │ │ STATE │ │SERVICE│ │   UI  │ │ PLUGINS  │       │
│    │   SERVICE   │ │ MNGR  │ │ LAYER │ │ MNGR  │ │  SYSTEM  │       │
│    │             │ │       │ │       │ │       │ │          │       │
│    └─────────────┘ └───────┘ └───────┘ └───────┘ └──────────┘       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Interaction Flow

### 2.1 User Searches for Tools

```
┌──────┐
│ User │ types "game"
└───┬──┘
    │
    ▼
┌─────────────────┐
│ SearchBar       │ (Component)
│ Component       │──────────┐
└─────────────────┘          │
                             │ emits 'ui:search:input'
                             ▼
                    ┌──────────────┐
                    │  Event Bus   │
                    └───────┬──────┘
                            │ forwards event
                            ▼
                    ┌──────────────┐
                    │ SearchPlugin │
                    └───────┬──────┘
                            │ filters tools
                            ▼
                    ┌──────────────┐
                    │StateManager  │ updates state.filters
                    └───────┬──────┘
                            │ emits 'state:changed'
                            ▼
                    ┌──────────────┐
                    │  Event Bus   │
                    └───────┬──────┘
                            │ forwards event
                            ▼
                    ┌──────────────┐
                    │  UI Manager  │ re-renders grid
                    └───────┬──────┘
                            │
                            ▼
                    ┌──────────────┐
                    │ ToolGrid     │ shows filtered
                    │ Component    │ results
                    └──────────────┘
```

### 2.2 User Opens 3D Mode

```
┌──────┐
│ User │ clicks "3D Experience"
└───┬──┘
    │
    ▼
┌─────────────────┐
│ ModeButton      │
│ Component       │─────────┐
└─────────────────┘         │ emits 'ui:mode:3d'
                            ▼
                   ┌──────────────┐
                   │  Event Bus   │
                   └───────┬──────┘
                           │
                           ▼
                   ┌──────────────┐
                   │ PluginSystem │ checks if enabled
                   └───────┬──────┘
                           │
                           ▼
                   ┌──────────────┐
                   │ 3D Plugin    │ initialize()
                   └───────┬──────┘
                           │
                           ├─────────────────┐
                           │                 │
                           ▼                 ▼
                   ┌──────────────┐  ┌──────────────┐
                   │StateManager  │  │ Three.js     │
                   │mode: '3d'    │  │ Scene Setup  │
                   └───────┬──────┘  └───────┬──────┘
                           │                 │
                           │ emits           │ renders
                           │ 'state:changed' │
                           ▼                 ▼
                   ┌──────────────┐  ┌──────────────┐
                   │  UI Manager  │  │ 3D Canvas    │
                   │ hide gallery │  │ show scene   │
                   └──────────────┘  └──────────────┘
```

---

## 3. Data Flow Architecture

### 3.1 Cold Start (Initial Load)

```
┌──────────────┐
│ Page Load    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Application  │ new Application()
│ Shell        │
└──────┬───────┘
       │ app.initialize()
       │
       ├────────────────────────────────────────────┐
       │                                            │
       ▼                                            ▼
┌──────────────┐                            ┌──────────────┐
│  EventBus    │                            │ StateManager │
│ initialize() │                            │ initialize() │
└──────────────┘                            └──────────────┘
       │                                            │
       │                                            │
       ▼                                            ▼
┌──────────────┐                            ┌──────────────┐
│ DataService  │                            │ loadState()  │
│ initialize() │                            │ from storage │
└──────┬───────┘                            └──────────────┘
       │
       │ try cache first
       ▼
┌──────────────┐
│ Storage      │ getCached('gallery')
│ Service      │
└──────┬───────┘
       │
       ├──────────── if cached ─────────┐
       │                                │
       │ if not cached                  │
       │ or expired                     │
       ▼                                ▼
┌──────────────┐              ┌──────────────┐
│ Fetch        │              │ Return       │
│ gallery.json │              │ Cached Data  │
└──────┬───────┘              └──────┬───────┘
       │                             │
       │ success                     │
       │                             │
       └─────────────┬───────────────┘
                     │
                     ▼
              ┌──────────────┐
              │ emit         │
              │'data:loaded' │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │ StateManager │ setState({ tools })
              └──────┬───────┘
                     │
                     │ emit 'state:changed'
                     ▼
              ┌──────────────┐
              │ UI Manager   │ render()
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │ Gallery      │ displays tools
              │ Displayed    │
              └──────────────┘
```

### 3.2 Warm Start (Has Cache)

```
┌──────────────┐
│ Page Load    │ (2nd+ visit)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ DataService  │ loadFromCache()
└──────┬───────┘
       │ cache hit!
       │ instant load (<50ms)
       ▼
┌──────────────┐
│ UI Renders   │ show cached data
└──────┬───────┘
       │
       │ background refresh
       ▼
┌──────────────┐
│ Check for    │ fetch gallery.json
│ Updates      │ (stale-while-revalidate)
└──────┬───────┘
       │
       ├─── if changed ───┐
       │                  │
       │ if same          │
       ▼                  ▼
┌──────────────┐  ┌──────────────┐
│ Do Nothing   │  │ Update Cache │
└──────────────┘  └──────┬───────┘
                         │
                         │ emit 'data:updated'
                         ▼
                  ┌──────────────┐
                  │ Show Toast   │
                  │ "New tools   │
                  │  available!" │
                  └──────────────┘
```

---

## 4. State Management Flow

### 4.1 State Update Cycle

```
┌─────────────────────────────────────────────────────────────┐
│                     STATE UPDATE CYCLE                       │
└─────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │   Action    │ (user clicks, API call, timer)
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │  EventBus   │ emit('ui:action')
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │   Service   │ (business logic)
    │   or Plugin │
    └──────┬──────┘
           │
           │ prepares new state
           ▼
    ┌─────────────┐
    │ StateManager│ updateState(newState)
    └──────┬──────┘
           │
           │ validates & merges
           │
           ├─────────────────────┐
           │                     │
           ▼                     ▼
    ┌─────────────┐      ┌─────────────┐
    │ Save to     │      │ Add to      │
    │ History     │      │ State Stack │
    └─────────────┘      └─────────────┘
           │                     │
           └──────────┬──────────┘
                      │
                      ▼
               ┌─────────────┐
               │  EventBus   │ emit('state:changed')
               └──────┬──────┘
                      │
                      ▼
               ┌─────────────┐
               │ UI Manager  │ render()
               └──────┬──────┘
                      │
                      ▼
               ┌─────────────┐
               │ DOM Updates │ (only diffs)
               └─────────────┘
```

### 4.2 State Object Structure

```
AppState
├── view
│   ├── mode: 'gallery' | 'archive' | '3d'
│   └── previousMode: string
│
├── filters
│   ├── category: string
│   ├── searchQuery: string
│   ├── tags: string[]
│   └── complexity: string
│
├── tools
│   ├── all: Tool[]
│   ├── filtered: Tool[]
│   ├── pinned: Set<string>
│   └── featured: string[]
│
├── user
│   ├── votes: Map<string, Vote>
│   ├── history
│   │   ├── stumble: StumbleEntry[]
│   │   ├── visited: Set<string>
│   │   └── recent: string[]
│   └── preferences
│       ├── theme: 'dark' | 'light'
│       ├── gridSize: number
│       └── enableAnimations: boolean
│
└── ui
    ├── modals
    │   ├── stumble: { open: bool, data: Object }
    │   ├── vote: { open: bool, data: Object }
    │   └── history: { open: bool, data: Object }
    ├── loading: boolean
    └── error: Error | null
```

---

## 5. Plugin System Architecture

### 5.1 Plugin Lifecycle

```
┌──────────────────────────────────────────────────────────┐
│                    PLUGIN LIFECYCLE                       │
└──────────────────────────────────────────────────────────┘

┌─────────────┐
│ Plugin Code │ (class definition)
└──────┬──────┘
       │
       │ PluginSystem.register()
       ▼
┌─────────────┐
│ REGISTERED  │ (stored, not running)
└──────┬──────┘
       │
       │ PluginSystem.initialize()
       │
       ├────── check dependencies ────┐
       │                              │
       │ all present                  │ missing
       ▼                              ▼
┌─────────────┐              ┌─────────────┐
│INITIALIZING │              │   ERROR     │
└──────┬──────┘              └─────────────┘
       │
       │ plugin.initialize()
       │ • setup event listeners
       │ • load config
       │ • prepare resources
       ▼
┌─────────────┐
│ INITIALIZED │ (ready, but not active)
└──────┬──────┘
       │
       │ PluginSystem.enable()
       │
       │ plugin.enable()
       │ • subscribe to events
       │ • show UI elements
       │ • start background tasks
       ▼
┌─────────────┐
│   ENABLED   │◄────────────┐
└──────┬──────┘             │
       │                    │
       │ PluginSystem.      │ PluginSystem.
       │ disable()          │ enable()
       │                    │
       │ plugin.disable()   │
       │ • unsubscribe      │
       │ • hide UI          │
       │ • stop tasks       │
       ▼                    │
┌─────────────┐             │
│  DISABLED   │─────────────┘
└──────┬──────┘
       │
       │ PluginSystem.unregister()
       │
       │ plugin.cleanup()
       │ • remove all listeners
       │ • clear resources
       ▼
┌─────────────┐
│  DESTROYED  │
└─────────────┘
```

### 5.2 Plugin Communication

```
┌─────────────────────────────────────────────────────────────┐
│              PLUGIN COMMUNICATION PATTERNS                   │
└─────────────────────────────────────────────────────────────┘

PATTERN 1: Plugin → Core
┌─────────────┐
│   Plugin    │ emit('plugin:action')
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  EventBus   │ route event
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ StateManager│ handle & update
└─────────────┘


PATTERN 2: Core → Plugin
┌─────────────┐
│StateManager │ emit('state:changed')
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  EventBus   │ broadcast
└──────┬──────┘
       │
       ├────────┬────────┬────────┐
       │        │        │        │
       ▼        ▼        ▼        ▼
   ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
   │Plugin│ │Plugin│ │Plugin│ │Plugin│
   │  1   │ │  2   │ │  3   │ │  4   │
   └──────┘ └──────┘ └──────┘ └──────┘


PATTERN 3: Plugin → Plugin (via EventBus)
┌─────────────┐
│  Plugin A   │ emit('pluginA:ready')
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  EventBus   │ route
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Plugin B   │ on('pluginA:ready', ...)
└─────────────┘


PATTERN 4: Plugin Dependencies
┌─────────────┐
│ PluginSystem│
└──────┬──────┘
       │
       │ Plugin B depends on Plugin A
       │
       ├─── initialize A first ────┐
       │                           │
       ▼                           │
   ┌──────┐                        │
   │Plugin│ enable()               │
   │  A   │────────────────────────┘
   └──────┘ emit('pluginA:ready')
       │
       │ wait for ready
       ▼
   ┌──────┐
   │Plugin│ enable()
   │  B   │ (can safely use A)
   └──────┘
```

---

## 6. Component Hierarchy

### 6.1 UI Component Tree

```
App
│
├── HeaderComponent
│   ├── TitleComponent
│   ├── SubtitleComponent
│   └── DescriptionComponent
│
├── SearchBarComponent
│   ├── InputComponent
│   └── IconComponent
│
├── ControlsComponent
│   ├── StumbleButtonComponent
│   ├── CategoryFilterComponent
│   │   └── DropdownComponent
│   ├── HistoryButtonComponent
│   └── ModeButtonsComponent
│       ├── GalleryModeButton
│       ├── ArchiveModeButton
│       └── ThreeDModeButton
│
├── MainContentComponent
│   ├── LoadingComponent
│   ├── ErrorComponent
│   ├── GalleryViewComponent
│   │   ├── SectionComponent (multiple)
│   │   │   ├── SectionTitleComponent
│   │   │   └── ToolGridComponent
│   │   │       └── ToolCardComponent (multiple)
│   │   │           ├── PinButtonComponent
│   │   │           ├── PreviewComponent
│   │   │           ├── TitleComponent
│   │   │           ├── DescriptionComponent
│   │   │           ├── MetaComponent
│   │   │           └── ActionsComponent
│   │   │               ├── ViewButton
│   │   │               ├── VoteButton
│   │   │               └── DownloadButton
│   │   │
│   │   └── ArchiveViewComponent (similar structure)
│   │
│   └── ThreeDViewComponent
│       ├── Canvas3DComponent
│       ├── BackButtonComponent
│       ├── GamepadStatusComponent
│       ├── ControlsHintComponent
│       ├── MobileControlsComponent
│       └── TooltipComponent
│
├── ModalManagerComponent
│   ├── StumbleModalComponent
│   │   ├── ModalHeaderComponent
│   │   ├── ModalBodyComponent
│   │   └── ModalActionsComponent
│   │
│   ├── VoteModalComponent
│   │   ├── VoteFormComponent
│   │   └── VoteActionsComponent
│   │
│   └── HistoryModalComponent
│       └── HistoryListComponent
│           └── HistoryItemComponent (multiple)
│
├── ToastComponent
│
└── FooterComponent
    ├── StatsComponent
    └── GitHubLinkComponent
```

### 6.2 Component Lifecycle Hooks

```
┌─────────────────────────────────────────────────────┐
│             COMPONENT LIFECYCLE                      │
└─────────────────────────────────────────────────────┘

┌─────────────┐
│ constructor │ new Component(props, eventBus)
└──────┬──────┘ • initialize properties
       │        • bind event handlers
       │        • setup initial state
       ▼
┌─────────────┐
│   mount()   │ component.mount(container)
└──────┬──────┘ • create DOM elements
       │        • insert into container
       │        • subscribe to events
       │        • start animations
       ▼
┌─────────────┐
│  mounted    │ (component is visible & interactive)
└──────┬──────┘
       │
       │ props change
       ▼
┌─────────────┐
│  update()   │ component.update(newProps)
└──────┬──────┘ • diff props
       │        • update DOM
       │        • re-render if needed
       ▼
┌─────────────┐
│  updated    │
└──────┬──────┘
       │
       │ component removed
       ▼
┌─────────────┐
│  unmount()  │ component.unmount()
└──────┬──────┘ • unsubscribe events
       │        • remove DOM elements
       │        • cleanup resources
       │        • stop animations
       ▼
┌─────────────┐
│ unmounted   │ (component destroyed)
└─────────────┘
```

---

## 7. Error Handling Flow

```
┌─────────────────────────────────────────────────────────┐
│                 ERROR HANDLING STRATEGY                  │
└─────────────────────────────────────────────────────────┘

┌─────────────┐
│   Error     │ (throws error)
│  Occurs     │
└──────┬──────┘
       │
       ├──────────┬──────────┬──────────┐
       │          │          │          │
       ▼          ▼          ▼          ▼
   ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
   │ Data  │ │ State │ │Plugin │ │  UI   │
   │ Error │ │ Error │ │ Error │ │ Error │
   └───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘
       │         │         │         │
       └─────────┴────┬────┴─────────┘
                      │
                      ▼
              ┌──────────────┐
              │ ErrorBoundary│ catches all errors
              └───────┬──────┘
                      │
                      │ classify error
                      │
       ┌──────────────┼──────────────┐
       │              │              │
       ▼              ▼              ▼
┌──────────┐   ┌──────────┐   ┌──────────┐
│ Fatal    │   │Recoverable│  │  Minor   │
│ Error    │   │  Error    │  │  Error   │
└────┬─────┘   └─────┬─────┘  └─────┬────┘
     │               │              │
     │               │              │
     ▼               ▼              ▼
┌──────────┐   ┌──────────┐   ┌──────────┐
│ Show     │   │ Retry    │   │ Log &    │
│ Error    │   │ Logic    │   │ Continue │
│ Page     │   └─────┬─────┘  └──────────┘
└──────────┘         │
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
   ┌──────────┐           ┌──────────┐
   │ Success  │           │ Failed   │
   │ Continue │           │ Show     │
   │          │           │ Error UI │
   └──────────┘           └──────────┘
```

---

## 8. Performance Optimization Strategies

### 8.1 Rendering Optimization

```
┌─────────────────────────────────────────────────────────┐
│              RENDERING OPTIMIZATION FLOW                 │
└─────────────────────────────────────────────────────────┘

State Change
     │
     ▼
┌─────────────┐
│ shouldUpdate│ check if render needed
└──────┬──────┘ • compare props
       │        • compare state
       │        • custom logic
       │
       ├─── no changes ───► Skip render
       │
       │ has changes
       ▼
┌─────────────┐
│ batchUpdate │ collect multiple updates
└──────┬──────┘ • debounce/throttle
       │        • group operations
       │        • single paint cycle
       ▼
┌─────────────┐
│ virtualDiff │ diff virtual DOM
└──────┬──────┘ • only changed nodes
       │        • minimal updates
       ▼
┌─────────────┐
│ applyPatch  │ update real DOM
└──────┬──────┘ • batch operations
       │        • use DocumentFragment
       │        • minimize reflows
       ▼
┌─────────────┐
│  Painted    │ browser renders
└─────────────┘
```

### 8.2 Data Loading Strategy

```
┌─────────────────────────────────────────────────────────┐
│            STALE-WHILE-REVALIDATE PATTERN                │
└─────────────────────────────────────────────────────────┘

User Requests Data
     │
     ▼
┌─────────────┐
│ Check Cache │
└──────┬──────┘
       │
       ├─── cache miss ───┐
       │                  │
       │ cache hit        │
       ▼                  ▼
┌─────────────┐    ┌─────────────┐
│ Return      │    │ Fetch from  │
│ Cached Data │    │ Network     │
│ Instantly   │    └──────┬──────┘
└──────┬──────┘           │
       │                  │
       │                  ▼
       │           ┌─────────────┐
       │           │ Update      │
       │           │ Cache       │
       │           └──────┬──────┘
       │                  │
       └──────────────────┴── both paths
                          │
                          ▼
                   ┌─────────────┐
                   │ Background  │
                   │ Revalidate  │
                   └──────┬──────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
    ┌─────────┐     ┌─────────┐     ┌─────────┐
    │ Cache   │     │ Data    │     │ Cache   │
    │ Fresh   │     │ Changed │     │ Expired │
    └─────────┘     └────┬────┘     └────┬────┘
                         │                │
                         │                │
                         ▼                ▼
                    ┌─────────┐     ┌─────────┐
                    │ Update  │     │ Force   │
                    │ Silently│     │ Refresh │
                    └─────────┘     └─────────┘
```

---

## 9. Security & Privacy Architecture

```
┌─────────────────────────────────────────────────────────┐
│            LOCAL-FIRST PRIVACY MODEL                     │
└─────────────────────────────────────────────────────────┘

┌─────────────┐
│ User Data   │
└──────┬──────┘
       │
       │ All data stays local
       │
       ├──────────┬──────────┬──────────┐
       │          │          │          │
       ▼          ▼          ▼          ▼
┌──────────┐┌──────────┐┌──────────┐┌──────────┐
│Local     ││IndexedDB ││Session   ││Memory    │
│Storage   ││          ││Storage   ││Only      │
└────┬─────┘└────┬─────┘└────┬─────┘└────┬─────┘
     │           │           │           │
     │           │           │           │
     └───────────┴─────┬─────┴───────────┘
                       │
                       │ NO external sync
                       │ NO tracking
                       │ NO analytics (optional local only)
                       │
                       ▼
               ┌──────────────┐
               │ Export to    │
               │ JSON         │ (user controlled)
               └──────┬───────┘
                      │
                      ▼
               ┌──────────────┐
               │ User's       │
               │ Device       │ (user owns data)
               └──────────────┘

Content Security Policy:
- No inline scripts (except this file)
- No external domains (except Three.js CDN)
- No eval() or Function() constructors
- Strict CSP headers
```

---

## 10. Future Architecture Extensions

### 10.1 Service Worker Layer (Future)

```
┌─────────────────────────────────────────────────────────┐
│          OFFLINE-FIRST WITH SERVICE WORKER               │
└─────────────────────────────────────────────────────────┘

Browser Request
     │
     ▼
┌─────────────┐
│  Service    │ intercepts all requests
│  Worker     │
└──────┬──────┘
       │
       │ check cache strategy
       │
       ├──────────┬──────────┬──────────┐
       │          │          │          │
       ▼          ▼          ▼          ▼
┌──────────┐┌──────────┐┌──────────┐┌──────────┐
│Network   ││Cache     ││Network   ││Cache     │
│First     ││First     ││Only      ││Only      │
└────┬─────┘└────┬─────┘└────┬─────┘└────┬─────┘
     │           │           │           │
     └───────────┴─────┬─────┴───────────┘
                       │
                       ▼
               ┌──────────────┐
               │ Return       │
               │ Response     │
               └──────────────┘
```

### 10.2 Plugin Marketplace (Future)

```
Community Plugin Ecosystem
     │
     ▼
┌─────────────┐
│ Plugin      │
│ Registry    │ (JSON manifest)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Plugin      │ browse & install
│ Browser UI  │
└──────┬──────┘
       │
       │ user clicks install
       ▼
┌─────────────┐
│ Download    │ fetch plugin code
│ Plugin      │
└──────┬──────┘
       │
       │ verify signature
       ▼
┌─────────────┐
│ Install     │ register with system
│ Plugin      │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ User's      │
│ Gallery     │ + new features!
└─────────────┘
```

---

**Document Version**: 1.0
**Created**: 2025-10-12
**Purpose**: Visual companion to ARCHITECTURE.md
