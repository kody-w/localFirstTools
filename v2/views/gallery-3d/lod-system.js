/**
 * LOD System - Level of Detail for 3D gallery
 * Local First Tools v2
 */

import { GALLERY_3D } from '../../core/constants.js';

class LODSystem {
    /**
     * Create LOD system
     * @param {Object} THREE - Three.js library
     * @param {THREE.Scene} scene
     */
    constructor(THREE, scene) {
        this.THREE = THREE;
        this.scene = scene;

        this.#toolObjects = new Map(); // toolId -> { group, lod, tool }
        this.#raycaster = new THREE.Raycaster();
        this.#mouse = new THREE.Vector2();
    }

    #toolObjects;
    #raycaster;
    #mouse;

    /**
     * Add a tool to the scene with LOD
     * @param {Object} tool
     * @param {Object} position
     * @param {Object} options
     */
    addTool(tool, position, options = {}) {
        const THREE = this.THREE;

        // Create LOD object
        const lod = new THREE.LOD();

        // High detail (close up)
        const highDetail = this.#createHighDetailFrame(tool);
        lod.addLevel(highDetail, GALLERY_3D.LOD_LEVELS.HIGH);

        // Medium detail
        const mediumDetail = this.#createMediumDetailFrame(tool);
        lod.addLevel(mediumDetail, GALLERY_3D.LOD_LEVELS.MEDIUM);

        // Low detail (far away)
        const lowDetail = this.#createLowDetailFrame(tool);
        lod.addLevel(lowDetail, GALLERY_3D.LOD_LEVELS.LOW);

        // Position LOD
        lod.position.set(position.x, position.y, position.z);

        if (options.rotation) {
            lod.rotation.set(
                options.rotation.x || 0,
                options.rotation.y || 0,
                options.rotation.z || 0
            );
        }

        // Store tool data
        lod.userData = { tool, type: 'tool-frame' };

        // Add to scene
        this.scene.add(lod);

        // Store reference
        this.#toolObjects.set(tool.id, {
            lod,
            tool,
            position
        });

        return lod;
    }

    /**
     * Create high detail frame
     * @param {Object} tool
     * @returns {THREE.Group}
     */
    #createHighDetailFrame(tool) {
        const THREE = this.THREE;
        const group = new THREE.Group();

        const frameWidth = 4;
        const frameHeight = 3;

        // Ornate frame
        const frameGeometry = new THREE.BoxGeometry(
            frameWidth + 0.3,
            frameHeight + 0.3,
            0.15
        );
        const frameMaterial = new THREE.MeshStandardMaterial({
            color: 0x333333,
            roughness: 0.3,
            metalness: 0.8
        });
        const frame = new THREE.Mesh(frameGeometry, frameMaterial);
        frame.castShadow = true;
        group.add(frame);

        // Inner frame detail
        const innerFrame = new THREE.Mesh(
            new THREE.BoxGeometry(frameWidth + 0.1, frameHeight + 0.1, 0.12),
            new THREE.MeshStandardMaterial({
                color: 0x222222,
                roughness: 0.5,
                metalness: 0.6
            })
        );
        innerFrame.position.z = 0.02;
        group.add(innerFrame);

        // Canvas
        const canvas = new THREE.Mesh(
            new THREE.PlaneGeometry(frameWidth, frameHeight),
            new THREE.MeshStandardMaterial({
                color: this.#getCategoryColor(tool.category),
                roughness: 0.8,
                metalness: 0.1,
                emissive: this.#getCategoryColor(tool.category),
                emissiveIntensity: 0.1
            })
        );
        canvas.position.z = 0.08;
        group.add(canvas);

        // Category icon (simple colored circle)
        const iconGeometry = new THREE.CircleGeometry(0.3, 32);
        const iconMaterial = new THREE.MeshBasicMaterial({
            color: 0x06ffa5,
            transparent: true,
            opacity: 0.9
        });
        const icon = new THREE.Mesh(iconGeometry, iconMaterial);
        icon.position.set(-frameWidth / 2 + 0.5, frameHeight / 2 - 0.5, 0.09);
        group.add(icon);

        // Featured star
        if (tool.featured) {
            const star = this.#createStar();
            star.position.set(frameWidth / 2 - 0.3, frameHeight / 2 - 0.3, 0.1);
            group.add(star);
        }

        // Title bar
        const titleBar = new THREE.Mesh(
            new THREE.PlaneGeometry(frameWidth - 0.5, 0.3),
            new THREE.MeshBasicMaterial({
                color: 0x000000,
                transparent: true,
                opacity: 0.7
            })
        );
        titleBar.position.set(0, -frameHeight / 2 + 0.3, 0.09);
        group.add(titleBar);

        return group;
    }

    /**
     * Create medium detail frame
     * @param {Object} tool
     * @returns {THREE.Group}
     */
    #createMediumDetailFrame(tool) {
        const THREE = this.THREE;
        const group = new THREE.Group();

        const frameWidth = 4;
        const frameHeight = 3;

        // Simple frame
        const frame = new THREE.Mesh(
            new THREE.BoxGeometry(frameWidth + 0.2, frameHeight + 0.2, 0.1),
            new THREE.MeshStandardMaterial({
                color: 0x333333,
                roughness: 0.5,
                metalness: 0.5
            })
        );
        frame.castShadow = true;
        group.add(frame);

        // Canvas
        const canvas = new THREE.Mesh(
            new THREE.PlaneGeometry(frameWidth, frameHeight),
            new THREE.MeshBasicMaterial({
                color: this.#getCategoryColor(tool.category)
            })
        );
        canvas.position.z = 0.06;
        group.add(canvas);

        return group;
    }

    /**
     * Create low detail frame (far away)
     * @param {Object} tool
     * @returns {THREE.Mesh}
     */
    #createLowDetailFrame(tool) {
        const THREE = this.THREE;

        // Just a colored plane
        const mesh = new THREE.Mesh(
            new THREE.PlaneGeometry(4, 3),
            new THREE.MeshBasicMaterial({
                color: this.#getCategoryColor(tool.category)
            })
        );

        return mesh;
    }

    /**
     * Create star shape for featured tools
     * @returns {THREE.Mesh}
     */
    #createStar() {
        const THREE = this.THREE;

        const starShape = new THREE.Shape();
        const outerRadius = 0.2;
        const innerRadius = 0.1;
        const spikes = 5;

        for (let i = 0; i < spikes * 2; i++) {
            const radius = i % 2 === 0 ? outerRadius : innerRadius;
            const angle = (i / (spikes * 2)) * Math.PI * 2 - Math.PI / 2;
            const x = Math.cos(angle) * radius;
            const y = Math.sin(angle) * radius;

            if (i === 0) {
                starShape.moveTo(x, y);
            } else {
                starShape.lineTo(x, y);
            }
        }
        starShape.closePath();

        const geometry = new THREE.ShapeGeometry(starShape);
        const material = new THREE.MeshBasicMaterial({
            color: 0xffd700,
            side: THREE.DoubleSide
        });

        return new THREE.Mesh(geometry, material);
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
     * Update LOD based on camera position
     * @param {THREE.Vector3} cameraPosition
     */
    update(cameraPosition) {
        for (const [, data] of this.#toolObjects) {
            data.lod.update(cameraPosition);
        }
    }

    /**
     * Get hovered tool (raycasting)
     * @param {THREE.Camera} camera
     * @param {number} width
     * @param {number} height
     * @returns {Object|null}
     */
    getHoveredTool(camera, width, height) {
        // Use center of screen for "look at" detection
        this.#mouse.set(0, 0);

        this.#raycaster.setFromCamera(this.#mouse, camera);

        const objects = Array.from(this.#toolObjects.values()).map(d => d.lod);
        const intersects = this.#raycaster.intersectObjects(objects, true);

        if (intersects.length > 0) {
            // Find parent LOD object
            let obj = intersects[0].object;
            while (obj.parent && !obj.userData?.tool) {
                obj = obj.parent;
            }

            if (obj.userData?.tool) {
                return obj.userData.tool;
            }
        }

        return null;
    }

    /**
     * Get tool by ID
     * @param {string} toolId
     * @returns {Object|null}
     */
    getTool(toolId) {
        return this.#toolObjects.get(toolId)?.tool || null;
    }

    /**
     * Get all tool objects
     * @returns {Map}
     */
    getAll() {
        return this.#toolObjects;
    }

    /**
     * Remove a tool
     * @param {string} toolId
     */
    removeTool(toolId) {
        const data = this.#toolObjects.get(toolId);
        if (data) {
            this.scene.remove(data.lod);
            this.#disposeLOD(data.lod);
            this.#toolObjects.delete(toolId);
        }
    }

    /**
     * Clear all tools
     */
    clear() {
        for (const [id] of this.#toolObjects) {
            this.removeTool(id);
        }
    }

    /**
     * Dispose LOD object
     * @param {THREE.LOD} lod
     */
    #disposeLOD(lod) {
        lod.traverse((child) => {
            if (child.geometry) {
                child.geometry.dispose();
            }
            if (child.material) {
                if (Array.isArray(child.material)) {
                    child.material.forEach(m => m.dispose());
                } else {
                    child.material.dispose();
                }
            }
        });
    }

    /**
     * Dispose of all resources
     */
    dispose() {
        this.clear();
    }
}

export { LODSystem };
