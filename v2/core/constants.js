/**
 * Constants - Application-wide constants
 * Local First Tools v2
 */

// Version
export const VERSION = '2.0.0';

// Config paths (relative to v2/)
export const CONFIG_PATH = '../vibe_gallery_config.json';
export const MANIFEST_PATH = '../tools-manifest.json';

// Storage keys
export const STORAGE_PREFIX = 'v2:';
export const STORAGE_KEYS = {
    PINNED_TOOLS: 'v2:pinnedTools',
    VOTES: 'v2:votes',
    USAGE: 'v2:usage',
    RECENTLY_OPENED: 'v2:recentlyOpened',
    COLLECTIONS: 'v2:collections',
    SEARCH_HISTORY: 'v2:searchHistory',
    THEME: 'v2:theme',
    TOUR_COMPLETED: 'v2:tourCompleted',
    ANALYTICS_ENABLED: 'v2:analyticsEnabled',
    VIEW_MODE: 'v2:viewMode',
    SORT_PREFERENCE: 'v2:sortPreference'
};

// Categories
export const CATEGORIES = {
    visual_art: {
        key: 'visual_art',
        title: 'Visual Art',
        icon: '🎨',
        color: '#ff6b9d'
    },
    '3d_immersive': {
        key: '3d_immersive',
        title: '3D Immersive',
        icon: '🌐',
        color: '#4ecdc4'
    },
    audio_music: {
        key: 'audio_music',
        title: 'Audio & Music',
        icon: '🎵',
        color: '#ffb347'
    },
    games_puzzles: {
        key: 'games_puzzles',
        title: 'Games & Puzzles',
        icon: '🎮',
        color: '#9b59b6'
    },
    experimental_ai: {
        key: 'experimental_ai',
        title: 'Experimental AI',
        icon: '🤖',
        color: '#00d4ff'
    },
    creative_tools: {
        key: 'creative_tools',
        title: 'Creative Tools',
        icon: '✏️',
        color: '#ff9ff3'
    },
    generative_art: {
        key: 'generative_art',
        title: 'Generative Art',
        icon: '🌀',
        color: '#5fa8ff'
    },
    particle_physics: {
        key: 'particle_physics',
        title: 'Particle & Physics',
        icon: '⚛️',
        color: '#5dade2'
    },
    educational_tools: {
        key: 'educational_tools',
        title: 'Educational',
        icon: '📚',
        color: '#f7dc6f'
    }
};

// Complexity levels
export const COMPLEXITY = {
    simple: {
        label: 'Simple',
        dots: 1,
        color: '#10b981'
    },
    intermediate: {
        label: 'Intermediate',
        dots: 2,
        color: '#f59e0b'
    },
    advanced: {
        label: 'Advanced',
        dots: 3,
        color: '#ef4444'
    }
};

// Interaction types
export const INTERACTION_TYPES = {
    game: 'Game',
    drawing: 'Drawing',
    visual: 'Visual',
    interactive: 'Interactive',
    audio: 'Audio',
    interface: 'Interface'
};

// View modes
export const VIEW_MODES = {
    grid: {
        key: 'grid',
        label: 'Grid',
        icon: 'grid'
    },
    list: {
        key: 'list',
        label: 'List',
        icon: 'list'
    },
    masonry: {
        key: 'masonry',
        label: 'Masonry',
        icon: 'masonry'
    },
    timeline: {
        key: 'timeline',
        label: 'Timeline',
        icon: 'timeline'
    },
    dashboard: {
        key: 'dashboard',
        label: 'Dashboard',
        icon: 'dashboard'
    },
    '3d': {
        key: '3d',
        label: '3D Gallery',
        icon: '3d'
    }
};

// Sort options
export const SORT_OPTIONS = {
    name: {
        key: 'name',
        label: 'Name',
        direction: 'asc'
    },
    date: {
        key: 'date',
        label: 'Date Added',
        direction: 'desc'
    },
    usage: {
        key: 'usage',
        label: 'Most Used',
        direction: 'desc'
    },
    votes: {
        key: 'votes',
        label: 'Most Voted',
        direction: 'desc'
    },
    complexity: {
        key: 'complexity',
        label: 'Complexity',
        direction: 'asc'
    },
    random: {
        key: 'random',
        label: 'Random',
        direction: 'asc'
    }
};

