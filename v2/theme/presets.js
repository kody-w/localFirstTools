/**
 * Theme Presets - Predefined themes
 * Local First Tools v2
 */

/**
 * Available themes with their display names
 */
export const THEMES = {
    dark: {
        name: 'Dark',
        description: 'Default dark theme with green accents'
    },
    light: {
        name: 'Light',
        description: 'Light theme for bright environments'
    },
    midnight: {
        name: 'Midnight',
        description: 'Pure black OLED-friendly theme'
    },
    highContrast: {
        name: 'High Contrast',
        description: 'Maximum contrast for accessibility'
    },
    cyberpunk: {
        name: 'Cyberpunk',
        description: 'Neon pink and cyan aesthetic'
    },
    nature: {
        name: 'Nature',
        description: 'Earthy green and brown tones'
    }
};

/**
 * Dark theme (default)
 */
const darkTheme = {
    // Background colors
    '--color-bg-primary': '#0a0a0a',
    '--color-bg-secondary': '#141414',
    '--color-bg-tertiary': '#1a1a1a',
    '--color-bg-elevated': '#222222',

    // Text colors
    '--color-text-primary': '#ffffff',
    '--color-text-secondary': '#a0a0a0',
    '--color-text-tertiary': '#666666',
    '--color-text-inverse': '#0a0a0a',

    // Accent colors
    '--color-accent': '#06ffa5',
    '--color-accent-hover': '#00e090',
    '--color-accent-subtle': 'rgba(6, 255, 165, 0.1)',

    // Semantic colors
    '--color-success': '#06ffa5',
    '--color-warning': '#ffb347',
    '--color-error': '#ff6b6b',
    '--color-info': '#00d4ff',

    // Border colors
    '--color-border': '#333333',
    '--color-border-subtle': '#222222',
    '--color-border-strong': '#444444',

    // Glass effect
    '--glass-bg': 'rgba(20, 20, 20, 0.8)',
    '--glass-border': 'rgba(255, 255, 255, 0.1)',
    '--glass-blur': 'blur(12px)',

    // Shadows
    '--shadow-sm': '0 2px 4px rgba(0, 0, 0, 0.3)',
    '--shadow-md': '0 4px 12px rgba(0, 0, 0, 0.4)',
    '--shadow-lg': '0 8px 24px rgba(0, 0, 0, 0.5)',
    '--shadow-glow': '0 0 20px rgba(6, 255, 165, 0.2)',

    // Category colors
    '--category-visual-art': '#ff6b9d',
    '--category-3d-immersive': '#4ecdc4',
    '--category-audio-music': '#ffb347',
    '--category-games-puzzles': '#9b59b6',
    '--category-experimental-ai': '#00d4ff',
    '--category-creative-tools': '#ff9ff3',
    '--category-generative-art': '#5fa8ff',
    '--category-particle-physics': '#5dade2',
    '--category-educational-tools': '#f7dc6f'
};

/**
 * Light theme
 */
const lightTheme = {
    '--color-bg-primary': '#ffffff',
    '--color-bg-secondary': '#f5f5f5',
    '--color-bg-tertiary': '#eeeeee',
    '--color-bg-elevated': '#ffffff',

    '--color-text-primary': '#1a1a1a',
    '--color-text-secondary': '#666666',
    '--color-text-tertiary': '#999999',
    '--color-text-inverse': '#ffffff',

    '--color-accent': '#00a86b',
    '--color-accent-hover': '#008f5b',
    '--color-accent-subtle': 'rgba(0, 168, 107, 0.1)',

    '--color-success': '#00a86b',
    '--color-warning': '#f5a623',
    '--color-error': '#dc3545',
    '--color-info': '#0095d9',

    '--color-border': '#e0e0e0',
    '--color-border-subtle': '#eeeeee',
    '--color-border-strong': '#cccccc',

    '--glass-bg': 'rgba(255, 255, 255, 0.9)',
    '--glass-border': 'rgba(0, 0, 0, 0.1)',
    '--glass-blur': 'blur(12px)',

    '--shadow-sm': '0 2px 4px rgba(0, 0, 0, 0.05)',
    '--shadow-md': '0 4px 12px rgba(0, 0, 0, 0.1)',
    '--shadow-lg': '0 8px 24px rgba(0, 0, 0, 0.15)',
    '--shadow-glow': '0 0 20px rgba(0, 168, 107, 0.15)',

    '--category-visual-art': '#e91e63',
    '--category-3d-immersive': '#009688',
    '--category-audio-music': '#ff9800',
    '--category-games-puzzles': '#9c27b0',
    '--category-experimental-ai': '#00bcd4',
    '--category-creative-tools': '#e91e63',
    '--category-generative-art': '#2196f3',
    '--category-particle-physics': '#03a9f4',
    '--category-educational-tools': '#ffc107'
};

