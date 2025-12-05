// WoWmon Storage & Export Manager
// Agent 8 - Comprehensive localStorage persistence and import/export functionality
// This file contains the complete StorageManager class for managing user data

class StorageManager {
    constructor() {
        this.STORAGE_KEYS = {
            FAVORITES: 'wowmon_favorites',
            TEAMS: 'wowmon_teams',
            PREFERENCES: 'wowmon_preferences',
            NOTES: 'wowmon_notes',
            SEARCH_HISTORY: 'wowmon_search_history',
            POKEDEX: 'wowmon_pokedex',
            ACHIEVEMENTS: 'wowmon_achievements'
        };
        this.MAX_STORAGE_SIZE = 5 * 1024 * 1024; // 5MB safety limit
        this.MAX_SEARCH_HISTORY = 50;
        this.MAX_TEAMS = 20;

        this.initializeStorage();
    }

    // Initialize storage with default values
    initializeStorage() {
        try {
            // Check if storage is available
            if (!this.isStorageAvailable()) {
                console.warn('localStorage not available');
                return false;
            }

            // Initialize favorites if not exists
            if (!localStorage.getItem(this.STORAGE_KEYS.FAVORITES)) {
                localStorage.setItem(this.STORAGE_KEYS.FAVORITES, JSON.stringify([]));
            }

            // Initialize teams if not exists
            if (!localStorage.getItem(this.STORAGE_KEYS.TEAMS)) {
                localStorage.setItem(this.STORAGE_KEYS.TEAMS, JSON.stringify([]));
            }

            // Initialize preferences if not exists
            if (!localStorage.getItem(this.STORAGE_KEYS.PREFERENCES)) {
                const defaultPreferences = {
                    viewMode: 'grid',
                    theme: 'default',
                    sortBy: 'id',
                    showTypes: true,
                    showStats: true,
                    autoSave: true,
                    soundEnabled: true
                };
                localStorage.setItem(this.STORAGE_KEYS.PREFERENCES, JSON.stringify(defaultPreferences));
            }

            // Initialize notes if not exists
            if (!localStorage.getItem(this.STORAGE_KEYS.NOTES)) {
                localStorage.setItem(this.STORAGE_KEYS.NOTES, JSON.stringify({}));
            }

            // Initialize search history if not exists
            if (!localStorage.getItem(this.STORAGE_KEYS.SEARCH_HISTORY)) {
                localStorage.setItem(this.STORAGE_KEYS.SEARCH_HISTORY, JSON.stringify([]));
            }

            // Initialize Pokedex entries if not exists
            if (!localStorage.getItem(this.STORAGE_KEYS.POKEDEX)) {
                localStorage.setItem(this.STORAGE_KEYS.POKEDEX, JSON.stringify({}));
            }

            return true;
        } catch (error) {
            console.error('Failed to initialize storage:', error);
            return false;
        }
    }

    // Check if localStorage is available
    isStorageAvailable() {
        try {
            const test = '__storage_test__';
            localStorage.setItem(test, test);
            localStorage.removeItem(test);
            return true;
        } catch (e) {
            return false;
        }
    }

    // Get current storage size
    getStorageSize() {
        let total = 0;
        for (let key in localStorage) {
            if (localStorage.hasOwnProperty(key)) {
                total += localStorage[key].length + key.length;
            }
        }
        return total;
    }

    // Get storage size as human-readable string
    getStorageSizeFormatted() {
        const bytes = this.getStorageSize();
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
    }

    // Check if storage quota would be exceeded
    checkStorageQuota(additionalSize = 0) {
        const currentSize = this.getStorageSize();
        return (currentSize + additionalSize) < this.MAX_STORAGE_SIZE;
    }

    // ==================== FAVORITES MANAGEMENT ====================

    getFavorites() {
        try {
            const favorites = localStorage.getItem(this.STORAGE_KEYS.FAVORITES);
            return favorites ? JSON.parse(favorites) : [];
        } catch (error) {
            console.error('Failed to get favorites:', error);
            return [];
        }
    }

    saveFavorite(creatureId) {
        try {
            const favorites = this.getFavorites();
            if (!favorites.includes(creatureId)) {
                favorites.push(creatureId);
                localStorage.setItem(this.STORAGE_KEYS.FAVORITES, JSON.stringify(favorites));
                return { success: true, message: 'Added to favorites!' };
            }
            return { success: false, message: 'Already in favorites' };
        } catch (error) {
            console.error('Failed to save favorite:', error);
            return { success: false, message: 'Failed to save favorite' };
        }
    }

