/**
 * Preview Modal - Split-view tool preview
 * Local First Tools v2
 */

import { EventBus, EVENTS } from '../core/event-bus.js';
import { ToolRepository } from '../data/tool-repository.js';
import { StorageManager } from '../storage/storage-manager.js';

class PreviewModal {
    constructor() {
        this.events = EventBus.getInstance();
        this.toolRepo = ToolRepository.getInstance();
        this.storage = StorageManager.getInstance();

        this.#container = null;
        this.#currentTool = null;
        this.#isVisible = false;
        this.#isFullscreen = false;

        this.#bindEvents();
    }

    #container;
    #currentTool;
    #isVisible;
    #isFullscreen;

    /**
     * Bind event listeners
     */
    #bindEvents() {
        this.events.on(EVENTS.TOOL_PREVIEW, ({ toolId, tool }) => {
            const toolData = tool || this.toolRepo.getById(toolId);
            if (toolData) {
                this.show(toolData, document.body);
            }
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (!this.#isVisible) return;

            switch (e.key) {
                case 'Escape':
                    this.hide();
                    break;
                case 'f':
                    this.toggleFullscreen();
                    break;
                case 'ArrowLeft':
                    this.#navigatePrev();
                    break;
                case 'ArrowRight':
                    this.#navigateNext();
                    break;
            }
        });
    }

