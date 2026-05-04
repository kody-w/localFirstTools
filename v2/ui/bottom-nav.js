/**
 * Bottom Navigation - Mobile bottom navigation bar
 * Local First Tools v2
 */

import { EventBus, EVENTS } from '../core/event-bus.js';
import { StateManager } from '../core/state-manager.js';

class BottomNav {
    constructor() {
        this.events = EventBus.getInstance();
        this.state = StateManager.getInstance();

        this.#container = null;
        this.#isVisible = false;
        this.#activeItem = 'home';
    }

    #container;
    #isVisible;
    #activeItem;

    /**
     * Initialize bottom navigation
     * @param {HTMLElement} parentContainer
     */
    initialize(parentContainer) {
        // Only show on mobile
        if (!this.#isMobile()) {
            this.#watchViewport();
            return;
        }

        this.#create(parentContainer);
        this.#bindEvents();
    }

    /**
     * Check if mobile viewport
     * @returns {boolean}
     */
    #isMobile() {
        return window.innerWidth <= 768 || 'ontouchstart' in window;
    }

    /**
     * Watch for viewport changes
     */
    #watchViewport() {
        const mediaQuery = window.matchMedia('(max-width: 768px)');

        mediaQuery.addEventListener('change', (e) => {
            if (e.matches) {
                this.show();
            } else {
                this.hide();
            }
        });
    }

    /**
     * Create bottom navigation
     * @param {HTMLElement} parentContainer
     */
    #create(parentContainer) {
        this.#container = document.createElement('nav');
        this.#container.className = 'bottom-nav';
        this.#container.setAttribute('role', 'navigation');
        this.#container.setAttribute('aria-label', 'Main navigation');

        this.#render();

        parentContainer.appendChild(this.#container);
        this.#isVisible = true;

        this.#injectStyles();

        // Add padding to body to account for nav
        document.body.style.paddingBottom = '64px';
    }

    /**
     * Render navigation items
     */
    #render() {
        const items = this.#getNavItems();

        this.#container.innerHTML = `
            ${items.map(item => `
                <button
                    class="bottom-nav-item ${this.#activeItem === item.id ? 'active' : ''}"
                    data-nav-id="${item.id}"
                    aria-label="${item.label}"
                    aria-current="${this.#activeItem === item.id ? 'page' : 'false'}"
                >
                    <span class="nav-icon">${item.icon}</span>
                    <span class="nav-label">${item.label}</span>
                    ${item.badge ? `<span class="nav-badge">${item.badge}</span>` : ''}
                </button>
            `).join('')}
        `;

        // Bind item clicks
        this.#container.querySelectorAll('.bottom-nav-item').forEach(btn => {
            btn.addEventListener('click', () => {
                const id = btn.dataset.navId;
                this.#handleNavClick(id);
            });
        });
    }

    /**
     * Get navigation items
     * @returns {Array}
     */
    #getNavItems() {
        const pinnedCount = (this.state.getSlice('pinnedTools') || []).length;

        return [
            {
                id: 'home',
                label: 'Home',
                icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/>
                    <polyline points="9 22 9 12 15 12 15 22"/>
                </svg>`
            },
            {
                id: 'search',
                label: 'Search',
                icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8"/>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                </svg>`
            },
            {
                id: 'favorites',
                label: 'Favorites',
                icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>`,
                badge: pinnedCount > 0 ? pinnedCount : null
            },
            {
                id: 'collections',
                label: 'Collections',
                icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/>
                </svg>`
            },
            {
                id: 'more',
                label: 'More',
                icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="1"/>
                    <circle cx="12" cy="5" r="1"/>
                    <circle cx="12" cy="19" r="1"/>
                </svg>`
            }
        ];
    }

    /**
     * Handle navigation click
     * @param {string} id
     */
    #handleNavClick(id) {
        this.#activeItem = id;
        this.#render();

        switch (id) {
            case 'home':
                this.events.emit(EVENTS.NAVIGATE, { to: 'home' });
                this.events.emit(EVENTS.FILTER_CLEAR);
                break;

            case 'search':
                this.events.emit(EVENTS.TOGGLE_SEARCH);
                this.#showSearchOverlay();
                break;

            case 'favorites':
                this.events.emit(EVENTS.FILTER_CHANGE, { pinned: true });
                break;

            case 'collections':
                this.events.emit(EVENTS.TOGGLE_COLLECTIONS);
                break;

            case 'more':
                this.#showMoreMenu();
                break;
        }

        // Haptic feedback
        if (navigator.vibrate) {
            navigator.vibrate(10);
        }
    }

    /**
     * Show search overlay
     */
    #showSearchOverlay() {
        const overlay = document.createElement('div');
        overlay.className = 'mobile-search-overlay';
        overlay.innerHTML = `
            <div class="search-overlay-content">
                <div class="search-header">
                    <input
                        type="search"
                        class="search-input"
                        placeholder="Search tools..."
                        autofocus
                    >
                    <button class="btn btn-icon search-cancel">Cancel</button>
                </div>
                <div class="search-results"></div>
            </div>
        `;

        document.body.appendChild(overlay);

        const input = overlay.querySelector('.search-input');
        const cancel = overlay.querySelector('.search-cancel');
        const results = overlay.querySelector('.search-results');

        // Focus input
        setTimeout(() => input?.focus(), 100);

        // Handle search
        input?.addEventListener('input', (e) => {
            this.events.emit(EVENTS.SEARCH, { query: e.target.value });
        });

        // Handle cancel
        cancel?.addEventListener('click', () => {
            overlay.remove();
            this.#activeItem = 'home';
            this.#render();
        });

        // Handle result selection
        this.events.once(EVENTS.SEARCH_RESULTS, ({ results: searchResults }) => {
            if (results) {
                results.innerHTML = searchResults.slice(0, 10).map(tool => `
                    <div class="search-result-item" data-tool-id="${tool.id}">
                        <span class="result-title">${tool.title}</span>
                        <span class="result-category">${tool.category}</span>
                    </div>
                `).join('');

                results.querySelectorAll('.search-result-item').forEach(item => {
                    item.addEventListener('click', () => {
                        const toolId = item.dataset.toolId;
                        this.events.emit(EVENTS.TOOL_OPEN, { toolId });
                        overlay.remove();
                    });
                });
            }
        });
    }

    /**
     * Show more menu
     */
    #showMoreMenu() {
        const menu = document.createElement('div');
        menu.className = 'bottom-nav-menu';
        menu.innerHTML = `
            <div class="menu-backdrop"></div>
            <div class="menu-content">
                <div class="menu-header">
                    <h3>More Options</h3>
                </div>
                <div class="menu-items">
                    <button class="menu-item" data-action="theme">
                        <span class="menu-icon">🎨</span>
                        <span>Change Theme</span>
                    </button>
                    <button class="menu-item" data-action="3d">
                        <span class="menu-icon">🎮</span>
                        <span>3D Gallery</span>
                    </button>
                    <button class="menu-item" data-action="analytics">
                        <span class="menu-icon">📊</span>
                        <span>Analytics</span>
                    </button>
                    <button class="menu-item" data-action="sync">
                        <span class="menu-icon">☁️</span>
                        <span>Backup & Sync</span>
                    </button>
                    <button class="menu-item" data-action="settings">
                        <span class="menu-icon">⚙️</span>
                        <span>Settings</span>
                    </button>
                    <button class="menu-item" data-action="help">
                        <span class="menu-icon">❓</span>
                        <span>Help & Tour</span>
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(menu);

        // Animate in
        requestAnimationFrame(() => menu.classList.add('visible'));

        // Handle backdrop click
        menu.querySelector('.menu-backdrop')?.addEventListener('click', () => {
            menu.classList.remove('visible');
            setTimeout(() => menu.remove(), 300);
            this.#activeItem = 'home';
            this.#render();
        });

        // Handle menu items
        menu.querySelectorAll('.menu-item').forEach(item => {
            item.addEventListener('click', () => {
                const action = item.dataset.action;
                menu.classList.remove('visible');
                setTimeout(() => menu.remove(), 300);

                this.#handleMenuAction(action);
            });
        });
    }

    /**
     * Handle menu action
     * @param {string} action
     */
    #handleMenuAction(action) {
        switch (action) {
            case 'theme':
                this.events.emit(EVENTS.THEME_TOGGLE);
                break;
            case '3d':
                this.events.emit(EVENTS.VIEW_CHANGE, { mode: '3d' });
                break;
            case 'analytics':
                this.events.emit(EVENTS.SHOW_ANALYTICS);
                break;
            case 'sync':
                this.events.emit(EVENTS.SHOW_SYNC);
                break;
            case 'settings':
                this.events.emit(EVENTS.SHOW_SETTINGS);
                break;
            case 'help':
                this.events.emit(EVENTS.TOUR_START);
                break;
        }

        this.#activeItem = 'home';
        this.#render();
    }

    /**
     * Bind event listeners
     */
    #bindEvents() {
        // Update badge when pins change
        this.state.subscribeToSlice('pinnedTools', () => {
            this.#render();
        });

        // Update active state on navigation
        this.events.on(EVENTS.NAVIGATE, ({ to }) => {
            this.#activeItem = to === 'archive' ? 'more' : 'home';
            this.#render();
        });
    }

    /**
     * Show bottom nav
     */
    show() {
        if (this.#isVisible) return;

        if (!this.#container) {
            this.#create(document.body);
        } else {
            this.#container.classList.add('visible');
            this.#isVisible = true;
            document.body.style.paddingBottom = '64px';
        }
    }

    /**
     * Hide bottom nav
     */
    hide() {
        if (!this.#isVisible) return;

        this.#container?.classList.remove('visible');
        this.#isVisible = false;
        document.body.style.paddingBottom = '0';
    }

    /**
     * Set active item
     * @param {string} id
     */
    setActive(id) {
        this.#activeItem = id;
        this.#render();
    }

    /**
     * Update badge
     * @param {string} itemId
     * @param {number|null} count
     */
    updateBadge(itemId, count) {
        const item = this.#container?.querySelector(`[data-nav-id="${itemId}"]`);
        if (!item) return;

        let badge = item.querySelector('.nav-badge');

        if (count && count > 0) {
            if (!badge) {
                badge = document.createElement('span');
                badge.className = 'nav-badge';
                item.appendChild(badge);
            }
            badge.textContent = count > 99 ? '99+' : count;
        } else if (badge) {
            badge.remove();
        }
    }

    /**
     * Inject styles
     */
    #injectStyles() {
        if (document.getElementById('bottom-nav-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'bottom-nav-styles';
        styles.textContent = `
            .bottom-nav {
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                height: 64px;
                background: var(--color-bg-elevated);
                border-top: 1px solid var(--color-border);
                display: flex;
                justify-content: space-around;
                align-items: center;
                z-index: 100;
                padding-bottom: env(safe-area-inset-bottom);
            }

            .bottom-nav-item {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 2px;
                padding: var(--space-2);
                background: none;
                border: none;
                color: var(--color-text-tertiary);
                cursor: pointer;
                position: relative;
                min-width: 60px;
                transition: color var(--duration-150);
            }

            .bottom-nav-item.active {
                color: var(--color-accent);
            }

            .bottom-nav-item:active {
                transform: scale(0.95);
            }

            .nav-icon {
                width: 24px;
                height: 24px;
            }

            .nav-icon svg {
                width: 100%;
                height: 100%;
            }

            .nav-label {
                font-size: 10px;
                font-weight: 500;
            }

            .nav-badge {
                position: absolute;
                top: 2px;
                right: 10px;
                min-width: 16px;
                height: 16px;
                padding: 0 4px;
                background: var(--color-accent);
                color: var(--color-bg-primary);
                border-radius: 8px;
                font-size: 10px;
                font-weight: 700;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            /* Mobile Search Overlay */
            .mobile-search-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: var(--color-bg-primary);
                z-index: 200;
            }

            .search-overlay-content {
                display: flex;
                flex-direction: column;
                height: 100%;
            }

            .search-header {
                display: flex;
                gap: var(--space-2);
                padding: var(--space-3);
                border-bottom: 1px solid var(--color-border);
            }

            .search-header .search-input {
                flex: 1;
                padding: var(--space-3);
                background: var(--color-bg-secondary);
                border: 1px solid var(--color-border);
                border-radius: var(--radius-lg);
                color: var(--color-text-primary);
                font-size: var(--text-base);
            }

            .search-cancel {
                color: var(--color-accent);
            }

            .search-results {
                flex: 1;
                overflow-y: auto;
                padding: var(--space-2);
            }

            .search-result-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: var(--space-3);
                border-radius: var(--radius-md);
                cursor: pointer;
            }

            .search-result-item:active {
                background: var(--color-bg-secondary);
            }

            .result-title {
                font-weight: 500;
            }

            .result-category {
                font-size: var(--text-xs);
                color: var(--color-text-tertiary);
            }

            /* Bottom Nav Menu */
            .bottom-nav-menu {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                z-index: 150;
            }

            .menu-backdrop {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.5);
                opacity: 0;
                transition: opacity var(--duration-300);
            }

            .bottom-nav-menu.visible .menu-backdrop {
                opacity: 1;
            }

            .menu-content {
                position: absolute;
                bottom: 64px;
                left: 0;
                right: 0;
                background: var(--color-bg-elevated);
                border-top-left-radius: var(--radius-xl);
                border-top-right-radius: var(--radius-xl);
                transform: translateY(100%);
                transition: transform var(--duration-300) var(--ease-out);
            }

            .bottom-nav-menu.visible .menu-content {
                transform: translateY(0);
            }

            .menu-header {
                padding: var(--space-4);
                border-bottom: 1px solid var(--color-border);
            }

            .menu-header h3 {
                margin: 0;
                font-size: var(--text-lg);
            }

            .menu-items {
                padding: var(--space-2);
            }

            .menu-item {
                display: flex;
                align-items: center;
                gap: var(--space-3);
                width: 100%;
                padding: var(--space-3) var(--space-4);
                background: none;
                border: none;
                color: var(--color-text-primary);
                font-size: var(--text-base);
                text-align: left;
                cursor: pointer;
                border-radius: var(--radius-md);
            }

            .menu-item:active {
                background: var(--color-bg-secondary);
            }

            .menu-icon {
                font-size: 20px;
            }

            /* Hide on desktop */
            @media (min-width: 769px) {
                .bottom-nav {
                    display: none;
                }
            }
        `;

        document.head.appendChild(styles);
    }

    /**
     * Destroy bottom nav
     */
    destroy() {
        this.#container?.remove();
        this.#container = null;
        this.#isVisible = false;
        document.body.style.paddingBottom = '0';
    }
}

export { BottomNav };
