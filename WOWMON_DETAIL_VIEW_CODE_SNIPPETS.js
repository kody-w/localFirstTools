/**
 * ============================================================================
 * WOWMON DETAIL VIEW SYSTEM - CODE SNIPPETS FOR INTEGRATION
 * ============================================================================
 *
 * Agent 4 - Detail View Specialist Deliverable
 *
 * This file contains all the JavaScript functions needed to integrate
 * the Pokemon detail view system into wowMon.html
 *
 * INTEGRATION STEPS:
 * 1. Copy the CSS from wowMon_detail_view.html to your wowMon.html <style> section
 * 2. Copy the HTML modal structure to your wowMon.html before </body>
 * 3. Copy all functions below to your wowMon.html <script> section
 * 4. Update data references (MOCK_CREATURES -> game.cartridge.creatures)
 * 5. Call showPokemonDetail(pokemonId) from your game to open the detail view
 *
 * ============================================================================
 */

// ============================================================================
// STATE MANAGEMENT
// ============================================================================

let currentPokemonId = null;
let allPokemonIds = []; // Will be populated from game.cartridge.creatures
let favorites = JSON.parse(localStorage.getItem('wowmon_favorites') || '[]');

// Initialize Pokemon IDs list (call this after cartridge is loaded)
function initializePokemonDetailView() {
    if (game && game.cartridge && game.cartridge.creatures) {
        allPokemonIds = Object.keys(game.cartridge.creatures);
        console.log('Pokemon Detail View initialized with', allPokemonIds.length, 'creatures');
    }
}

// ============================================================================
// MAIN FUNCTIONS
// ============================================================================

/**
 * Main function to show Pokemon detail view
 * @param {string} pokemonId - The ID of the Pokemon to display
 */
function showPokemonDetail(pokemonId) {
    const pokemon = game.cartridge.creatures[pokemonId]; // Update this reference

    if (!pokemon) {
        console.error('Pokemon not found:', pokemonId);
        return;
    }

    currentPokemonId = pokemonId;

    // Update header
    document.getElementById('detailPokemonName').textContent = pokemon.name;
    const pokemonIndex = allPokemonIds.indexOf(pokemonId) + 1;
    document.getElementById('detailPokemonNumber').textContent = `#${String(pokemonIndex).padStart(3, '0')}`;

    // Update favorite button
    const favoriteBtn = document.getElementById('favoriteBtn');
    if (favorites.includes(pokemonId)) {
        favoriteBtn.classList.add('active');
    } else {
        favoriteBtn.classList.remove('active');
    }

    // Populate all tabs
    populateOverviewTab(pokemon);
    populateStatsTab(pokemon);
    populateMovesTab(pokemon);
    populateEvolutionTab(pokemon);
    populateAbilitiesTab(pokemon);

    // Show modal
    document.getElementById('pokemonDetailModal').classList.add('active');

    // Reset to overview tab
    switchTab('overview');
}

/**
 * Close the Pokemon detail modal
 */
function closePokemonDetail() {
    document.getElementById('pokemonDetailModal').classList.remove('active');
    currentPokemonId = null;
}

/**
 * Switch between tabs
 * @param {string} tabName - Name of the tab to switch to
 */
function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');

    // Update tab panes
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.remove('active');
    });
    document.getElementById(`${tabName}-tab`).classList.add('active');

    // If switching to stats tab, redraw radar chart
    if (tabName === 'stats' && currentPokemonId) {
        const pokemon = game.cartridge.creatures[currentPokemonId];
        setTimeout(() => drawStatsRadarChart(pokemon), 100);
    }
}

// ============================================================================
// TAB POPULATION FUNCTIONS
// ============================================================================

/**
 * Populate the overview tab
 */
function populateOverviewTab(pokemon) {
    // Sprite (using emoji or text placeholder)
    const spriteElement = document.getElementById('detailSprite');
    const spriteEmojis = {
        'murloc': '🐟', 'murloc_warrior': '🔱', 'murloc_king': '👑',
        'wolf': '🐺', 'dire_wolf': '🐺',
        'imp': '😈', 'felguard': '👹',
        'wisp': '✨', 'ancient_wisp': '🌟',
        'gnoll': '🐕', 'kobold': '⛏️',
        'treant': '🌳', 'naga': '🐍',
        'elemental': '💠'
    };
    spriteElement.textContent = spriteEmojis[pokemon.id] || pokemon.name.substring(0, 1);

    // Types
    const typesContainer = document.getElementById('detailTypes');
    typesContainer.innerHTML = pokemon.type.map(type =>
        `<span class="type-badge ${type}">${type}</span>`
    ).join('');

    // Height and weight (use real data or generate)
    document.getElementById('detailHeight').textContent = pokemon.height || `${Math.floor(Math.random() * 20 + 10) / 10}m`;
    document.getElementById('detailWeight').textContent = pokemon.weight || `${Math.floor(Math.random() * 100 + 20)}kg`;

    // Description
    document.getElementById('detailDescription').textContent = pokemon.description;
}

