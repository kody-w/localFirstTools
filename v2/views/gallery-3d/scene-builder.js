/**
 * Scene Builder - Three.js scene setup
 * Local First Tools v2
 */

import { GALLERY_3D } from '../../core/constants.js';

class SceneBuilder {
    /**
     * Create scene builder
     * @param {Object} THREE - Three.js library
     * @param {HTMLCanvasElement} canvas
     */
    constructor(THREE, canvas) {
        this.THREE = THREE;
        this.canvas = canvas;

        this.scene = null;
        this.camera = null;
        this.renderer = null;
    }

    /**
     * Initialize the scene
     */
    async initialize() {
        const THREE = this.THREE;

        // Create scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x0a0a0a);
        this.scene.fog = new THREE.Fog(0x0a0a0a, 20, 100);

        // Create camera
        const width = this.canvas.parentElement.clientWidth;
        const height = this.canvas.parentElement.clientHeight;

        this.camera = new THREE.PerspectiveCamera(
            GALLERY_3D.FOV,
            width / height,
            GALLERY_3D.NEAR,
            GALLERY_3D.FAR
        );
        this.camera.position.set(0, 2, 5);

        // Create renderer
        this.renderer = new THREE.WebGLRenderer({
            canvas: this.canvas,
            antialias: true,
            alpha: false
        });
        this.renderer.setSize(width, height);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;

        // Build environment
        this.#buildEnvironment();

        // Add lights
        this.#addLights();
    }

    /**
     * Build gallery environment
     */
    #buildEnvironment() {
        const THREE = this.THREE;

        // Floor
        const floorGeometry = new THREE.PlaneGeometry(50, 200);
        const floorMaterial = new THREE.MeshStandardMaterial({
            color: 0x1a1a1a,
            roughness: 0.8,
            metalness: 0.2
        });
        const floor = new THREE.Mesh(floorGeometry, floorMaterial);
        floor.rotation.x = -Math.PI / 2;
        floor.receiveShadow = true;
        this.scene.add(floor);

        // Ceiling
        const ceilingGeometry = new THREE.PlaneGeometry(50, 200);
        const ceilingMaterial = new THREE.MeshStandardMaterial({
            color: 0x141414,
            roughness: 1,
            metalness: 0
        });
        const ceiling = new THREE.Mesh(ceilingGeometry, ceilingMaterial);
        ceiling.rotation.x = Math.PI / 2;
        ceiling.position.y = 5;
        this.scene.add(ceiling);

        // Walls
        const wallMaterial = new THREE.MeshStandardMaterial({
            color: 0x1a1a1a,
            roughness: 0.9,
            metalness: 0.1
        });

        // Left wall
        const leftWall = new THREE.Mesh(
            new THREE.PlaneGeometry(200, 5),
            wallMaterial
        );
        leftWall.position.set(-10, 2.5, -50);
        leftWall.rotation.y = Math.PI / 2;
        this.scene.add(leftWall);

        // Right wall
        const rightWall = new THREE.Mesh(
            new THREE.PlaneGeometry(200, 5),
            wallMaterial
        );
        rightWall.position.set(10, 2.5, -50);
        rightWall.rotation.y = -Math.PI / 2;
        this.scene.add(rightWall);

