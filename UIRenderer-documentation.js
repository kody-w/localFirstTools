/**
 * UIRenderer - Modern UI Rendering System for Game Store
 *
 * A static class that handles all UI rendering using modern DOM manipulation.
 * Uses createElement() exclusively - no innerHTML for dynamic content.
 *
 * Features:
 * - Category tabs with active state management
 * - Game card grid with install/play states
 * - Detailed game modal views
 * - Input mode-aware control hints
 * - Toast notifications with auto-dismiss
 * - Accessibility support (ARIA labels, roles, etc.)
 * - Empty state handling
 * - Performance optimized with DocumentFragment
 *
 * @author UIRenderer System
 * @version 1.0.0
 */

class UIRenderer {
    /**
     * Render category tabs
     * @param {Array<string>} categories - Array of category names
     * @param {string} activeCategory - Currently active category
     *
     * @example
     * UIRenderer.renderCategories(
     *   ['all', 'action', 'puzzle', 'arcade', 'strategy'],
     *   'all'
     * );
     */
    static renderCategories(categories, activeCategory) {
        const container = document.getElementById('categoryTabs');

        // Clear existing content
        while (container.firstChild) {
            container.removeChild(container.firstChild);
        }

        // Create fragment for better performance
        const fragment = document.createDocumentFragment();

        categories.forEach(category => {
            const tab = document.createElement('button');
            tab.className = 'category-tab';
            tab.dataset.category = category;
            tab.textContent = category.charAt(0).toUpperCase() + category.slice(1);
            tab.setAttribute('aria-label', `Filter by ${category}`);
            tab.setAttribute('role', 'tab');

            if (category === activeCategory) {
                tab.classList.add('active');
                tab.setAttribute('aria-selected', 'true');
            } else {
                tab.setAttribute('aria-selected', 'false');
            }

            fragment.appendChild(tab);
        });

        container.appendChild(fragment);
    }

    /**
     * Render game cards in grid
     * @param {Array<Game>} games - Array of game objects
     * @param {Set} favorites - Set of favorited game IDs
     * @param {Set} installed - Set of installed game IDs
     *
     * @example
     * const games = [
     *   { id: 'tetris', name: 'Tetris', icon: '🧱', description: '...', size: '8 KB' }
     * ];
     * const favorites = new Set(['tetris']);
     * const installed = new Set(['tetris']);
     * UIRenderer.renderGames(games, favorites, installed);
     */
    static renderGames(games, favorites, installed) {
        const grid = document.getElementById('gamesGrid');

        // Clear existing content
        while (grid.firstChild) {
            grid.removeChild(grid.firstChild);
        }

        // Handle empty state
        if (games.length === 0) {
            const noGamesContainer = document.createElement('div');
            noGamesContainer.className = 'no-games';

            const icon = document.createElement('div');
            icon.className = 'no-games-icon';
            icon.textContent = '🎮';
            icon.setAttribute('aria-hidden', 'true');

            const text = document.createElement('div');
            text.className = 'no-games-text';
            text.textContent = 'No games found';

            noGamesContainer.appendChild(icon);
            noGamesContainer.appendChild(text);
            grid.appendChild(noGamesContainer);
            return;
        }

        // Create fragment for better performance
        const fragment = document.createDocumentFragment();

        games.forEach(game => {
            const card = UIRenderer._createGameCard(game, favorites, installed);
            fragment.appendChild(card);
        });

        grid.appendChild(fragment);
    }