/**
 * Midnight theme (OLED black)
 */
const midnightTheme = {
    '--color-bg-primary': '#000000',
    '--color-bg-secondary': '#0a0a0a',
    '--color-bg-tertiary': '#111111',
    '--color-bg-elevated': '#1a1a1a',

    '--color-text-primary': '#ffffff',
    '--color-text-secondary': '#888888',
    '--color-text-tertiary': '#555555',
    '--color-text-inverse': '#000000',

    '--color-accent': '#06ffa5',
    '--color-accent-hover': '#00e090',
    '--color-accent-subtle': 'rgba(6, 255, 165, 0.08)',

    '--color-success': '#06ffa5',
    '--color-warning': '#ffb347',
    '--color-error': '#ff6b6b',
    '--color-info': '#00d4ff',

    '--color-border': '#222222',
    '--color-border-subtle': '#1a1a1a',
    '--color-border-strong': '#333333',

    '--glass-bg': 'rgba(0, 0, 0, 0.9)',
    '--glass-border': 'rgba(255, 255, 255, 0.05)',
    '--glass-blur': 'blur(16px)',

    '--shadow-sm': '0 2px 4px rgba(0, 0, 0, 0.5)',
    '--shadow-md': '0 4px 12px rgba(0, 0, 0, 0.6)',
    '--shadow-lg': '0 8px 24px rgba(0, 0, 0, 0.7)',
    '--shadow-glow': '0 0 30px rgba(6, 255, 165, 0.15)',

    '--category-visual-art': '#ff6b9d',
    '--category-3d-immersive': '#4ecdc4',
    '--category-audio-music': '#ffb347',
    '--category-games-puzzles': '#9b59b6',
    '--category-experimental-ai': '#00d4ff',
    '--category-creative-tools': '#ff9ff3',
    '--category-generative-art': '#5fa8ff',
    '--category-particle-physics': '#5dade2',
    '--category-educational-tools': '#f7dc6f'
};

/**
 * High contrast theme
 */
const highContrastTheme = {
    '--color-bg-primary': '#000000',
    '--color-bg-secondary': '#000000',
    '--color-bg-tertiary': '#1a1a1a',
    '--color-bg-elevated': '#1a1a1a',

    '--color-text-primary': '#ffffff',
    '--color-text-secondary': '#ffffff',
    '--color-text-tertiary': '#cccccc',
    '--color-text-inverse': '#000000',

    '--color-accent': '#ffff00',
    '--color-accent-hover': '#ffff66',
    '--color-accent-subtle': 'rgba(255, 255, 0, 0.2)',

    '--color-success': '#00ff00',
    '--color-warning': '#ffff00',
    '--color-error': '#ff0000',
    '--color-info': '#00ffff',

    '--color-border': '#ffffff',
    '--color-border-subtle': '#cccccc',
    '--color-border-strong': '#ffffff',

    '--glass-bg': 'rgba(0, 0, 0, 0.95)',
    '--glass-border': 'rgba(255, 255, 255, 0.5)',
    '--glass-blur': 'blur(0px)',

    '--shadow-sm': 'none',
    '--shadow-md': 'none',
    '--shadow-lg': '0 0 0 2px #ffffff',
    '--shadow-glow': '0 0 0 3px #ffff00',

    '--category-visual-art': '#ff00ff',
    '--category-3d-immersive': '#00ffff',
    '--category-audio-music': '#ffff00',
    '--category-games-puzzles': '#ff00ff',
    '--category-experimental-ai': '#00ffff',
    '--category-creative-tools': '#ff00ff',
    '--category-generative-art': '#00ffff',
    '--category-particle-physics': '#00ffff',
    '--category-educational-tools': '#ffff00'
};

/**
 * Cyberpunk theme
 */
