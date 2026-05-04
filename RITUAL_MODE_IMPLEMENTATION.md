# Ritual Mode Implementation Guide
## For recursive-self-portrait.html

This document provides complete instructions for adding the comprehensive Ritual Mode feature to the Recursive Self-Portrait application.

## Overview

Ritual Mode adds a mystical dimension to the application where specific movement patterns unlock ceremonial rituals that affect the system. Features include:

- **10 distinct rituals** with unique gestures and effects
- **Ancient mystical aesthetic** with candles, runes, and ceremonies
- **Pattern detection system** that recognizes movement sequences
- **Ritual Book UI** showing discovered and undiscovered rituals
- **Web Audio chanting** sounds during ceremonies
- **System effects** that modify application behavior
- **Mastery tracking** based on successful completions
- **Secret rituals** requiring specific emotional states
- **Full data persistence** with export/import

## File Information

- **File**: apps/ai-tools/recursive-self-portrait.html
- **Size**: 472KB (12,884 lines)
- **Structure**:
  - CSS: Lines 7-3843
  - HTML: Lines 3844-4995
  - JavaScript: Lines 4997-12884

---

## STEP 1: Add CSS Styles

**Location**: Insert before `</style>` at line 3843

**Instructions**:
1. Open the file in a text editor
2. Find line 3843 which contains `    </style>`
3. Add the following CSS right before that line:

