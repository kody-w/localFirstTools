/**
 * Analytics Dashboard - Analytics UI
 * Local First Tools v2
 */

import { EventBus, EVENTS } from '../../core/event-bus.js';
import { AnalyticsTracker } from './tracker.js';

class AnalyticsDashboard {
    constructor() {
        this.events = EventBus.getInstance();
        this.tracker = AnalyticsTracker.getInstance();

        this.#container = null;
        this.#isVisible = false;
    }

    #container;
    #isVisible;

    /**
     * Show analytics dashboard
     * @param {HTMLElement} parentContainer
     */
    show(parentContainer) {
        if (this.#isVisible) return;

        this.#container = document.createElement('div');
        this.#container.className = 'analytics-dashboard';
        this.#render();

        parentContainer.appendChild(this.#container);
        this.#isVisible = true;

        this.#injectStyles();

        // Animate in
        requestAnimationFrame(() => {
            this.#container.classList.add('visible');
        });
    }

    /**
     * Hide analytics dashboard
     */
    hide() {
        if (!this.#isVisible || !this.#container) return;

        this.#container.classList.remove('visible');

        setTimeout(() => {
            this.#container?.remove();
            this.#container = null;
            this.#isVisible = false;
        }, 300);
    }

    /**
     * Toggle visibility
     * @param {HTMLElement} parentContainer
     */
    toggle(parentContainer) {
        if (this.#isVisible) {
            this.hide();
        } else {
            this.show(parentContainer);
        }
    }

    /**
     * Render dashboard content
     */
    #render() {
        const data = this.tracker.getAllData();
        const mostUsed = this.tracker.getMostUsedTools(5);
        const recentlyUsed = this.tracker.getRecentlyUsedTools(5);
        const popularSearches = this.tracker.getPopularSearches(5);
        const sessionStats = this.tracker.getSessionStats();

        this.#container.innerHTML = `
            <div class="dashboard-header">
                <h2>Analytics Dashboard</h2>
                <button class="dashboard-close" aria-label="Close dashboard">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M18 6L6 18M6 6l12 12"/>
                    </svg>
                </button>
            </div>

            <div class="dashboard-grid">
                <!-- Overview Stats -->
                <div class="dashboard-card stats-overview">
                    <h3>Overview</h3>
                    <div class="stats-grid">
                        <div class="stat-item">
                            <span class="stat-value">${data.totalOpens}</span>
                            <span class="stat-label">Total Opens</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-value">${Object.keys(data.toolUsage).length}</span>
                            <span class="stat-label">Tools Used</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-value">${data.totalPins}</span>
                            <span class="stat-label">Total Pins</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-value">${sessionStats.totalSessions}</span>
                            <span class="stat-label">Sessions</span>
                        </div>
                    </div>
                </div>

                <!-- Most Used Tools -->
                <div class="dashboard-card">
                    <h3>Most Used Tools</h3>
                    ${this.#renderToolList(mostUsed)}
                </div>

                <!-- Recently Used -->
                <div class="dashboard-card">
                    <h3>Recently Used</h3>
                    ${this.#renderToolList(recentlyUsed, true)}
                </div>

                <!-- Popular Searches -->
                <div class="dashboard-card">
                    <h3>Popular Searches</h3>
                    ${this.#renderSearchList(popularSearches)}
                </div>

                <!-- Category Distribution -->
                <div class="dashboard-card">
                    <h3>Category Views</h3>
                    ${this.#renderCategoryChart(data.categoryViews)}
                </div>

                <!-- Session Info -->
                <div class="dashboard-card">
                    <h3>Session Stats</h3>
                    <div class="session-stats">
                        <p><strong>Average Session:</strong> ${this.#formatDuration(sessionStats.avgDuration)}</p>
                        <p><strong>Total Time:</strong> ${this.#formatDuration(sessionStats.totalTime)}</p>
                        <p><strong>Current Session:</strong> ${this.#formatDuration(Date.now() - data.currentSession.start)}</p>
                    </div>
                </div>
            </div>

            <div class="dashboard-actions">
                <button class="btn btn-secondary" id="export-analytics">
                    Export Data
                </button>
                <button class="btn btn-ghost" id="clear-analytics">
                    Clear Data
                </button>
            </div>
        `;

        // Bind events
        this.#container.querySelector('.dashboard-close')?.addEventListener('click', () => this.hide());

        this.#container.querySelector('#export-analytics')?.addEventListener('click', () => {
            this.#exportData();
        });

        this.#container.querySelector('#clear-analytics')?.addEventListener('click', () => {
            if (confirm('Are you sure you want to clear all analytics data?')) {
                this.tracker.clearData();
                this.#render();
            }
        });
    }

    /**
     * Render tool list
     * @param {Array} tools
     * @param {boolean} showTime
     * @returns {string}
     */
    #renderToolList(tools, showTime = false) {
        if (tools.length === 0) {
            return '<p class="empty-message">No data yet</p>';
        }

        return `
            <ul class="tool-list">
                ${tools.map(tool => `
                    <li class="tool-list-item">
                        <span class="tool-title">${tool.title || tool.id}</span>
                        <span class="tool-stat">
                            ${showTime
                                ? this.#formatTimeAgo(tool.lastOpened)
                                : `${tool.opens} opens`
                            }
                        </span>
                    </li>
                `).join('')}
            </ul>
        `;
    }

    /**
     * Render search list
     * @param {Array} searches
     * @returns {string}
     */
    #renderSearchList(searches) {
        if (searches.length === 0) {
            return '<p class="empty-message">No searches yet</p>';
        }

        return `
            <ul class="search-list">
                ${searches.map(({ query, count }) => `
                    <li class="search-list-item">
                        <span class="search-query">"${query}"</span>
                        <span class="search-count">${count}x</span>
                    </li>
                `).join('')}
            </ul>
        `;
    }

    /**
     * Render category chart
     * @param {Object} categoryViews
     * @returns {string}
     */
    #renderCategoryChart(categoryViews) {
        const entries = Object.entries(categoryViews);

        if (entries.length === 0) {
            return '<p class="empty-message">No category data yet</p>';
        }

        const max = Math.max(...entries.map(([, v]) => v));

        return `
            <div class="category-chart">
                ${entries
                    .sort((a, b) => b[1] - a[1])
                    .slice(0, 8)
                    .map(([category, count]) => `
                        <div class="chart-row">
                            <span class="chart-label">${this.#formatCategoryName(category)}</span>
                            <div class="chart-bar-container">
                                <div class="chart-bar" style="width: ${(count / max) * 100}%"></div>
                            </div>
                            <span class="chart-value">${count}</span>
                        </div>
                    `).join('')}
            </div>
        `;
    }

    /**
     * Format category name
     * @param {string} category
     * @returns {string}
     */
    #formatCategoryName(category) {
        return category
            .replace(/_/g, ' ')
            .replace(/\b\w/g, c => c.toUpperCase());
    }

    /**
     * Format duration
     * @param {number} ms
     * @returns {string}
     */
    #formatDuration(ms) {
        if (!ms || ms < 0) return '0s';

        const seconds = Math.floor(ms / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);

        if (hours > 0) {
            return `${hours}h ${minutes % 60}m`;
        }
        if (minutes > 0) {
            return `${minutes}m ${seconds % 60}s`;
        }
        return `${seconds}s`;
    }

    /**
     * Format time ago
     * @param {number} timestamp
     * @returns {string}
     */
    #formatTimeAgo(timestamp) {
        if (!timestamp) return 'Never';

        const seconds = Math.floor((Date.now() - timestamp) / 1000);

        if (seconds < 60) return 'Just now';
        if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
        if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
        if (seconds < 604800) return `${Math.floor(seconds / 86400)}d ago`;

        return new Date(timestamp).toLocaleDateString();
    }

    /**
     * Export analytics data
     */
    #exportData() {
        const data = this.tracker.exportData();
        const blob = new Blob([data], { type: 'application/json' });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = `analytics-${new Date().toISOString().split('T')[0]}.json`;
        a.click();

        URL.revokeObjectURL(url);

        this.events.emit(EVENTS.NOTIFICATION, {
            message: 'Analytics data exported',
            type: 'success'
        });
    }

    /**
     * Inject dashboard styles
     */
    #injectStyles() {
        if (document.getElementById('analytics-dashboard-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'analytics-dashboard-styles';
        styles.textContent = `
            .analytics-dashboard {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%) scale(0.95);
                width: 90%;
                max-width: 800px;
                max-height: 85vh;
                background: var(--color-bg-elevated);
                border: 1px solid var(--color-border);
                border-radius: var(--radius-xl);
                box-shadow: var(--shadow-lg);
                overflow: hidden;
                opacity: 0;
                transition: all var(--duration-300) var(--ease-out);
                z-index: 1000;
            }

            .analytics-dashboard.visible {
                opacity: 1;
                transform: translate(-50%, -50%) scale(1);
            }

            .dashboard-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: var(--space-4) var(--space-5);
                border-bottom: 1px solid var(--color-border);
            }

            .dashboard-header h2 {
                margin: 0;
                font-size: var(--text-xl);
            }

            .dashboard-close {
                background: none;
                border: none;
                color: var(--color-text-secondary);
                cursor: pointer;
                padding: var(--space-2);
                border-radius: var(--radius-md);
                transition: all var(--duration-150);
            }

            .dashboard-close:hover {
                color: var(--color-text-primary);
                background: var(--color-bg-tertiary);
            }

            .dashboard-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: var(--space-4);
                padding: var(--space-5);
                max-height: calc(85vh - 140px);
                overflow-y: auto;
            }

            @media (max-width: 640px) {
                .dashboard-grid {
                    grid-template-columns: 1fr;
                }
            }

            .dashboard-card {
                background: var(--color-bg-secondary);
                border-radius: var(--radius-lg);
                padding: var(--space-4);
            }

            .dashboard-card h3 {
                margin: 0 0 var(--space-3) 0;
                font-size: var(--text-sm);
                text-transform: uppercase;
                letter-spacing: 0.05em;
                color: var(--color-text-secondary);
            }

            .stats-overview {
                grid-column: span 2;
            }

            @media (max-width: 640px) {
                .stats-overview {
                    grid-column: span 1;
                }
            }

            .stats-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: var(--space-4);
            }

            @media (max-width: 640px) {
                .stats-grid {
                    grid-template-columns: repeat(2, 1fr);
                }
            }

            .stat-item {
                text-align: center;
            }

            .stat-value {
                display: block;
                font-size: var(--text-2xl);
                font-weight: 700;
                color: var(--color-accent);
            }

            .stat-label {
                font-size: var(--text-xs);
                color: var(--color-text-tertiary);
            }

            .tool-list, .search-list {
                list-style: none;
                padding: 0;
                margin: 0;
            }

            .tool-list-item, .search-list-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: var(--space-2) 0;
                border-bottom: 1px solid var(--color-border-subtle);
            }

            .tool-list-item:last-child, .search-list-item:last-child {
                border-bottom: none;
            }

            .tool-title, .search-query {
                font-size: var(--text-sm);
                color: var(--color-text-primary);
            }

            .tool-stat, .search-count {
                font-size: var(--text-xs);
                color: var(--color-text-tertiary);
            }

            .search-query {
                color: var(--color-accent);
            }

            .category-chart {
                display: flex;
                flex-direction: column;
                gap: var(--space-2);
            }

            .chart-row {
                display: grid;
                grid-template-columns: 80px 1fr 40px;
                align-items: center;
                gap: var(--space-2);
            }

            .chart-label {
                font-size: var(--text-xs);
                color: var(--color-text-secondary);
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }

            .chart-bar-container {
                height: 8px;
                background: var(--color-bg-tertiary);
                border-radius: var(--radius-sm);
                overflow: hidden;
            }

            .chart-bar {
                height: 100%;
                background: var(--color-accent);
                border-radius: var(--radius-sm);
                transition: width var(--duration-300);
            }

            .chart-value {
                font-size: var(--text-xs);
                color: var(--color-text-tertiary);
                text-align: right;
            }

            .session-stats p {
                margin: var(--space-2) 0;
                font-size: var(--text-sm);
                color: var(--color-text-secondary);
            }

            .session-stats strong {
                color: var(--color-text-primary);
            }

            .empty-message {
                color: var(--color-text-tertiary);
                font-size: var(--text-sm);
                text-align: center;
                padding: var(--space-4);
            }

            .dashboard-actions {
                display: flex;
                gap: var(--space-3);
                padding: var(--space-4) var(--space-5);
                border-top: 1px solid var(--color-border);
                justify-content: flex-end;
            }
        `;

        document.head.appendChild(styles);
    }
}

export { AnalyticsDashboard };