        // Add accent lines
        this.#addAccentLines();
    }

    /**
     * Add accent lighting lines
     */
    #addAccentLines() {
        const THREE = this.THREE;

        const lineMaterial = new THREE.MeshBasicMaterial({
            color: 0x06ffa5,
            transparent: true,
            opacity: 0.5
        });

        // Floor accent lines
        for (let i = -50; i <= 0; i += 10) {
            const lineGeometry = new THREE.PlaneGeometry(20, 0.1);
            const line = new THREE.Mesh(lineGeometry, lineMaterial);
            line.rotation.x = -Math.PI / 2;
            line.position.set(0, 0.01, i);
            this.scene.add(line);
        }

        // Wall accent lights
        const lightGeometry = new THREE.BoxGeometry(0.1, 0.5, 0.1);
        const lightMaterial = new THREE.MeshBasicMaterial({
            color: 0x06ffa5
        });

        for (let z = -5; z >= -100; z -= 12) {
            // Left side
            const leftLight = new THREE.Mesh(lightGeometry, lightMaterial);
            leftLight.position.set(-9.9, 4, z);
            this.scene.add(leftLight);

            // Right side
            const rightLight = new THREE.Mesh(lightGeometry, lightMaterial);
            rightLight.position.set(9.9, 4, z);
            this.scene.add(rightLight);
        }
    }

    /**
     * Add lighting to scene
     */
    #addLights() {
        const THREE = this.THREE;

        // Ambient light
        const ambient = new THREE.AmbientLight(0xffffff, 0.3);
        this.scene.add(ambient);

        // Main directional light
        const mainLight = new THREE.DirectionalLight(0xffffff, 0.8);
        mainLight.position.set(5, 10, 5);
        mainLight.castShadow = true;
        mainLight.shadow.mapSize.width = 2048;
        mainLight.shadow.mapSize.height = 2048;
        mainLight.shadow.camera.near = 0.5;
        mainLight.shadow.camera.far = 50;
        this.scene.add(mainLight);

        // Accent point lights along the hall
        for (let z = 0; z >= -100; z -= 20) {
            const pointLight = new THREE.PointLight(0x06ffa5, 0.5, 15);
            pointLight.position.set(0, 4, z);
            this.scene.add(pointLight);
        }

        // Fill light from below
        const fillLight = new THREE.HemisphereLight(0x404040, 0x080820, 0.5);
        this.scene.add(fillLight);
    }

    /**
     * Create a tool frame (artwork in gallery)
     * @param {Object} tool
     * @param {Object} position
     * @param {Object} rotation
     * @returns {THREE.Group}
     */
    createToolFrame(tool, position, rotation = { x: 0, y: 0, z: 0 }) {
        const THREE = this.THREE;
        const group = new THREE.Group();

        // Frame dimensions
        const frameWidth = 4;
        const frameHeight = 3;
        const frameDepth = 0.1;

        // Frame
        const frameGeometry = new THREE.BoxGeometry(
            frameWidth + 0.2,
            frameHeight + 0.2,
            frameDepth
        );
        const frameMaterial = new THREE.MeshStandardMaterial({
            color: 0x333333,
            roughness: 0.3,
            metalness: 0.8
        });
        const frame = new THREE.Mesh(frameGeometry, frameMaterial);
        frame.castShadow = true;
        group.add(frame);

        // Inner canvas
        const canvasGeometry = new THREE.PlaneGeometry(frameWidth, frameHeight);
        const canvasMaterial = new THREE.MeshStandardMaterial({
            color: this.#getCategoryColor(tool.category),
            roughness: 0.9,
            metalness: 0.1
        });
        const canvas = new THREE.Mesh(canvasGeometry, canvasMaterial);
        canvas.position.z = frameDepth / 2 + 0.01;
        group.add(canvas);

        // Title text (using a simple plane with color)
        const titlePlane = new THREE.Mesh(
            new THREE.PlaneGeometry(3.5, 0.4),
            new THREE.MeshBasicMaterial({
                color: 0x06ffa5,
                transparent: true,
                opacity: 0.8
            })
        );
        titlePlane.position.set(0, -frameHeight / 2 - 0.4, frameDepth / 2 + 0.02);
        group.add(titlePlane);

        // Spotlight for this frame
        const spotlight = new THREE.SpotLight(0xffffff, 0.5, 8, Math.PI / 6, 0.5);
        spotlight.position.set(0, 2, 2);
        spotlight.target = frame;
        group.add(spotlight);

        // Position and rotate group
        group.position.set(position.x, position.y, position.z);
        group.rotation.set(rotation.x, rotation.y, rotation.z);

        // Store tool reference
        group.userData = { tool, type: 'tool-frame' };

        return group;
    }

    /**
     * Get category color
     * @param {string} category
     * @returns {number}
     */
    #getCategoryColor(category) {
        const colors = {
            visual_art: 0xff6b9d,
            '3d_immersive': 0x4ecdc4,
            audio_music: 0xffb347,
            games_puzzles: 0x9b59b6,
            experimental_ai: 0x00d4ff,
            creative_tools: 0xff9ff3,
            generative_art: 0x5fa8ff,
            particle_physics: 0x5dade2,
            educational_tools: 0xf7dc6f
        };

        return colors[category] || 0x888888;
    }

    /**
     * Render the scene
     */
    render() {
        if (this.renderer && this.scene && this.camera) {
            this.renderer.render(this.scene, this.camera);
        }
    }

    /**
     * Resize renderer and camera
     * @param {number} width
     * @param {number} height
     */
    resize(width, height) {
        if (this.camera) {
            this.camera.aspect = width / height;
            this.camera.updateProjectionMatrix();
        }

        if (this.renderer) {
            this.renderer.setSize(width, height);
        }
    }

    /**
     * Get scene
     * @returns {THREE.Scene}
     */
    getScene() {
        return this.scene;
    }

    /**
     * Get camera
     * @returns {THREE.PerspectiveCamera}
     */
    getCamera() {
        return this.camera;
    }

    /**
     * Get renderer
     * @returns {THREE.WebGLRenderer}
     */
    getRenderer() {
        return this.renderer;
    }

    /**
     * Dispose of all resources
     */
    dispose() {
        // Dispose geometries and materials
        this.scene?.traverse((object) => {
            if (object.geometry) {
                object.geometry.dispose();
            }
            if (object.material) {
                if (Array.isArray(object.material)) {
                    object.material.forEach(m => m.dispose());
                } else {
                    object.material.dispose();
                }
            }
        });

        // Dispose renderer
        if (this.renderer) {
            this.renderer.dispose();
            this.renderer = null;
        }

        this.scene = null;
        this.camera = null;
    }
}

export { SceneBuilder };
