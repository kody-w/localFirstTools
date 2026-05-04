/**
 * Skeleton Loader - Loading placeholder animations
 * Local First Tools v2
 */

class SkeletonLoader {
    /**
     * Create skeleton loader
     * @param {Object} options
     */
    constructor(options = {}) {
        this.options = {
            count: 6,
            type: 'card',
            animate: true,
            ...options
        };
    }

    /**
     * Render skeleton grid
     * @param {number} count - Number of skeleton cards
     * @returns {HTMLElement}
     */
    renderGrid(count = this.options.count) {
        const container = document.createElement('div');
        container.className = 'skeleton-grid';

        for (let i = 0; i < count; i++) {
            container.appendChild(this.renderCard());
        }

        return container;
    }

    /**
     * Render a single skeleton card
     * @returns {HTMLElement}
     */
    renderCard() {
        const card = document.createElement('div');
        card.className = 'skeleton-card';

        card.innerHTML = `
            <div class="skeleton-header">
                <div class="skeleton skeleton-badge"></div>
                <div class="skeleton" style="width: 24px; height: 24px; border-radius: 50%;"></div>
            </div>
            <div class="skeleton-body">
                <div class="skeleton skeleton-title"></div>
                <div class="skeleton skeleton-text"></div>
                <div class="skeleton skeleton-text short"></div>
            </div>
            <div class="skeleton-footer">
                <div class="skeleton skeleton-button"></div>
                <div class="skeleton skeleton-button" style="width: 80px;"></div>
            </div>
        `;

        return card;
    }

    /**
     * Render skeleton list
     * @param {number} count
     * @returns {HTMLElement}
     */
    renderList(count = this.options.count) {
        const container = document.createElement('div');
        container.className = 'skeleton-list';

        for (let i = 0; i < count; i++) {
            container.appendChild(this.renderListItem());
        }

        return container;
    }

    /**
     * Render a single skeleton list item
     * @returns {HTMLElement}
     */
    renderListItem() {
        const item = document.createElement('div');
        item.className = 'skeleton-list-item';

        item.innerHTML = `
            <div class="skeleton skeleton-avatar"></div>
            <div class="skeleton-content">
                <div class="skeleton skeleton-title" style="width: 60%;"></div>
                <div class="skeleton skeleton-text" style="width: 80%;"></div>
            </div>
            <div class="skeleton skeleton-button" style="width: 60px;"></div>
        `;

        return item;
    }

    /**
     * Render skeleton section
     * @returns {HTMLElement}
     */
    renderSection() {
        const section = document.createElement('div');
        section.className = 'skeleton-section';

        section.innerHTML = `
            <div class="skeleton-header" style="margin-bottom: 16px;">
                <div class="skeleton skeleton-title" style="width: 200px;"></div>
                <div class="skeleton skeleton-badge" style="width: 40px;"></div>
            </div>
            <div class="skeleton-grid">
                ${Array(3).fill(0).map(() => this.renderCard().outerHTML).join('')}
            </div>
        `;

        return section;
    }

    /**
     * Render inline skeleton text
     * @param {string} width
     * @returns {HTMLElement}
     */
    renderText(width = '100%') {
        const text = document.createElement('div');
        text.className = 'skeleton skeleton-text';
        text.style.width = width;
        return text;
    }

    /**
     * Render skeleton avatar
     * @param {string} size
     * @returns {HTMLElement}
     */
    renderAvatar(size = '40px') {
        const avatar = document.createElement('div');
        avatar.className = 'skeleton skeleton-avatar';
        avatar.style.width = size;
        avatar.style.height = size;
        return avatar;
    }

    /**
     * Render skeleton image
     * @param {string} height
     * @returns {HTMLElement}
     */
    renderImage(height = '200px') {
        const image = document.createElement('div');
        image.className = 'skeleton skeleton-image';
        image.style.height = height;
        return image;
    }

    /**
     * Show skeleton in container
     * @param {HTMLElement} container
     * @param {string} type - 'grid', 'list', 'section'
     * @param {number} count
     */
    show(container, type = 'grid', count = this.options.count) {
        container.innerHTML = '';

        let skeleton;
        switch (type) {
            case 'list':
                skeleton = this.renderList(count);
                break;
            case 'section':
                skeleton = this.renderSection();
                break;
            case 'grid':
            default:
                skeleton = this.renderGrid(count);
        }

        container.appendChild(skeleton);
    }

    /**
     * Hide skeleton and show content
     * @param {HTMLElement} container
     * @param {HTMLElement|string} content
     * @param {boolean} animate
     */
    hide(container, content, animate = true) {
        if (animate) {
            container.style.opacity = '0';
            container.style.transition = 'opacity 150ms ease-out';

            setTimeout(() => {
                if (typeof content === 'string') {
                    container.innerHTML = content;
                } else if (content instanceof HTMLElement) {
                    container.innerHTML = '';
                    container.appendChild(content);
                }

                container.style.opacity = '1';
            }, 150);
        } else {
            if (typeof content === 'string') {
                container.innerHTML = content;
            } else if (content instanceof HTMLElement) {
                container.innerHTML = '';
                container.appendChild(content);
            }
        }
    }

    /**
     * Create loading overlay
     * @param {string} message
     * @returns {HTMLElement}
     */
    createOverlay(message = 'Loading...') {
        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay';

        overlay.innerHTML = `
            <div class="loading-spinner"></div>
            <p class="loading-message">${message}</p>
        `;

        return overlay;
    }
}

/**
 * Factory function to create skeleton loaders
 * @param {Object} options
 * @returns {SkeletonLoader}
 */
export function createSkeletonLoader(options = {}) {
    return new SkeletonLoader(options);
}

/**
 * Quick helpers for common skeleton patterns
 */
export const Skeleton = {
    /**
     * Render skeleton grid into container
     * @param {HTMLElement} container
     * @param {number} count
     */
    showGrid(container, count = 6) {
        const loader = new SkeletonLoader();
        loader.show(container, 'grid', count);
    },

    /**
     * Render skeleton list into container
     * @param {HTMLElement} container
     * @param {number} count
     */
    showList(container, count = 6) {
        const loader = new SkeletonLoader();
        loader.show(container, 'list', count);
    },

    /**
     * Create a skeleton card element
     * @returns {HTMLElement}
     */
    card() {
        const loader = new SkeletonLoader();
        return loader.renderCard();
    },

    /**
     * Create skeleton grid element
     * @param {number} count
     * @returns {HTMLElement}
     */
    grid(count = 6) {
        const loader = new SkeletonLoader();
        return loader.renderGrid(count);
    }
};

export { SkeletonLoader };