    removeFavorite(creatureId) {
        try {
            let favorites = this.getFavorites();
            const index = favorites.indexOf(creatureId);
            if (index > -1) {
                favorites.splice(index, 1);
                localStorage.setItem(this.STORAGE_KEYS.FAVORITES, JSON.stringify(favorites));
                return { success: true, message: 'Removed from favorites!' };
            }
            return { success: false, message: 'Not in favorites' };
        } catch (error) {
            console.error('Failed to remove favorite:', error);
            return { success: false, message: 'Failed to remove favorite' };
        }
    }

    toggleFavorite(creatureId) {
        const favorites = this.getFavorites();
        if (favorites.includes(creatureId)) {
            return this.removeFavorite(creatureId);
        } else {
            return this.saveFavorite(creatureId);
        }
    }

    isFavorite(creatureId) {
        return this.getFavorites().includes(creatureId);
    }

    getFavoritesCount() {
        return this.getFavorites().length;
    }

    // ==================== TEAM MANAGEMENT ====================

    getTeams() {
        try {
            const teams = localStorage.getItem(this.STORAGE_KEYS.TEAMS);
            return teams ? JSON.parse(teams) : [];
        } catch (error) {
            console.error('Failed to get teams:', error);
            return [];
        }
    }

    saveTeam(team, teamName) {
        try {
            if (!team || !Array.isArray(team.creatures)) {
                return { success: false, message: 'Invalid team data' };
            }

            if (team.creatures.length === 0) {
                return { success: false, message: 'Team is empty' };
            }

            if (team.creatures.length > 6) {
                return { success: false, message: 'Team cannot have more than 6 creatures' };
            }

            const teams = this.getTeams();

            // Check if we've reached max teams
            if (teams.length >= this.MAX_TEAMS) {
                return { success: false, message: 'Maximum number of teams reached' };
            }

            const newTeam = {
                id: Date.now().toString(),
                name: teamName || `Team ${teams.length + 1}`,
                creatures: team.creatures.map(c => ({
                    id: c.id,
                    nickname: c.nickname || null,
                    level: c.level,
                    moves: c.moves || []
                })),
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString()
            };

            teams.push(newTeam);
            localStorage.setItem(this.STORAGE_KEYS.TEAMS, JSON.stringify(teams));
            return { success: true, message: 'Team saved!', teamId: newTeam.id };
        } catch (error) {
            console.error('Failed to save team:', error);
            return { success: false, message: 'Failed to save team' };
        }
    }

    updateTeam(teamId, updatedTeam) {
        try {
            const teams = this.getTeams();
            const index = teams.findIndex(t => t.id === teamId);

            if (index === -1) {
                return { success: false, message: 'Team not found' };
            }

            teams[index] = {
                ...teams[index],
                ...updatedTeam,
                updatedAt: new Date().toISOString()
            };

            localStorage.setItem(this.STORAGE_KEYS.TEAMS, JSON.stringify(teams));
            return { success: true, message: 'Team updated!' };
        } catch (error) {
            console.error('Failed to update team:', error);
            return { success: false, message: 'Failed to update team' };
        }
    }

    deleteTeam(teamId) {
        try {
            let teams = this.getTeams();
            const initialLength = teams.length;
            teams = teams.filter(t => t.id !== teamId);

            if (teams.length === initialLength) {
                return { success: false, message: 'Team not found' };
            }

            localStorage.setItem(this.STORAGE_KEYS.TEAMS, JSON.stringify(teams));
            return { success: true, message: 'Team deleted!' };
        } catch (error) {
            console.error('Failed to delete team:', error);
            return { success: false, message: 'Failed to delete team' };
        }
    }

    getTeam(teamId) {
        const teams = this.getTeams();
        return teams.find(t => t.id === teamId) || null;
    }

    // ==================== NOTES MANAGEMENT ====================

    getNotes() {
        try {
            const notes = localStorage.getItem(this.STORAGE_KEYS.NOTES);
            return notes ? JSON.parse(notes) : {};
        } catch (error) {
            console.error('Failed to get notes:', error);
            return {};
        }
    }

