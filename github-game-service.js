/**
 * GitHub Game Service
 * Fetches HTML games from GitHub repository and provides local game management
 *
 * @author LocalFirst Tools
 * @version 1.0.0
 */

'use strict';

// ===== GAME DATA MODEL =====
class Game {
    constructor(data) {
        this.id = data.id || '';
        this.name = data.name || 'Unknown Game';
        this.description = data.description || 'No description available';
        this.icon = data.icon || '🎮';
        this.category = data.category || 'arcade';
        this.url = data.url || '';
        this.size = data.size || '0 KB';
        this.isEmulated = data.isEmulated || false;
        this.isLocal = data.isLocal || false;
        this.code = data.code || null;
        this.author = data.author || 'Unknown';
        this.version = data.version || '1.0';
    }

    toJSON() {
        return {
            id: this.id,
            name: this.name,
            description: this.description,
            icon: this.icon,
            category: this.category,
            author: this.author,
            version: this.version,
            code: this.code,
            isLocal: true
        };
    }
}

// ===== GITHUB SERVICE =====
class GitHubService {
    /**
     * Fetch games from GitHub repository
     * @returns {Promise<Game[]>} Array of Game objects
     */
    static async fetchGames() {
        const owner = 'kody-w';
        const name = 'localFirstTools';
        const branch = 'main';
        const apiUrl = `https://api.github.com/repos/${owner}/${name}/contents?ref=${branch}`;

        try {
            const response = await fetch(apiUrl);
            if (!response.ok) {
                throw new Error(`GitHub API error: ${response.status} ${response.statusText}`);
            }

            const contents = await response.json();

            // Filter for HTML game files
            const gameFiles = contents.filter(item =>
                item.type === 'file' &&
                item.name.endsWith('.html') &&
                !item.name.includes('index') &&
                !item.name.includes('gallery') &&
                !item.name.includes('template') &&
                !item.name.includes('steamdeck')
            );

            return gameFiles.map(file => {
                const baseName = file.name.replace('.html', '');
                const gameInfo = GitHubService.getGameInfo(baseName);

                return new Game({
                    id: baseName,
                    name: gameInfo.name || GitHubService.formatName(baseName),
                    description: gameInfo.description,
                    icon: gameInfo.icon,
                    category: gameInfo.category,
                    url: file.download_url || `https://raw.githubusercontent.com/${owner}/${name}/${branch}/${file.name}`,
                    size: GitHubService.formatFileSize(file.size)
                });
            });
        } catch (error) {
            console.error('Error fetching games from GitHub:', error);
            // Return empty array as fallback
            return [];
        }
    }

    /**
     * Get game metadata from database of known games
     * @param {string} filename - The filename without extension
     * @returns {Object} Game metadata (icon, category, description, name)
     */
    static getGameInfo(filename) {
        const gameDatabase = {
            'snake': {
                icon: '🐍',
                category: 'arcade',
                description: 'The classic snake game - eat food and grow longer without hitting yourself!',
                name: 'Snake Classic'
            },
            'tetris': {
                icon: '🧱',
                category: 'puzzle',
                description: 'Stack falling blocks and clear lines in this timeless puzzle game',
                name: 'Tetris'
            },
            'breakout': {
                icon: '🎯',
                category: 'arcade',
                description: 'Break all the bricks with your paddle and ball. Classic brick-breaker action!',
                name: 'Breakout'
            },
            'pong': {
                icon: '🏓',
                category: 'arcade',
                description: 'The original tennis-like arcade game. Bounce the ball past your opponent!',
                name: 'Pong'
            },
            'space-invaders': {
                icon: '👾',
                category: 'action',
                description: 'Defend Earth from waves of alien invaders. Shoot them before they land!',
                name: 'Space Invaders'
            },
            'flappy': {
                icon: '🐦',
                category: 'arcade',
                description: 'Navigate through pipes in this addictive tap-to-flap game',
                name: 'Flappy Bird Clone'
            },
            'asteroids': {
                icon: '☄️',
                category: 'action',
                description: 'Destroy asteroids and survive in space. Classic vector-style shooter!',
                name: 'Asteroids'
            },
            'pacman': {
                icon: '👻',
                category: 'arcade',
                description: 'Eat all the dots and avoid the ghosts in this maze-chase classic',
                name: 'Pac-Man Clone'
            }
        };

        const lowerFilename = filename.toLowerCase();
        for (const [key, info] of Object.entries(gameDatabase)) {
            if (lowerFilename.includes(key)) {
                return info;
            }
        }

        // Default fallback
        return {
            icon: '🎮',
            category: 'arcade',
            description: 'An HTML game from the repository',
            name: null
        };
    }

