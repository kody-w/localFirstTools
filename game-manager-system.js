// Game Management System for RetroPlay Console
// Complete JavaScript implementation with proper async handling

class StateManager {
    constructor() {
        this.state = {
            installedGames: new Set(),
            favorites: new Set(),
            currentView: 'store', // 'store' or 'library'
            currentCategory: 'all',
            searchQuery: '',
            currentGame: null,
            gameHistory: []
        };
        this.listeners = new Map();
        this.loadState();
    }

    loadState() {
        try {
            const savedState = localStorage.getItem('retroplay_state');
            if (savedState) {
                const parsed = JSON.parse(savedState);
                this.state.installedGames = new Set(parsed.installedGames || []);
                this.state.favorites = new Set(parsed.favorites || []);
                this.state.currentView = parsed.currentView || 'store';
                this.state.currentCategory = parsed.currentCategory || 'all';
                this.state.gameHistory = parsed.gameHistory || [];
            }
        } catch (error) {
            console.error('Error loading state:', error);
        }
    }

    saveState() {
        try {
            const stateToSave = {
                installedGames: Array.from(this.state.installedGames),
                favorites: Array.from(this.state.favorites),
                currentView: this.state.currentView,
                currentCategory: this.state.currentCategory,
                gameHistory: this.state.gameHistory
            };
            localStorage.setItem('retroplay_state', JSON.stringify(stateToSave));
        } catch (error) {
            console.error('Error saving state:', error);
        }
    }

    subscribe(event, callback) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, []);
        }
        this.listeners.get(event).push(callback);
    }

    emit(event, data) {
        if (this.listeners.has(event)) {
            this.listeners.get(event).forEach(callback => callback(data));
        }
    }

    updateState(updates) {
        Object.assign(this.state, updates);
        this.saveState();
        this.emit('stateChanged', this.state);
    }

    getState() {
        return { ...this.state };
    }
}

class GameManager {
    constructor(stateManager, gameLibrary) {
        this.stateManager = stateManager;
        this.gameLibrary = gameLibrary || {};
        this.currentGame = null;
        this.gameRunning = false;
        this.gameLoop = null;
        this.blobUrls = new Map(); // Track blob URLs for cleanup

        // DOM elements
        this.gameDisplay = document.getElementById('game-display');
        this.emulatorContainer = document.getElementById('emulator-container');
        this.gameIframe = document.getElementById('game-iframe');
        this.modalOverlay = document.getElementById('modal-overlay');
        this.gameDetailsModal = document.getElementById('game-details-modal');
        this.gamesGrid = document.getElementById('games-grid');
        this.storeView = document.getElementById('store-view');
        this.libraryView = document.getElementById('library-view');
        this.searchInput = document.getElementById('search-input');
        this.categoryFilter = document.getElementById('category-filter');
        this.viewToggle = document.getElementById('view-toggle');

        this.setupEventDelegation();
        this.setupStateListeners();
        this.initializeFilters();
    }

    setupEventDelegation() {
        // Event delegation for game cards (launch, favorite, details)
        if (this.gamesGrid) {
            this.gamesGrid.addEventListener('click', (e) => {
                const target = e.target;
                const gameCard = target.closest('.game-card');

                if (!gameCard) return;

                const gameId = gameCard.dataset.gameId;

                // Handle play/launch button
                if (target.closest('.play-button')) {
                    e.stopPropagation();
                    this.launchGame(gameId);
                }
                // Handle favorite button
                else if (target.closest('.favorite-button')) {
                    e.stopPropagation();
                    this.toggleFavorite(gameId);
                }
                // Handle card click for details (but not play or favorite buttons)
                else {
                    this.showGameDetails(gameId);
                }
            });
        }

        // Close emulator button
        const closeEmulatorBtn = document.getElementById('close-emulator');
        if (closeEmulatorBtn) {
            closeEmulatorBtn.addEventListener('click', () => this.closeEmulator());
        }

        // Modal close buttons
        if (this.modalOverlay) {
            this.modalOverlay.addEventListener('click', (e) => {
                if (e.target === this.modalOverlay) {
                    this.closeModal();
                }
            });
        }

        const closeModalBtns = document.querySelectorAll('.close-modal');
        closeModalBtns.forEach(btn => {
            btn.addEventListener('click', () => this.closeModal());
        });

        // View toggle (store/library)
        if (this.viewToggle) {
            this.viewToggle.addEventListener('change', (e) => {
                const view = e.target.value;
                this.stateManager.updateState({ currentView: view });
                this.filterGames();
            });
        }

        // Category filter
        if (this.categoryFilter) {
            this.categoryFilter.addEventListener('change', (e) => {
                const category = e.target.value;
                this.stateManager.updateState({ currentCategory: category });
                this.filterGames();
            });
        }

        // Search input
        if (this.searchInput) {
            this.searchInput.addEventListener('input', (e) => {
                const query = e.target.value.toLowerCase();
                this.stateManager.updateState({ searchQuery: query });
                this.filterGames();
            });
        }

        // Play button in details modal
        const playFromModalBtn = document.getElementById('play-from-modal');
        if (playFromModalBtn) {
            playFromModalBtn.addEventListener('click', () => {
                const gameId = playFromModalBtn.dataset.gameId;
                this.closeModal();
                this.launchGame(gameId);
            });
        }
    }