    /**
     * Create a single game card element
     * @private
     * @param {Game} game - Game object
     * @param {Set} favorites - Set of favorited game IDs
     * @param {Set} installed - Set of installed game IDs
     * @returns {HTMLElement} Game card element
     */
    static _createGameCard(game, favorites, installed) {
        const card = document.createElement('div');
        card.className = 'game-card';
        card.dataset.gameId = game.id;
        card.setAttribute('role', 'article');
        card.setAttribute('aria-label', `${game.name} game card`);
        card.tabIndex = 0;

        // Game icon
        const icon = document.createElement('div');
        icon.className = 'game-icon';
        icon.textContent = game.icon;
        icon.setAttribute('aria-hidden', 'true');

        // Game title
        const title = document.createElement('h3');
        title.className = 'game-title';
        title.textContent = game.name;

        // Game description
        const description = document.createElement('p');
        description.className = 'game-description';
        description.textContent = game.description;

        // Meta section (size + play button)
        const meta = document.createElement('div');
        meta.className = 'game-meta';

        // Size indicator
        const size = document.createElement('span');
        size.className = 'game-size';
        size.textContent = game.size;
        size.setAttribute('aria-label', `Game size: ${game.size}`);

        // Play/Install button
        const playButton = document.createElement('button');
        playButton.className = 'play-button';
        playButton.dataset.action = 'launch';
        playButton.dataset.gameId = game.id;

        const isInstalled = installed.has(game.id);
        playButton.textContent = isInstalled ? 'Play' : 'Install';
        playButton.setAttribute('aria-label', `${isInstalled ? 'Play' : 'Install'} ${game.name}`);

        // Stop propagation on play button so card click doesn't trigger
        playButton.addEventListener('click', (e) => {
            e.stopPropagation();
        });

        // Assemble meta section
        meta.appendChild(size);
        meta.appendChild(playButton);

        // Assemble card
        card.appendChild(icon);
        card.appendChild(title);
        card.appendChild(description);
        card.appendChild(meta);

        return card;
    }

    /**
     * Render game detail view in modal
     * @param {Game} game - Game object to display
     * @param {boolean} isFavorite - Whether game is favorited
     *
     * @example
     * const game = {
     *   id: 'tetris',
     *   name: 'Tetris',
     *   icon: '🧱',
     *   description: 'Classic block game',
     *   category: 'puzzle',
     *   size: '8 KB',
     *   author: 'Built-in',
     *   version: '1.0'
     * };
     * UIRenderer.renderGameDetail(game, true);
     */
    static renderGameDetail(game, isFavorite) {
        const content = document.getElementById('gameDetailContent');

        // Clear existing content
        while (content.firstChild) {
            content.removeChild(content.firstChild);
        }

        // Header section with icon and info
        const header = document.createElement('div');
        header.style.display = 'flex';
        header.style.gap = '30px';
        header.style.marginBottom = '30px';
        header.style.flexWrap = 'wrap';

        // Large game icon
        const icon = document.createElement('div');
        icon.style.fontSize = '120px';
        icon.textContent = game.icon;
        icon.setAttribute('aria-hidden', 'true');

        // Info section
        const info = document.createElement('div');
        info.style.flex = '1';
        info.style.minWidth = '300px';

        // Game title
        const title = document.createElement('h1');
        title.style.fontSize = '36px';
        title.style.marginBottom = '10px';
        title.textContent = game.name;

        // Description
        const desc = document.createElement('p');
        desc.style.fontSize = '18px';
        desc.style.color = '#8b8b8b';
        desc.style.lineHeight = '1.6';
        desc.style.marginBottom = '20px';
        desc.textContent = game.description;

        // Meta information (category, size, etc.)
        const metaInfo = document.createElement('div');
        metaInfo.style.color = '#8b8b8b';
        metaInfo.style.fontSize = '14px';

        const categorySpan = document.createElement('span');
        categorySpan.textContent = `Category: ${game.category}`;

        const separator = document.createTextNode(' | ');

        const sizeSpan = document.createElement('span');
        sizeSpan.textContent = `Size: ${game.size}`;

        metaInfo.appendChild(categorySpan);
        metaInfo.appendChild(separator);
        metaInfo.appendChild(sizeSpan);

        // Additional metadata if available
        if (game.author && game.author !== 'Unknown') {
            const authorSeparator = document.createTextNode(' | ');
            const authorSpan = document.createElement('span');
            authorSpan.textContent = `Author: ${game.author}`;
            metaInfo.appendChild(authorSeparator);
            metaInfo.appendChild(authorSpan);
        }

        if (game.version) {
            const versionSeparator = document.createTextNode(' | ');
            const versionSpan = document.createElement('span');
            versionSpan.textContent = `Version: ${game.version}`;
            metaInfo.appendChild(versionSeparator);
            metaInfo.appendChild(versionSpan);
        }

        // Assemble info section
        info.appendChild(title);
        info.appendChild(desc);
        info.appendChild(metaInfo);

        // Assemble header
        header.appendChild(icon);
        header.appendChild(info);

        // Action buttons section
        const actions = document.createElement('div');
        actions.style.display = 'flex';
        actions.style.gap = '15px';
        actions.style.marginTop = '30px';
        actions.style.flexWrap = 'wrap';

        // Play button
        const playBtn = document.createElement('button');
        playBtn.className = 'play-button';
        playBtn.style.padding = '12px 30px';
        playBtn.style.fontSize = '16px';
        playBtn.dataset.action = 'launch-detail';
        playBtn.dataset.gameId = game.id;
        playBtn.textContent = 'Play Now';
        playBtn.setAttribute('aria-label', `Play ${game.name}`);

        // Favorite toggle button
        const favBtn = document.createElement('button');
        favBtn.className = 'nav-button';
        favBtn.style.padding = '12px 30px';
        favBtn.style.fontSize = '16px';
        favBtn.dataset.action = 'toggle-favorite';
        favBtn.dataset.gameId = game.id;
        favBtn.textContent = isFavorite ? '★ Favorited' : '☆ Add to Favorites';
        favBtn.setAttribute('aria-label', isFavorite ? `Remove ${game.name} from favorites` : `Add ${game.name} to favorites`);
        favBtn.setAttribute('aria-pressed', isFavorite ? 'true' : 'false');

        // Assemble actions
        actions.appendChild(playBtn);
        actions.appendChild(favBtn);

        // Assemble final content
        content.appendChild(header);
        content.appendChild(actions);
    }