    getNote(creatureId) {
        const notes = this.getNotes();
        return notes[creatureId] || '';
    }

    saveNote(creatureId, noteText) {
        try {
            const notes = this.getNotes();
            if (noteText && noteText.trim()) {
                notes[creatureId] = noteText.trim();
            } else {
                delete notes[creatureId];
            }
            localStorage.setItem(this.STORAGE_KEYS.NOTES, JSON.stringify(notes));
            return { success: true, message: 'Note saved!' };
        } catch (error) {
            console.error('Failed to save note:', error);
            return { success: false, message: 'Failed to save note' };
        }
    }

    deleteNote(creatureId) {
        try {
            const notes = this.getNotes();
            delete notes[creatureId];
            localStorage.setItem(this.STORAGE_KEYS.NOTES, JSON.stringify(notes));
            return { success: true, message: 'Note deleted!' };
        } catch (error) {
            console.error('Failed to delete note:', error);
            return { success: false, message: 'Failed to delete note' };
        }
    }

    // ==================== SEARCH HISTORY ====================

    getSearchHistory() {
        try {
            const history = localStorage.getItem(this.STORAGE_KEYS.SEARCH_HISTORY);
            return history ? JSON.parse(history) : [];
        } catch (error) {
            console.error('Failed to get search history:', error);
            return [];
        }
    }

    addSearchHistory(searchTerm) {
        try {
            if (!searchTerm || !searchTerm.trim()) return;

            let history = this.getSearchHistory();

            // Remove if already exists
            history = history.filter(term => term !== searchTerm);

            // Add to beginning
            history.unshift(searchTerm);

            // Limit size
            if (history.length > this.MAX_SEARCH_HISTORY) {
                history = history.slice(0, this.MAX_SEARCH_HISTORY);
            }

            localStorage.setItem(this.STORAGE_KEYS.SEARCH_HISTORY, JSON.stringify(history));
        } catch (error) {
            console.error('Failed to add search history:', error);
        }
    }

    clearSearchHistory() {
        try {
            localStorage.setItem(this.STORAGE_KEYS.SEARCH_HISTORY, JSON.stringify([]));
            return { success: true, message: 'Search history cleared!' };
        } catch (error) {
            console.error('Failed to clear search history:', error);
            return { success: false, message: 'Failed to clear search history' };
        }
    }

    // ==================== PREFERENCES ====================

    getPreferences() {
        try {
            const prefs = localStorage.getItem(this.STORAGE_KEYS.PREFERENCES);
            return prefs ? JSON.parse(prefs) : {};
        } catch (error) {
            console.error('Failed to get preferences:', error);
            return {};
        }
    }

    savePreferences(preferences) {
        try {
            const current = this.getPreferences();
            const updated = { ...current, ...preferences };
            localStorage.setItem(this.STORAGE_KEYS.PREFERENCES, JSON.stringify(updated));
            return { success: true, message: 'Preferences saved!' };
        } catch (error) {
            console.error('Failed to save preferences:', error);
            return { success: false, message: 'Failed to save preferences' };
        }
    }

    getPreference(key, defaultValue = null) {
        const prefs = this.getPreferences();
        return prefs.hasOwnProperty(key) ? prefs[key] : defaultValue;
    }

    setPreference(key, value) {
        const prefs = this.getPreferences();
        prefs[key] = value;
        return this.savePreferences(prefs);
    }

    // ==================== POKEDEX ENTRIES ====================

    getPokedexEntries() {
        try {
            const pokedex = localStorage.getItem(this.STORAGE_KEYS.POKEDEX);
            return pokedex ? JSON.parse(pokedex) : {};
        } catch (error) {
            console.error('Failed to get pokedex entries:', error);
            return {};
        }
    }

    markCreatureSeen(creatureId) {
        try {
            const pokedex = this.getPokedexEntries();
            if (!pokedex[creatureId]) {
                pokedex[creatureId] = {
                    seen: true,
                    caught: false,
                    firstSeenAt: new Date().toISOString()
                };
            } else {
                pokedex[creatureId].seen = true;
            }
            localStorage.setItem(this.STORAGE_KEYS.POKEDEX, JSON.stringify(pokedex));
        } catch (error) {
            console.error('Failed to mark creature as seen:', error);
        }
    }