    /**
     * Show preview modal
     * @param {Object} tool
     * @param {HTMLElement} parentContainer
     */
    show(tool, parentContainer) {
        this.#currentTool = tool;

        if (!this.#container) {
            this.#container = document.createElement('div');
            this.#container.className = 'preview-modal';
            this.#injectStyles();
        }

        this.#render();

        if (!this.#container.parentElement) {
            parentContainer.appendChild(this.#container);
        }

        this.#isVisible = true;

        requestAnimationFrame(() => {
            this.#container.classList.add('visible');
        });

        this.events.emit(EVENTS.MODAL_OPEN, { type: 'preview', tool });
    }

    /**
     * Hide preview modal
     */
    hide() {
        if (!this.#isVisible) return;

        this.#container.classList.remove('visible');
        this.#isFullscreen = false;
        this.#container.classList.remove('fullscreen');

        setTimeout(() => {
            this.#container?.remove();
            this.#container = null;
            this.#isVisible = false;
            this.#currentTool = null;
        }, 300);

        this.events.emit(EVENTS.MODAL_CLOSE, { type: 'preview' });
    }

    /**
     * Toggle fullscreen mode
     */
    toggleFullscreen() {
        this.#isFullscreen = !this.#isFullscreen;
        this.#container?.classList.toggle('fullscreen', this.#isFullscreen);
    }

    /**
     * Render preview content
     */
    #render() {
        const tool = this.#currentTool;
        const isPinned = this.storage.get('pinnedTools')?.includes(tool.id);

        this.#container.innerHTML = `
            <div class="preview-backdrop"></div>
            <div class="preview-content">
                <div class="preview-header">
                    <div class="preview-title">
                        <h2>${tool.title}</h2>
                        <div class="preview-badges">
                            ${tool.featured ? '<span class="badge badge-featured">Featured</span>' : ''}
                            ${tool.polished ? '<span class="badge badge-polished">Polished</span>' : ''}
                            <span class="badge badge-complexity badge-${tool.complexity}">${tool.complexity || 'unknown'}</span>
                        </div>
                    </div>
                    <div class="preview-actions">
                        <button class="btn btn-icon" id="preview-pin" title="${isPinned ? 'Unpin' : 'Pin'}">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="${isPinned ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2">
                                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                            </svg>
                        </button>
                        <button class="btn btn-icon" id="preview-fullscreen" title="Fullscreen (F)">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M8 3H5a2 2 0 00-2 2v3m18 0V5a2 2 0 00-2-2h-3m0 18h3a2 2 0 002-2v-3M3 16v3a2 2 0 002 2h3"/>
                            </svg>
                        </button>
                        <button class="btn btn-icon preview-close" title="Close (Esc)">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M18 6L6 18M6 6l12 12"/>
                            </svg>
                        </button>
                    </div>
                </div>

                <div class="preview-body">
                    <div class="preview-iframe-container">
                        <iframe
                            src="${tool.file}"
                            class="preview-iframe"
                            title="${tool.title} Preview"
                            sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
                        ></iframe>
                        <div class="preview-loading">
                            <div class="loading-spinner"></div>
                            <span>Loading preview...</span>
                        </div>
                    </div>

                    <div class="preview-sidebar">
                        <div class="sidebar-section">
                            <h3>Description</h3>
                            <p>${tool.description || 'No description available'}</p>
                        </div>

                        <div class="sidebar-section">
                            <h3>Category</h3>
                            <span class="category-badge" style="--category-color: var(--category-${tool.category?.replace(/_/g, '-')})">
                                ${this.#formatCategory(tool.category)}
                            </span>
                        </div>

                        ${tool.tags && tool.tags.length > 0 ? `
                            <div class="sidebar-section">
                                <h3>Tags</h3>
                                <div class="tag-list">
                                    ${tool.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                                </div>
                            </div>
                        ` : ''}

                        <div class="sidebar-section">
                            <h3>File</h3>
                            <code class="file-path">${tool.file}</code>
                        </div>

                        <div class="sidebar-actions">
                            <button class="btn btn-primary btn-block" id="preview-open">
                                Open Full App
                            </button>
                            <button class="btn btn-secondary btn-block" id="preview-download">
                                Download HTML
                            </button>
                        </div>
                    </div>
                </div>

                <div class="preview-nav">
                    <button class="btn btn-icon preview-prev" title="Previous (←)">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M15 18l-6-6 6-6"/>
                        </svg>
                    </button>
                    <button class="btn btn-icon preview-next" title="Next (→)">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M9 18l6-6-6-6"/>
                        </svg>
                    </button>
                </div>
            </div>
        `;

        // Bind event handlers
        this.#container.querySelector('.preview-backdrop')?.addEventListener('click', () => this.hide());
        this.#container.querySelector('.preview-close')?.addEventListener('click', () => this.hide());
        this.#container.querySelector('#preview-fullscreen')?.addEventListener('click', () => this.toggleFullscreen());

        this.#container.querySelector('#preview-pin')?.addEventListener('click', () => {
            this.events.emit(EVENTS.TOOL_PIN_TOGGLE, { toolId: tool.id });
            this.#render();
        });

        this.#container.querySelector('#preview-open')?.addEventListener('click', () => {
            window.open(tool.file, '_blank');
        });

        this.#container.querySelector('#preview-download')?.addEventListener('click', () => {
            this.#downloadTool(tool);
        });

        this.#container.querySelector('.preview-prev')?.addEventListener('click', () => this.#navigatePrev());
        this.#container.querySelector('.preview-next')?.addEventListener('click', () => this.#navigateNext());

        // Handle iframe load
        const iframe = this.#container.querySelector('.preview-iframe');
        const loading = this.#container.querySelector('.preview-loading');

        iframe?.addEventListener('load', () => {
            loading?.classList.add('hidden');
        });
    }

    /**
     * Navigate to previous tool
     */
    #navigatePrev() {
        const tools = this.toolRepo.getAll();
        const currentIndex = tools.findIndex(t => t.id === this.#currentTool?.id);

        if (currentIndex > 0) {
            this.#currentTool = tools[currentIndex - 1];
            this.#render();
        }
    }

    /**
     * Navigate to next tool
     */
    #navigateNext() {
        const tools = this.toolRepo.getAll();
        const currentIndex = tools.findIndex(t => t.id === this.#currentTool?.id);

        if (currentIndex < tools.length - 1) {
            this.#currentTool = tools[currentIndex + 1];
            this.#render();
        }
    }

    /**
     * Download tool HTML
     * @param {Object} tool
     */
    async #downloadTool(tool) {
        try {
            const response = await fetch(tool.file);
            const html = await response.text();

            const blob = new Blob([html], { type: 'text/html' });
            const url = URL.createObjectURL(blob);

            const a = document.createElement('a');
            a.href = url;
            a.download = tool.file.split('/').pop() || `${tool.title}.html`;
            a.click();

            URL.revokeObjectURL(url);

            this.events.emit(EVENTS.NOTIFICATION, {
                message: 'Download started',
                type: 'success'
            });
        } catch (e) {
            this.events.emit(EVENTS.NOTIFICATION, {
                message: 'Download failed',
                type: 'error'
            });
        }
    }

    /**
     * Format category name
     * @param {string} category
     * @returns {string}
     */
    #formatCategory(category) {
        if (!category) return 'Uncategorized';
        return category.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    }

    /**
     * Inject preview styles
     */
    #injectStyles() {
        if (document.getElementById('preview-modal-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'preview-modal-styles';
        styles.textContent = `
            .preview-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 1000;
                opacity: 0;
                transition: opacity var(--duration-300);
            }

            .preview-modal.visible {
                opacity: 1;
            }

            .preview-backdrop {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.85);
            }

            .preview-content {
                position: relative;
                width: 95%;
                height: 90%;
                max-width: 1400px;
                margin: 2.5% auto;
                background: var(--color-bg-elevated);
                border-radius: var(--radius-xl);
                display: flex;
                flex-direction: column;
                overflow: hidden;
                transform: scale(0.95);
                transition: transform var(--duration-300);
            }

            .preview-modal.visible .preview-content {
                transform: scale(1);
            }

            .preview-modal.fullscreen .preview-content {
                width: 100%;
                height: 100%;
                max-width: none;
                margin: 0;
                border-radius: 0;
            }

            .preview-modal.fullscreen .preview-sidebar {
                display: none;
            }

            .preview-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: var(--space-3) var(--space-4);
                border-bottom: 1px solid var(--color-border);
                background: var(--color-bg-secondary);
            }