/**
 * Populate the stats tab with radar chart and stat bars
 */
function populateStatsTab(pokemon) {
    const stats = {
        hp: pokemon.baseHp || 50,
        attack: pokemon.baseAttack || 50,
        defense: pokemon.baseDefense || 50,
        spAttack: pokemon.baseSpAttack || pokemon.baseAttack || 50,
        spDefense: pokemon.baseSpDefense || pokemon.baseDefense || 50,
        speed: pokemon.baseSpeed || 50
    };

    // Draw radar chart
    drawStatsRadarChart(pokemon);

    // Create stat bars
    const statsBarsList = document.getElementById('statsBarsList');
    const statNames = {
        hp: 'HP',
        attack: 'Attack',
        defense: 'Defense',
        spAttack: 'Sp. Atk',
        spDefense: 'Sp. Def',
        speed: 'Speed'
    };

    let bst = 0;
    let html = '';

    for (const [key, label] of Object.entries(statNames)) {
        const value = stats[key];
        bst += value;
        const percentage = (value / 150) * 100; // Max stat assumed to be 150

        let colorClass = 'low';
        if (value >= 100) colorClass = 'excellent';
        else if (value >= 80) colorClass = 'good';
        else if (value >= 60) colorClass = 'average';

        html += `
            <div class="stat-row">
                <div class="stat-name">
                    <span>${label}</span>
                    <span>${value}</span>
                </div>
                <div class="stat-bar">
                    <div class="stat-bar-fill ${colorClass}" style="width: ${percentage}%"></div>
                </div>
            </div>
        `;
    }

    statsBarsList.innerHTML = html;

    // Update BST
    const percentile = Math.floor((bst / 600) * 100);
    document.getElementById('baseStatTotal').innerHTML = `Base Stat Total: ${bst}<br><small style="font-size: 14px;">Top ${100 - percentile}% of all Pokemon</small>`;
}

/**
 * Draw the stats radar chart on canvas
 */