    markCreatureCaught(creatureId) {
        try {
            const pokedex = this.getPokedexEntries();
            if (!pokedex[creatureId]) {
                pokedex[creatureId] = {
                    seen: true,
                    caught: true,
                    firstSeenAt: new Date().toISOString(),
                    firstCaughtAt: new Date().toISOString()
                };
            } else {
                pokedex[creatureId].seen = true;
                pokedex[creatureId].caught = true;
                if (!pokedex[creatureId].firstCaughtAt) {
                    pokedex[creatureId].firstCaughtAt = new Date().toISOString();
                }
            }
            localStorage.setItem(this.STORAGE_KEYS.POKEDEX, JSON.stringify(pokedex));
        } catch (error) {
            console.error('Failed to mark creature as caught:', error);
        }
    }

    getPokedexEntry(creatureId) {
        const pokedex = this.getPokedexEntries();
        return pokedex[creatureId] || { seen: false, caught: false };
    }

    getPokedexStats() {
        const pokedex = this.getPokedexEntries();
        const entries = Object.values(pokedex);
        return {
            totalSeen: entries.filter(e => e.seen).length,
            totalCaught: entries.filter(e => e.caught).length,
            total: entries.length
        };
    }

    // ==================== EXPORT FUNCTIONALITY ====================

    exportFavorites() {
        try {
            const favorites = this.getFavorites();
            const exportData = {
                type: 'wowmon_favorites',
                version: '1.0',
                timestamp: new Date().toISOString(),
                data: favorites
            };
            return {
                success: true,
                data: exportData,
                json: JSON.stringify(exportData, null, 2)
            };
        } catch (error) {
            console.error('Failed to export favorites:', error);
            return { success: false, message: 'Failed to export favorites' };
        }
    }

    exportTeams() {
        try {
            const teams = this.getTeams();
            const exportData = {
                type: 'wowmon_teams',
                version: '1.0',
                timestamp: new Date().toISOString(),
                data: teams
            };
            return {
                success: true,
                data: exportData,
                json: JSON.stringify(exportData, null, 2)
            };
        } catch (error) {
            console.error('Failed to export teams:', error);
            return { success: false, message: 'Failed to export teams' };
        }
    }

    exportTeamShowdownFormat(teamId) {
        try {
            const team = this.getTeam(teamId);
            if (!team) {
                return { success: false, message: 'Team not found' };
            }

            let showdownText = `=== ${team.name} ===\n\n`;
            team.creatures.forEach(creature => {
                showdownText += `${creature.nickname || creature.id} (${creature.id})\n`;
                showdownText += `Level: ${creature.level}\n`;
                if (creature.moves && creature.moves.length > 0) {
                    creature.moves.forEach(move => {
                        showdownText += `- ${move}\n`;
                    });
                }
                showdownText += `\n`;
            });

            return { success: true, text: showdownText };
        } catch (error) {
            console.error('Failed to export team in Showdown format:', error);
            return { success: false, message: 'Failed to export team' };
        }
    }

    exportNotes() {
        try {
            const notes = this.getNotes();
            const exportData = {
                type: 'wowmon_notes',
                version: '1.0',
                timestamp: new Date().toISOString(),
                data: notes
            };
            return {
                success: true,
                data: exportData,
                json: JSON.stringify(exportData, null, 2)
            };
        } catch (error) {
            console.error('Failed to export notes:', error);
            return { success: false, message: 'Failed to export notes' };
        }
    }

    exportPokedex() {
        try {
            const pokedex = this.getPokedexEntries();
            const exportData = {
                type: 'wowmon_pokedex',
                version: '1.0',
                timestamp: new Date().toISOString(),
                data: pokedex,
                stats: this.getPokedexStats()
            };
            return {
                success: true,
                data: exportData,
                json: JSON.stringify(exportData, null, 2)
            };
        } catch (error) {
            console.error('Failed to export pokedex:', error);
            return { success: false, message: 'Failed to export pokedex' };
        }
    }

