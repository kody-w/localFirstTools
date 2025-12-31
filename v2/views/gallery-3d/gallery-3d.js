/**
 * Gallery 3D - Main controller for 3D gallery experience
 * Local First Tools v2
 */

import { StateManager } from '../../core/state-manager.js';
import { EventBus, EVENTS } from '../../core/event-bus.js';
import { ToolRepository } from '../../data/tool-repository.js';
import { GALLERY_3D } from '../../core/constants.js';
import { SceneBuilder } from './scene-builder.js';
import { LODSystem } from './lod-system.js';
import { Controls3D } from './controls.js';

class Gallery3D {
    constructor() {
        this.state = StateManager.getInstance();
        this.events = EventBus.getInstance();
        this.toolRepo = ToolRepository.getInstance();

        this.#container = null;
        this.#canvas = null;
        this.#sceneBuilder = null;
        this.#lodSystem = null;
        this.#controls = null;
        this.#animationId = null;
        this.#isRunning = false;
        this.#tools = [];
        this.#hoveredTool = null;
    }

    #container;
    #canvas;
    #sceneBuilder;
    #lodSystem;
    #controls;
    #animationId;
    #isRunning;
    #tools;
    #hoveredTool;

    /**
     * Initialize the 3D gallery
     * @param {HTMLElement} container
     */
    async initialize(container) {
        this.#container = container;
        this.#container.className = 'gallery-3d-container';

        // Check for WebGL support
        if (!this.#checkWebGLSupport()) {
            this.#renderFallback();
            return;
        }

        // Create canvas
        this.#canvas = document.createElement('canvas');
        this.#canvas.className = 'gallery-3d-canvas';
        this.#container.innerHTML = '';
        this.#container.appendChild(this.#canvas);

        // Add UI overlay
        this.#addUIOverlay();

        // Initialize Three.js components
        await this.#initThreeJS();

        // Setup event listeners
        this.#setupEvents();

        // Start render loop
        this.start();

        this.events.emit(EVENTS.GALLERY_3D_ENTER);
    }