    /**
     * Format filename to human-readable name
     * @param {string} baseName - Filename without extension
     * @returns {string} Formatted name
     */
    static formatName(baseName) {
        return baseName
            .replace(/[-_]/g, ' ')
            .replace(/\b\w/g, letter => letter.toUpperCase());
    }

    /**
     * Format file size from bytes to readable format
     * @param {number} bytes - File size in bytes
     * @returns {string} Formatted file size
     */
    static formatFileSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return Math.round(bytes / 1024) + ' KB';
        return Math.round(bytes / (1024 * 1024)) + ' MB';
    }
}

// ===== LOCAL GAME SERVICE =====
class LocalGameService {
    /**
     * Get built-in Tetris game
     * @returns {Game} Complete Tetris game as embedded HTML
     */
    static getBuiltInTetris() {
        return new Game({
            id: 'built-in-tetris',
            name: 'Tetris Classic',
            description: 'The classic block-stacking puzzle game. Stack the falling pieces and clear lines!',
            icon: '🧱',
            category: 'puzzle',
            author: 'Built-in',
            version: '1.0',
            isLocal: true,
            size: '8 KB',
            code: `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tetris Classic</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-family: 'Arial', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        #game {
            text-align: center;
            background: rgba(0, 0, 0, 0.3);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
        }

        h1 {
            font-size: 48px;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }

        canvas {
            border: 4px solid #fff;
            background: #000;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
            display: block;
            margin: 20px auto;
        }

        #score {
            font-size: 28px;
            margin: 15px 0;
            font-weight: bold;
        }

        #controls {
            margin-top: 20px;
            font-size: 14px;
            color: rgba(255, 255, 255, 0.8);
            line-height: 1.8;
        }

        .score-value {
            color: #ffd700;
        }
    </style>
</head>
<body>
    <div id="game">
        <h1>🧱 TETRIS</h1>
        <div id="score">Score: <span id="scoreValue" class="score-value">0</span></div>
        <canvas id="canvas"></canvas>
        <div id="controls">
            <strong>Controls:</strong><br>
            ← → Move Left/Right | ↓ Drop Faster | ↑ Rotate<br>
            Press SPACE to Pause/Resume
        </div>
    </div>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const COLS = 10;
        const ROWS = 20;
        const BLOCK_SIZE = 30;

        canvas.width = COLS * BLOCK_SIZE;
        canvas.height = ROWS * BLOCK_SIZE;

        let board = Array(ROWS).fill().map(() => Array(COLS).fill(0));
        let score = 0;
        let gameRunning = true;
        let isPaused = false;

        const colors = [
            null,
            '#FF0D72', // I-piece (hot pink)
            '#0DC2FF', // J-piece (cyan)
            '#0DFF72', // L-piece (green)
            '#F538FF', // O-piece (purple)
            '#FF8E0D', // S-piece (orange)
            '#FFE138', // T-piece (yellow)
            '#3877FF'  // Z-piece (blue)
        ];

        const pieces = [
            [[1,1,1,1]], // I
            [[2,0,0],[2,2,2]], // J
            [[0,0,3],[3,3,3]], // L
            [[4,4],[4,4]], // O
            [[0,5,5],[5,5,0]], // S
            [[0,6,0],[6,6,6]], // T
            [[7,7,0],[0,7,7]]  // Z
        ];

        class Piece {
            constructor() {
                this.type = Math.floor(Math.random() * pieces.length);
                this.shape = pieces[this.type];
                this.color = this.type + 1;
                this.x = Math.floor(COLS / 2) - Math.floor(this.shape[0].length / 2);
                this.y = 0;
            }

            rotate() {
                const rotated = this.shape[0].map((_, i) =>
                    this.shape.map(row => row[i]).reverse()
                );
                if (this.valid(this.x, this.y, rotated)) {
                    this.shape = rotated;
                }
            }

            valid(x, y, shape = this.shape) {
                for (let row = 0; row < shape.length; row++) {
                    for (let col = 0; col < shape[row].length; col++) {
                        if (shape[row][col]) {
                            const newX = x + col;
                            const newY = y + row;
                            if (newX < 0 || newX >= COLS || newY >= ROWS) {
                                return false;
                            }
                            if (newY >= 0 && board[newY][newX]) {
                                return false;
                            }
                        }
                    }
                }
                return true;
            }

            lock() {
                for (let row = 0; row < this.shape.length; row++) {
                    for (let col = 0; col < this.shape[row].length; col++) {
                        if (this.shape[row][col]) {
                            if (this.y + row < 0) {
                                gameRunning = false;
                                setTimeout(() => {
                                    alert('Game Over! Your Score: ' + score);
                                    resetGame();
                                }, 100);
                                return;
                            }
                            board[this.y + row][this.x + col] = this.color;
                        }
                    }
                }
                clearLines();
            }

            move(dir) {
                const newX = this.x + dir;
                if (this.valid(newX, this.y)) {
                    this.x = newX;
                    return true;
                }
                return false;
            }

            drop() {
                if (this.valid(this.x, this.y + 1)) {
                    this.y++;
                    return true;
                }
                this.lock();
                return false;
            }
        }

        let currentPiece = new Piece();
        let dropCounter = 0;
        let lastTime = 0;

        function clearLines() {
            let linesCleared = 0;
            for (let row = ROWS - 1; row >= 0; row--) {
                if (board[row].every(cell => cell > 0)) {
                    board.splice(row, 1);
                    board.unshift(Array(COLS).fill(0));
                    linesCleared++;
                    row++;
                }
            }
            if (linesCleared > 0) {
                score += linesCleared * 100 * linesCleared;
                document.getElementById('scoreValue').textContent = score;
            }
        }

        function draw() {
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Draw board
            for (let row = 0; row < ROWS; row++) {
                for (let col = 0; col < COLS; col++) {
                    if (board[row][col]) {
                        ctx.fillStyle = colors[board[row][col]];
                        ctx.fillRect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1);

                        // Add highlight effect
                        ctx.fillStyle = 'rgba(255, 255, 255, 0.1)';
                        ctx.fillRect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE / 2);
                    }
                }
            }

            // Draw current piece
            for (let row = 0; row < currentPiece.shape.length; row++) {
                for (let col = 0; col < currentPiece.shape[row].length; col++) {
                    if (currentPiece.shape[row][col]) {
                        ctx.fillStyle = colors[currentPiece.color];
                        ctx.fillRect(
                            (currentPiece.x + col) * BLOCK_SIZE,
                            (currentPiece.y + row) * BLOCK_SIZE,
                            BLOCK_SIZE - 1, BLOCK_SIZE - 1
                        );

                        // Add highlight effect
                        ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
                        ctx.fillRect(
                            (currentPiece.x + col) * BLOCK_SIZE,
                            (currentPiece.y + row) * BLOCK_SIZE,
                            BLOCK_SIZE - 1, BLOCK_SIZE / 2
                        );
                    }
                }
            }

            // Draw pause indicator
            if (isPaused) {
                ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = '#fff';
                ctx.font = 'bold 40px Arial';
                ctx.textAlign = 'center';
                ctx.fillText('PAUSED', canvas.width / 2, canvas.height / 2);
            }
        }

        function update(time = 0) {
            if (!gameRunning) return;

            if (isPaused) {
                draw();
                requestAnimationFrame(update);
                return;
            }

            const deltaTime = time - lastTime;
            lastTime = time;
            dropCounter += deltaTime;

            if (dropCounter > 1000) {
                if (!currentPiece.drop()) {
                    currentPiece = new Piece();
                }
                dropCounter = 0;
            }

            draw();
            requestAnimationFrame(update);
        }

        function resetGame() {
            board = Array(ROWS).fill().map(() => Array(COLS).fill(0));
            score = 0;
            document.getElementById('scoreValue').textContent = score;
            currentPiece = new Piece();
            gameRunning = true;
            isPaused = false;
            dropCounter = 0;
            lastTime = 0;
            update();
        }

        document.addEventListener('keydown', e => {
            if (!gameRunning) return;

            switch(e.key) {
                case 'ArrowLeft':
                    e.preventDefault();
                    if (!isPaused) currentPiece.move(-1);
                    break;
                case 'ArrowRight':
                    e.preventDefault();
                    if (!isPaused) currentPiece.move(1);
                    break;
                case 'ArrowDown':
                    e.preventDefault();
                    if (!isPaused) {
                        currentPiece.drop();
                        dropCounter = 0;
                    }
                    break;
                case 'ArrowUp':
                    e.preventDefault();
                    if (!isPaused) currentPiece.rotate();
                    break;
                case ' ':
                    e.preventDefault();
                    isPaused = !isPaused;
                    break;
            }
        });

        // Start the game
        update();
    <\/script>
</body>
</html>`
        });
    }