    exportAllData() {
        try {
            const exportData = {
                type: 'wowmon_all_data',
                version: '1.0',
                timestamp: new Date().toISOString(),
                data: {
                    favorites: this.getFavorites(),
                    teams: this.getTeams(),
                    notes: this.getNotes(),
                    preferences: this.getPreferences(),
                    searchHistory: this.getSearchHistory(),
                    pokedex: this.getPokedexEntries()
                }
            };
            return {
                success: true,
                data: exportData,
                json: JSON.stringify(exportData, null, 2)
            };
        } catch (error) {
            console.error('Failed to export all data:', error);
            return { success: false, message: 'Failed to export data' };
        }
    }

    // ==================== IMPORT FUNCTIONALITY ====================

    validateImportData(data, expectedType) {
        if (!data || typeof data !== 'object') {
            return { valid: false, message: 'Invalid data format' };
        }

        if (!data.type || !data.version) {
            return { valid: false, message: 'Missing type or version' };
        }

        if (expectedType && data.type !== expectedType) {
            return { valid: false, message: `Expected type ${expectedType}, got ${data.type}` };
        }

        if (!data.data) {
            return { valid: false, message: 'Missing data field' };
        }

        return { valid: true };
    }

    importFavorites(jsonString, merge = true) {
        try {
            const importData = JSON.parse(jsonString);
            const validation = this.validateImportData(importData, 'wowmon_favorites');

            if (!validation.valid) {
                return { success: false, message: validation.message };
            }

            if (!Array.isArray(importData.data)) {
                return { success: false, message: 'Invalid favorites data format' };
            }

            let favorites = merge ? this.getFavorites() : [];

            // Add imported favorites (avoid duplicates)
            importData.data.forEach(id => {
                if (!favorites.includes(id)) {
                    favorites.push(id);
                }
            });

            localStorage.setItem(this.STORAGE_KEYS.FAVORITES, JSON.stringify(favorites));
            return { success: true, message: `Imported ${importData.data.length} favorites!` };
        } catch (error) {
            console.error('Failed to import favorites:', error);
            return { success: false, message: 'Failed to parse import data' };
        }
    }

    importTeams(jsonString, merge = true) {
        try {
            const importData = JSON.parse(jsonString);
            const validation = this.validateImportData(importData, 'wowmon_teams');

            if (!validation.valid) {
                return { success: false, message: validation.message };
            }

            if (!Array.isArray(importData.data)) {
                return { success: false, message: 'Invalid teams data format' };
            }

            let teams = merge ? this.getTeams() : [];

            // Add imported teams
            importData.data.forEach(team => {
                // Ensure team has required fields
                if (team.creatures && Array.isArray(team.creatures)) {
                    teams.push({
                        ...team,
                        id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
                        importedAt: new Date().toISOString()
                    });
                }
            });

            // Check max teams limit
            if (teams.length > this.MAX_TEAMS) {
                teams = teams.slice(0, this.MAX_TEAMS);
            }

            localStorage.setItem(this.STORAGE_KEYS.TEAMS, JSON.stringify(teams));
            return { success: true, message: `Imported ${importData.data.length} teams!` };
        } catch (error) {
            console.error('Failed to import teams:', error);
            return { success: false, message: 'Failed to parse import data' };
        }
    }

    importNotes(jsonString, merge = true) {
        try {
            const importData = JSON.parse(jsonString);
            const validation = this.validateImportData(importData, 'wowmon_notes');

            if (!validation.valid) {
                return { success: false, message: validation.message };
            }

            if (typeof importData.data !== 'object') {
                return { success: false, message: 'Invalid notes data format' };
            }

            let notes = merge ? this.getNotes() : {};

            // Add imported notes
            Object.assign(notes, importData.data);

            localStorage.setItem(this.STORAGE_KEYS.NOTES, JSON.stringify(notes));
            return { success: true, message: 'Notes imported successfully!' };
        } catch (error) {
            console.error('Failed to import notes:', error);
            return { success: false, message: 'Failed to parse import data' };
        }
    }