    /**
     * Check WebGL support
     * @returns {boolean}
     */
    #checkWebGLSupport() {
        try {
            const canvas = document.createElement('canvas');
            return !!(
                window.WebGLRenderingContext &&
                (canvas.getContext('webgl') || canvas.getContext('experimental-webgl'))
            );
        } catch (e) {
            return false;
        }
    }

    /**
     * Initialize Three.js scene
     */
    async #initThreeJS() {
        // Dynamic import Three.js from CDN
        const THREE = await this.#loadThreeJS();

        if (!THREE) {
            this.#renderFallback();
            return;
        }

        // Create scene builder
        this.#sceneBuilder = new SceneBuilder(THREE, this.#canvas);
        await this.#sceneBuilder.initialize();

        // Create LOD system
        this.#lodSystem = new LODSystem(THREE, this.#sceneBuilder.getScene());

        // Create controls
        this.#controls = new Controls3D(
            this.#sceneBuilder.getCamera(),
            this.#canvas,
            this.events
        );

        // Load tools into scene
        this.#tools = this.state.getSlice('filteredTools');
        await this.#loadToolsIntoScene(this.#tools);
    }

    /**
     * Load Three.js dynamically
     * @returns {Promise<Object|null>}
     */
    async #loadThreeJS() {
        // Check if already loaded
        if (window.THREE) {
            return window.THREE;
        }

        try {
            // Try to use ES module import
            const module = await import('https://unpkg.com/three@0.160.0/build/three.module.js');
            return module;
        } catch (e) {
            console.warn('Failed to load Three.js:', e);

            // Try script tag fallback
            return new Promise((resolve) => {
                const script = document.createElement('script');
                script.src = 'https://unpkg.com/three@0.160.0/build/three.min.js';
                script.onload = () => resolve(window.THREE);
                script.onerror = () => resolve(null);
                document.head.appendChild(script);
            });
        }
    }

    /**
     * Load tools into the 3D scene
     * @param {Array} tools
     */
    async #loadToolsIntoScene(tools) {
        if (!this.#sceneBuilder || !this.#lodSystem) return;

        // Clear existing
        this.#lodSystem.clear();

        // Create tool frames in a gallery layout
        const layout = this.#calculateGalleryLayout(tools.length);

        for (let i = 0; i < tools.length; i++) {
            const tool = tools[i];
            const position = layout.positions[i];

            this.#lodSystem.addTool(tool, position, {
                rotation: layout.rotations[i]
            });
        }
    }

    /**
     * Calculate gallery layout positions
     * @param {number} count
     * @returns {Object}
     */
    #calculateGalleryLayout(count) {
        const positions = [];
        const rotations = [];

        // Gallery hall layout: tools on left and right walls
        const hallWidth = 20;
        const hallLength = Math.ceil(count / 2) * 6;
        const spacing = 6;

        for (let i = 0; i < count; i++) {
            const side = i % 2 === 0 ? -1 : 1; // Alternate left/right
            const index = Math.floor(i / 2);

            positions.push({
                x: side * (hallWidth / 2),
                y: 2, // Eye level
                z: -index * spacing
            });

            // Face inward
            rotations.push({
                x: 0,
                y: side > 0 ? -Math.PI / 2 : Math.PI / 2,
                z: 0
            });
        }

        return { positions, rotations, hallLength };
    }

    /**
     * Add UI overlay
     */
    #addUIOverlay() {
        const overlay = document.createElement('div');
        overlay.className = 'gallery-3d-overlay';
        overlay.innerHTML = `
            <div class="gallery-3d-hud">
                <div class="gallery-3d-controls-hint">
                    <span>🎮 WASD/Arrows to move</span>
                    <span>🖱️ Mouse to look</span>
                    <span>⏎ Enter to open tool</span>
                    <span>⎋ ESC to exit</span>
                </div>
            </div>
            <div class="gallery-3d-tool-info" id="gallery-3d-tool-info" style="display: none;">
                <h3 class="tool-info-title"></h3>
                <p class="tool-info-description"></p>
                <span class="tool-info-hint">Press Enter to open</span>
            </div>
            <button class="gallery-3d-exit-btn" id="gallery-3d-exit">
                Exit 3D Gallery
            </button>
        `;

        this.#container.appendChild(overlay);
        this.#injectStyles();

        // Bind exit button
        const exitBtn = overlay.querySelector('#gallery-3d-exit');
        exitBtn?.addEventListener('click', () => this.exit());
    }

    /**
     * Setup event listeners
     */
    #setupEvents() {
        // Resize handler
        window.addEventListener('resize', this.#handleResize.bind(this));

        // Keyboard for exit
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.#isRunning) {
                this.exit();
            }
        });

        // Subscribe to tool changes
        this.state.subscribeToSlice('filteredTools', (tools) => {
            if (this.#isRunning) {
                this.#loadToolsIntoScene(tools);
            }
        });
    }

    /**
     * Handle resize
     */
    #handleResize() {
        if (!this.#sceneBuilder) return;

        const width = this.#container.clientWidth;
        const height = this.#container.clientHeight;

        this.#sceneBuilder.resize(width, height);
    }

    /**
     * Start the render loop
     */
    start() {
        if (this.#isRunning) return;

        this.#isRunning = true;
        this.#animate();
    }

    /**
     * Animation loop
     */
    #animate() {
        if (!this.#isRunning) return;

        this.#animationId = requestAnimationFrame(() => this.#animate());

        // Update controls
        if (this.#controls) {
            this.#controls.update();
        }

        // Update LOD based on camera position
        if (this.#lodSystem && this.#sceneBuilder) {
            const camera = this.#sceneBuilder.getCamera();
            this.#lodSystem.update(camera.position);

            // Check for hovered tool
            const hoveredTool = this.#lodSystem.getHoveredTool(
                camera,
                this.#container.clientWidth,
                this.#container.clientHeight
            );

            this.#updateToolInfo(hoveredTool);
        }

        // Render
        if (this.#sceneBuilder) {
            this.#sceneBuilder.render();
        }
    }

    /**
     * Update tool info display
     * @param {Object|null} tool
     */
    #updateToolInfo(tool) {
        const infoEl = document.getElementById('gallery-3d-tool-info');
        if (!infoEl) return;

        if (tool && tool !== this.#hoveredTool) {
            this.#hoveredTool = tool;

            infoEl.querySelector('.tool-info-title').textContent = tool.title;
            infoEl.querySelector('.tool-info-description').textContent =
                tool.description || 'No description';
            infoEl.style.display = 'block';

            this.events.emit(EVENTS.GALLERY_3D_TOOL_HOVER, { tool });
        } else if (!tool && this.#hoveredTool) {
            this.#hoveredTool = null;
            infoEl.style.display = 'none';
        }
    }

    /**
     * Stop the render loop
     */
    stop() {
        this.#isRunning = false;

        if (this.#animationId) {
            cancelAnimationFrame(this.#animationId);
            this.#animationId = null;
        }
    }

    /**
     * Exit 3D gallery
     */
    exit() {
        this.stop();

        if (this.#controls) {
            this.#controls.dispose();
        }

        if (this.#sceneBuilder) {
            this.#sceneBuilder.dispose();
        }

        this.events.emit(EVENTS.GALLERY_3D_EXIT);
        this.events.emit(EVENTS.VIEW_CHANGE, { mode: 'grid' });
    }

    /**
     * Render tools in the gallery
     * @param {Array} tools
     */
    render(tools) {
        this.#tools = tools;

        if (this.#isRunning) {
            this.#loadToolsIntoScene(tools);
        }
    }

    /**
     * Render fallback for no WebGL
     */
    #renderFallback() {
        this.#container.innerHTML = `
            <div class="gallery-3d-fallback">
                <div class="fallback-icon">🎮</div>
                <h2>3D Gallery Not Available</h2>
                <p>Your browser doesn't support WebGL, which is required for the 3D gallery experience.</p>
                <button class="btn btn-primary" onclick="this.closest('.gallery-3d-container').dispatchEvent(new CustomEvent('exit'))">
                    Return to Gallery
                </button>
            </div>
        `;

        this.#container.addEventListener('exit', () => {
            this.events.emit(EVENTS.VIEW_CHANGE, { mode: 'grid' });
        });
    }

    /**
     * Inject 3D gallery styles
     */
    #injectStyles() {
        if (document.getElementById('gallery-3d-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'gallery-3d-styles';
        styles.textContent = `
            .gallery-3d-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                z-index: 1000;
                background: #000;
            }

            .gallery-3d-canvas {
                width: 100%;
                height: 100%;
                display: block;
            }

            .gallery-3d-overlay {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
            }

            .gallery-3d-hud {
                position: absolute;
                bottom: var(--space-5);
                left: 50%;
                transform: translateX(-50%);
            }

            .gallery-3d-controls-hint {
                display: flex;
                gap: var(--space-4);
                padding: var(--space-3) var(--space-4);
                background: rgba(0, 0, 0, 0.7);
                border-radius: var(--radius-lg);
                font-size: var(--text-sm);
                color: var(--text-secondary);
            }

            .gallery-3d-tool-info {
                position: absolute;
                bottom: 100px;
                left: 50%;
                transform: translateX(-50%);
                max-width: 400px;
                padding: var(--space-4);
                background: var(--glass-bg);
                backdrop-filter: var(--glass-blur);
                border: 1px solid var(--glass-border);
                border-radius: var(--radius-xl);
                text-align: center;
            }

            .tool-info-title {
                font-size: var(--text-lg);
                margin-bottom: var(--space-2);
            }

            .tool-info-description {
                font-size: var(--text-sm);
                color: var(--text-secondary);
                margin-bottom: var(--space-2);
            }

            .tool-info-hint {
                font-size: var(--text-xs);
                color: var(--color-accent);
            }

            .gallery-3d-exit-btn {
                position: absolute;
                top: var(--space-4);
                right: var(--space-4);
                padding: var(--space-2) var(--space-4);
                background: var(--color-error);
                color: white;
                border: none;
                border-radius: var(--radius-lg);
                cursor: pointer;
                pointer-events: auto;
                font-size: var(--text-sm);
                transition: all var(--duration-150);
            }

            .gallery-3d-exit-btn:hover {
                background: #dc2626;
            }

            .gallery-3d-fallback {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100%;
                text-align: center;
                color: var(--text-primary);
            }

            .fallback-icon {
                font-size: 64px;
                margin-bottom: var(--space-4);
            }
        `;
        document.head.appendChild(styles);
    }

    /**
     * Destroy the gallery
     */
    destroy() {
        this.stop();

        if (this.#controls) {
            this.#controls.dispose();
            this.#controls = null;
        }

        if (this.#lodSystem) {
            this.#lodSystem.dispose();
            this.#lodSystem = null;
        }

        if (this.#sceneBuilder) {
            this.#sceneBuilder.dispose();
            this.#sceneBuilder = null;
        }

        window.removeEventListener('resize', this.#handleResize);

        this.#container = null;
        this.#canvas = null;
    }
}

export { Gallery3D };