            .preview-title {
                display: flex;
                align-items: center;
                gap: var(--space-3);
            }

            .preview-title h2 {
                margin: 0;
                font-size: var(--text-lg);
            }

            .preview-badges {
                display: flex;
                gap: var(--space-2);
            }

            .preview-actions {
                display: flex;
                gap: var(--space-2);
            }

            .preview-body {
                flex: 1;
                display: flex;
                min-height: 0;
            }

            .preview-iframe-container {
                flex: 1;
                position: relative;
                background: #fff;
            }

            .preview-iframe {
                width: 100%;
                height: 100%;
                border: none;
            }

            .preview-loading {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                gap: var(--space-3);
                background: var(--color-bg-primary);
                color: var(--color-text-secondary);
                transition: opacity var(--duration-300);
            }

            .preview-loading.hidden {
                opacity: 0;
                pointer-events: none;
            }

            .loading-spinner {
                width: 32px;
                height: 32px;
                border: 3px solid var(--color-border);
                border-top-color: var(--color-accent);
                border-radius: 50%;
                animation: spin 1s linear infinite;
            }

            @keyframes spin {
                to { transform: rotate(360deg); }
            }

            .preview-sidebar {
                width: 300px;
                padding: var(--space-4);
                border-left: 1px solid var(--color-border);
                overflow-y: auto;
                background: var(--color-bg-secondary);
            }

            .sidebar-section {
                margin-bottom: var(--space-4);
            }

            .sidebar-section h3 {
                font-size: var(--text-xs);
                text-transform: uppercase;
                letter-spacing: 0.05em;
                color: var(--color-text-tertiary);
                margin-bottom: var(--space-2);
            }

            .sidebar-section p {
                font-size: var(--text-sm);
                color: var(--color-text-secondary);
                margin: 0;
            }

            .category-badge {
                display: inline-block;
                padding: var(--space-1) var(--space-2);
                background: var(--category-color, var(--color-accent));
                color: var(--color-bg-primary);
                border-radius: var(--radius-sm);
                font-size: var(--text-sm);
                font-weight: 500;
            }

            .tag-list {
                display: flex;
                flex-wrap: wrap;
                gap: var(--space-1);
            }

            .tag-list .tag {
                padding: var(--space-1) var(--space-2);
                background: var(--color-bg-tertiary);
                border-radius: var(--radius-sm);
                font-size: var(--text-xs);
            }

            .file-path {
                display: block;
                padding: var(--space-2);
                background: var(--color-bg-tertiary);
                border-radius: var(--radius-sm);
                font-size: var(--text-xs);
                word-break: break-all;
            }

            .sidebar-actions {
                margin-top: var(--space-4);
                display: flex;
                flex-direction: column;
                gap: var(--space-2);
            }

            .btn-block {
                width: 100%;
            }

            .preview-nav {
                position: absolute;
                top: 50%;
                left: 0;
                right: 0;
                display: flex;
                justify-content: space-between;
                padding: 0 var(--space-4);
                pointer-events: none;
                transform: translateY(-50%);
            }

            .preview-nav button {
                pointer-events: auto;
                background: var(--glass-bg);
                backdrop-filter: var(--glass-blur);
                border: 1px solid var(--glass-border);
            }

            .preview-nav button:hover {
                background: var(--color-bg-elevated);
            }

            @media (max-width: 768px) {
                .preview-content {
                    width: 100%;
                    height: 100%;
                    margin: 0;
                    border-radius: 0;
                }

                .preview-body {
                    flex-direction: column;
                }

                .preview-sidebar {
                    width: 100%;
                    max-height: 200px;
                    border-left: none;
                    border-top: 1px solid var(--color-border);
                }

                .preview-nav {
                    display: none;
                }
            }
        `;

        document.head.appendChild(styles);
    }

    /**
     * Check if modal is visible
     * @returns {boolean}
     */
    isVisible() {
        return this.#isVisible;
    }

    /**
     * Get current tool
     * @returns {Object|null}
     */
    getCurrentTool() {
        return this.#currentTool;
    }
}

export { PreviewModal };
