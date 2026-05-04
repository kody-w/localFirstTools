/**
 * Main Entry Point - Application initialization
 * Local First Tools v2
 */

import { StateManager } from './core/state-manager.js';
import { EventBus, EVENTS } from './core/event-bus.js';
import { VERSION, CATEGORIES, STORAGE_KEYS } from './core/constants.js';
import { StorageManager } from './storage/storage-manager.js';
import { DataLoader } from './data/data-loader.js';
import { ToolRepository } from './data/tool-repository.js';

class App {
    constructor() {
        this.state = StateManager.getInstance();
        this.events = EventBus.getInstance();
        this.storage = StorageManager.getInstance();
        this.dataLoader = DataLoader.getInstance();
        this.toolRepo = ToolRepository.getInstance();

        this.#initialized = false;
    }

    #initialized;

    /**
     * Initialize the application
     */
    async initialize() {
        if (this.#initialized) {
            console.warn('App already initialized');
            return;
        }

        console.log(`Local First Tools v${VERSION} initializing...`);

        try {
            // Show loading state
            this.#renderLoadingState();

            // Hydrate state from storage
            await this.state.hydrate(this.storage);

            // Load configuration
            const configResult = await this.dataLoader.loadConfig();

            if (!configResult.success) {
                throw new Error(configResult.error);
            }

            // Initialize tool repository
            this.toolRepo.initialize(configResult.data);

            // Update state with loaded data
            this.state.setState(() => ({
                tools: this.toolRepo.getAll(),
                filteredTools: this.toolRepo.getAll(),
                config: configResult.data,
                isLoading: false,
                error: null
            }));

            // Apply saved theme
            this.#applyTheme(this.state.getSlice('user').theme);

            // Set up event listeners
            this.#setupEventListeners();

            // Render the UI
            this.#renderApp();

            // Emit data loaded event
            this.events.emit(EVENTS.DATA_LOADED, {
                toolCount: this.toolRepo.count(),
                source: configResult.source
            });

            this.#initialized = true;
            console.log(`Loaded ${this.toolRepo.count()} tools from ${configResult.source}`);

        } catch (error) {
            console.error('Failed to initialize app:', error);
            this.state.setState(() => ({
                isLoading: false,
                error: error.message
            }));
            this.#renderErrorState(error.message);
        }
    }