    importPokedex(jsonString, merge = true) {
        try {
            const importData = JSON.parse(jsonString);
            const validation = this.validateImportData(importData, 'wowmon_pokedex');

            if (!validation.valid) {
                return { success: false, message: validation.message };
            }

            if (typeof importData.data !== 'object') {
                return { success: false, message: 'Invalid pokedex data format' };
            }

            let pokedex = merge ? this.getPokedexEntries() : {};

            // Merge imported pokedex data
            Object.keys(importData.data).forEach(creatureId => {
                const existing = pokedex[creatureId];
                const imported = importData.data[creatureId];

                if (merge && existing) {
                    // Merge, keeping "most complete" data
                    pokedex[creatureId] = {
                        seen: existing.seen || imported.seen,
                        caught: existing.caught || imported.caught,
                        firstSeenAt: existing.firstSeenAt || imported.firstSeenAt,
                        firstCaughtAt: existing.firstCaughtAt || imported.firstCaughtAt
                    };
                } else {
                    pokedex[creatureId] = imported;
                }
            });

            localStorage.setItem(this.STORAGE_KEYS.POKEDEX, JSON.stringify(pokedex));
            return { success: true, message: 'Pokedex imported successfully!' };
        } catch (error) {
            console.error('Failed to import pokedex:', error);
            return { success: false, message: 'Failed to parse import data' };
        }
    }

    importAllData(jsonString) {
        try {
            const importData = JSON.parse(jsonString);
            const validation = this.validateImportData(importData, 'wowmon_all_data');

            if (!validation.valid) {
                return { success: false, message: validation.message };
            }

            const data = importData.data;
            let imported = 0;

            // Import each data type
            if (data.favorites) {
                const result = this.importFavorites(JSON.stringify({
                    type: 'wowmon_favorites',
                    version: '1.0',
                    data: data.favorites
                }), true);
                if (result.success) imported++;
            }

            if (data.teams) {
                const result = this.importTeams(JSON.stringify({
                    type: 'wowmon_teams',
                    version: '1.0',
                    data: data.teams
                }), true);
                if (result.success) imported++;
            }

            if (data.notes) {
                const result = this.importNotes(JSON.stringify({
                    type: 'wowmon_notes',
                    version: '1.0',
                    data: data.notes
                }), true);
                if (result.success) imported++;
            }

            if (data.preferences) {
                this.savePreferences(data.preferences);
                imported++;
            }

            if (data.searchHistory && Array.isArray(data.searchHistory)) {
                localStorage.setItem(this.STORAGE_KEYS.SEARCH_HISTORY, JSON.stringify(data.searchHistory));
                imported++;
            }

            if (data.pokedex) {
                const result = this.importPokedex(JSON.stringify({
                    type: 'wowmon_pokedex',
                    version: '1.0',
                    data: data.pokedex
                }), true);
                if (result.success) imported++;
            }

            return { success: true, message: `Imported ${imported} data categories!` };
        } catch (error) {
            console.error('Failed to import all data:', error);
            return { success: false, message: 'Failed to parse import data' };
        }
    }

    // ==================== SHARING FEATURES ====================

    generateShareableURL(data) {
        try {
            const encoded = btoa(JSON.stringify(data));
            const baseUrl = window.location.href.split('?')[0];
            return `${baseUrl}?share=${encoded}`;
        } catch (error) {
            console.error('Failed to generate shareable URL:', error);
            return null;
        }
    }

    parseSharedURL() {
        try {
            const urlParams = new URLSearchParams(window.location.search);
            const shared = urlParams.get('share');
            if (shared) {
                return JSON.parse(atob(shared));
            }
            return null;
        } catch (error) {
            console.error('Failed to parse shared URL:', error);
            return null;
        }
    }

    copyToClipboard(text) {
        try {
            if (navigator.clipboard && navigator.clipboard.writeText) {
                return navigator.clipboard.writeText(text)
                    .then(() => ({ success: true, message: 'Copied to clipboard!' }))
                    .catch(() => ({ success: false, message: 'Failed to copy' }));
            } else {
                // Fallback for older browsers
                const textarea = document.createElement('textarea');
                textarea.value = text;
                textarea.style.position = 'fixed';
                textarea.style.opacity = '0';
                document.body.appendChild(textarea);
                textarea.select();
                const success = document.execCommand('copy');
                document.body.removeChild(textarea);
                return Promise.resolve({
                    success: success,
                    message: success ? 'Copied to clipboard!' : 'Failed to copy'
                });
            }
        } catch (error) {
            console.error('Failed to copy to clipboard:', error);
            return Promise.resolve({ success: false, message: 'Failed to copy' });
        }
    }

    // ==================== DATA MANAGEMENT ====================

