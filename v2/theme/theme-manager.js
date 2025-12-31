/**
 * Theme Manager - Theme switching and persistence
 * Local First Tools v2
 */

import { EventBus, EVENTS } from '../core/event-bus.js';
import { StorageManager } from '../storage/storage-manager.js';
import { THEMES, getThemeColors } from './presets.js';

class ThemeManager {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {ThemeManager}
     */
    static getInstance() {
        if (!ThemeManager.#instance) {
            ThemeManager.#instance = new ThemeManager();
        }
        return ThemeManager.#instance;
    }

    constructor() {
        if (ThemeManager.#instance) {
            return ThemeManager.#instance;
        }

        this.events = EventBus.getInstance();
        this.storage = StorageManager.getInstance();

        this.#currentTheme = 'dark';
        this.#customTheme = null;
        this.#systemPreference = this.#getSystemPreference();

        this.#initialize();
    }

    #currentTheme;
    #customTheme;
    #systemPreference;

    /**
     * Initialize theme manager
     */
    #initialize() {
        // Load saved theme preference
        const savedTheme = this.storage.get('theme');

        if (savedTheme === 'system') {
            this.#applySystemPreference();
        } else if (savedTheme && THEMES[savedTheme]) {
            this.setTheme(savedTheme);
        } else if (savedTheme === 'custom') {
            const customColors = this.storage.get('customTheme');
            if (customColors) {
                this.#customTheme = customColors;
                this.setTheme('custom');
            }
        } else {
            // Default to dark theme
            this.setTheme('dark');
        }

        // Listen for system preference changes
        this.#watchSystemPreference();

        // Listen for theme toggle events
        this.events.on(EVENTS.THEME_TOGGLE, () => this.toggle());
    }

    /**
     * Get system color scheme preference
     * @returns {string}
     */
    #getSystemPreference() {
        if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        return 'light';
    }

    /**
     * Watch for system preference changes
     */
    #watchSystemPreference() {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

        mediaQuery.addEventListener('change', (e) => {
            this.#systemPreference = e.matches ? 'dark' : 'light';

            const savedTheme = this.storage.get('theme');
            if (savedTheme === 'system') {
                this.#applySystemPreference();
            }
        });
    }

    /**
     * Apply system color preference
     */
    #applySystemPreference() {
        this.#applyTheme(this.#systemPreference);
        this.#currentTheme = 'system';
    }

    /**
     * Set active theme
     * @param {string} themeName
     */
    setTheme(themeName) {
        if (themeName === 'system') {
            this.#applySystemPreference();
            this.storage.set('theme', 'system');
            return;
        }

        if (themeName === 'custom' && this.#customTheme) {
            this.#applyCustomTheme(this.#customTheme);
            this.#currentTheme = 'custom';
            this.storage.set('theme', 'custom');
            return;
        }

        if (!THEMES[themeName]) {
            console.warn(`Theme "${themeName}" not found, using dark`);
            themeName = 'dark';
        }

        this.#applyTheme(themeName);
        this.#currentTheme = themeName;
        this.storage.set('theme', themeName);
    }

    /**
     * Apply theme by name
     * @param {string} themeName
     */
    #applyTheme(themeName) {
        const colors = getThemeColors(themeName);
        this.#applyColors(colors);

        // Update document attribute
        document.documentElement.setAttribute('data-theme', themeName);

        // Update meta theme-color for mobile browsers
        const metaThemeColor = document.querySelector('meta[name="theme-color"]');
        if (metaThemeColor) {
            metaThemeColor.content = colors['--color-bg-primary'] || '#0a0a0a';
        }

        this.events.emit(EVENTS.THEME_CHANGE, { theme: themeName, colors });
    }

    /**
     * Apply custom theme colors
     * @param {Object} colors
     */
    #applyCustomTheme(colors) {
        this.#applyColors(colors);
        document.documentElement.setAttribute('data-theme', 'custom');

        this.events.emit(EVENTS.THEME_CHANGE, { theme: 'custom', colors });
    }

    /**
     * Apply color variables to document
     * @param {Object} colors
     */
    #applyColors(colors) {
        const root = document.documentElement;

        for (const [property, value] of Object.entries(colors)) {
            root.style.setProperty(property, value);
        }
    }

    /**
     * Toggle between themes
     */
    toggle() {
        const themes = Object.keys(THEMES);
        const currentIndex = themes.indexOf(this.#currentTheme);
        const nextIndex = (currentIndex + 1) % themes.length;

        this.setTheme(themes[nextIndex]);
    }

    /**
     * Cycle to next theme
     */
    next() {
        this.toggle();
    }

    /**
     * Cycle to previous theme
     */
    previous() {
        const themes = Object.keys(THEMES);
        const currentIndex = themes.indexOf(this.#currentTheme);
        const prevIndex = (currentIndex - 1 + themes.length) % themes.length;

        this.setTheme(themes[prevIndex]);
    }

    /**
     * Get current theme name
     * @returns {string}
     */
    getCurrentTheme() {
        return this.#currentTheme;
    }

    /**
     * Get all available themes
     * @returns {Object}
     */
    getAvailableThemes() {
        return { ...THEMES };
    }

    /**
     * Get theme colors
     * @param {string} themeName
     * @returns {Object}
     */
    getThemeColors(themeName) {
        return getThemeColors(themeName);
    }

    /**
     * Create custom theme
     * @param {Object} colors
     */
    createCustomTheme(colors) {
        // Merge with dark theme defaults
        this.#customTheme = {
            ...getThemeColors('dark'),
            ...colors
        };

        this.storage.set('customTheme', this.#customTheme);
        this.setTheme('custom');
    }

    /**
     * Get custom theme colors
     * @returns {Object|null}
     */
    getCustomTheme() {
        return this.#customTheme ? { ...this.#customTheme } : null;
    }

    /**
     * Reset to default theme
     */
    resetToDefault() {
        this.#customTheme = null;
        this.storage.remove('customTheme');
        this.setTheme('dark');
    }

    /**
     * Check if current theme is dark
     * @returns {boolean}
     */
    isDark() {
        if (this.#currentTheme === 'system') {
            return this.#systemPreference === 'dark';
        }
        return this.#currentTheme === 'dark' || this.#currentTheme === 'midnight';
    }

    /**
     * Get computed color value
     * @param {string} variable - CSS variable name
     * @returns {string}
     */
    getColor(variable) {
        return getComputedStyle(document.documentElement).getPropertyValue(variable).trim();
    }

    /**
     * Export current theme as JSON
     * @returns {string}
     */
    exportTheme() {
        const colors = {};
        const root = document.documentElement;
        const style = getComputedStyle(root);

        // Get all custom properties
        for (const prop of Object.keys(getThemeColors('dark'))) {
            colors[prop] = style.getPropertyValue(prop).trim();
        }

        return JSON.stringify({
            name: this.#currentTheme,
            colors
        }, null, 2);
    }

    /**
     * Import theme from JSON
     * @param {string} json
     */
    importTheme(json) {
        try {
            const { colors } = JSON.parse(json);
            this.createCustomTheme(colors);
        } catch (e) {
            console.error('Failed to import theme:', e);
            throw new Error('Invalid theme format');
        }
    }
}

export { ThemeManager };