function drawStatsRadarChart(pokemon) {
    const canvas = document.getElementById('statsRadarCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = 120;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Stats data
    const stats = [
        { label: 'HP', value: pokemon.baseHp || 50 },
        { label: 'Attack', value: pokemon.baseAttack || 50 },
        { label: 'Defense', value: pokemon.baseDefense || 50 },
        { label: 'Sp.Atk', value: pokemon.baseSpAttack || pokemon.baseAttack || 50 },
        { label: 'Sp.Def', value: pokemon.baseSpDefense || pokemon.baseDefense || 50 },
        { label: 'Speed', value: pokemon.baseSpeed || 50 }
    ];

    const maxStat = 150; // Maximum stat value for scaling
    const numStats = stats.length;
    const angleStep = (Math.PI * 2) / numStats;

    // Draw grid circles
    ctx.strokeStyle = 'rgba(15, 56, 15, 0.2)';
    ctx.lineWidth = 1;
    for (let i = 1; i <= 5; i++) {
        ctx.beginPath();
        const r = (radius / 5) * i;
        for (let j = 0; j <= numStats; j++) {
            const angle = angleStep * j - Math.PI / 2;
            const x = centerX + Math.cos(angle) * r;
            const y = centerY + Math.sin(angle) * r;
            if (j === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.stroke();
    }

    // Draw axes
    ctx.strokeStyle = 'rgba(15, 56, 15, 0.3)';
    ctx.lineWidth = 1;
    for (let i = 0; i < numStats; i++) {
        const angle = angleStep * i - Math.PI / 2;
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(
            centerX + Math.cos(angle) * radius,
            centerY + Math.sin(angle) * radius
        );
        ctx.stroke();
    }

    // Draw stat polygon
    ctx.fillStyle = 'rgba(74, 90, 58, 0.5)';
    ctx.strokeStyle = '#0f380f';
    ctx.lineWidth = 3;
    ctx.beginPath();

    for (let i = 0; i <= numStats; i++) {
        const stat = stats[i % numStats];
        const angle = angleStep * i - Math.PI / 2;
        const value = (stat.value / maxStat) * radius;
        const x = centerX + Math.cos(angle) * value;
        const y = centerY + Math.sin(angle) * value;

        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    }

    ctx.closePath();
    ctx.fill();
    ctx.stroke();

    // Draw stat points
    ctx.fillStyle = '#0f380f';
    for (let i = 0; i < numStats; i++) {
        const stat = stats[i];
        const angle = angleStep * i - Math.PI / 2;
        const value = (stat.value / maxStat) * radius;
        const x = centerX + Math.cos(angle) * value;
        const y = centerY + Math.sin(angle) * value;

        ctx.beginPath();
        ctx.arc(x, y, 5, 0, Math.PI * 2);
        ctx.fill();
    }

    // Draw labels
    ctx.fillStyle = '#0f380f';
    ctx.font = 'bold 14px monospace';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    for (let i = 0; i < numStats; i++) {
        const stat = stats[i];
        const angle = angleStep * i - Math.PI / 2;
        const labelRadius = radius + 30;
        const x = centerX + Math.cos(angle) * labelRadius;
        const y = centerY + Math.sin(angle) * labelRadius;

        ctx.fillText(stat.label, x, y);
    }
}

/**
 * Populate the moves tab
 */
function populateMovesTab(pokemon) {
    const movesList = document.getElementById('movesList');
    let html = '';

    pokemon.moves.forEach(moveId => {
        const move = game.cartridge.moves[moveId]; // Update this reference

        if (!move) {
            console.warn('Move not found:', moveId);
            return;
        }

        html += `
            <div class="move-card">
                <div class="move-name">${move.name}</div>
                <div class="move-type type-badge ${move.type}">${move.type}</div>
                <div class="move-category">${move.category || 'physical'}</div>
                <div class="move-stat">PWR: ${move.power || '-'}</div>
                <div class="move-stat">ACC: ${move.accuracy || '-'}</div>
            </div>
        `;
    });

    movesList.innerHTML = html || '<p>No moves available.</p>';
}

/**
 * Filter moves based on search input
 */
function filterMoves() {
    const searchTerm = document.getElementById('movesSearch').value.toLowerCase();
    const moveCards = document.querySelectorAll('.move-card');

    moveCards.forEach(card => {
        const moveName = card.querySelector('.move-name').textContent.toLowerCase();
        if (moveName.includes(searchTerm)) {
            card.style.display = 'grid';
        } else {
            card.style.display = 'none';
        }
    });
}

/**
 * Populate the evolution tab with evolution chain
 */
function populateEvolutionTab(pokemon) {
    const evolutionChain = document.getElementById('evolutionChain');

    // Build evolution chain
    const chain = buildEvolutionChain(pokemon);

    if (chain.length <= 1) {
        evolutionChain.innerHTML = '<div class="no-evolution">This Pokemon does not evolve.</div>';
        return;
    }

    let html = '';

    chain.forEach((stage, index) => {
        const stageData = game.cartridge.creatures[stage.id]; // Update this reference
        const isCurrent = stage.id === currentPokemonId;

        const spriteEmojis = {
            'murloc': '🐟', 'murloc_warrior': '🔱', 'murloc_king': '👑',
            'wolf': '🐺', 'dire_wolf': '🐺',
            'imp': '😈', 'felguard': '👹',
            'wisp': '✨', 'ancient_wisp': '🌟',
            'gnoll': '🐕', 'kobold': '⛏️',
            'treant': '🌳', 'naga': '🐍',
            'elemental': '💠'
        };

        html += `
            <div class="evolution-stage">
                <div class="evolution-sprite ${isCurrent ? 'current' : ''}" onclick="showPokemonDetail('${stage.id}')">
                    <div style="font-size: 48px;">${spriteEmojis[stage.id] || stageData.name[0]}</div>
                    <div class="evolution-name">${stageData.name}</div>
                </div>
                ${stage.condition ? `<div class="evolution-condition">${stage.condition}</div>` : ''}
            </div>
        `;

        if (index < chain.length - 1) {
            html += '<div class="evolution-arrow">→</div>';
        }
    });

    evolutionChain.innerHTML = html;
}

/**
 * Build the complete evolution chain for a Pokemon
 */
function buildEvolutionChain(pokemon) {
    const chain = [];

    // Find the base form
    let currentId = pokemon.id;
    while (true) {
        const current = game.cartridge.creatures[currentId]; // Update this reference
        if (!current || !current.evolveFrom) break;
        currentId = current.evolveFrom;
    }

    // Build chain from base
    while (currentId) {
        const current = game.cartridge.creatures[currentId]; // Update this reference
        if (!current) break;

        let condition = '';
        if (current.evolveLevel) {
            condition = `Level ${current.evolveLevel}`;
        } else if (current.evolveStone) {
            condition = current.evolveStone;
        } else if (current.evolveMethod) {
            condition = current.evolveMethod;
        }

        chain.push({
            id: currentId,
            condition: condition
        });

        currentId = current.evolveTo;
    }

    return chain;
}

/**
 * Populate the abilities tab
 */
function populateAbilitiesTab(pokemon) {
    const abilitiesList = document.getElementById('abilitiesList');

    // If creature has abilities defined, use them
    if (pokemon.abilities && pokemon.abilities.length > 0) {
        let html = '';
        pokemon.abilities.forEach(ability => {
            html += `
                <div class="ability-card">
                    <div class="ability-header">
                        <div class="ability-name">${ability.name}</div>
                        <div class="ability-tag">${ability.type || 'Normal'} Ability</div>
                    </div>
                    <div class="ability-description">${ability.description}</div>
                </div>
            `;
        });
        abilitiesList.innerHTML = html;
        return;
    }

    // Otherwise, generate based on type
    const typeAbilities = {
        'water': [
            { name: 'Torrent', type: 'Normal', description: 'Powers up Water-type moves when the Pokemon\'s HP is low.' },
            { name: 'Swift Swim', type: 'Hidden', description: 'Boosts the Pokemon\'s Speed stat in rain.' }
        ],
        'fire': [
            { name: 'Blaze', type: 'Normal', description: 'Powers up Fire-type moves when the Pokemon\'s HP is low.' },
            { name: 'Flash Fire', type: 'Hidden', description: 'Powers up the Pokemon\'s Fire-type moves if it\'s hit by one.' }
        ],
        'nature': [
            { name: 'Overgrow', type: 'Normal', description: 'Powers up Nature-type moves when the Pokemon\'s HP is low.' },
            { name: 'Chlorophyll', type: 'Hidden', description: 'Boosts the Pokemon\'s Speed stat in harsh sunlight.' }
        ],
        'beast': [
            { name: 'Intimidate', type: 'Normal', description: 'Lowers opposing Pokemon\'s Attack stat when the Pokemon enters battle.' },
            { name: 'Guts', type: 'Hidden', description: 'Boosts Attack if the Pokemon has a status condition.' }
        ],
        'demon': [
            { name: 'Cursed Body', type: 'Normal', description: 'May disable a move used on the Pokemon.' },
            { name: 'Pressure', type: 'Hidden', description: 'The Pokemon raises opposing Pokemon\'s PP usage.' }
        ],
        'spirit': [
            { name: 'Levitate', type: 'Normal', description: 'Gives immunity to Ground-type moves.' },
            { name: 'Prankster', type: 'Hidden', description: 'Gives priority to status moves.' }
        ],
        'magic': [
            { name: 'Magic Guard', type: 'Normal', description: 'The Pokemon only takes damage from attacks.' },
            { name: 'Magic Bounce', type: 'Hidden', description: 'Reflects status moves instead of being hit by them.' }
        ],
        'shadow': [
            { name: 'Shadow Tag', type: 'Normal', description: 'Prevents opposing Pokemon from fleeing.' },
            { name: 'Infiltrator', type: 'Hidden', description: 'Passes through the opposing Pokemon\'s barriers and substitutes.' }
        ]
    };

    const primaryType = pokemon.type[0];
    const abilities = typeAbilities[primaryType] || [
        { name: 'Adaptability', type: 'Normal', description: 'Powers up moves of the same type as the Pokemon.' }
    ];

    let html = '';
    abilities.forEach(ability => {
        html += `
            <div class="ability-card">
                <div class="ability-header">
                    <div class="ability-name">${ability.name}</div>
                    <div class="ability-tag">${ability.type} Ability</div>
                </div>
                <div class="ability-description">${ability.description}</div>
            </div>
        `;
    });

    abilitiesList.innerHTML = html;
}

// ============================================================================
// NAVIGATION & ACTIONS
// ============================================================================

/**
 * Navigate to previous/next Pokemon
 */
function navigatePokemon(direction) {
    if (!currentPokemonId) return;

    const currentIndex = allPokemonIds.indexOf(currentPokemonId);
    let newIndex = currentIndex + direction;

    // Wrap around
    if (newIndex < 0) newIndex = allPokemonIds.length - 1;
    if (newIndex >= allPokemonIds.length) newIndex = 0;

    showPokemonDetail(allPokemonIds[newIndex]);
}

/**
 * Toggle favorite status for current Pokemon
 */
function toggleFavorite() {
    if (!currentPokemonId) return;

    const pokemon = game.cartridge.creatures[currentPokemonId];
    const favoriteBtn = document.getElementById('favoriteBtn');

    if (favorites.includes(currentPokemonId)) {
        favorites = favorites.filter(id => id !== currentPokemonId);
        favoriteBtn.classList.remove('active');
        alert(`${pokemon.name} removed from favorites!`);
    } else {
        favorites.push(currentPokemonId);
        favoriteBtn.classList.add('active');
        alert(`${pokemon.name} added to favorites!`);
    }

    localStorage.setItem('wowmon_favorites', JSON.stringify(favorites));
}

/**
 * Add Pokemon to team
 */
function addToTeam() {
    if (!currentPokemonId) return;

    const pokemon = game.cartridge.creatures[currentPokemonId];

    // Check if team is full
    if (game.player.creatures.length >= 6) {
        alert('Your team is full! (Maximum 6 creatures)');
        return;
    }

    // Create new creature instance
    const newCreature = {
        id: pokemon.id,
        name: pokemon.name,
        level: 5,
        hp: pokemon.baseHp,
        maxHp: pokemon.baseHp,
        attack: pokemon.baseAttack,
        defense: pokemon.baseDefense,
        speed: pokemon.baseSpeed,
        exp: 0,
        moves: pokemon.moves.slice(0, 4),
        pp: {}
    };

    // Initialize PP for each move
    pokemon.moves.slice(0, 4).forEach(moveId => {
        const move = game.cartridge.moves[moveId];
        if (move) {
            newCreature.pp[moveId] = move.pp;
        }
    });

    // Add to team
    game.player.creatures.push(newCreature);

    alert(`${pokemon.name} added to your team!`);
    console.log('Creature added to team:', newCreature);
}

/**
 * Share Pokemon (copy URL with ID)
 */
function sharePokemon() {
    if (!currentPokemonId) return;

    const pokemon = game.cartridge.creatures[currentPokemonId];
    const url = `${window.location.origin}${window.location.pathname}?pokemon=${currentPokemonId}`;

    // Copy to clipboard
    if (navigator.clipboard) {
        navigator.clipboard.writeText(url).then(() => {
            alert(`Share link copied to clipboard!\n\n${pokemon.name}\n${url}`);
        }).catch(err => {
            console.error('Failed to copy:', err);
            fallbackCopyToClipboard(url);
        });
    } else {
        fallbackCopyToClipboard(url);
    }
}

/**
 * Fallback clipboard copy for older browsers
 */
function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.top = '0';
    textArea.style.left = '0';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
        document.execCommand('copy');
        alert(`Share link copied to clipboard!\n${text}`);
    } catch (err) {
        console.error('Fallback copy failed:', err);
        alert(`Share link:\n${text}`);
    }

    document.body.removeChild(textArea);
}

// ============================================================================
// EVENT LISTENERS
// ============================================================================

// Close modal on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && document.getElementById('pokemonDetailModal').classList.contains('active')) {
        closePokemonDetail();
    }

    // Arrow navigation
    if (document.getElementById('pokemonDetailModal').classList.contains('active')) {
        if (e.key === 'ArrowLeft') {
            navigatePokemon(-1);
        } else if (e.key === 'ArrowRight') {
            navigatePokemon(1);
        }
    }
});