    /**
     * Update controls footer based on input mode
     * @param {string} inputMode - Current input mode (gamepad, keyboard, mouse, touch)
     *
     * @example
     * UIRenderer.updateControlsFooter('gamepad');
     * UIRenderer.updateControlsFooter('keyboard');
     * UIRenderer.updateControlsFooter('mouse');
     * UIRenderer.updateControlsFooter('touch');
     */
    static updateControlsFooter(inputMode) {
        const footer = document.getElementById('controlsFooter');

        // Clear existing content
        while (footer.firstChild) {
            footer.removeChild(footer.firstChild);
        }

        // Define control hints for each input mode
        const controlSchemes = {
            'gamepad': [
                { icon: 'A', text: 'Select' },
                { icon: 'B', text: 'Back' },
                { icon: 'X', text: 'Details' },
                { icon: 'Y', text: 'Favorite' }
            ],
            'keyboard': [
                { icon: '↵', text: 'Select' },
                { icon: 'ESC', text: 'Back' },
                { icon: '↑↓', text: 'Navigate' },
                { icon: 'F', text: 'Favorite' }
            ],
            'touch': [
                { icon: '👆', text: 'Tap to Select' },
                { icon: '📱', text: 'Swipe to Scroll' }
            ],
            'mouse': [
                { icon: '🖱️', text: 'Click to Select' },
                { icon: '↻', text: 'Scroll to Browse' }
            ]
        };

        // Get hints for current mode, fallback to mouse
        const hints = controlSchemes[inputMode] || controlSchemes.mouse;

        // Create fragment for better performance
        const fragment = document.createDocumentFragment();

        hints.forEach(hint => {
            const hintDiv = document.createElement('div');
            hintDiv.className = 'control-hint';

            const iconSpan = document.createElement('span');
            iconSpan.className = 'button-icon';
            iconSpan.textContent = hint.icon;
            iconSpan.setAttribute('aria-hidden', 'true');

            const textSpan = document.createElement('span');
            textSpan.textContent = hint.text;

            hintDiv.appendChild(iconSpan);
            hintDiv.appendChild(textSpan);
            fragment.appendChild(hintDiv);
        });

        footer.appendChild(fragment);
    }

    /**
     * Show toast notification
     * @param {string} message - Message to display
     * @param {number} duration - Duration in milliseconds (default: 3000)
     *
     * @example
     * UIRenderer.showToast('Game installed successfully!');
     * UIRenderer.showToast('Error loading game', 5000);
     */
    static showToast(message, duration = 3000) {
        const toast = document.getElementById('toast');

        // Clear existing content and set new message
        while (toast.firstChild) {
            toast.removeChild(toast.firstChild);
        }

        const messageText = document.createTextNode(message);
        toast.appendChild(messageText);

        toast.setAttribute('role', 'status');
        toast.setAttribute('aria-live', 'polite');

        // Show toast
        toast.classList.add('show');

        // Auto-hide after duration
        setTimeout(() => {
            toast.classList.remove('show');
        }, duration);
    }

    /**
     * Clear all toast notifications
     *
     * @example
     * UIRenderer.hideToast();
     */
    static hideToast() {
        const toast = document.getElementById('toast');
        toast.classList.remove('show');
    }
}

// ===== USAGE EXAMPLES =====