// Themes
export const THEMES = {
    dark: {
        key: 'dark',
        label: 'Dark',
        icon: '🌙'
    },
    light: {
        key: 'light',
        label: 'Light',
        icon: '☀️'
    },
    'high-contrast': {
        key: 'high-contrast',
        label: 'High Contrast',
        icon: '◐'
    }
};

// Keyboard shortcuts
export const KEYBOARD_SHORTCUTS = {
    FOCUS_SEARCH: '/',
    CLOSE_MODAL: 'Escape',
    TOGGLE_THEME: 't',
    TOGGLE_FEATURED: 'f',
    PIN_FOCUSED: 'p',
    OPEN_ANALYTICS: 'a',
    OPEN_COMPARISON: 'c',
    SHOW_SHORTCUTS: '?',
    RESET_VIEW: 'h',
    REFRESH: 'r',
    CATEGORY_1: '1',
    CATEGORY_2: '2',
    CATEGORY_3: '3',
    CATEGORY_4: '4',
    CATEGORY_5: '5',
    CATEGORY_6: '6',
    CATEGORY_7: '7',
    CATEGORY_8: '8',
    CATEGORY_9: '9',
    CATEGORY_ALL: '0',
    NAVIGATE_UP: 'ArrowUp',
    NAVIGATE_DOWN: 'ArrowDown',
    NAVIGATE_LEFT: 'ArrowLeft',
    NAVIGATE_RIGHT: 'ArrowRight',
    SELECT: 'Enter',
    PREVIEW: 'Space'
};

// Search operators
export const SEARCH_OPERATORS = {
    'tag:': 'filterByTag',
    'cat:': 'filterByCategory',
    'category:': 'filterByCategory',
    'level:': 'filterByComplexity',
    'complexity:': 'filterByComplexity',
    'type:': 'filterByType',
    'file:': 'filterByFilename',
    'filename:': 'filterByFilename',
    'folder:': 'filterByFolder',
    'path:': 'filterByFolder',
    'is:': 'filterByFlag',
    'before:': 'filterByDateBefore',
    'after:': 'filterByDateAfter'
};

// Flag values for 'is:' operator
export const SEARCH_FLAGS = {
    featured: 'featured',
    pinned: 'pinned',
    recent: 'recent',
    popular: 'popular',
    new: 'new'
};

// Limits
export const LIMITS = {
    RECENT_TOOLS: 10,
    SEARCH_HISTORY: 20,
    SEARCH_SUGGESTIONS: 8,
    COMPARISON_MAX: 4,
    VIRTUAL_SCROLL_BUFFER: 5,
    TOOL_DESCRIPTION_LENGTH: 150,
    TOOL_TITLE_LENGTH: 50
};

// Debounce times (ms)
export const DEBOUNCE = {
    SEARCH: 150,
    FILTER: 100,
    RESIZE: 200,
    SCROLL: 16
};

// Animation durations (ms)
export const ANIMATION = {
    FAST: 150,
    NORMAL: 250,
    SLOW: 400,
    VERY_SLOW: 700
};

// 3D Gallery settings
export const GALLERY_3D = {
    FOV: 75,
    NEAR: 0.1,
    FAR: 1000,
    MOVEMENT_SPEED: 0.1,
    LOOK_SPEED: 0.002,
    CONTROLLER_DEADZONE: 0.15,
    LOD_LEVELS: {
        HIGH: 15,
        MEDIUM: 40,
        LOW: 80
    }
};

// Breakpoints (px)
export const BREAKPOINTS = {
    SM: 640,
    MD: 768,
    LG: 1024,
    XL: 1280,
    XXL: 1536
};

// Default tool card height for virtual scrolling
export const DEFAULT_CARD_HEIGHT = 380;

// API endpoints (for future use)
export const API = {
    BASE_URL: '',
    ENDPOINTS: {}
};