const cyberpunkTheme = {
    '--color-bg-primary': '#0d0221',
    '--color-bg-secondary': '#1a0a2e',
    '--color-bg-tertiary': '#261044',
    '--color-bg-elevated': '#2d1556',

    '--color-text-primary': '#ffffff',
    '--color-text-secondary': '#b8b8d1',
    '--color-text-tertiary': '#7a7a9d',
    '--color-text-inverse': '#0d0221',

    '--color-accent': '#ff00ff',
    '--color-accent-hover': '#ff66ff',
    '--color-accent-subtle': 'rgba(255, 0, 255, 0.15)',

    '--color-success': '#00ff9f',
    '--color-warning': '#ffb800',
    '--color-error': '#ff0055',
    '--color-info': '#00d4ff',

    '--color-border': '#4a2c7d',
    '--color-border-subtle': '#3a1f5f',
    '--color-border-strong': '#6b3fa0',

    '--glass-bg': 'rgba(26, 10, 46, 0.85)',
    '--glass-border': 'rgba(255, 0, 255, 0.2)',
    '--glass-blur': 'blur(12px)',

    '--shadow-sm': '0 2px 4px rgba(255, 0, 255, 0.2)',
    '--shadow-md': '0 4px 12px rgba(255, 0, 255, 0.3)',
    '--shadow-lg': '0 8px 24px rgba(255, 0, 255, 0.4)',
    '--shadow-glow': '0 0 30px rgba(255, 0, 255, 0.5)',

    '--category-visual-art': '#ff00ff',
    '--category-3d-immersive': '#00ffff',
    '--category-audio-music': '#ffb800',
    '--category-games-puzzles': '#ff00aa',
    '--category-experimental-ai': '#00d4ff',
    '--category-creative-tools': '#ff66ff',
    '--category-generative-art': '#00ffff',
    '--category-particle-physics': '#00d4ff',
    '--category-educational-tools': '#ffff00'
};

/**
 * Nature theme
 */
const natureTheme = {
    '--color-bg-primary': '#1a2f1a',
    '--color-bg-secondary': '#243524',
    '--color-bg-tertiary': '#2e3f2e',
    '--color-bg-elevated': '#3a4f3a',

    '--color-text-primary': '#f0f5f0',
    '--color-text-secondary': '#b8c8b8',
    '--color-text-tertiary': '#8fa88f',
    '--color-text-inverse': '#1a2f1a',

    '--color-accent': '#7cb342',
    '--color-accent-hover': '#9ccc65',
    '--color-accent-subtle': 'rgba(124, 179, 66, 0.15)',

    '--color-success': '#7cb342',
    '--color-warning': '#ffb74d',
    '--color-error': '#e57373',
    '--color-info': '#4dd0e1',

    '--color-border': '#4a5f4a',
    '--color-border-subtle': '#3a4f3a',
    '--color-border-strong': '#5a6f5a',

    '--glass-bg': 'rgba(36, 53, 36, 0.85)',
    '--glass-border': 'rgba(124, 179, 66, 0.2)',
    '--glass-blur': 'blur(12px)',

    '--shadow-sm': '0 2px 4px rgba(0, 0, 0, 0.2)',
    '--shadow-md': '0 4px 12px rgba(0, 0, 0, 0.3)',
    '--shadow-lg': '0 8px 24px rgba(0, 0, 0, 0.4)',
    '--shadow-glow': '0 0 20px rgba(124, 179, 66, 0.3)',

    '--category-visual-art': '#f48fb1',
    '--category-3d-immersive': '#4db6ac',
    '--category-audio-music': '#ffb74d',
    '--category-games-puzzles': '#ba68c8',
    '--category-experimental-ai': '#4dd0e1',
    '--category-creative-tools': '#f06292',
    '--category-generative-art': '#64b5f6',
    '--category-particle-physics': '#4fc3f7',
    '--category-educational-tools': '#ffd54f'
};

/**
 * Theme color definitions
 */
const themeColors = {
    dark: darkTheme,
    light: lightTheme,
    midnight: midnightTheme,
    highContrast: highContrastTheme,
    cyberpunk: cyberpunkTheme,
    nature: natureTheme
};

/**
 * Get colors for a theme
 * @param {string} themeName
 * @returns {Object}
 */
export function getThemeColors(themeName) {
    return themeColors[themeName] || darkTheme;
}

/**
 * Get theme info
 * @param {string} themeName
 * @returns {Object|null}
 */
export function getThemeInfo(themeName) {
    return THEMES[themeName] || null;
}

/**
 * Get all theme names
 * @returns {string[]}
 */
export function getThemeNames() {
    return Object.keys(THEMES);
}
