/**
 * WowMon Comparison Tool
 * A comprehensive side-by-side creature comparison system
 *
 * Features:
 * - Compare 2-4 creatures simultaneously
 * - Visual stat comparisons with overlays
 * - Type effectiveness analysis
 * - Battle simulation predictions
 * - Move pool overlap detection
 * - Shareable comparison URLs
 */

class WowMonComparisonTool {
    constructor(gameEngine) {
        this.gameEngine = gameEngine;
        this.comparisonList = []; // Array of creature IDs being compared
        this.maxComparisons = 4;
        this.comparisonPanel = null;
        this.init();
    }

    init() {
        this.createComparisonPanel();
        this.loadFromURL();
    }

    /**
     * Create the comparison panel UI
     */
    createComparisonPanel() {
        const panel = document.createElement('div');
        panel.id = 'comparison-panel';
        panel.className = 'comparison-panel';
        panel.innerHTML = `
            <div class="comparison-header">
                <h2>Creature Comparison</h2>
                <div class="comparison-controls">
                    <button id="comparison-toggle" class="comparison-btn" aria-label="Toggle comparison panel">
                        Compare (0)
                    </button>
                    <button id="comparison-clear" class="comparison-btn" aria-label="Clear all comparisons">
                        Clear All
                    </button>
                    <button id="comparison-share" class="comparison-btn" aria-label="Share comparison">
                        Share
                    </button>
                    <button id="comparison-export" class="comparison-btn" aria-label="Export as image">
                        Export
                    </button>
                    <button id="comparison-close" class="comparison-btn" aria-label="Close panel">
                        ✕
                    </button>
                </div>
            </div>
            <div id="comparison-content" class="comparison-content">
                <div class="comparison-empty">
                    <p>Select creatures to compare (2-4 recommended)</p>
                    <p>Use the "Add to Compare" button from creature details</p>
                </div>
            </div>
        `;

        document.body.appendChild(panel);
        this.comparisonPanel = panel;

        // Add styles
        this.injectStyles();

        // Attach event listeners
        this.attachEventListeners();
    }