    clearAllData(confirm = false) {
        if (!confirm) {
            return { success: false, message: 'Confirmation required' };
        }

        try {
            Object.values(this.STORAGE_KEYS).forEach(key => {
                localStorage.removeItem(key);
            });
            this.initializeStorage();
            return { success: true, message: 'All data cleared!' };
        } catch (error) {
            console.error('Failed to clear all data:', error);
            return { success: false, message: 'Failed to clear data' };
        }
    }

    clearFavorites(confirm = false) {
        if (!confirm) {
            return { success: false, message: 'Confirmation required' };
        }

        try {
            localStorage.setItem(this.STORAGE_KEYS.FAVORITES, JSON.stringify([]));
            return { success: true, message: 'Favorites cleared!' };
        } catch (error) {
            console.error('Failed to clear favorites:', error);
            return { success: false, message: 'Failed to clear favorites' };
        }
    }

    clearTeams(confirm = false) {
        if (!confirm) {
            return { success: false, message: 'Confirmation required' };
        }

        try {
            localStorage.setItem(this.STORAGE_KEYS.TEAMS, JSON.stringify([]));
            return { success: true, message: 'Teams cleared!' };
        } catch (error) {
            console.error('Failed to clear teams:', error);
            return { success: false, message: 'Failed to clear teams' };
        }
    }

    clearNotes(confirm = false) {
        if (!confirm) {
            return { success: false, message: 'Confirmation required' };
        }

        try {
            localStorage.setItem(this.STORAGE_KEYS.NOTES, JSON.stringify({}));
            return { success: true, message: 'Notes cleared!' };
        } catch (error) {
            console.error('Failed to clear notes:', error);
            return { success: false, message: 'Failed to clear notes' };
        }
    }

    clearPokedex(confirm = false) {
        if (!confirm) {
            return { success: false, message: 'Confirmation required' };
        }

        try {
            localStorage.setItem(this.STORAGE_KEYS.POKEDEX, JSON.stringify({}));
            return { success: true, message: 'Pokedex cleared!' };
        } catch (error) {
            console.error('Failed to clear pokedex:', error);
            return { success: false, message: 'Failed to clear pokedex' };
        }
    }

    // ==================== DOWNLOAD HELPERS ====================

    downloadJSON(data, filename) {
        try {
            const dataStr = JSON.stringify(data, null, 2);
            const dataBlob = new Blob([dataStr], { type: 'application/json' });
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
            return { success: true, message: 'Downloaded successfully!' };
        } catch (error) {
            console.error('Failed to download JSON:', error);
            return { success: false, message: 'Failed to download file' };
        }
    }

    downloadText(text, filename) {
        try {
            const dataBlob = new Blob([text], { type: 'text/plain' });
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
            return { success: true, message: 'Downloaded successfully!' };
        } catch (error) {
            console.error('Failed to download text:', error);
            return { success: false, message: 'Failed to download file' };
        }
    }

    // ==================== AUTO-BACKUP ====================

    createAutoBackup() {
        try {
            const backup = this.exportAllData();
            if (backup.success) {
                localStorage.setItem('wowmon_auto_backup', backup.json);
                localStorage.setItem('wowmon_auto_backup_timestamp', new Date().toISOString());
                return { success: true, message: 'Auto-backup created!' };
            }
            return { success: false, message: 'Failed to create backup' };
        } catch (error) {
            console.error('Failed to create auto-backup:', error);
            return { success: false, message: 'Failed to create backup' };
        }
    }

    restoreAutoBackup() {
        try {
            const backup = localStorage.getItem('wowmon_auto_backup');
            if (!backup) {
                return { success: false, message: 'No backup found' };
            }

            const result = this.importAllData(backup);
            if (result.success) {
                return { success: true, message: 'Backup restored successfully!' };
            }
            return { success: false, message: 'Failed to restore backup' };
        } catch (error) {
            console.error('Failed to restore auto-backup:', error);
            return { success: false, message: 'Failed to restore backup' };
        }
    }

    getAutoBackupInfo() {
        try {
            const timestamp = localStorage.getItem('wowmon_auto_backup_timestamp');
            if (!timestamp) {
                return { exists: false };
            }

            return {
                exists: true,
                timestamp: timestamp,
                date: new Date(timestamp).toLocaleString()
            };
        } catch (error) {
            console.error('Failed to get auto-backup info:', error);
            return { exists: false };
        }
    }
}

// Export for use in other modules if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = StorageManager;
}