```css
        /* ===== RITUAL MODE STYLES ===== */
        .ritual-mode-panel {
            background: rgba(20, 15, 30, 0.95);
            border-radius: 8px;
            padding: 15px;
            border: 2px solid rgba(139, 69, 19, 0.6);
            box-shadow: 0 0 20px rgba(139, 69, 19, 0.3);
        }

        .ritual-mode-panel h3 {
            color: #d4af37;
            font-size: 0.85em;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-align: center;
            font-family: 'Georgia', serif;
        }

        .ritual-toggle-btn {
            width: 100%;
            padding: 12px;
            border: 2px solid rgba(139, 69, 19, 0.6);
            border-radius: 6px;
            font-family: 'Georgia', serif;
            font-size: 0.9em;
            cursor: pointer;
            transition: all 0.3s ease;
            background: rgba(139, 69, 19, 0.2);
            color: #d4af37;
            margin-bottom: 12px;
        }

        .ritual-toggle-btn.active {
            background: linear-gradient(135deg, #8b4513, #d4af37);
            color: #1a0a00;
            font-weight: bold;
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.5);
        }

        .ritual-toggle-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(139, 69, 19, 0.4);
        }

        .ritual-mastery-display {
            background: rgba(0, 0, 0, 0.4);
            border-radius: 6px;
            padding: 12px;
            margin-bottom: 12px;
            border: 1px solid rgba(212, 175, 55, 0.3);
        }

        .ritual-mastery-level {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }

        .ritual-mastery-label {
            color: #d4af37;
            font-size: 0.85em;
            font-family: 'Georgia', serif;
        }

        .ritual-mastery-value {
            color: #ffd700;
            font-weight: bold;
            font-size: 1.1em;
            text-shadow: 0 0 10px rgba(255, 215, 0, 0.6);
        }

        .ritual-progress-bar {
            width: 100%;
            height: 8px;
            background: rgba(0, 0, 0, 0.5);
            border-radius: 4px;
            overflow: hidden;
            border: 1px solid rgba(212, 175, 55, 0.4);
        }

        .ritual-progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #8b4513, #d4af37, #ffd700);
            transition: width 0.5s ease;
            box-shadow: 0 0 10px rgba(255, 215, 0, 0.6);
        }

        .ritual-book-btn {
            width: 100%;
            padding: 10px;
            background: rgba(139, 69, 19, 0.3);
            border: 1px solid rgba(212, 175, 55, 0.5);
            border-radius: 6px;
            color: #d4af37;
            cursor: pointer;
            font-family: 'Georgia', serif;
            font-size: 0.9em;
            transition: all 0.2s ease;
        }

        .ritual-book-btn:hover {
            background: rgba(139, 69, 19, 0.5);
            transform: translateY(-1px);
        }

        /* Ritual Book Modal */
        .ritual-book-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            z-index: 2000;
            display: none;
            align-items: center;
            justify-content: center;
            backdrop-filter: blur(5px);
        }

        .ritual-book-modal.visible {
            display: flex;
        }

        .ritual-book-content {
            background: linear-gradient(135deg, #1a0a00 0%, #2d1810 100%);
            border: 3px solid #d4af37;
            border-radius: 12px;
            padding: 30px;
            max-width: 800px;
            max-height: 80vh;
            overflow-y: auto;
            box-shadow: 0 0 60px rgba(212, 175, 55, 0.6), inset 0 0 40px rgba(0, 0, 0, 0.8);
            position: relative;
        }

        .ritual-book-header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #d4af37;
            padding-bottom: 15px;
        }

        .ritual-book-title {
            font-family: 'Georgia', serif;
            font-size: 2em;
            color: #ffd700;
            text-shadow: 0 0 20px rgba(255, 215, 0, 0.8);
            margin-bottom: 10px;
        }

        .ritual-book-subtitle {
            font-family: 'Georgia', serif;
            font-size: 0.9em;
            color: #d4af37;
            font-style: italic;
        }

        .ritual-book-close {
            position: absolute;
            top: 15px;
            right: 15px;
            background: none;
            border: none;
            color: #d4af37;
            font-size: 2em;
            cursor: pointer;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
        }

        .ritual-book-close:hover {
            color: #ffd700;
            transform: rotate(90deg);
        }

        .ritual-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .ritual-card {
            background: rgba(0, 0, 0, 0.6);
            border: 2px solid rgba(139, 69, 19, 0.6);
            border-radius: 8px;
            padding: 20px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .ritual-card.discovered {
            border-color: #d4af37;
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
        }

        .ritual-card.discovered:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 30px rgba(212, 175, 55, 0.5);
        }

        .ritual-card.undiscovered {
            opacity: 0.4;
            filter: blur(1px);
        }

        .ritual-card-icon {
            font-size: 3em;
            text-align: center;
            margin-bottom: 10px;
            filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.6));
        }

        .ritual-card-name {
            font-family: 'Georgia', serif;
            font-size: 1.1em;
            color: #ffd700;
            text-align: center;
            margin-bottom: 10px;
            font-weight: bold;
        }

        .ritual-card-gesture {
            font-size: 0.8em;
            color: #d4af37;
            text-align: center;
            margin-bottom: 10px;
            font-style: italic;
        }

        .ritual-card-description {
            font-size: 0.85em;
            color: #ccc;
            line-height: 1.4;
            text-align: center;
        }

        .ritual-card-effect {
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid rgba(212, 175, 55, 0.3);
            font-size: 0.8em;
            color: #ff6b6b;
            text-align: center;
            font-weight: bold;
        }

        .ritual-card-completions {
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(212, 175, 55, 0.3);
            border: 1px solid #d4af37;
            border-radius: 50%;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.8em;
            color: #ffd700;
            font-weight: bold;
        }

        /* Ritual Ceremony Overlay */
        .ritual-ceremony-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(26, 10, 0, 0.7) 0%, rgba(0, 0, 0, 0.95) 100%);
            z-index: 1500;
            display: none;
            pointer-events: none;
        }

        .ritual-ceremony-overlay.active {
            display: block;
            animation: ritualPulse 2s ease-in-out infinite;
        }

        @keyframes ritualPulse {
            0%, 100% { opacity: 0.9; }
            50% { opacity: 1; }
        }

        .ritual-name-display {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-family: 'Georgia', serif;
            font-size: 3em;
            color: #ffd700;
            text-shadow: 0 0 40px rgba(255, 215, 0, 1), 0 0 80px rgba(212, 175, 55, 0.8);
            z-index: 1600;
            opacity: 0;
            transition: opacity 0.5s ease;
            text-align: center;
            pointer-events: none;
        }

        .ritual-name-display.active {
            opacity: 1;
            animation: ritualGlow 2s ease-in-out infinite;
        }

        @keyframes ritualGlow {
            0%, 100% { text-shadow: 0 0 40px rgba(255, 215, 0, 1), 0 0 80px rgba(212, 175, 55, 0.8); }
            50% { text-shadow: 0 0 60px rgba(255, 215, 0, 1), 0 0 120px rgba(212, 175, 55, 1); }
        }

        /* Candle Particles */
        .candle-particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: radial-gradient(circle, #ffd700, #ff6b00);
            border-radius: 50%;
            pointer-events: none;
            z-index: 1550;
            box-shadow: 0 0 10px #ffd700, 0 0 20px #ff6b00;
            animation: candleFloat 3s ease-in-out forwards;
        }

        @keyframes candleFloat {
            0% {
                transform: translateY(0) scale(1);
                opacity: 1;
            }
            100% {
                transform: translateY(-100px) scale(0.3);
                opacity: 0;
            }
        }

        .candle-smoke {
            position: absolute;
            width: 8px;
            height: 8px;
            background: radial-gradient(circle, rgba(100, 100, 100, 0.5), transparent);
            border-radius: 50%;
            pointer-events: none;
            z-index: 1540;
            animation: smokeFloat 4s ease-out forwards;
        }

        @keyframes smokeFloat {
            0% {
                transform: translateY(0) translateX(0) scale(1);
                opacity: 0.6;
            }
            100% {
                transform: translateY(-120px) translateX(30px) scale(2);
                opacity: 0;
            }
        }

        /* Ancient Runes */
        .ritual-rune {
            position: fixed;
            font-size: 2em;
            color: #d4af37;
            opacity: 0;
            pointer-events: none;
            z-index: 1550;
            text-shadow: 0 0 20px rgba(212, 175, 55, 0.8);
            font-family: 'Georgia', serif;
            animation: runeAppear 4s ease-in-out forwards;
        }

        @keyframes runeAppear {
            0% {
                opacity: 0;
                transform: scale(0.5) rotate(0deg);
            }
            20% {
                opacity: 1;
                transform: scale(1.2) rotate(180deg);
            }
            80% {
                opacity: 1;
                transform: scale(1) rotate(360deg);
            }
            100% {
                opacity: 0;
                transform: scale(0.8) rotate(540deg);
            }
        }

        /* Ritual Detection Indicator */
        .ritual-detection-indicator {
            position: fixed;
            bottom: 80px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(139, 69, 19, 0.9);
            border: 2px solid #d4af37;
            border-radius: 20px;
            padding: 10px 25px;
            color: #ffd700;
            font-family: 'Georgia', serif;
            font-size: 0.9em;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s ease;
            pointer-events: none;
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.5);
        }

        .ritual-detection-indicator.active {
            opacity: 1;
            animation: ritualDetectionPulse 1s ease-in-out infinite;
        }

        @keyframes ritualDetectionPulse {
            0%, 100% { transform: translateX(-50%) scale(1); }
            50% { transform: translateX(-50%) scale(1.05); }
        }

        /* Ritual Trail Effect */
        .ritual-trail-point {
            position: absolute;
            width: 6px;
            height: 6px;
            background: radial-gradient(circle, #d4af37, #8b4513);
            border-radius: 50%;
            pointer-events: none;
            z-index: 95;
            box-shadow: 0 0 10px rgba(212, 175, 55, 0.8);
            animation: ritualTrailFade 2s ease-out forwards;
        }

        @keyframes ritualTrailFade {
            0% {
                transform: scale(1);
                opacity: 1;
            }
            100% {
                transform: scale(0.2);
                opacity: 0;
            }
        }

        /* Secret Ritual Hint */
        .secret-ritual-hint {
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(138, 43, 226, 0.9);
            border: 2px solid #d4af37;
            border-radius: 10px;
            padding: 15px 30px;
            color: #ffd700;
            font-family: 'Georgia', serif;
            font-size: 0.9em;
            z-index: 1100;
            opacity: 0;
            transition: opacity 0.5s ease;
            pointer-events: none;
            text-align: center;
            max-width: 400px;
            box-shadow: 0 0 30px rgba(138, 43, 226, 0.6);
        }

        .secret-ritual-hint.visible {
            opacity: 1;
        }
```