    setupStateListeners() {
        this.stateManager.subscribe('stateChanged', (state) => {
            this.updateUI(state);
        });
    }

    initializeFilters() {
        // Set initial filter values from state
        const state = this.stateManager.getState();

        if (this.viewToggle) {
            this.viewToggle.value = state.currentView;
        }

        if (this.categoryFilter) {
            this.categoryFilter.value = state.currentCategory;
        }

        // Initial render
        this.filterGames();
    }

    async launchGame(gameId) {
        try {
            const game = this.gameLibrary[gameId];

            if (!game) {
                throw new Error(`Game ${gameId} not found in library`);
            }

            console.log(`Launching game: ${game.name}`);

            // Mark game as installed
            const state = this.stateManager.getState();
            state.installedGames.add(gameId);
            this.stateManager.updateState({
                installedGames: state.installedGames,
                currentGame: gameId
            });

            // Add to game history
            this.addToHistory(gameId);

            // Handle different game types
            if (game.type === 'local') {
                await this.launchLocalGame(game);
            } else if (game.type === 'iframe') {
                await this.launchIframeGame(game);
            } else {
                // Default: embedded game with canvas/renderer
                await this.launchEmbeddedGame(game);
            }

            // Show emulator container
            if (this.emulatorContainer) {
                this.emulatorContainer.style.display = 'flex';
            }

            console.log(`Game ${game.name} launched successfully`);
        } catch (error) {
            console.error('Error launching game:', error);
            alert(`Failed to launch game: ${error.message}`);
        }
    }

    async launchLocalGame(game) {
        // Create blob URL for local game files
        let blobUrl;

        if (game.htmlContent) {
            // Create blob from HTML content
            const blob = new Blob([game.htmlContent], { type: 'text/html' });
            blobUrl = URL.createObjectURL(blob);
        } else if (game.url) {
            // Fetch and create blob from URL
            const response = await fetch(game.url);
            if (!response.ok) {
                throw new Error(`Failed to fetch game: ${response.status}`);
            }
            const blob = await response.blob();
            blobUrl = URL.createObjectURL(blob);
        } else {
            throw new Error('No game content or URL provided');
        }

        // Store blob URL for cleanup
        this.blobUrls.set(game.id, blobUrl);

        // Set iframe src
        if (this.gameIframe) {
            this.gameIframe.src = blobUrl;
        }
    }

    async launchIframeGame(game) {
        // Set iframe src directly for external games
        if (this.gameIframe && game.url) {
            this.gameIframe.src = game.url;
        } else {
            throw new Error('Invalid iframe game configuration');
        }
    }

    async launchEmbeddedGame(game) {
        // Stop any current game
        if (this.currentGame) {
            this.stopCurrentGame();
        }

        // Clear the display
        if (this.gameDisplay) {
            this.gameDisplay.innerHTML = '';
        }

        // Initialize the new game
        this.currentGame = game;

        if (game.initialize) {
            await game.initialize(this.gameDisplay);
        }

        // Set up game loop
        if (game.update || game.render) {
            let lastTime = performance.now();
            this.gameRunning = true;

            this.gameLoop = setInterval(() => {
                if (!this.gameRunning) return;

                const currentTime = performance.now();
                const deltaTime = currentTime - lastTime;

                if (game.update) {
                    game.update(deltaTime);
                }

                if (game.render) {
                    game.render();
                }

                lastTime = currentTime;
            }, 1000 / 60); // 60 FPS
        }
    }

    stopCurrentGame() {
        if (this.gameLoop) {
            clearInterval(this.gameLoop);
            this.gameLoop = null;
        }

        this.gameRunning = false;

        if (this.currentGame && this.currentGame.cleanup) {
            this.currentGame.cleanup();
        }

        this.currentGame = null;
    }