/**
 * Example 1: Render Categories
 */
function example1_renderCategories() {
    const categories = ['all', 'action', 'puzzle', 'arcade', 'strategy', 'adventure'];
    const activeCategory = 'all';

    UIRenderer.renderCategories(categories, activeCategory);
}

/**
 * Example 2: Render Games with Empty State
 */
function example2_renderGames() {
    const games = [
        {
            id: 'tetris',
            name: 'Tetris',
            icon: '🧱',
            description: 'The classic block-stacking puzzle game',
            size: '8 KB',
            category: 'puzzle'
        },
        {
            id: 'snake',
            name: 'Snake Classic',
            icon: '🐍',
            description: 'Eat food and grow longer!',
            size: '5 KB',
            category: 'arcade'
        }
    ];

    const favorites = new Set(['tetris']);
    const installed = new Set(['tetris', 'snake']);

    UIRenderer.renderGames(games, favorites, installed);
}

/**
 * Example 3: Show Empty State
 */
function example3_emptyState() {
    UIRenderer.renderGames([], new Set(), new Set());
    // Displays "No games found" message
}

/**
 * Example 4: Render Game Detail Modal
 */
function example4_gameDetail() {
    const game = {
        id: 'tetris',
        name: 'Tetris',
        icon: '🧱',
        description: 'The classic block-stacking puzzle game. Stack blocks and clear lines!',
        category: 'puzzle',
        size: '8 KB',
        author: 'Built-in',
        version: '1.0'
    };

    const isFavorite = true;

    UIRenderer.renderGameDetail(game, isFavorite);
}

/**
 * Example 5: Update Controls for Different Input Modes
 */
function example5_inputModes() {
    // Gamepad connected
    UIRenderer.updateControlsFooter('gamepad');

    // Keyboard detected
    UIRenderer.updateControlsFooter('keyboard');

    // Mouse detected
    UIRenderer.updateControlsFooter('mouse');

    // Touch device
    UIRenderer.updateControlsFooter('touch');
}

/**
 * Example 6: Show Toast Notifications
 */
function example6_toasts() {
    // Success message
    UIRenderer.showToast('Game installed successfully!');

    // Error with longer duration
    UIRenderer.showToast('Failed to load game', 5000);

    // Info message
    UIRenderer.showToast('Added to favorites');

    // Manual hide
    setTimeout(() => {
        UIRenderer.hideToast();
    }, 2000);
}

/**
 * Example 7: Complete Workflow
 */
function example7_completeWorkflow() {
    // 1. Render categories
    UIRenderer.renderCategories(['all', 'action', 'puzzle'], 'all');

    // 2. Render games
    const games = [
        {
            id: 'game1',
            name: 'Space Shooter',
            icon: '🚀',
            description: 'Defend against aliens',
            size: '12 KB',
            category: 'action'
        }
    ];
    UIRenderer.renderGames(games, new Set(), new Set());

    // 3. Show input controls
    UIRenderer.updateControlsFooter('mouse');

    // 4. Show notification
    UIRenderer.showToast('Welcome to Game Store!');
}

// ===== KEY FEATURES =====

/**
 * 1. Modern DOM Manipulation
 *    - Uses createElement() exclusively
 *    - No innerHTML for dynamic content
 *    - Prevents XSS vulnerabilities
 *
 * 2. Performance Optimized
 *    - Uses DocumentFragment for batch DOM updates
 *    - Removes all children before re-rendering
 *    - Event delegation friendly
 *
 * 3. Accessibility
 *    - ARIA labels and roles
 *    - Keyboard navigation support
 *    - Screen reader friendly
 *
 * 4. Empty State Handling
 *    - Shows "No games found" when list is empty
 *    - Provides clear user feedback
 *
 * 5. Dynamic Button Text
 *    - "Play" for installed games
 *    - "Install" for non-installed games
 *    - Context-aware UI
 *
 * 6. Event Handling
 *    - Cards clickable for details
 *    - Play button has stopPropagation
 *    - Modal has close button
 *    - Favorite toggle functionality
 *
 * 7. Input Mode Awareness
 *    - Gamepad controls
 *    - Keyboard shortcuts
 *    - Mouse interactions
 *    - Touch gestures
 *
 * 8. Toast Notifications
 *    - Auto-dismiss after duration
 *    - Accessible with ARIA live regions
 *    - Manual dismiss option
 */

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = UIRenderer;
}