// Close modal on background click
document.getElementById('pokemonDetailModal')?.addEventListener('click', (e) => {
    if (e.target.id === 'pokemonDetailModal') {
        closePokemonDetail();
    }
});

// Check for Pokemon ID in URL on load
window.addEventListener('load', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const pokemonId = urlParams.get('pokemon');

    if (pokemonId) {
        // Wait for game to load
        const checkGame = setInterval(() => {
            if (game && game.cartridge && game.cartridge.creatures && game.cartridge.creatures[pokemonId]) {
                clearInterval(checkGame);
                initializePokemonDetailView();
                showPokemonDetail(pokemonId);
            }
        }, 100);
    }
});

// ============================================================================
// INITIALIZATION
// ============================================================================

console.log('Pokemon Detail View System loaded successfully!');
console.log('Call initializePokemonDetailView() after loading game cartridge.');
console.log('Available functions:');
console.log('  - showPokemonDetail(pokemonId)');
console.log('  - closePokemonDetail()');
console.log('  - switchTab(tabName)');
console.log('  - navigatePokemon(direction)');
console.log('  - toggleFavorite()');
console.log('  - addToTeam()');
console.log('  - sharePokemon()');

/**
 * ============================================================================
 * END OF POKEMON DETAIL VIEW SYSTEM
 * ============================================================================
 */