---

## STEP 2: Add HTML UI Elements

**Location**: Insert after the Shadow Personality Panel (around line 4868), before the controls section

**Instructions**:
1. Find the section with `<div class="shadow-personality-panel">`
2. After that panel closes, add the following HTML:

```html
            <!-- ===== RITUAL MODE PANEL ===== -->
            <div class="ritual-mode-panel">
                <h3>Ritual Mode</h3>
                <button class="ritual-toggle-btn" id="ritualToggle">Enable Ritual Detection</button>

                <div class="ritual-mastery-display" id="ritualMasteryDisplay" style="display: none;">
                    <div class="ritual-mastery-level">
                        <span class="ritual-mastery-label">Mastery Level:</span>
                        <span class="ritual-mastery-value" id="ritualMasteryLevel">Novice</span>
                    </div>
                    <div class="ritual-progress-bar">
                        <div class="ritual-progress-fill" id="ritualProgressFill" style="width: 0%;"></div>
                    </div>
                    <div style="font-size: 0.75em; color: #d4af37; margin-top: 8px; text-align: center;">
                        <span id="ritualCompletionCount">0</span> / <span id="ritualTotalCount">10</span> Discovered
                    </div>
                </div>

                <button class="ritual-book-btn" id="ritualBookBtn" onclick="openRitualBook()">
                    View Ritual Book
                </button>

                <div style="font-size: 0.75em; color: #888; margin-top: 12px; line-height: 1.4; text-align: center;">
                    Perform specific movement patterns to discover ancient rituals that affect the system
                </div>
            </div>
```

