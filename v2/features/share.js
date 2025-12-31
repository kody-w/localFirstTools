/**
 * Share - Social sharing functionality
 * Local First Tools v2
 */

import { EventBus, EVENTS } from '../core/event-bus.js';
import { ToolRepository } from '../data/tool-repository.js';

class ShareManager {
    constructor() {
        this.events = EventBus.getInstance();
        this.toolRepo = ToolRepository.getInstance();

        this.#container = null;
        this.#currentTool = null;
        this.#isVisible = false;

        this.#bindEvents();
    }

    #container;
    #currentTool;
    #isVisible;

    /**
     * Bind event listeners
     */
    #bindEvents() {
        this.events.on(EVENTS.TOOL_SHARE, ({ toolId, tool }) => {
            const toolData = tool || this.toolRepo.getById(toolId);
            if (toolData) {
                this.show(toolData, document.body);
            }
        });
    }

    /**
     * Show share dialog
     * @param {Object} tool
     * @param {HTMLElement} parentContainer
     */
    show(tool, parentContainer) {
        this.#currentTool = tool;

        this.#container = document.createElement('div');
        this.#container.className = 'share-modal';
        this.#render();

        parentContainer.appendChild(this.#container);
        this.#isVisible = true;

        this.#injectStyles();

        requestAnimationFrame(() => {
            this.#container.classList.add('visible');
        });
    }

    /**
     * Hide share dialog
     */
    hide() {
        if (!this.#isVisible || !this.#container) return;

        this.#container.classList.remove('visible');

        setTimeout(() => {
            this.#container?.remove();
            this.#container = null;
            this.#isVisible = false;
            this.#currentTool = null;
        }, 300);
    }

    /**
     * Render share dialog
     */
    #render() {
        const tool = this.#currentTool;
        const shareUrl = this.#getShareUrl(tool);
        const shareText = `Check out "${tool.title}" - ${tool.description || 'A cool local-first tool'}`;

        this.#container.innerHTML = `
            <div class="share-backdrop"></div>
            <div class="share-content">
                <div class="share-header">
                    <h3>Share "${tool.title}"</h3>
                    <button class="btn btn-icon share-close" aria-label="Close">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M18 6L6 18M6 6l12 12"/>
                        </svg>
                    </button>
                </div>

                <div class="share-body">
                    <!-- Social Share Buttons -->
                    <div class="share-social">
                        <button class="share-btn share-twitter" data-platform="twitter" title="Share on Twitter/X">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                            </svg>
                        </button>
                        <button class="share-btn share-linkedin" data-platform="linkedin" title="Share on LinkedIn">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                            </svg>
                        </button>
                        <button class="share-btn share-facebook" data-platform="facebook" title="Share on Facebook">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                            </svg>
                        </button>
                        <button class="share-btn share-reddit" data-platform="reddit" title="Share on Reddit">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M12 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0zm5.01 4.744c.688 0 1.25.561 1.25 1.249a1.25 1.25 0 0 1-2.498.056l-2.597-.547-.8 3.747c1.824.07 3.48.632 4.674 1.488.308-.309.73-.491 1.207-.491.968 0 1.754.786 1.754 1.754 0 .716-.435 1.333-1.01 1.614a3.111 3.111 0 0 1 .042.52c0 2.694-3.13 4.87-7.004 4.87-3.874 0-7.004-2.176-7.004-4.87 0-.183.015-.366.043-.534A1.748 1.748 0 0 1 4.028 12c0-.968.786-1.754 1.754-1.754.463 0 .898.196 1.207.49 1.207-.883 2.878-1.43 4.744-1.487l.885-4.182a.342.342 0 0 1 .14-.197.35.35 0 0 1 .238-.042l2.906.617a1.214 1.214 0 0 1 1.108-.701zM9.25 12C8.561 12 8 12.562 8 13.25c0 .687.561 1.248 1.25 1.248.687 0 1.248-.561 1.248-1.249 0-.688-.561-1.249-1.249-1.249zm5.5 0c-.687 0-1.248.561-1.248 1.25 0 .687.561 1.248 1.249 1.248.688 0 1.249-.561 1.249-1.249 0-.687-.562-1.249-1.25-1.249zm-5.466 3.99a.327.327 0 0 0-.231.094.33.33 0 0 0 0 .463c.842.842 2.484.913 2.961.913.477 0 2.105-.056 2.961-.913a.361.361 0 0 0 .029-.463.33.33 0 0 0-.464 0c-.547.533-1.684.73-2.512.73-.828 0-1.979-.196-2.512-.73a.326.326 0 0 0-.232-.095z"/>
                            </svg>
                        </button>
                        <button class="share-btn share-email" data-platform="email" title="Share via Email">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                                <polyline points="22,6 12,13 2,6"/>
                            </svg>
                        </button>
                    </div>

                    <!-- Copy Link -->
                    <div class="share-link">
                        <label for="share-url">Or copy link:</label>
                        <div class="share-link-input">
                            <input type="text" id="share-url" value="${shareUrl}" readonly>
                            <button class="btn btn-secondary" id="copy-link">Copy</button>
                        </div>
                    </div>

                    <!-- Native Share (if available) -->
                    ${navigator.share ? `
                        <button class="btn btn-primary btn-block" id="native-share">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 8px;">
                                <circle cx="18" cy="5" r="3"/>
                                <circle cx="6" cy="12" r="3"/>
                                <circle cx="18" cy="19" r="3"/>
                                <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/>
                                <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/>
                            </svg>
                            Share via device
                        </button>
                    ` : ''}

                    <!-- QR Code -->
                    <div class="share-qr">
                        <button class="btn btn-ghost btn-sm" id="show-qr">Show QR Code</button>
                        <div class="qr-container" id="qr-container" style="display: none;">
                            <canvas id="qr-canvas"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        `;

        this.#bindEventHandlers(shareUrl, shareText);
    }

    /**
     * Bind event handlers
     * @param {string} shareUrl
     * @param {string} shareText
     */
    #bindEventHandlers(shareUrl, shareText) {
        // Close button
        this.#container.querySelector('.share-backdrop')?.addEventListener('click', () => this.hide());
        this.#container.querySelector('.share-close')?.addEventListener('click', () => this.hide());

        // Social share buttons
        this.#container.querySelectorAll('.share-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const platform = btn.dataset.platform;
                this.#shareToPlat(platform, shareUrl, shareText);
            });
        });

        // Copy link
        this.#container.querySelector('#copy-link')?.addEventListener('click', () => {
            this.#copyToClipboard(shareUrl);
        });

        // Native share
        this.#container.querySelector('#native-share')?.addEventListener('click', () => {
            this.#nativeShare(shareUrl, shareText);
        });

        // QR Code
        this.#container.querySelector('#show-qr')?.addEventListener('click', () => {
            this.#showQRCode(shareUrl);
        });
    }

    /**
     * Get share URL for tool
     * @param {Object} tool
     * @returns {string}
     */
    #getShareUrl(tool) {
        // Build URL with tool parameter
        const baseUrl = window.location.origin + window.location.pathname;
        const url = new URL(baseUrl);
        url.searchParams.set('tool', tool.id);
        return url.toString();
    }

    /**
     * Share to social platform
     * @param {string} platform
     * @param {string} url
     * @param {string} text
     */
    #shareToPlat(platform, url, text) {
        const encodedUrl = encodeURIComponent(url);
        const encodedText = encodeURIComponent(text);

        let shareUrl = '';

        switch (platform) {
            case 'twitter':
                shareUrl = `https://twitter.com/intent/tweet?text=${encodedText}&url=${encodedUrl}`;
                break;
            case 'linkedin':
                shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodedUrl}`;
                break;
            case 'facebook':
                shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}`;
                break;
            case 'reddit':
                shareUrl = `https://reddit.com/submit?url=${encodedUrl}&title=${encodedText}`;
                break;
            case 'email':
                shareUrl = `mailto:?subject=${encodedText}&body=${encodedUrl}`;
                break;
        }

        if (shareUrl) {
            window.open(shareUrl, '_blank', 'width=600,height=400');
        }

        this.events.emit(EVENTS.TOOL_SHARED, {
            toolId: this.#currentTool.id,
            platform
        });
    }

    /**
     * Copy to clipboard
     * @param {string} text
     */
    async #copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);

            this.events.emit(EVENTS.NOTIFICATION, {
                message: 'Link copied to clipboard!',
                type: 'success'
            });

            // Update button text temporarily
            const btn = this.#container.querySelector('#copy-link');
            if (btn) {
                const originalText = btn.textContent;
                btn.textContent = 'Copied!';
                setTimeout(() => {
                    btn.textContent = originalText;
                }, 2000);
            }
        } catch (e) {
            // Fallback for older browsers
            const input = this.#container.querySelector('#share-url');
            if (input) {
                input.select();
                document.execCommand('copy');
            }
        }
    }

    /**
     * Use native share API
     * @param {string} url
     * @param {string} text
     */
    async #nativeShare(url, text) {
        try {
            await navigator.share({
                title: this.#currentTool.title,
                text: text,
                url: url
            });

            this.events.emit(EVENTS.TOOL_SHARED, {
                toolId: this.#currentTool.id,
                platform: 'native'
            });
        } catch (e) {
            if (e.name !== 'AbortError') {
                this.events.emit(EVENTS.NOTIFICATION, {
                    message: 'Share failed',
                    type: 'error'
                });
            }
        }
    }

    /**
     * Show QR code for URL
     * @param {string} url
     */
    #showQRCode(url) {
        const container = this.#container.querySelector('#qr-container');
        const canvas = this.#container.querySelector('#qr-canvas');
        const btn = this.#container.querySelector('#show-qr');

        if (!container || !canvas) return;

        if (container.style.display === 'none') {
            // Generate simple QR code using canvas
            this.#generateQR(canvas, url);
            container.style.display = 'block';
            btn.textContent = 'Hide QR Code';
        } else {
            container.style.display = 'none';
            btn.textContent = 'Show QR Code';
        }
    }

    /**
     * Generate simple QR code
     * @param {HTMLCanvasElement} canvas
     * @param {string} text
     */
    #generateQR(canvas, text) {
        // Simple placeholder - in production, use a QR library
        const ctx = canvas.getContext('2d');
        canvas.width = 150;
        canvas.height = 150;

        // Draw placeholder pattern
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, 150, 150);

        ctx.fillStyle = '#000000';
        ctx.font = '10px monospace';
        ctx.textAlign = 'center';
        ctx.fillText('QR Code', 75, 70);
        ctx.fillText('(requires QR library)', 75, 85);

        // Draw simple pattern based on URL hash
        const hash = this.#simpleHash(text);
        ctx.fillStyle = '#000000';

        for (let i = 0; i < 10; i++) {
            for (let j = 0; j < 10; j++) {
                if ((hash >> (i + j)) & 1) {
                    ctx.fillRect(20 + i * 11, 20 + j * 11, 10, 10);
                }
            }
        }
    }

    /**
     * Simple hash function
     * @param {string} str
     * @returns {number}
     */
    #simpleHash(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            hash = ((hash << 5) - hash) + str.charCodeAt(i);
            hash = hash & hash;
        }
        return Math.abs(hash);
    }

    /**
     * Inject share styles
     */
    #injectStyles() {
        if (document.getElementById('share-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'share-styles';
        styles.textContent = `
            .share-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 1000;
                opacity: 0;
                transition: opacity var(--duration-300);
            }

            .share-modal.visible {
                opacity: 1;
            }

            .share-backdrop {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
            }

            .share-content {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%) scale(0.95);
                width: 90%;
                max-width: 400px;
                background: var(--color-bg-elevated);
                border-radius: var(--radius-xl);
                overflow: hidden;
                transition: transform var(--duration-300);
            }

            .share-modal.visible .share-content {
                transform: translate(-50%, -50%) scale(1);
            }

            .share-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: var(--space-4);
                border-bottom: 1px solid var(--color-border);
            }

            .share-header h3 {
                margin: 0;
                font-size: var(--text-lg);
            }

            .share-body {
                padding: var(--space-4);
            }

            .share-social {
                display: flex;
                justify-content: center;
                gap: var(--space-3);
                margin-bottom: var(--space-4);
            }

            .share-btn {
                width: 48px;
                height: 48px;
                border-radius: var(--radius-full);
                border: none;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all var(--duration-150);
            }

            .share-twitter {
                background: #000000;
                color: #ffffff;
            }

            .share-linkedin {
                background: #0077b5;
                color: #ffffff;
            }

            .share-facebook {
                background: #1877f2;
                color: #ffffff;
            }

            .share-reddit {
                background: #ff4500;
                color: #ffffff;
            }

            .share-email {
                background: var(--color-bg-tertiary);
                color: var(--color-text-primary);
            }

            .share-btn:hover {
                transform: scale(1.1);
            }

            .share-link {
                margin-bottom: var(--space-4);
            }

            .share-link label {
                display: block;
                font-size: var(--text-sm);
                color: var(--color-text-secondary);
                margin-bottom: var(--space-2);
            }

            .share-link-input {
                display: flex;
                gap: var(--space-2);
            }

            .share-link-input input {
                flex: 1;
                padding: var(--space-2) var(--space-3);
                background: var(--color-bg-tertiary);
                border: 1px solid var(--color-border);
                border-radius: var(--radius-md);
                color: var(--color-text-primary);
                font-size: var(--text-sm);
            }

            #native-share {
                margin-bottom: var(--space-4);
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .share-qr {
                text-align: center;
            }

            .qr-container {
                margin-top: var(--space-3);
            }

            #qr-canvas {
                border-radius: var(--radius-md);
            }
        `;

        document.head.appendChild(styles);
    }
}

export { ShareManager };