    /**
     * Render loading skeleton
     */
    #renderLoadingState() {
        const app = document.getElementById('app');
        app.innerHTML = `
            <header class="header">
                <div class="header-brand">
                    <span class="header-title">Local First Tools</span>
                    <span class="header-version">v${VERSION}</span>
                </div>
                <div class="header-search">
                    <div class="search-container">
                        <input type="text" class="search-input" placeholder="Loading..." disabled>
                    </div>
                </div>
            </header>
            <div class="loading-container">
                <div class="skeleton-grid">
                    ${this.#generateSkeletons(12)}
                </div>
            </div>
        `;
    }

    /**
     * Generate skeleton placeholders
     * @param {number} count
     * @returns {string}
     */
    #generateSkeletons(count) {
        return Array(count).fill(0).map(() => `
            <div class="skeleton-card">
                <div class="skeleton skeleton-image"></div>
                <div class="skeleton skeleton-title"></div>
                <div class="skeleton skeleton-text"></div>
                <div class="skeleton skeleton-text short"></div>
            </div>
        `).join('');
    }

    /**
     * Render error state
     * @param {string} message
     */
    #renderErrorState(message) {
        const app = document.getElementById('app');
        app.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">
                    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="12" y1="8" x2="12" y2="12"/>
                        <line x1="12" y1="16" x2="12.01" y2="16"/>
                    </svg>
                </div>
                <h2 class="empty-title">Failed to Load</h2>
                <p class="empty-description">${message}</p>
                <button class="btn btn-primary" onclick="window.app.initialize()">
                    Try Again
                </button>
            </div>
        `;
    }

    /**
     * Render the main application
     */
    #renderApp() {
        const { tools, user } = this.state.getState();
        const categories = this.toolRepo.getCategoriesWithCounts();

        const app = document.getElementById('app');
        app.innerHTML = `
            <header class="header">
                <div class="header-brand">
                    <span class="header-title">Local First Tools</span>
                    <span class="header-version">v${VERSION}</span>
                </div>
                <div class="header-search">
                    <div class="search-container">
                        <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="11" cy="11" r="8"/>
                            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                        </svg>
                        <input type="text"
                               class="search-input"
                               id="search-input"
                               placeholder="Search tools... (Press / to focus)"
                               aria-label="Search tools">
                        <div class="search-suggestions" id="search-suggestions"></div>
                    </div>
                </div>
                <div class="header-actions">
                    <button class="icon-btn" id="theme-toggle" aria-label="Toggle theme" title="Toggle theme (T)">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
                        </svg>
                    </button>
                    <button class="icon-btn" id="analytics-btn" aria-label="Analytics" title="Analytics (A)">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <line x1="18" y1="20" x2="18" y2="10"/>
                            <line x1="12" y1="20" x2="12" y2="4"/>
                            <line x1="6" y1="20" x2="6" y2="14"/>
                        </svg>
                    </button>
                    <button class="icon-btn" id="help-btn" aria-label="Keyboard shortcuts" title="Keyboard shortcuts (?)">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"/>
                            <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
                            <line x1="12" y1="17" x2="12.01" y2="17"/>
                        </svg>
                    </button>
                </div>
            </header>

            <nav class="category-nav" role="navigation" aria-label="Category navigation">
                <button class="category-btn active" data-category="all">
                    <span>All</span>
                    <span class="category-count">${tools.length}</span>
                </button>
                ${categories.map(cat => `
                    <button class="category-btn" data-category="${cat.key}">
                        <span>${cat.icon} ${cat.title}</span>
                        <span class="category-count">${cat.count}</span>
                    </button>
                `).join('')}
            </nav>

            <div class="filter-bar">
                <div class="filter-group">
                    <label class="filter-label" for="complexity-filter">Complexity:</label>
                    <select class="filter-select" id="complexity-filter">
                        <option value="">All</option>
                        <option value="simple">Simple</option>
                        <option value="intermediate">Intermediate</option>
                        <option value="advanced">Advanced</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label class="filter-label" for="type-filter">Type:</label>
                    <select class="filter-select" id="type-filter">
                        <option value="">All</option>
                        <option value="game">Game</option>
                        <option value="drawing">Drawing</option>
                        <option value="visual">Visual</option>
                        <option value="interactive">Interactive</option>
                        <option value="audio">Audio</option>
                        <option value="interface">Interface</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label class="filter-label" for="special-filter">Show:</label>
                    <select class="filter-select" id="special-filter">
                        <option value="">All Tools</option>
                        <option value="featured">Featured</option>
                        <option value="polished">Polished</option>
                        <option value="pinned">Pinned</option>
                    </select>
                </div>
            </div>

            <div class="active-filters" id="active-filters"></div>

            <div class="stats-bar">
                <span class="stat-item">Showing <span id="shown-count">${tools.length}</span> tools</span>
            </div>

            <main class="main-content" id="main-content" role="main">
                <div class="tools-container" id="tools-container">
                    ${this.#renderToolCards(tools)}
                </div>
            </main>

            <nav class="bottom-nav" role="navigation" aria-label="Mobile navigation">
                <button class="nav-item active" data-view="gallery">
                    <span class="nav-icon">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="3" y="3" width="7" height="7"/>
                            <rect x="14" y="3" width="7" height="7"/>
                            <rect x="14" y="14" width="7" height="7"/>
                            <rect x="3" y="14" width="7" height="7"/>
                        </svg>
                    </span>
                    <span class="nav-label">Gallery</span>
                </button>
                <button class="nav-item" data-view="pinned">
                    <span class="nav-icon">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                        </svg>
                    </span>
                    <span class="nav-label">Pinned</span>
                </button>
                <button class="nav-item" data-view="search">
                    <span class="nav-icon">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="11" cy="11" r="8"/>
                            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                        </svg>
                    </span>
                    <span class="nav-label">Search</span>
                </button>
                <button class="nav-item" data-view="more">
                    <span class="nav-icon">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="1"/>
                            <circle cx="19" cy="12" r="1"/>
                            <circle cx="5" cy="12" r="1"/>
                        </svg>
                    </span>
                    <span class="nav-label">More</span>
                </button>
            </nav>

            <div class="modal-container" id="modal-container" aria-hidden="true" role="dialog">
                <div class="modal-backdrop" id="modal-backdrop"></div>
                <div class="modal-content" id="modal-content"></div>
            </div>

            <div class="toast-container" id="toast-container" role="alert" aria-live="polite"></div>
        `;

        this.#bindUIEvents();
    }

    /**
     * Render tool cards
     * @param {Array} tools
     * @returns {string}
     */
    #renderToolCards(tools) {
        if (tools.length === 0) {
            return `
                <div class="empty-state">
                    <div class="empty-icon">
                        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="11" cy="11" r="8"/>
                            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                        </svg>
                    </div>
                    <h2 class="empty-title">No tools found</h2>
                    <p class="empty-description">Try adjusting your filters or search query</p>
                    <button class="btn btn-secondary" id="reset-filters-btn">Reset Filters</button>
                </div>
            `;
        }

        const { pinnedTools } = this.state.getSlice('user');
        const pinnedSet = new Set(pinnedTools);

        return tools.map(tool => {
            const category = this.toolRepo.getCategory(tool.category);
            const isPinned = pinnedSet.has(tool.id);

            return `
                <article class="tool-card ${isPinned ? 'pinned' : ''}" data-tool-id="${tool.id}">
                    <div class="tool-card-header">
                        <span class="tool-category" style="--cat-color: ${category?.color || '#888'}">
                            ${category?.icon || ''} ${category?.title || tool.category}
                        </span>
                        <button class="pin-btn ${isPinned ? 'active' : ''}"
                                data-tool-id="${tool.id}"
                                aria-label="${isPinned ? 'Unpin' : 'Pin'} ${tool.title}">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="${isPinned ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2">
                                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                            </svg>
                        </button>
                    </div>
                    <div class="tool-card-content">
                        <h3 class="tool-title">${tool.title}</h3>
                        <p class="tool-description">${tool.description || 'No description available'}</p>
                    </div>
                    <div class="tool-card-meta">
                        <span class="complexity-badge complexity-${tool.complexity}">
                            ${tool.complexity}
                        </span>
                        ${tool.featured ? '<span class="featured-badge">Featured</span>' : ''}
                        ${tool.tags.slice(0, 3).map(tag => `
                            <span class="tag-badge">${tag}</span>
                        `).join('')}
                    </div>
                    <div class="tool-card-actions">
                        <a href="../${tool.path}" class="btn btn-primary tool-open-btn" target="_blank">
                            Open Tool
                        </a>
                        <button class="btn btn-secondary tool-preview-btn" data-tool-id="${tool.id}">
                            Preview
                        </button>
                    </div>
                </article>
            `;
        }).join('');
    }

    /**
     * Bind UI event listeners
     */
    #bindUIEvents() {
        // Search input
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            let debounceTimer;
            searchInput.addEventListener('input', (e) => {
                clearTimeout(debounceTimer);
                debounceTimer = setTimeout(() => {
                    this.#handleSearch(e.target.value);
                }, 150);
            });
        }

        // Category buttons
        document.querySelectorAll('.category-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.#handleCategoryClick(e.currentTarget.dataset.category);
            });
        });

        // Filter selects
        ['complexity-filter', 'type-filter', 'special-filter'].forEach(id => {
            const select = document.getElementById(id);
            if (select) {
                select.addEventListener('change', () => this.#applyFilters());
            }
        });

        // Theme toggle
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.#toggleTheme());
        }

        // Pin buttons
        document.querySelectorAll('.pin-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.#handlePinToggle(e.currentTarget.dataset.toolId);
            });
        });

        // Tool card clicks for preview
        document.querySelectorAll('.tool-preview-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.#handlePreview(e.currentTarget.dataset.toolId);
            });
        });

        // Track tool opens
        document.querySelectorAll('.tool-open-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const toolId = e.currentTarget.closest('.tool-card').dataset.toolId;
                this.#trackToolOpen(toolId);
            });
        });

        // Modal backdrop close
        const backdrop = document.getElementById('modal-backdrop');
        if (backdrop) {
            backdrop.addEventListener('click', () => this.#closeModal());
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.#handleKeyboard(e));

        // Reset filters button (if exists)
        const resetBtn = document.getElementById('reset-filters-btn');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => this.#resetFilters());
        }
    }

    /**
     * Set up application event listeners
     */
    #setupEventListeners() {
        // Listen for state changes
        this.state.subscribeToSlice('filteredTools', (tools) => {
            this.#renderToolsContainer(tools);
        });

        // Listen for theme changes
        this.events.on(EVENTS.THEME_CHANGE, (theme) => {
            this.#applyTheme(theme);
        });
    }

    /**
     * Handle search input
     * @param {string} query
     */
    #handleSearch(query) {
        const filters = this.state.getSlice('filters');
        this.state.setSlice('filters', { ...filters, searchTerm: query });
        this.#applyFilters();
        this.events.emit(EVENTS.SEARCH_QUERY, { query });
    }

    /**
     * Handle category click
     * @param {string} category
     */
    #handleCategoryClick(category) {
        // Update UI
        document.querySelectorAll('.category-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.category === category);
        });

        const filters = this.state.getSlice('filters');
        this.state.setSlice('filters', { ...filters, category });
        this.#applyFilters();
    }

    /**
     * Apply all current filters
     */
    #applyFilters() {
        const filters = this.state.getSlice('filters');
        const complexityFilter = document.getElementById('complexity-filter')?.value || '';
        const typeFilter = document.getElementById('type-filter')?.value || '';
        const specialFilter = document.getElementById('special-filter')?.value || '';

        let tools = this.toolRepo.getAll();

        // Category filter
        if (filters.category && filters.category !== 'all') {
            tools = tools.filter(t => t.category === filters.category);
        }

        // Complexity filter
        if (complexityFilter) {
            tools = tools.filter(t => t.complexity === complexityFilter);
        }

        // Type filter
        if (typeFilter) {
            tools = tools.filter(t => t.interactionType === typeFilter);
        }

        // Special filter
        if (specialFilter === 'featured') {
            tools = tools.filter(t => t.featured);
        } else if (specialFilter === 'polished') {
            tools = tools.filter(t => t.polished);
        } else if (specialFilter === 'pinned') {
            const pinnedSet = new Set(this.state.getSlice('user').pinnedTools);
            tools = tools.filter(t => pinnedSet.has(t.id));
        }

        // Search filter
        if (filters.searchTerm) {
            const query = filters.searchTerm.toLowerCase();
            tools = tools.filter(t =>
                t.title.toLowerCase().includes(query) ||
                t.description.toLowerCase().includes(query) ||
                t.tags.some(tag => tag.toLowerCase().includes(query))
            );
        }

        this.state.setSlice('filteredTools', tools);

        // Update count
        const countEl = document.getElementById('shown-count');
        if (countEl) {
            countEl.textContent = tools.length;
        }

        this.events.emit(EVENTS.FILTERS_CHANGED, { tools, filters });
    }

    /**
     * Reset all filters
     */
    #resetFilters() {
        this.state.resetFilters();

        // Reset UI elements
        document.querySelectorAll('.category-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.category === 'all');
        });

        ['complexity-filter', 'type-filter', 'special-filter'].forEach(id => {
            const select = document.getElementById(id);
            if (select) select.value = '';
        });

        const searchInput = document.getElementById('search-input');
        if (searchInput) searchInput.value = '';

        this.#applyFilters();
        this.events.emit(EVENTS.FILTERS_RESET);
    }

    /**
     * Render tools container
     * @param {Array} tools
     */
    #renderToolsContainer(tools) {
        const container = document.getElementById('tools-container');
        if (container) {
            container.innerHTML = this.#renderToolCards(tools);
            this.#bindUIEvents(); // Rebind events for new elements
        }
    }

    /**
     * Handle pin toggle
     * @param {string} toolId
     */
    #handlePinToggle(toolId) {
        const user = this.state.getSlice('user');
        const pinnedTools = [...user.pinnedTools];
        const index = pinnedTools.indexOf(toolId);

        if (index === -1) {
            pinnedTools.push(toolId);
            this.events.emit(EVENTS.TOOL_PIN, { toolId });
        } else {
            pinnedTools.splice(index, 1);
            this.events.emit(EVENTS.TOOL_UNPIN, { toolId });
        }

        this.state.setSlice('user', { ...user, pinnedTools });
        this.storage.set(STORAGE_KEYS.PINNED_TOOLS, pinnedTools);

        // Re-render to update pin states
        this.#applyFilters();
    }

    /**
     * Handle tool preview
     * @param {string} toolId
     */
    #handlePreview(toolId) {
        const tool = this.toolRepo.getById(toolId);
        if (!tool) return;

        const category = this.toolRepo.getCategory(tool.category);
        const modalContent = document.getElementById('modal-content');

        modalContent.innerHTML = `
            <div class="preview-modal">
                <header class="preview-header">
                    <h2>${tool.title}</h2>
                    <button class="modal-close-btn" aria-label="Close">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <line x1="18" y1="6" x2="6" y2="18"/>
                            <line x1="6" y1="6" x2="18" y2="18"/>
                        </svg>
                    </button>
                </header>
                <div class="preview-body">
                    <div class="preview-meta">
                        <span class="tool-category" style="--cat-color: ${category?.color || '#888'}">
                            ${category?.icon || ''} ${category?.title || tool.category}
                        </span>
                        <span class="complexity-badge complexity-${tool.complexity}">${tool.complexity}</span>
                    </div>
                    <p class="preview-description">${tool.description || 'No description available'}</p>
                    <div class="preview-tags">
                        ${tool.tags.map(tag => `<span class="tag-badge">${tag}</span>`).join('')}
                    </div>
                    <div class="preview-iframe-container">
                        <iframe src="../${tool.path}" title="${tool.title}" sandbox="allow-scripts allow-same-origin"></iframe>
                    </div>
                </div>
                <footer class="preview-footer">
                    <a href="../${tool.path}" class="btn btn-primary" target="_blank">Open Full Screen</a>
                </footer>
            </div>
        `;

        this.#openModal();

        // Bind close button
        modalContent.querySelector('.modal-close-btn')?.addEventListener('click', () => this.#closeModal());

        this.events.emit(EVENTS.TOOL_PREVIEW, { toolId });
    }

    /**
     * Track tool open
     * @param {string} toolId
     */
    #trackToolOpen(toolId) {
        const user = this.state.getSlice('user');
        const usage = { ...user.usage };
        usage[toolId] = (usage[toolId] || 0) + 1;

        // Update recently opened
        const recentlyOpened = [toolId, ...user.recentlyOpened.filter(id => id !== toolId)].slice(0, 10);

        this.state.setSlice('user', { ...user, usage, recentlyOpened });
        this.storage.set(STORAGE_KEYS.USAGE, usage);
        this.storage.set(STORAGE_KEYS.RECENTLY_OPENED, recentlyOpened);

        this.events.emit(EVENTS.TOOL_OPEN, { toolId });
    }

    /**
     * Open modal
     */
    #openModal() {
        const modal = document.getElementById('modal-container');
        modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        this.events.emit(EVENTS.MODAL_OPEN);
    }

    /**
     * Close modal
     */
    #closeModal() {
        const modal = document.getElementById('modal-container');
        modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
        this.events.emit(EVENTS.MODAL_CLOSE);
    }

    /**
     * Toggle theme
     */
    #toggleTheme() {
        const user = this.state.getSlice('user');
        const newTheme = user.theme === 'dark' ? 'light' : 'dark';

        this.state.setSlice('user', { ...user, theme: newTheme });
        this.storage.set(STORAGE_KEYS.THEME, newTheme);
        this.#applyTheme(newTheme);

        this.events.emit(EVENTS.THEME_CHANGE, newTheme);
    }

    /**
     * Apply theme to document
     * @param {string} theme
     */
    #applyTheme(theme) {
        document.documentElement.className = `theme-${theme}`;
    }

    /**
     * Handle keyboard shortcuts
     * @param {KeyboardEvent} e
     */
    #handleKeyboard(e) {
        // Don't trigger shortcuts when typing in inputs
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
            if (e.key === 'Escape') {
                e.target.blur();
            }
            return;
        }

        switch (e.key) {
            case '/':
                e.preventDefault();
                document.getElementById('search-input')?.focus();
                break;
            case 't':
                this.#toggleTheme();
                break;
            case 'Escape':
                this.#closeModal();
                break;
            case '?':
                this.#showKeyboardShortcuts();
                break;
        }

        this.events.emit(EVENTS.KEYBOARD_SHORTCUT, { key: e.key });
    }

    /**
     * Show keyboard shortcuts modal
     */
    #showKeyboardShortcuts() {
        const modalContent = document.getElementById('modal-content');
        modalContent.innerHTML = `
            <div class="shortcuts-modal">
                <header class="shortcuts-header">
                    <h2>Keyboard Shortcuts</h2>
                    <button class="modal-close-btn" aria-label="Close">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <line x1="18" y1="6" x2="6" y2="18"/>
                            <line x1="6" y1="6" x2="18" y2="18"/>
                        </svg>
                    </button>
                </header>
                <div class="shortcuts-body">
                    <div class="shortcut-item">
                        <kbd>/</kbd>
                        <span>Focus search</span>
                    </div>
                    <div class="shortcut-item">
                        <kbd>t</kbd>
                        <span>Toggle theme</span>
                    </div>
                    <div class="shortcut-item">
                        <kbd>Esc</kbd>
                        <span>Close modal / Clear focus</span>
                    </div>
                    <div class="shortcut-item">
                        <kbd>?</kbd>
                        <span>Show shortcuts</span>
                    </div>
                </div>
            </div>
        `;

        this.#openModal();
        modalContent.querySelector('.modal-close-btn')?.addEventListener('click', () => this.#closeModal());
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
    window.app.initialize();
});

// Register service worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('./sw.js')
            .then(registration => {
                console.log('ServiceWorker registered:', registration.scope);
            })
            .catch(error => {
                console.log('ServiceWorker registration failed:', error);
            });
    });
}

export { App };