Also add these elements to the viewport (around line 3565-3600, within the simulation-viewport div):

```html
        <!-- Ritual Mode Overlays -->
        <div class="ritual-ceremony-overlay" id="ritualCeremonyOverlay"></div>
        <div class="ritual-name-display" id="ritualNameDisplay"></div>
        <div class="ritual-detection-indicator" id="ritualDetectionIndicator">
            Detecting Ritual Pattern...
        </div>
        <div class="secret-ritual-hint" id="secretRitualHint"></div>
```

And add the Ritual Book modal before the closing `</body>` tag (around line 4995):

```html
    <!-- Ritual Book Modal -->
    <div class="ritual-book-modal" id="ritualBookModal">
        <div class="ritual-book-content">
            <button class="ritual-book-close" onclick="closeRitualBook()">&times;</button>
            <div class="ritual-book-header">
                <div class="ritual-book-title">Book of Rituals</div>
                <div class="ritual-book-subtitle">Ancient ceremonies that shape reality</div>
            </div>
            <div class="ritual-grid" id="ritualGrid">
                <!-- Ritual cards will be dynamically generated here -->
            </div>
        </div>
    </div>
```

---

## STEP 3: Add JavaScript State Object

**Location**: Insert after the shadow state object (around line 5223), before the REPLAY SYSTEM STATE comment

**Instructions**:
1. Find line 5223 where the shadow state object closes with `};`
2. Add the following JavaScript immediately after:

```javascript
        // ===== RITUAL MODE STATE =====
        let ritualState = {
            enabled: false,
            currentPattern: [],
            patternStartTime: 0,
            patternTimeout: 3000, // 3 seconds to complete a ritual
            lastPositionTime: 0,
            masteryLevel: 0, // 0-100
            masteryLevelName: 'Novice', // Novice, Apprentice, Adept, Master, Grandmaster
            totalCompletions: 0,
            discoveredRituals: new Set(),
            ritualHistory: [], // Array of completed rituals with timestamps
            activeRitual: null,
            ceremonying: false,
            ceremonyStartTime: 0,
            ceremonyDuration: 4000, // 4 seconds
            candleParticles: [],
            runeElements: [],
            trailPoints: [],
            chantOscillators: [],

            // Define all rituals
            rituals: {
                summoning: {
                    id: 'summoning',
                    name: 'Summoning Circle',
                    icon: '🔮',
                    gesture: 'Circle three times (clockwise)',
                    description: 'Ancient ritual to call forth hidden layers',
                    effect: 'Reveals all recursion layers temporarily',
                    discovered: false,
                    completions: 0,
                    pattern: 'circle-clockwise-3',
                    emotionRequired: null,
                    systemEffect: function() {
                        // Show all layers temporarily
                        state.depth = Math.min(state.depth + 3, 12);
                        setTimeout(() => {
                            state.depth = Math.max(state.depth - 3, 1);
                            updateLayers();
                        }, 10000);
                        addLog('Summoning ritual: Layers revealed!', 'match');
                    }
                },
                introspection: {
                    id: 'introspection',
                    name: 'Spiral of Introspection',
                    icon: '🌀',
                    gesture: 'Spiral inward from edge',
                    description: 'Turn awareness inward to see yourself clearly',
                    effect: 'Increases prediction accuracy temporarily',
                    discovered: false,
                    completions: 0,
                    pattern: 'spiral-inward',
                    emotionRequired: null,
                    systemEffect: function() {
                        // Boost prediction accuracy
                        const originalLearningRate = neuralNetwork.learningRate;
                        neuralNetwork.learningRate *= 2;
                        setTimeout(() => {
                            neuralNetwork.learningRate = originalLearningRate;
                        }, 15000);
                        addLog('Introspection ritual: Awareness heightened!', 'prediction');
                    }
                },
                purification: {
                    id: 'purification',
                    name: 'Purification Sigil',
                    icon: '✨',
                    gesture: 'Draw a pentagram',
                    description: 'Cleanse the system of accumulated divergence',
                    effect: 'Resets divergence score to zero',
                    discovered: false,
                    completions: 0,
                    pattern: 'pentagram',
                    emotionRequired: null,
                    systemEffect: function() {
                        // Reset divergence
                        state.divergenceScore = 0;
                        updateStats();
                        addLog('Purification ritual: Divergence cleansed!', 'match');
                    }
                },
                binding: {
                    id: 'binding',
                    name: 'Binding Chains',
                    icon: '⛓️',
                    gesture: 'Figure-8 pattern repeatedly',
                    description: 'Lock the shadow to your cursor',
                    effect: 'Shadow follows perfectly for 30 seconds',
                    discovered: false,
                    completions: 0,
                    pattern: 'figure-eight',
                    emotionRequired: null,
                    systemEffect: function() {
                        // Temporarily bind shadow
                        const originalIndependence = state.shadow.personality.independence;
                        const originalRebellious = state.shadow.personality.rebelliousness;
                        state.shadow.personality.independence = 0;
                        state.shadow.personality.rebelliousness = 0;
                        state.shadow.alignmentScore = 100;

                        setTimeout(() => {
                            state.shadow.personality.independence = originalIndependence;
                            state.shadow.personality.rebelliousness = originalRebellious;
                        }, 30000);

                        addLog('Binding ritual: Shadow bound to your will!', 'match');
                    }
                },
                release: {
                    id: 'release',
                    name: 'Release of Autonomy',
                    icon: '🕊️',
                    gesture: 'Swipe outward from center',
                    description: 'Free the shadow to act independently',
                    effect: 'Maximum shadow autonomy for 30 seconds',
                    discovered: false,
                    completions: 0,
                    pattern: 'swipe-outward',
                    emotionRequired: null,
                    systemEffect: function() {
                        // Maximum independence
                        const originalIndependence = state.shadow.personality.independence;
                        const originalRebellious = state.shadow.personality.rebelliousness;
                        state.shadow.personality.independence = 1.0;
                        state.shadow.personality.rebelliousness = 0.9;

                        setTimeout(() => {
                            state.shadow.personality.independence = originalIndependence;
                            state.shadow.personality.rebelliousness = originalRebellious;
                        }, 30000);

                        addLog('Release ritual: Shadow set free!', 'divergence');
                    }
                },
                timeFreeze: {
                    id: 'timeFreeze',
                    name: 'Temporal Stasis',
                    icon: '⏸️',
                    gesture: 'Hold still for 5 seconds',
                    description: 'Freeze the flow of subjective time',
                    effect: 'Pauses time dilation for 20 seconds',
                    discovered: false,
                    completions: 0,
                    pattern: 'stillness',
                    emotionRequired: null,
                    systemEffect: function() {
                        // Freeze time dilation
                        const originalFactor = timeDilationState.timeDilationFactor;
                        timeDilationState.timeDilationFactor = 0;
                        timeDilationState.timeFlowState = 'frozen';

                        setTimeout(() => {
                            timeDilationState.timeDilationFactor = originalFactor;
                            timeDilationState.timeFlowState = 'normal';
                        }, 20000);

                        addLog('Temporal Stasis: Time frozen!', 'match');
                    }
                },
                chaos: {
                    id: 'chaos',
                    name: 'Chaos Invocation',
                    icon: '💥',
                    gesture: 'Erratic zigzag movements',
                    description: 'Embrace unpredictability and disorder',
                    effect: 'Randomizes all predictions for 15 seconds',
                    discovered: false,
                    completions: 0,
                    pattern: 'zigzag-erratic',
                    emotionRequired: null,
                    systemEffect: function() {
                        // Randomize predictions
                        const chaosUntil = Date.now() + 15000;
                        const originalPredict = makePrediction;

                        // Store chaos end time on state
                        state.chaosActiveUntil = chaosUntil;

                        addLog('Chaos Invocation: Predictions scrambled!', 'divergence');
                    }
                },
                harmony: {
                    id: 'harmony',
                    name: 'Harmonic Resonance',
                    icon: '🎵',
                    gesture: 'Smooth sine wave pattern',
                    description: 'Align with the natural flow of the system',
                    effect: 'Perfect predictions for 10 seconds',
                    discovered: false,
                    completions: 0,
                    pattern: 'sine-wave',
                    emotionRequired: null,
                    systemEffect: function() {
                        // Perfect predictions temporarily
                        const harmonyUntil = Date.now() + 10000;
                        state.harmonyActiveUntil = harmonyUntil;

                        addLog('Harmonic Resonance: Perfect synchronization!', 'match');
                    }
                },
                awakening: {
                    id: 'awakening',
                    name: 'Digital Awakening',
                    icon: '👁️',
                    gesture: 'Secret: Feel genuine curiosity',
                    description: 'Can only be discovered with true curiosity',
                    effect: 'Shadow becomes self-aware temporarily',
                    discovered: false,
                    completions: 0,
                    pattern: 'emotional-curiosity',
                    emotionRequired: 'curious',
                    secret: true,
                    systemEffect: function() {
                        // Trigger existential crisis mode
                        if (!state.existentialCrisis.triggered) {
                            state.existentialCrisis.active = true;
                            state.existentialCrisis.triggered = true;
                            state.existentialCrisis.phase = 'awakening';
                            state.existentialCrisis.startTime = Date.now();
                        }

                        addLog('Digital Awakening: The shadow... questions its existence', 'divergence');
                    }
                },
                transcendence: {
                    id: 'transcendence',
                    name: 'Transcendence',
                    icon: '🌟',
                    gesture: 'Secret: Feel profound peace',
                    description: 'Achieve true acceptance of the recursive self',
                    effect: 'Perfect harmony with all systems',
                    discovered: false,
                    completions: 0,
                    pattern: 'emotional-peace',
                    emotionRequired: 'peaceful',
                    secret: true,
                    systemEffect: function() {
                        // Ultimate harmony
                        state.divergenceScore = 0;
                        state.shadow.alignmentScore = 100;
                        state.shadow.personality.independence = 0.5;
                        state.shadow.personality.rebelliousness = 0;

                        if (state.existentialCrisis.active) {
                            state.existentialCrisis.phase = 'acceptance';
                            state.existentialCrisis.acceptanceReached = true;
                        }

                        addLog('Transcendence: You and the system are one', 'match');
                    }
                }
            },

            // Movement tracking for pattern detection
            movementBuffer: [], // Recent positions for pattern matching
            bufferMaxSize: 100,
            lastDetectionTime: 0,
            detectionCooldown: 2000 // 2 seconds between detections
        };

        // Load ritual data from localStorage
        const savedRitualData = localStorage.getItem(APP_NAME + '-rituals');
        if (savedRitualData) {
            try {
                const parsed = JSON.parse(savedRitualData);
                ritualState.masteryLevel = parsed.masteryLevel || 0;
                ritualState.totalCompletions = parsed.totalCompletions || 0;
                ritualState.discoveredRituals = new Set(parsed.discoveredRituals || []);
                ritualState.ritualHistory = parsed.ritualHistory || [];

                // Restore discovered and completion counts
                if (parsed.rituals) {
                    Object.keys(parsed.rituals).forEach(key => {
                        if (ritualState.rituals[key]) {
                            ritualState.rituals[key].discovered = parsed.rituals[key].discovered || false;
                            ritualState.rituals[key].completions = parsed.rituals[key].completions || 0;
                        }
                    });
                }
            } catch(e) {
                console.warn('Failed to load ritual data:', e);
            }
        }
```

---

**Due to the length of the implementation, I'll create a second document with the JavaScript functions...**