    closeEmulator() {
        console.log('Closing emulator');

        // Stop current game
        this.stopCurrentGame();

        // Clear iframe
        if (this.gameIframe) {
            this.gameIframe.src = 'about:blank';
        }

        // Cleanup blob URLs
        this.blobUrls.forEach((url, gameId) => {
            URL.revokeObjectURL(url);
        });
        this.blobUrls.clear();

        // Hide emulator container
        if (this.emulatorContainer) {
            this.emulatorContainer.style.display = 'none';
        }

        // Update state
        this.stateManager.updateState({ currentGame: null });
    }

    showGameDetails(gameId) {
        const game = this.gameLibrary[gameId];

        if (!game) {
            console.error(`Game ${gameId} not found`);
            return;
        }

        console.log(`Showing details for: ${game.name}`);

        // Populate modal with game details
        const modalTitle = document.getElementById('modal-game-title');
        const modalIcon = document.getElementById('modal-game-icon');
        const modalDescription = document.getElementById('modal-game-description');
        const modalCategory = document.getElementById('modal-game-category');
        const modalRating = document.getElementById('modal-game-rating');
        const modalPlays = document.getElementById('modal-game-plays');
        const playFromModalBtn = document.getElementById('play-from-modal');

        if (modalTitle) modalTitle.textContent = game.name;
        if (modalIcon) modalIcon.textContent = game.icon || '🎮';
        if (modalDescription) modalDescription.textContent = game.description || 'No description available';
        if (modalCategory) modalCategory.textContent = game.category || 'Uncategorized';
        if (modalRating) modalRating.textContent = `⭐ ${game.rating || 'N/A'}`;
        if (modalPlays) modalPlays.textContent = `🎮 ${game.plays || 0} plays`;

        if (playFromModalBtn) {
            playFromModalBtn.dataset.gameId = gameId;
        }

        // Show modal
        if (this.modalOverlay) {
            this.modalOverlay.style.display = 'flex';
        }

        if (this.gameDetailsModal) {
            this.gameDetailsModal.style.display = 'block';
        }
    }