    /**
     * Create a Game object from JSON data
     * @param {string|Object} json - JSON string or object
     * @returns {Game} Game object
     * @throws {Error} If JSON is invalid or missing required fields
     */
    static createGameFromJSON(json) {
        try {
            const data = typeof json === 'string' ? JSON.parse(json) : json;

            // Validate required fields
            if (!data.name || !data.code) {
                throw new Error('Invalid game file: missing required fields (name, code)');
            }

            // Generate ID if not present
            if (!data.id) {
                data.id = 'local-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
            }

            data.isLocal = true;
            return new Game(data);
        } catch (error) {
            console.error('Error creating game from JSON:', error);
            throw error;
        }
    }

    /**
     * Export a single game to JSON file
     * @param {Game} game - Game object to export
     */
    static exportGame(game) {
        try {
            const gameData = game.toJSON();
            const blob = new Blob([JSON.stringify(gameData, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);

            const a = document.createElement('a');
            a.href = url;
            a.download = `${game.id}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Error exporting game:', error);
            throw error;
        }
    }

    /**
     * Export all games to a single JSON file
     * @param {Game[]} games - Array of games to export
     * @returns {boolean} Success status
     */
    static exportAllGames(games) {
        try {
            const localGames = games.filter(g => g.isLocal);
            if (localGames.length === 0) {
                console.warn('No local games to export');
                return false;
            }

            const exportData = {
                version: '1.0',
                exported: new Date().toISOString(),
                timestamp: Date.now(),
                count: localGames.length,
                games: localGames.map(g => g.toJSON())
            };

            const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);

            const a = document.createElement('a');
            a.href = url;
            a.download = `games-export-${Date.now()}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            return true;
        } catch (error) {
            console.error('Error exporting all games:', error);
            throw error;
        }
    }

    /**
     * Import games from JSON file content
     * @param {string|Object} json - JSON string or object
     * @returns {Game[]} Array of imported games
     * @throws {Error} If import fails
     */
    static importGamesFromJSON(json) {
        try {
            const data = typeof json === 'string' ? JSON.parse(json) : json;
            const importedGames = [];

            // Check if it's a single game or multiple games export
            if (data.games && Array.isArray(data.games)) {
                // Multiple games export
                for (const gameData of data.games) {
                    try {
                        const game = LocalGameService.createGameFromJSON(gameData);
                        importedGames.push(game);
                    } catch (err) {
                        console.error('Failed to import game:', err);
                    }
                }
            } else if (data.name && data.code) {
                // Single game
                const game = LocalGameService.createGameFromJSON(data);
                importedGames.push(game);
            } else {
                throw new Error('Invalid import file format');
            }

            return importedGames;
        } catch (error) {
            console.error('Error importing games from JSON:', error);
            throw error;
        }
    }
}

// ===== EXPORTS =====
// For ES6 modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { GitHubService, LocalGameService, Game };
}

// For browser global
if (typeof window !== 'undefined') {
    window.GitHubService = GitHubService;
    window.LocalGameService = LocalGameService;
    window.Game = Game;
}

console.log('GitHub Game Service loaded successfully ✓');