    /**
     * Inject CSS styles for the comparison panel
     */
    injectStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .comparison-panel {
                position: fixed;
                top: 0;
                right: -600px;
                width: 600px;
                height: 100vh;
                background: var(--gb-lightest, #9bbc0f);
                border-left: 4px solid var(--gb-darkest, #0f380f);
                box-shadow: -4px 0 20px rgba(0,0,0,0.5);
                transition: right 0.3s ease;
                z-index: 9999;
                overflow-y: auto;
                font-family: monospace;
            }

            .comparison-panel.active {
                right: 0;
            }

            .comparison-header {
                padding: 15px;
                background: var(--gb-dark, #306230);
                color: var(--gb-lightest, #9bbc0f);
                position: sticky;
                top: 0;
                z-index: 10;
            }

            .comparison-header h2 {
                margin: 0 0 10px 0;
                font-size: 18px;
            }

            .comparison-controls {
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
            }

            .comparison-btn {
                background: var(--gb-lightest, #9bbc0f);
                color: var(--gb-darkest, #0f380f);
                border: 2px solid var(--gb-darkest, #0f380f);
                padding: 6px 12px;
                font-family: monospace;
                font-size: 12px;
                cursor: pointer;
                transition: all 0.1s;
            }

            .comparison-btn:hover {
                background: var(--gb-light, #8bac0f);
            }

            .comparison-btn:active {
                transform: translateY(2px);
            }

            .comparison-content {
                padding: 20px;
            }

            .comparison-empty {
                text-align: center;
                padding: 40px 20px;
                color: var(--gb-darkest, #0f380f);
            }

            .comparison-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 15px;
                margin-bottom: 30px;
            }

            .creature-card {
                background: var(--gb-light, #8bac0f);
                border: 3px solid var(--gb-darkest, #0f380f);
                padding: 15px;
                position: relative;
            }

            .creature-card-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
            }

            .creature-card-header h3 {
                margin: 0;
                font-size: 16px;
                color: var(--gb-darkest, #0f380f);
            }

            .creature-remove-btn {
                background: #8b0000;
                color: #fff;
                border: none;
                padding: 4px 8px;
                cursor: pointer;
                font-family: monospace;
                font-size: 10px;
            }

            .creature-type-badges {
                display: flex;
                gap: 5px;
                margin-bottom: 10px;
                flex-wrap: wrap;
            }

            .type-badge {
                background: var(--gb-darkest, #0f380f);
                color: var(--gb-lightest, #9bbc0f);
                padding: 3px 8px;
                font-size: 10px;
                text-transform: uppercase;
            }

            .stat-comparison {
                margin: 10px 0;
            }

            .stat-row {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin: 5px 0;
                font-size: 11px;
            }

            .stat-name {
                width: 80px;
                font-weight: bold;
            }

            .stat-bar-container {
                flex: 1;
                height: 12px;
                background: var(--gb-darkest, #0f380f);
                position: relative;
                margin: 0 5px;
            }

            .stat-bar {
                height: 100%;
                background: var(--gb-dark, #306230);
                transition: width 0.3s;
            }

            .stat-bar.best {
                background: #4a9d00;
            }

            .stat-value {
                width: 40px;
                text-align: right;
                font-weight: bold;
            }

            .comparison-section {
                background: var(--gb-light, #8bac0f);
                border: 3px solid var(--gb-darkest, #0f380f);
                padding: 15px;
                margin: 20px 0;
            }

            .comparison-section h3 {
                margin: 0 0 15px 0;
                font-size: 16px;
                color: var(--gb-darkest, #0f380f);
            }

            .radar-chart-container {
                width: 100%;
                height: 300px;
                display: flex;
                justify-content: center;
                align-items: center;
                background: var(--gb-lightest, #9bbc0f);
                border: 2px solid var(--gb-darkest, #0f380f);
            }

            .type-effectiveness-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                gap: 10px;
            }

            .effectiveness-card {
                background: var(--gb-lightest, #9bbc0f);
                border: 2px solid var(--gb-darkest, #0f380f);
                padding: 10px;
                font-size: 11px;
            }

            .effectiveness-card h4 {
                margin: 0 0 8px 0;
                font-size: 12px;
            }

            .effectiveness-vs {
                margin: 5px 0;
            }

            .effectiveness-multiplier {
                font-weight: bold;
                padding: 2px 6px;
            }

            .effectiveness-multiplier.super-effective {
                background: #4a9d00;
                color: #fff;
            }

            .effectiveness-multiplier.not-very-effective {
                background: #8b0000;
                color: #fff;
            }

            .effectiveness-multiplier.neutral {
                background: var(--gb-dark, #306230);
                color: var(--gb-lightest, #9bbc0f);
            }

            .battle-prediction {
                background: var(--gb-lightest, #9bbc0f);
                border: 2px solid var(--gb-darkest, #0f380f);
                padding: 15px;
                margin: 10px 0;
            }

            .battle-prediction h4 {
                margin: 0 0 10px 0;
                font-size: 14px;
            }

            .battle-matchup {
                display: grid;
                grid-template-columns: 1fr auto 1fr;
                align-items: center;
                gap: 10px;
                margin: 10px 0;
                padding: 10px;
                background: var(--gb-light, #8bac0f);
            }

            .battle-matchup-creature {
                text-align: center;
                font-size: 12px;
                font-weight: bold;
            }

            .battle-matchup-vs {
                font-size: 16px;
                font-weight: bold;
                color: var(--gb-darkest, #0f380f);
            }

            .battle-matchup-winner {
                background: #4a9d00;
                color: #fff;
            }

            .battle-matchup-loser {
                opacity: 0.6;
            }

            .shared-moves-section {
                background: var(--gb-lightest, #9bbc0f);
                border: 2px solid var(--gb-darkest, #0f380f);
                padding: 10px;
                margin: 10px 0;
            }

            .shared-moves-list {
                display: flex;
                flex-wrap: wrap;
                gap: 5px;
                margin-top: 10px;
            }

            .move-badge {
                background: var(--gb-darkest, #0f380f);
                color: var(--gb-lightest, #9bbc0f);
                padding: 5px 10px;
                font-size: 10px;
            }

            .comparison-totals {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
                gap: 10px;
                margin: 15px 0;
            }

            .total-stat-card {
                background: var(--gb-lightest, #9bbc0f);
                border: 2px solid var(--gb-darkest, #0f380f);
                padding: 10px;
                text-align: center;
            }

            .total-stat-card.best {
                border-color: #4a9d00;
                border-width: 3px;
            }

            .total-stat-value {
                font-size: 20px;
                font-weight: bold;
                color: var(--gb-darkest, #0f380f);
            }

            .total-stat-label {
                font-size: 10px;
                margin-top: 5px;
            }

            @media (max-width: 768px) {
                .comparison-panel {
                    width: 100%;
                    right: -100%;
                }

                .comparison-grid {
                    grid-template-columns: 1fr;
                }
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Attach event listeners to comparison controls
     */
    attachEventListeners() {
        document.getElementById('comparison-toggle').addEventListener('click', () => {
            this.togglePanel();
        });

        document.getElementById('comparison-clear').addEventListener('click', () => {
            this.clearAll();
        });

        document.getElementById('comparison-share').addEventListener('click', () => {
            this.shareComparison();
        });

        document.getElementById('comparison-export').addEventListener('click', () => {
            this.exportAsImage();
        });

        document.getElementById('comparison-close').addEventListener('click', () => {
            this.togglePanel();
        });
    }

    /**
     * Add a creature to the comparison list
     * @param {string|object} creatureIdOrInstance - Creature ID or instance
     */
    addToComparison(creatureIdOrInstance) {
        let creatureId;

        // Handle both creature ID strings and creature instances
        if (typeof creatureIdOrInstance === 'string') {
            creatureId = creatureIdOrInstance;
        } else if (creatureIdOrInstance && creatureIdOrInstance.id) {
            creatureId = creatureIdOrInstance.id;
        } else {
            console.error('Invalid creature reference');
            return false;
        }

        // Check if already in comparison
        if (this.comparisonList.includes(creatureId)) {
            console.log('Creature already in comparison');
            return false;
        }

        // Check max limit
        if (this.comparisonList.length >= this.maxComparisons) {
            alert(`Maximum ${this.maxComparisons} creatures can be compared at once`);
            return false;
        }

        // Verify creature exists in cartridge
        if (!this.gameEngine.cartridge || !this.gameEngine.cartridge.creatures[creatureId]) {
            console.error('Creature not found in cartridge');
            return false;
        }

        this.comparisonList.push(creatureId);
        this.updateComparisonView();
        this.updateToggleButton();

        // Announce for screen readers
        this.announce(`${this.gameEngine.cartridge.creatures[creatureId].name} added to comparison`);

        return true;
    }

    /**
     * Remove a creature from comparison
     * @param {string} creatureId - Creature ID to remove
     */
    removeFromComparison(creatureId) {
        const index = this.comparisonList.indexOf(creatureId);
        if (index > -1) {
            const creatureName = this.gameEngine.cartridge.creatures[creatureId].name;
            this.comparisonList.splice(index, 1);
            this.updateComparisonView();
            this.updateToggleButton();
            this.announce(`${creatureName} removed from comparison`);
        }
    }

    /**
     * Clear all comparisons
     */
    clearAll() {
        this.comparisonList = [];
        this.updateComparisonView();
        this.updateToggleButton();
        this.announce('All comparisons cleared');
    }

    /**
     * Toggle the comparison panel visibility
     */
    togglePanel() {
        this.comparisonPanel.classList.toggle('active');
        const isActive = this.comparisonPanel.classList.contains('active');
        this.announce(isActive ? 'Comparison panel opened' : 'Comparison panel closed');
    }

    /**
     * Update the toggle button text
     */
    updateToggleButton() {
        const btn = document.getElementById('comparison-toggle');
        btn.textContent = `Compare (${this.comparisonList.length})`;
    }

    /**
     * Render the comparison view
     */
    renderComparisonView() {
        const content = document.getElementById('comparison-content');

        if (this.comparisonList.length === 0) {
            content.innerHTML = `
                <div class="comparison-empty">
                    <p>Select creatures to compare (2-4 recommended)</p>
                    <p>Use the "Add to Compare" button from creature details</p>
                </div>
            `;
            return;
        }

        const creatures = this.comparisonList.map(id => {
            const base = this.gameEngine.cartridge.creatures[id];
            // Create a level 50 instance for fair comparison
            return this.createComparisonCreature(base, 50);
        });

        let html = '';

        // Individual creature cards
        html += '<div class="comparison-grid">';
        creatures.forEach((creature, index) => {
            html += this.renderCreatureCard(creature, this.comparisonList[index]);
        });
        html += '</div>';

        // Base stat totals comparison
        html += '<div class="comparison-section">';
        html += '<h3>Base Stat Totals</h3>';
        html += this.renderStatTotals(creatures);
        html += '</div>';

        // Side-by-side stat comparison
        html += '<div class="comparison-section">';
        html += '<h3>Stat Comparison (Level 50)</h3>';
        html += this.renderStatComparison(creatures);
        html += '</div>';

        // Radar chart
        html += '<div class="comparison-section">';
        html += '<h3>Stat Radar Chart</h3>';
        html += '<div id="radar-chart-container" class="radar-chart-container"></div>';
        html += '</div>';

        // Type effectiveness
        if (creatures.length >= 2) {
            html += '<div class="comparison-section">';
            html += '<h3>Type Effectiveness</h3>';
            html += this.renderTypeEffectiveness(creatures);
            html += '</div>';

            // Battle predictions
            html += '<div class="comparison-section">';
            html += '<h3>Battle Predictions</h3>';
            html += this.renderBattlePredictions(creatures);
            html += '</div>';
        }

        // Shared moves
        if (creatures.length >= 2) {
            html += '<div class="comparison-section">';
            html += '<h3>Move Pool Analysis</h3>';
            html += this.renderMovePoolAnalysis(creatures);
            html += '</div>';
        }

        content.innerHTML = html;

        // Draw radar chart after DOM is updated
        if (creatures.length >= 2) {
            setTimeout(() => this.drawComparativeRadarChart(creatures), 100);
        }
    }

    /**
     * Create a creature instance for comparison at a specific level
     */
    createComparisonCreature(baseCreature, level) {
        return {
            id: baseCreature.id,
            name: baseCreature.name,
            type: baseCreature.type,
            level: level,
            hp: this.calculateStat(baseCreature.baseHp, level),
            maxHp: this.calculateStat(baseCreature.baseHp, level),
            attack: this.calculateStat(baseCreature.baseAttack, level),
            defense: this.calculateStat(baseCreature.baseDefense, level),
            speed: this.calculateStat(baseCreature.baseSpeed, level),
            baseHp: baseCreature.baseHp,
            baseAttack: baseCreature.baseAttack,
            baseDefense: baseCreature.baseDefense,
            baseSpeed: baseCreature.baseSpeed,
            moves: baseCreature.moves,
            evolveLevel: baseCreature.evolveLevel,
            evolveTo: baseCreature.evolveTo,
            description: baseCreature.description
        };
    }

    /**
     * Calculate stat at a given level (simplified Pokemon formula)
     */
    calculateStat(baseStat, level) {
        return Math.floor(((2 * baseStat * level) / 100) + 5);
    }

    /**
     * Render an individual creature card
     */
    renderCreatureCard(creature, creatureId) {
        const baseTotal = creature.baseHp + creature.baseAttack + creature.baseDefense + creature.baseSpeed;

        return `
            <div class="creature-card">
                <div class="creature-card-header">
                    <h3>${creature.name}</h3>
                    <button class="creature-remove-btn" onclick="comparisonTool.removeFromComparison('${creatureId}')">
                        Remove
                    </button>
                </div>
                <div class="creature-type-badges">
                    ${creature.type.map(t => `<span class="type-badge">${t}</span>`).join('')}
                </div>
                <div class="stat-comparison">
                    <div class="stat-row">
                        <span class="stat-name">HP</span>
                        <span class="stat-value">${creature.hp}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-name">Attack</span>
                        <span class="stat-value">${creature.attack}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-name">Defense</span>
                        <span class="stat-value">${creature.defense}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-name">Speed</span>
                        <span class="stat-value">${creature.speed}</span>
                    </div>
                </div>
                <div style="margin-top: 10px; padding-top: 10px; border-top: 2px solid var(--gb-darkest);">
                    <strong>BST:</strong> ${baseTotal}<br>
                    <strong>Stage:</strong> ${this.getEvolutionStage(creature)}
                </div>
                <div style="margin-top: 10px; font-size: 10px; line-height: 1.4;">
                    ${creature.description}
                </div>
            </div>
        `;
    }

    /**
     * Get evolution stage of a creature
     */
    getEvolutionStage(creature) {
        let stage = 1;
        let currentId = creature.id;
        const creatures = this.gameEngine.cartridge.creatures;

        // Count backwards through pre-evolutions
        Object.values(creatures).forEach(c => {
            if (c.evolveTo === currentId) {
                stage++;
                currentId = c.id;
            }
        });

        // Count forwards through evolutions
        let nextEvo = creature.evolveTo;
        while (nextEvo) {
            const next = creatures[nextEvo];
            if (next && next.evolveTo) {
                nextEvo = next.evolveTo;
            } else {
                break;
            }
        }

        return `Stage ${stage}`;
    }

    /**
     * Render stat totals comparison
     */
    renderStatTotals(creatures) {
        const totals = creatures.map(c => ({
            name: c.name,
            total: c.baseHp + c.baseAttack + c.baseDefense + c.baseSpeed
        }));

        const maxTotal = Math.max(...totals.map(t => t.total));

        let html = '<div class="comparison-totals">';
        totals.forEach(t => {
            const isBest = t.total === maxTotal;
            html += `
                <div class="total-stat-card ${isBest ? 'best' : ''}">
                    <div class="total-stat-value">${t.total}</div>
                    <div class="total-stat-label">${t.name}</div>
                    ${isBest ? '<div style="font-size: 10px; color: #4a9d00;">★ HIGHEST</div>' : ''}
                </div>
            `;
        });
        html += '</div>';

        return html;
    }

    /**
     * Render side-by-side stat comparison with bars
     */
    renderStatComparison(creatures) {
        const stats = ['hp', 'attack', 'defense', 'speed'];
        const statLabels = { hp: 'HP', attack: 'Attack', defense: 'Defense', speed: 'Speed' };

        let html = '';

        stats.forEach(stat => {
            const values = creatures.map(c => c[stat]);
            const maxValue = Math.max(...values);
            const maxOverall = 200; // Max stat value for scaling

            html += `<div class="stat-row" style="margin: 15px 0;">`;
            html += `<div class="stat-name">${statLabels[stat]}</div>`;
            html += `<div style="flex: 1; display: grid; grid-template-columns: repeat(${creatures.length}, 1fr); gap: 5px;">`;

            creatures.forEach((creature, index) => {
                const value = creature[stat];
                const percentage = (value / maxOverall) * 100;
                const isBest = value === maxValue;

                html += `
                    <div style="text-align: center;">
                        <div class="stat-bar-container">
                            <div class="stat-bar ${isBest ? 'best' : ''}" style="width: ${percentage}%"></div>
                        </div>
                        <div class="stat-value" style="width: auto; margin-top: 3px; font-size: 10px;">
                            ${value} ${isBest ? '★' : ''}
                        </div>
                    </div>
                `;
            });

            html += `</div>`;
            html += `</div>`;
        });

        return html;
    }

    /**
     * Draw a comparative radar chart showing all creatures
     */
    drawComparativeRadarChart(creatures) {
        const container = document.getElementById('radar-chart-container');
        if (!container) return;

        const canvas = document.createElement('canvas');
        canvas.width = container.clientWidth;
        canvas.height = 280;
        container.innerHTML = '';
        container.appendChild(canvas);

        const ctx = canvas.getContext('2d');
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const radius = Math.min(centerX, centerY) - 40;

        const stats = ['HP', 'Attack', 'Defense', 'Speed'];
        const angles = stats.map((_, i) => (Math.PI * 2 * i) / stats.length - Math.PI / 2);

        // Colors for each creature
        const colors = [
            '#306230',
            '#8b0000',
            '#00008b',
            '#8b8b00'
        ];

        // Draw background grid
        ctx.strokeStyle = '#0f380f';
        ctx.lineWidth = 1;

        for (let i = 1; i <= 5; i++) {
            const r = (radius / 5) * i;
            ctx.beginPath();
            angles.forEach((angle, idx) => {
                const x = centerX + r * Math.cos(angle);
                const y = centerY + r * Math.sin(angle);
                if (idx === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            });
            ctx.closePath();
            ctx.stroke();
        }

        // Draw axes
        angles.forEach((angle, idx) => {
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            const x = centerX + radius * Math.cos(angle);
            const y = centerY + radius * Math.sin(angle);
            ctx.lineTo(x, y);
            ctx.stroke();

            // Draw labels
            const labelX = centerX + (radius + 25) * Math.cos(angle);
            const labelY = centerY + (radius + 25) * Math.sin(angle);
            ctx.fillStyle = '#0f380f';
            ctx.font = 'bold 12px monospace';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(stats[idx], labelX, labelY);
        });

        // Draw each creature's stats
        creatures.forEach((creature, creatureIdx) => {
            const statValues = [
                creature.baseHp,
                creature.baseAttack,
                creature.baseDefense,
                creature.baseSpeed
            ];

            const maxStat = 120; // Normalize to this value
            const points = statValues.map((value, idx) => {
                const normalized = Math.min(value / maxStat, 1);
                const r = radius * normalized;
                return {
                    x: centerX + r * Math.cos(angles[idx]),
                    y: centerY + r * Math.sin(angles[idx])
                };
            });

            // Fill
            ctx.fillStyle = colors[creatureIdx] + '40'; // 40 = 25% opacity
            ctx.beginPath();
            points.forEach((point, idx) => {
                if (idx === 0) ctx.moveTo(point.x, point.y);
                else ctx.lineTo(point.x, point.y);
            });
            ctx.closePath();
            ctx.fill();

            // Stroke
            ctx.strokeStyle = colors[creatureIdx];
            ctx.lineWidth = 2;
            ctx.stroke();
        });

        // Draw legend
        const legendY = 10;
        creatures.forEach((creature, idx) => {
            ctx.fillStyle = colors[idx];
            ctx.fillRect(10, legendY + idx * 20, 15, 15);
            ctx.fillStyle = '#0f380f';
            ctx.font = 'bold 11px monospace';
            ctx.textAlign = 'left';
            ctx.fillText(creature.name, 30, legendY + idx * 20 + 11);
        });
    }

    /**
     * Render type effectiveness between creatures
     */
    renderTypeEffectiveness(creatures) {
        let html = '<div class="type-effectiveness-grid">';

        for (let i = 0; i < creatures.length; i++) {
            for (let j = i + 1; j < creatures.length; j++) {
                const c1 = creatures[i];
                const c2 = creatures[j];

                html += `<div class="effectiveness-card">`;
                html += `<h4>${c1.name} vs ${c2.name}</h4>`;

                // Calculate type effectiveness both ways
                const c1vsC2 = this.calculateTypeEffectiveness(c1.type, c2.type);
                const c2vsC1 = this.calculateTypeEffectiveness(c2.type, c1.type);

                html += `<div class="effectiveness-vs">`;
                html += `${c1.name} attacking: `;
                html += `<span class="effectiveness-multiplier ${this.getEffectivenessClass(c1vsC2)}">`;
                html += `${c1vsC2}x`;
                html += `</span>`;
                html += `</div>`;

                html += `<div class="effectiveness-vs">`;
                html += `${c2.name} attacking: `;
                html += `<span class="effectiveness-multiplier ${this.getEffectivenessClass(c2vsC1)}">`;
                html += `${c2vsC1}x`;
                html += `</span>`;
                html += `</div>`;

                html += `</div>`;
            }
        }

        html += '</div>';
        return html;
    }

    /**
     * Calculate type effectiveness multiplier
     */
    calculateTypeEffectiveness(attackerTypes, defenderTypes) {
        // Simplified type chart for WoWmon types
        const typeChart = {
            water: { fire: 2, earth: 2, water: 0.5, nature: 0.5 },
            fire: { nature: 2, ice: 2, water: 0.5, earth: 0.5, fire: 0.5 },
            nature: { water: 2, earth: 2, fire: 0.5, beast: 0.5 },
            earth: { fire: 2, electric: 2, nature: 0.5, water: 0.5 },
            electric: { water: 2, shadow: 0.5, earth: 0 },
            ice: { nature: 2, beast: 2, water: 0.5, fire: 0.5 },
            beast: { normal: 2, magic: 0.5, demon: 0.5 },
            shadow: { magic: 2, spirit: 2, normal: 0.5 },
            magic: { beast: 2, demon: 2, magic: 0.5 },
            demon: { spirit: 2, nature: 2, magic: 0.5 },
            spirit: { shadow: 2, demon: 2, normal: 0.5 },
            undead: { nature: 2, shadow: 0.5, spirit: 0.5 },
            dragon: { dragon: 2, ice: 0.5 },
            metal: { earth: 2, fire: 0.5, water: 0.5 }
        };

        let multiplier = 1;

        attackerTypes.forEach(atkType => {
            defenderTypes.forEach(defType => {
                if (typeChart[atkType] && typeChart[atkType][defType] !== undefined) {
                    multiplier *= typeChart[atkType][defType];
                }
            });
        });

        return multiplier;
    }

    /**
     * Get CSS class for effectiveness display
     */
    getEffectivenessClass(multiplier) {
        if (multiplier > 1) return 'super-effective';
        if (multiplier < 1) return 'not-very-effective';
        return 'neutral';
    }

    /**
     * Render battle prediction analysis
     */
    renderBattlePredictions(creatures) {
        let html = '';

        for (let i = 0; i < creatures.length; i++) {
            for (let j = i + 1; j < creatures.length; j++) {
                const result = this.simulateBattle(creatures[i], creatures[j]);

                html += `<div class="battle-prediction">`;
                html += `<h4>Battle Simulation</h4>`;
                html += `<div class="battle-matchup">`;
                html += `<div class="battle-matchup-creature ${result.winner === 0 ? 'battle-matchup-winner' : 'battle-matchup-loser'}">`;
                html += `${creatures[i].name}`;
                html += `</div>`;
                html += `<div class="battle-matchup-vs">VS</div>`;
                html += `<div class="battle-matchup-creature ${result.winner === 1 ? 'battle-matchup-winner' : 'battle-matchup-loser'}">`;
                html += `${creatures[j].name}`;
                html += `</div>`;
                html += `</div>`;
                html += `<div style="font-size: 11px; line-height: 1.6;">`;
                html += `<strong>Predicted Winner:</strong> ${result.winnerName}<br>`;
                html += `<strong>Reason:</strong> ${result.reason}<br>`;
                html += `<strong>Type Advantage:</strong> ${result.typeAdvantage}<br>`;
                html += `<strong>Key Factors:</strong> ${result.keyFactors.join(', ')}`;
                html += `</div>`;
                html += `</div>`;
            }
        }

        return html;
    }

    /**
     * Simulate a basic battle between two creatures
     */
    simulateBattle(creature1, creature2) {
        const typeEff1 = this.calculateTypeEffectiveness(creature1.type, creature2.type);
        const typeEff2 = this.calculateTypeEffectiveness(creature2.type, creature1.type);

        // Calculate damage potential
        const damage1 = creature1.attack * typeEff1;
        const damage2 = creature2.attack * typeEff2;

        // Calculate survivability
        const survival1 = creature1.hp * creature1.defense;
        const survival2 = creature2.hp * creature2.defense;

        // Calculate overall battle score
        const score1 = damage1 + survival1 + creature1.speed * 0.5;
        const score2 = damage2 + survival2 + creature2.speed * 0.5;

        const winner = score1 > score2 ? 0 : 1;
        const winnerCreature = winner === 0 ? creature1 : creature2;
        const loserCreature = winner === 0 ? creature2 : creature1;

        const keyFactors = [];
        if (Math.abs(typeEff1 - typeEff2) > 0.5) {
            keyFactors.push('Type advantage');
        }
        if (Math.abs(creature1.speed - creature2.speed) > 20) {
            keyFactors.push('Speed advantage');
        }
        if (Math.abs(creature1.attack - creature2.attack) > 15) {
            keyFactors.push('Attack power');
        }
        if (Math.abs(creature1.defense - creature2.defense) > 15) {
            keyFactors.push('Defense');
        }
        if (keyFactors.length === 0) {
            keyFactors.push('Balanced matchup');
        }

        let typeAdvantageText;
        if (typeEff1 > typeEff2) {
            typeAdvantageText = `${creature1.name} has type advantage (${typeEff1}x vs ${typeEff2}x)`;
        } else if (typeEff2 > typeEff1) {
            typeAdvantageText = `${creature2.name} has type advantage (${typeEff2}x vs ${typeEff1}x)`;
        } else {
            typeAdvantageText = 'No significant type advantage';
        }

        return {
            winner: winner,
            winnerName: winnerCreature.name,
            reason: `Higher overall battle score (${Math.round(winner === 0 ? score1 : score2)} vs ${Math.round(winner === 0 ? score2 : score1)})`,
            typeAdvantage: typeAdvantageText,
            keyFactors: keyFactors
        };
    }

    /**
     * Render move pool overlap analysis
     */
    renderMovePoolAnalysis(creatures) {
        let html = '';

        // Find shared moves between all creatures
        const allMoves = creatures[0].moves || [];
        const sharedMoves = allMoves.filter(move =>
            creatures.every(c => (c.moves || []).includes(move))
        );

        html += `<div class="shared-moves-section">`;
        html += `<h4>Shared Moves (${sharedMoves.length})</h4>`;
        if (sharedMoves.length > 0) {
            html += `<div class="shared-moves-list">`;
            sharedMoves.forEach(moveId => {
                const move = this.gameEngine.cartridge.moves[moveId];
                if (move) {
                    html += `<span class="move-badge">${move.name}</span>`;
                }
            });
            html += `</div>`;
        } else {
            html += `<p style="font-size: 11px; margin-top: 10px;">No moves in common</p>`;
        }
        html += `</div>`;

        // Show unique moves for each
        html += `<div style="margin-top: 15px;">`;
        html += `<h4 style="margin-bottom: 10px;">Unique Moves</h4>`;
        creatures.forEach(creature => {
            const uniqueMoves = (creature.moves || []).filter(move =>
                !sharedMoves.includes(move)
            );

            html += `<div class="shared-moves-section" style="margin-bottom: 10px;">`;
            html += `<strong>${creature.name}:</strong> ${uniqueMoves.length} unique`;
            if (uniqueMoves.length > 0) {
                html += `<div class="shared-moves-list" style="margin-top: 5px;">`;
                uniqueMoves.forEach(moveId => {
                    const move = this.gameEngine.cartridge.moves[moveId];
                    if (move) {
                        html += `<span class="move-badge">${move.name}</span>`;
                    }
                });
                html += `</div>`;
            }
            html += `</div>`;
        });
        html += `</div>`;

        return html;
    }

    /**
     * Update the comparison view
     */
    updateComparisonView() {
        this.renderComparisonView();
        this.updateURL();
    }

    /**
     * Share the comparison via URL
     */
    shareComparison() {
        const url = this.getComparisonURL();

        if (navigator.clipboard) {
            navigator.clipboard.writeText(url).then(() => {
                alert('Comparison URL copied to clipboard!');
            }).catch(() => {
                this.showShareDialog(url);
            });
        } else {
            this.showShareDialog(url);
        }
    }

    /**
     * Show share dialog with URL
     */
    showShareDialog(url) {
        const dialog = prompt('Share this URL:', url);
    }

    /**
     * Get shareable URL with comparison data
     */
    getComparisonURL() {
        const baseURL = window.location.origin + window.location.pathname;
        const params = new URLSearchParams();
        params.set('compare', this.comparisonList.join(','));
        return `${baseURL}?${params.toString()}`;
    }

    /**
     * Update URL with current comparison
     */
    updateURL() {
        if (this.comparisonList.length > 0) {
            const params = new URLSearchParams(window.location.search);
            params.set('compare', this.comparisonList.join(','));
            const newURL = `${window.location.pathname}?${params.toString()}`;
            window.history.replaceState({}, '', newURL);
        } else {
            // Remove compare parameter
            const params = new URLSearchParams(window.location.search);
            params.delete('compare');
            const newURL = params.toString() ?
                `${window.location.pathname}?${params.toString()}` :
                window.location.pathname;
            window.history.replaceState({}, '', newURL);
        }
    }

    /**
     * Load comparison from URL parameters
     */
    loadFromURL() {
        const params = new URLSearchParams(window.location.search);
        const compareParam = params.get('compare');

        if (compareParam) {
            const ids = compareParam.split(',').filter(id => id.trim());
            ids.forEach(id => {
                if (this.gameEngine.cartridge && this.gameEngine.cartridge.creatures[id]) {
                    this.addToComparison(id);
                }
            });

            if (this.comparisonList.length > 0) {
                this.togglePanel();
            }
        }
    }

    /**
     * Export comparison as image (basic implementation)
     */
    exportAsImage() {
        alert('Export feature: Use your browser\'s screenshot tool or print to PDF functionality to save this comparison.');
        // In a full implementation, this would use html2canvas or similar library
        // to render the comparison-content div as an image
    }

    /**
     * Announce message for screen readers
     */
    announce(message) {
        const liveRegion = document.querySelector('.live-region');
        if (liveRegion) {
            liveRegion.textContent = message;
            setTimeout(() => {
                liveRegion.textContent = '';
            }, 1000);
        }
    }

    /**
     * Compare two creatures and return detailed comparison object
     * @param {object} creature1 - First creature
     * @param {object} creature2 - Second creature
     * @returns {object} Comparison results
     */
    compareStats(creature1, creature2) {
        const comparison = {
            hp: {
                c1: creature1.hp,
                c2: creature2.hp,
                winner: creature1.hp > creature2.hp ? creature1.name : creature2.name,
                difference: Math.abs(creature1.hp - creature2.hp)
            },
            attack: {
                c1: creature1.attack,
                c2: creature2.attack,
                winner: creature1.attack > creature2.attack ? creature1.name : creature2.name,
                difference: Math.abs(creature1.attack - creature2.attack)
            },
            defense: {
                c1: creature1.defense,
                c2: creature2.defense,
                winner: creature1.defense > creature2.defense ? creature1.name : creature2.name,
                difference: Math.abs(creature1.defense - creature2.defense)
            },
            speed: {
                c1: creature1.speed,
                c2: creature2.speed,
                winner: creature1.speed > creature2.speed ? creature1.name : creature2.name,
                difference: Math.abs(creature1.speed - creature2.speed)
            },
            total: {
                c1: creature1.hp + creature1.attack + creature1.defense + creature1.speed,
                c2: creature2.hp + creature2.attack + creature2.defense + creature2.speed
            }
        };

        comparison.total.winner = comparison.total.c1 > comparison.total.c2 ?
            creature1.name : creature2.name;
        comparison.total.difference = Math.abs(comparison.total.c1 - comparison.total.c2);

        return comparison;
    }
}

// HTML structure for integration into WowMon game
const COMPARISON_HTML_STRUCTURE = `
<!-- Add this button to creature detail views -->
<button class="comparison-add-btn" onclick="comparisonTool.addToComparison(currentCreatureId)">
    Add to Compare
</button>

<!-- The comparison panel is automatically created by the WowMonComparisonTool constructor -->
`;

// Export for use in WowMon
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { WowMonComparisonTool, COMPARISON_HTML_STRUCTURE };
}

// Auto-initialize if gameEngine exists
if (typeof window !== 'undefined') {
    window.WowMonComparisonTool = WowMonComparisonTool;
}