    closeModal() {
        console.log('Closing modal');

        if (this.modalOverlay) {
            this.modalOverlay.style.display = 'none';
        }

        // Hide all modals
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            modal.style.display = 'none';
        });
    }

    toggleFavorite(gameId) {
        const state = this.stateManager.getState();

        if (state.favorites.has(gameId)) {
            state.favorites.delete(gameId);
            console.log(`Removed ${gameId} from favorites`);
        } else {
            state.favorites.add(gameId);
            console.log(`Added ${gameId} to favorites`);
        }

        // Update state and save to localStorage
        this.stateManager.updateState({ favorites: state.favorites });

        // Update UI for this specific game card
        this.updateFavoriteButton(gameId, state.favorites.has(gameId));
    }

    updateFavoriteButton(gameId, isFavorite) {
        const gameCard = document.querySelector(`[data-game-id="${gameId}"]`);
        if (!gameCard) return;

        const favoriteBtn = gameCard.querySelector('.favorite-button');
        if (favoriteBtn) {
            favoriteBtn.classList.toggle('favorited', isFavorite);
            favoriteBtn.textContent = isFavorite ? '❤️' : '🤍';
        }
    }

    filterGames() {
        const state = this.stateManager.getState();
        const { currentView, currentCategory, searchQuery, installedGames, favorites } = state;

        console.log('Filtering games:', { currentView, currentCategory, searchQuery });

        // Get all game cards
        const gameCards = this.gamesGrid ? this.gamesGrid.querySelectorAll('.game-card') : [];

        gameCards.forEach(card => {
            const gameId = card.dataset.gameId;
            const game = this.gameLibrary[gameId];

            if (!game) {
                card.style.display = 'none';
                return;
            }

            let showCard = true;

            // Filter by view (store/library)
            if (currentView === 'library') {
                // Only show installed games in library view
                if (!installedGames.has(gameId)) {
                    showCard = false;
                }
            }

            // Filter by category
            if (showCard && currentCategory !== 'all') {
                if (currentCategory === 'favorites') {
                    showCard = favorites.has(gameId);
                } else if (game.category !== currentCategory) {
                    showCard = false;
                }
            }

            // Filter by search query
            if (showCard && searchQuery) {
                const searchLower = searchQuery.toLowerCase();
                const nameMatch = game.name.toLowerCase().includes(searchLower);
                const descMatch = game.description && game.description.toLowerCase().includes(searchLower);
                const categoryMatch = game.category && game.category.toLowerCase().includes(searchLower);

                showCard = nameMatch || descMatch || categoryMatch;
            }

            card.style.display = showCard ? 'block' : 'none';
        });

        // Update view counts
        this.updateViewCounts();
    }

    updateViewCounts() {
        const visibleCards = this.gamesGrid ?
            Array.from(this.gamesGrid.querySelectorAll('.game-card')).filter(card =>
                card.style.display !== 'none'
            ).length : 0;

        const countElement = document.getElementById('visible-games-count');
        if (countElement) {
            countElement.textContent = `Showing ${visibleCards} games`;
        }
    }

    updateUI(state) {
        // Update all game cards based on current state
        const gameCards = this.gamesGrid ? this.gamesGrid.querySelectorAll('.game-card') : [];

        gameCards.forEach(card => {
            const gameId = card.dataset.gameId;

            // Update favorite status
            const isFavorite = state.favorites.has(gameId);
            this.updateFavoriteButton(gameId, isFavorite);

            // Update installed status
            const isInstalled = state.installedGames.has(gameId);
            const installedBadge = card.querySelector('.installed-badge');
            if (installedBadge) {
                installedBadge.style.display = isInstalled ? 'block' : 'none';
            }
        });

        // Re-filter games
        this.filterGames();
    }

    addToHistory(gameId) {
        const state = this.stateManager.getState();
        const history = state.gameHistory || [];

        // Remove if already in history
        const index = history.indexOf(gameId);
        if (index > -1) {
            history.splice(index, 1);
        }

        // Add to beginning
        history.unshift(gameId);

        // Keep only last 10 games
        if (history.length > 10) {
            history.pop();
        }

        this.stateManager.updateState({ gameHistory: history });
    }

    renderGameCard(game) {
        const state = this.stateManager.getState();
        const isFavorite = state.favorites.has(game.id);
        const isInstalled = state.installedGames.has(game.id);

        const card = document.createElement('div');
        card.className = 'game-card';
        card.dataset.gameId = game.id;

        card.innerHTML = `
            <div class="game-icon">${game.icon || '🎮'}</div>
            <div class="game-info">
                <h3 class="game-name">${game.name}</h3>
                <p class="game-description">${game.description || ''}</p>
                <div class="game-meta">
                    <span class="game-category">${game.category || 'Game'}</span>
                    ${game.rating ? `<span class="game-rating">⭐ ${game.rating}</span>` : ''}
                </div>
            </div>
            <div class="game-actions">
                <button class="play-button" title="Play">▶️ Play</button>
                <button class="favorite-button ${isFavorite ? 'favorited' : ''}" title="Favorite">
                    ${isFavorite ? '❤️' : '🤍'}
                </button>
            </div>
            ${isInstalled ? '<span class="installed-badge">Installed</span>' : ''}
        `;

        return card;
    }

    renderAllGames() {
        if (!this.gamesGrid) return;

        this.gamesGrid.innerHTML = '';

        Object.values(this.gameLibrary).forEach(game => {
            const card = this.renderGameCard(game);
            this.gamesGrid.appendChild(card);
        });

        this.filterGames();
    }

    // Public API methods
    addGame(game) {
        if (!game.id) {
            throw new Error('Game must have an id');
        }

        this.gameLibrary[game.id] = game;
        this.renderAllGames();
    }

    removeGame(gameId) {
        delete this.gameLibrary[gameId];

        // Remove from state
        const state = this.stateManager.getState();
        state.installedGames.delete(gameId);
        state.favorites.delete(gameId);

        this.stateManager.updateState({
            installedGames: state.installedGames,
            favorites: state.favorites
        });

        this.renderAllGames();
    }

    getGameById(gameId) {
        return this.gameLibrary[gameId];
    }

    getAllGames() {
        return Object.values(this.gameLibrary);
    }

    getInstalledGames() {
        const state = this.stateManager.getState();
        return Array.from(state.installedGames)
            .map(id => this.gameLibrary[id])
            .filter(game => game);
    }

    getFavoriteGames() {
        const state = this.stateManager.getState();
        return Array.from(state.favorites)
            .map(id => this.gameLibrary[id])
            .filter(game => game);
    }

    destroy() {
        // Cleanup
        this.closeEmulator();
        this.closeModal();

        // Remove event listeners (if needed)
        this.stateManager.listeners.clear();
    }
}

// Export for use in modules or global scope
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { GameManager, StateManager };
}
