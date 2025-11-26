# Ritual Mode JavaScript Functions
## Part 2: Functions and Integration

This document contains all the JavaScript functions needed for Ritual Mode.

---

## STEP 4: Add Ritual Mode Functions

**Location**: Insert after the state definitions, before the main initialization code (around line 5400-5500)

**Instructions**:
1. Find a good spot after all state definitions but before complex class definitions
2. Add all the following functions:

```javascript
        // ===== RITUAL MODE FUNCTIONS =====

        function toggleRitualMode() {
            ritualState.enabled = !ritualState.enabled;
            const ritualToggleBtn = document.getElementById('ritualToggle');
            const ritualMasteryDisplay = document.getElementById('ritualMasteryDisplay');

            if (ritualState.enabled) {
                ritualToggleBtn.classList.add('active');
                ritualToggleBtn.textContent = 'Ritual Detection Active';
                ritualMasteryDisplay.style.display = 'block';
                addLog('Ritual mode activated - Perform gestures to discover rituals', 'match');
                updateRitualMasteryDisplay();
            } else {
                ritualToggleBtn.classList.remove('active');
                ritualToggleBtn.textContent = 'Enable Ritual Detection';
                ritualMasteryDisplay.style.display = 'none';
                addLog('Ritual mode deactivated', 'normal');
            }

            saveRitualData();
        }

        function trackRitualMovement(x, y) {
            if (!ritualState.enabled || !state.isObserving) return;

            const now = Date.now();
            const position = { x, y, timestamp: now };

            // Add to movement buffer
            ritualState.movementBuffer.push(position);

            // Keep buffer at max size
            if (ritualState.movementBuffer.length > ritualState.bufferMaxSize) {
                ritualState.movementBuffer.shift();
            }

            // Create trail point
            if (ritualState.enabled) {
                createRitualTrailPoint(x, y);
            }

            // Check for patterns every 100ms
            if (now - ritualState.lastDetectionTime > 100) {
                ritualState.lastDetectionTime = now;
                detectRitualPattern();
            }
        }

        function detectRitualPattern() {
            if (ritualState.movementBuffer.length < 10) return;
            if (Date.now() - ritualState.lastDetectionTime < ritualState.detectionCooldown) return;

            const buffer = ritualState.movementBuffer;

            // Check each ritual pattern
            for (const key in ritualState.rituals) {
                const ritual = ritualState.rituals[key];

                // Skip emotional rituals unless emotion matches
                if (ritual.emotionRequired && state.emotionState.current !== ritual.emotionRequired) {
                    continue;
                }

                let detected = false;

                switch (ritual.pattern) {
                    case 'circle-clockwise-3':
                        detected = detectCircle(buffer, 3, true);
                        break;
                    case 'spiral-inward':
                        detected = detectSpiral(buffer, 'inward');
                        break;
                    case 'pentagram':
                        detected = detectPentagram(buffer);
                        break;
                    case 'figure-eight':
                        detected = detectFigureEight(buffer);
                        break;
                    case 'swipe-outward':
                        detected = detectSwipeOutward(buffer);
                        break;
                    case 'stillness':
                        detected = detectStillness(buffer);
                        break;
                    case 'zigzag-erratic':
                        detected = detectZigzag(buffer);
                        break;
                    case 'sine-wave':
                        detected = detectSineWave(buffer);
                        break;
                    case 'emotional-curiosity':
                        detected = state.emotionState.current === 'curious' &&
                                   state.emotionState.confidence > 0.6;
                        break;
                    case 'emotional-peace':
                        detected = state.emotionState.current === 'peaceful' &&
                                   state.emotionState.confidence > 0.7;
                        break;
                }

                if (detected) {
                    triggerRitual(ritual);
                    ritualState.lastDetectionTime = Date.now();
                    break; // Only one ritual at a time
                }
            }
        }

        // Pattern detection algorithms
        function detectCircle(buffer, rotations, clockwise) {
            if (buffer.length < 30) return false;

            const recentBuffer = buffer.slice(-50);
            let angle = 0;
            let lastAngle = null;
            let rotationCount = 0;

            for (let i = 1; i < recentBuffer.length; i++) {
                const dx = recentBuffer[i].x - recentBuffer[0].x;
                const dy = recentBuffer[i].y - recentBuffer[0].y;
                const currentAngle = Math.atan2(dy, dx);

                if (lastAngle !== null) {
                    let angleDiff = currentAngle - lastAngle;

                    // Normalize angle difference
                    if (angleDiff > Math.PI) angleDiff -= 2 * Math.PI;
                    if (angleDiff < -Math.PI) angleDiff += 2 * Math.PI;

                    if (clockwise && angleDiff > 0) angle += angleDiff;
                    if (!clockwise && angleDiff < 0) angle += Math.abs(angleDiff);
                }

                lastAngle = currentAngle;
            }

            rotationCount = Math.abs(angle) / (2 * Math.PI);
            return rotationCount >= rotations * 0.8; // Allow some tolerance
        }

        function detectSpiral(buffer, direction) {
            if (buffer.length < 40) return false;

            const recentBuffer = buffer.slice(-60);
            const centerX = recentBuffer[0].x;
            const centerY = recentBuffer[0].y;

            let distances = [];
            let angles = [];

            for (let i = 0; i < recentBuffer.length; i++) {
                const dx = recentBuffer[i].x - centerX;
                const dy = recentBuffer[i].y - centerY;
                const dist = Math.sqrt(dx * dx + dy * dy);
                const angle = Math.atan2(dy, dx);

                distances.push(dist);
                angles.push(angle);
            }

            // Check if distance consistently decreases (inward) or increases (outward)
            let directionConsistent = true;
            for (let i = 1; i < distances.length - 1; i++) {
                if (direction === 'inward') {
                    if (distances[i] > distances[i-1] + 5) directionConsistent = false;
                } else {
                    if (distances[i] < distances[i-1] - 5) directionConsistent = false;
                }
            }

            // Check for angular progression (spiral)
            let totalAngleChange = 0;
            for (let i = 1; i < angles.length; i++) {
                let diff = angles[i] - angles[i-1];
                if (diff > Math.PI) diff -= 2 * Math.PI;
                if (diff < -Math.PI) diff += 2 * Math.PI;
                totalAngleChange += diff;
            }

            return directionConsistent && Math.abs(totalAngleChange) > Math.PI * 1.5;
        }

        function detectPentagram(buffer) {
            if (buffer.length < 50) return false;

            // Simplified: Check for 5 major direction changes
            const recentBuffer = buffer.slice(-70);
            let directionChanges = 0;
            let lastDirection = null;

            for (let i = 5; i < recentBuffer.length; i += 5) {
                const dx = recentBuffer[i].x - recentBuffer[i-5].x;
                const dy = recentBuffer[i].y - recentBuffer[i-5].y;
                const angle = Math.atan2(dy, dx);

                if (lastDirection !== null) {
                    let angleDiff = Math.abs(angle - lastDirection);
                    if (angleDiff > Math.PI) angleDiff = 2 * Math.PI - angleDiff;

                    // Significant direction change
                    if (angleDiff > Math.PI / 3) {
                        directionChanges++;
                    }
                }

                lastDirection = angle;
            }

            return directionChanges >= 4 && directionChanges <= 6;
        }

        function detectFigureEight(buffer) {
            if (buffer.length < 40) return false;

            // Check for crossing pattern
            const recentBuffer = buffer.slice(-60);
            const midPoint = Math.floor(recentBuffer.length / 2);

            let crossings = 0;
            for (let i = 1; i < midPoint; i++) {
                for (let j = midPoint; j < recentBuffer.length - 1; j++) {
                    if (linesIntersect(
                        recentBuffer[i-1].x, recentBuffer[i-1].y,
                        recentBuffer[i].x, recentBuffer[i].y,
                        recentBuffer[j-1].x, recentBuffer[j-1].y,
                        recentBuffer[j].x, recentBuffer[j].y
                    )) {
                        crossings++;
                    }
                }
            }

            return crossings >= 2;
        }

        function linesIntersect(x1, y1, x2, y2, x3, y3, x4, y4) {
            const denom = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1);
            if (denom === 0) return false;

            const ua = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / denom;
            const ub = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / denom;

            return (ua >= 0 && ua <= 1 && ub >= 0 && ub <= 1);
        }

        function detectSwipeOutward(buffer) {
            if (buffer.length < 20) return false;

            const recentBuffer = buffer.slice(-30);
            const centerX = recentBuffer[0].x;
            const centerY = recentBuffer[0].y;

            let distances = [];
            for (let i = 0; i < recentBuffer.length; i++) {
                const dx = recentBuffer[i].x - centerX;
                const dy = recentBuffer[i].y - centerY;
                distances.push(Math.sqrt(dx * dx + dy * dy));
            }

            // Check for consistent outward movement
            let increasing = true;
            for (let i = 1; i < distances.length; i++) {
                if (distances[i] < distances[i-1] - 5) increasing = false;
            }

            const totalDistance = distances[distances.length-1] - distances[0];
            return increasing && totalDistance > 100;
        }

        function detectStillness(buffer) {
            if (buffer.length < 20) return false;

            const recentBuffer = buffer.slice(-25);
            const firstPos = recentBuffer[0];

            // Check all positions are within small radius
            for (let i = 1; i < recentBuffer.length; i++) {
                const dx = recentBuffer[i].x - firstPos.x;
                const dy = recentBuffer[i].y - firstPos.y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist > 10) return false; // Movement detected
            }

            // Check time span
            const timeSpan = recentBuffer[recentBuffer.length-1].timestamp - recentBuffer[0].timestamp;
            return timeSpan >= 4000; // 4+ seconds of stillness
        }

        function detectZigzag(buffer) {
            if (buffer.length < 30) return false;

            const recentBuffer = buffer.slice(-50);
            let directionChanges = 0;
            let lastDirection = null;

            for (let i = 3; i < recentBuffer.length; i += 3) {
                const dx = recentBuffer[i].x - recentBuffer[i-3].x;
                const dy = recentBuffer[i].y - recentBuffer[i-3].y;
                const angle = Math.atan2(dy, dx);

                if (lastDirection !== null) {
                    let angleDiff = Math.abs(angle - lastDirection);
                    if (angleDiff > Math.PI) angleDiff = 2 * Math.PI - angleDiff;

                    if (angleDiff > Math.PI / 4) {
                        directionChanges++;
                    }
                }

                lastDirection = angle;
            }

            return directionChanges >= 6; // Many quick direction changes
        }

        function detectSineWave(buffer) {
            if (buffer.length < 40) return false;

            const recentBuffer = buffer.slice(-60);

            // Fit sine wave to y coordinates
            let crossings = 0;
            let avgY = 0;
            for (let i = 0; i < recentBuffer.length; i++) {
                avgY += recentBuffer[i].y;
            }
            avgY /= recentBuffer.length;

            let lastAbove = recentBuffer[0].y > avgY;
            for (let i = 1; i < recentBuffer.length; i++) {
                const above = recentBuffer[i].y > avgY;
                if (above !== lastAbove) {
                    crossings++;
                    lastAbove = above;
                }
            }

            // Smooth wave should cross average line 2-4 times
            return crossings >= 2 && crossings <= 5;
        }

        function triggerRitual(ritual) {
            // Check cooldown
            if (ritualState.ceremonying) return;

            // Mark as discovered
            const wasDiscovered = ritual.discovered;
            ritual.discovered = true;
            ritual.completions++;
            ritualState.discoveredRituals.add(ritual.id);

            // Add to history
            ritualState.ritualHistory.push({
                ritualId: ritual.id,
                ritualName: ritual.name,
                timestamp: Date.now(),
                sessionActions: state.actions.length
            });

            // Update mastery
            ritualState.totalCompletions++;
            updateRitualMastery();

            // Start ceremony
            performRitualCeremony(ritual);

            // Log discovery
            if (!wasDiscovered) {
                addLog(`RITUAL DISCOVERED: ${ritual.name}!`, 'match');

                // Show hint for secret rituals if this reveals them
                if (ritualState.totalCompletions >= 5 && !ritual.secret) {
                    showSecretRitualHint();
                }
            } else {
                addLog(`Ritual performed: ${ritual.name} (${ritual.completions}x)`, 'match');
            }

            // Save data
            saveRitualData();
            updateRitualMasteryDisplay();
        }

        function performRitualCeremony(ritual) {
            ritualState.ceremonying = true;
            ritualState.activeRitual = ritual;
            ritualState.ceremonyStartTime = Date.now();

            // Show ceremony overlay
            const overlay = document.getElementById('ritualCeremonyOverlay');
            const nameDisplay = document.getElementById('ritualNameDisplay');

            overlay.classList.add('active');
            nameDisplay.textContent = `${ritual.icon} ${ritual.name} ${ritual.icon}`;
            nameDisplay.classList.add('active');

            // Play chanting sound
            playRitualChant();

            // Spawn candle particles around cursor
            spawnCandleParticles(lastMousePos.x, lastMousePos.y);

            // Spawn mystical runes
            spawnMysticalRunes();

            // Apply ritual effect after 2 seconds
            setTimeout(() => {
                ritual.systemEffect();

                // End ceremony after total duration
                setTimeout(() => {
                    endRitualCeremony();
                }, ritualState.ceremonyDuration - 2000);

            }, 2000);
        }

        function endRitualCeremony() {
            ritualState.ceremonying = false;
            ritualState.activeRitual = null;

            const overlay = document.getElementById('ritualCeremonyOverlay');
            const nameDisplay = document.getElementById('ritualNameDisplay');

            overlay.classList.remove('active');
            nameDisplay.classList.remove('active');

            // Stop chanting
            stopRitualChant();

            // Clean up particles
            ritualState.candleParticles.forEach(p => p.remove());
            ritualState.candleParticles = [];

            ritualState.runeElements.forEach(r => r.remove());
            ritualState.runeElements = [];
        }

        function spawnCandleParticles(x, y) {
            const particleCount = 30;

            for (let i = 0; i < particleCount; i++) {
                setTimeout(() => {
                    const particle = document.createElement('div');
                    particle.className = 'candle-particle';

                    const angle = (Math.PI * 2 * i) / particleCount;
                    const radius = Math.random() * 30 + 10;
                    const offsetX = Math.cos(angle) * radius;
                    const offsetY = Math.sin(angle) * radius;

                    particle.style.left = (x + offsetX) + 'px';
                    particle.style.top = (y + offsetY) + 'px';

                    viewport.appendChild(particle);
                    ritualState.candleParticles.push(particle);

                    // Remove after animation
                    setTimeout(() => {
                        particle.remove();
                        const index = ritualState.candleParticles.indexOf(particle);
                        if (index > -1) ritualState.candleParticles.splice(index, 1);
                    }, 3000);

                    // Occasional smoke
                    if (Math.random() < 0.3) {
                        const smoke = document.createElement('div');
                        smoke.className = 'candle-smoke';
                        smoke.style.left = (x + offsetX) + 'px';
                        smoke.style.top = (y + offsetY) + 'px';
                        viewport.appendChild(smoke);

                        setTimeout(() => smoke.remove(), 4000);
                    }
                }, i * 50);
            }
        }

        function spawnMysticalRunes() {
            const runes = ['ᚠ', 'ᚢ', 'ᚦ', 'ᚨ', 'ᚱ', 'ᚲ', 'ᚷ', 'ᚹ', '☥', '⚛️', '🜏', '🜍'];
            const runeCount = 8;
            const viewportRect = viewport.getBoundingClientRect();

            for (let i = 0; i < runeCount; i++) {
                setTimeout(() => {
                    const rune = document.createElement('div');
                    rune.className = 'ritual-rune';
                    rune.textContent = runes[Math.floor(Math.random() * runes.length)];

                    // Random position around the edges
                    const side = Math.floor(Math.random() * 4);
                    let x, y;

                    switch(side) {
                        case 0: // top
                            x = Math.random() * viewportRect.width;
                            y = 50;
                            break;
                        case 1: // right
                            x = viewportRect.width - 50;
                            y = Math.random() * viewportRect.height;
                            break;
                        case 2: // bottom
                            x = Math.random() * viewportRect.width;
                            y = viewportRect.height - 50;
                            break;
                        case 3: // left
                            x = 50;
                            y = Math.random() * viewportRect.height;
                            break;
                    }

                    rune.style.left = x + 'px';
                    rune.style.top = y + 'px';

                    document.body.appendChild(rune);
                    ritualState.runeElements.push(rune);

                    setTimeout(() => {
                        rune.remove();
                        const index = ritualState.runeElements.indexOf(rune);
                        if (index > -1) ritualState.runeElements.splice(index, 1);
                    }, 4000);
                }, i * 200);
            }
        }

        function playRitualChant() {
            if (!audioContext || !soundEnabled) return;

            try {
                // Create multiple oscillators for chant-like sound
                const frequencies = [
                    110,  // A2
                    146.83, // D3
                    164.81, // E3
                    220    // A3
                ];

                ritualState.chantOscillators = [];

                frequencies.forEach((freq, index) => {
                    const osc = audioContext.createOscillator();
                    const gain = audioContext.createGain();

                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(freq, audioContext.currentTime);

                    gain.gain.setValueAtTime(0, audioContext.currentTime);
                    gain.gain.linearRampToValueAtTime(0.05, audioContext.currentTime + 0.5);
                    gain.gain.setValueAtTime(0.05, audioContext.currentTime + 3.5);
                    gain.gain.linearRampToValueAtTime(0, audioContext.currentTime + 4);

                    osc.connect(gain);
                    gain.connect(masterGain);

                    osc.start(audioContext.currentTime + index * 0.1);
                    osc.stop(audioContext.currentTime + 4);

                    ritualState.chantOscillators.push({ osc, gain });
                });
            } catch(e) {
                console.warn('Could not play ritual chant:', e);
            }
        }

        function stopRitualChant() {
            ritualState.chantOscillators.forEach(({ osc, gain }) => {
                try {
                    osc.stop();
                } catch(e) {
                    // Already stopped
                }
            });
            ritualState.chantOscillators = [];
        }

        function createRitualTrailPoint(x, y) {
            if (ritualState.trailPoints.length > 20) return; // Limit trail points

            const point = document.createElement('div');
            point.className = 'ritual-trail-point';
            point.style.left = x + 'px';
            point.style.top = y + 'px';

            viewport.appendChild(point);
            ritualState.trailPoints.push(point);

            setTimeout(() => {
                point.remove();
                const index = ritualState.trailPoints.indexOf(point);
                if (index > -1) ritualState.trailPoints.splice(index, 1);
            }, 2000);
        }

        function updateRitualMastery() {
            // Calculate mastery level based on completions
            const completions = ritualState.totalCompletions;

            if (completions >= 100) {
                ritualState.masteryLevel = 100;
                ritualState.masteryLevelName = 'Grandmaster';
            } else if (completions >= 50) {
                ritualState.masteryLevel = 75 + ((completions - 50) / 50) * 25;
                ritualState.masteryLevelName = 'Master';
            } else if (completions >= 25) {
                ritualState.masteryLevel = 50 + ((completions - 25) / 25) * 25;
                ritualState.masteryLevelName = 'Adept';
            } else if (completions >= 10) {
                ritualState.masteryLevel = 25 + ((completions - 10) / 15) * 25;
                ritualState.masteryLevelName = 'Apprentice';
            } else {
                ritualState.masteryLevel = (completions / 10) * 25;
                ritualState.masteryLevelName = 'Novice';
            }
        }

        function updateRitualMasteryDisplay() {
            const levelEl = document.getElementById('ritualMasteryLevel');
            const progressFill = document.getElementById('ritualProgressFill');
            const completionCount = document.getElementById('ritualCompletionCount');
            const totalCount = document.getElementById('ritualTotalCount');

            if (levelEl) levelEl.textContent = ritualState.masteryLevelName;
            if (progressFill) progressFill.style.width = ritualState.masteryLevel + '%';

            const discovered = ritualState.discoveredRituals.size;
            const total = Object.keys(ritualState.rituals).length;

            if (completionCount) completionCount.textContent = discovered;
            if (totalCount) totalCount.textContent = total;
        }

        function showSecretRitualHint() {
            const hint = document.getElementById('secretRitualHint');
            if (!hint) return;

            hint.textContent = 'You sense hidden rituals that require specific emotional states...';
            hint.classList.add('visible');

            setTimeout(() => {
                hint.classList.remove('visible');
            }, 5000);
        }

        function openRitualBook() {
            const modal = document.getElementById('ritualBookModal');
            const grid = document.getElementById('ritualGrid');

            if (!modal || !grid) return;

            // Clear existing cards
            grid.innerHTML = '';

            // Generate ritual cards
            Object.values(ritualState.rituals).forEach(ritual => {
                const card = document.createElement('div');
                card.className = 'ritual-card';

                if (ritual.discovered) {
                    card.classList.add('discovered');
                } else {
                    card.classList.add('undiscovered');
                }

                const completionsDisplay = ritual.discovered ?
                    `<div class="ritual-card-completions">${ritual.completions}</div>` : '';

                const displayName = ritual.discovered || !ritual.secret ? ritual.name : '???';
                const displayGesture = ritual.discovered || !ritual.secret ? ritual.gesture : 'Unknown';
                const displayDescription = ritual.discovered || !ritual.secret ? ritual.description : 'Locked ritual - discover its secret';
                const displayEffect = ritual.discovered ? `Effect: ${ritual.effect}` : '';

                card.innerHTML = `
                    ${completionsDisplay}
                    <div class="ritual-card-icon">${ritual.discovered || !ritual.secret ? ritual.icon : '🔒'}</div>
                    <div class="ritual-card-name">${displayName}</div>
                    <div class="ritual-card-gesture">${displayGesture}</div>
                    <div class="ritual-card-description">${displayDescription}</div>
                    ${displayEffect ? `<div class="ritual-card-effect">${displayEffect}</div>` : ''}
                `;

                grid.appendChild(card);
            });

            modal.classList.add('visible');
        }

        function closeRitualBook() {
            const modal = document.getElementById('ritualBookModal');
            if (modal) modal.classList.remove('visible');
        }

        function saveRitualData() {
            const ritualData = {
                masteryLevel: ritualState.masteryLevel,
                totalCompletions: ritualState.totalCompletions,
                discoveredRituals: Array.from(ritualState.discoveredRituals),
                ritualHistory: ritualState.ritualHistory,
                rituals: {}
            };

            // Save each ritual's discovered state and completions
            Object.keys(ritualState.rituals).forEach(key => {
                ritualData.rituals[key] = {
                    discovered: ritualState.rituals[key].discovered,
                    completions: ritualState.rituals[key].completions
                };
            });

            localStorage.setItem(APP_NAME + '-rituals', JSON.stringify(ritualData));
        }
```

---

## STEP 5: Integrate Ritual Mode into Existing Functions

**Location**: Various integration points throughout the code

### 5.1: Update the mousemove event handler

Find the existing viewport mousemove handler (around line 11000-11500) and add ritual tracking:

```javascript
        viewport.addEventListener('mousemove', (e) => {
            // ... existing code ...

            // RITUAL MODE: Track movement
            trackRitualMovement(e.clientX, e.clientY);

            // ... rest of existing code ...
        });
```

### 5.2: Update the exportData function

Find the exportData function (around line 8120) and update it to include ritual data:

```javascript
        function exportData() {
            // ... existing code ...

            const dataStr = JSON.stringify({
                sessionHistory: state.sessionHistory,
                sensoryReport: sensoryReport,
                behaviorModel: state.behaviorModel,
                currentSession: {
                    actions: state.actions,
                    predictions: state.predictions,
                    divergenceScore: state.divergenceScore,
                    metaObservations: state.metaObservations,
                    emotionState: state.emotionState
                },
                biometrics: {
                    // ... existing biometrics code ...
                },
                fingerprintImage: fingerprintDataURL,
                shadowProfile: ShadowSelf.getShadowProfile(),
                existentialCrisis: {
                    // ... existing existential crisis code ...
                },
                // ADD THIS: Ritual data
                ritualData: {
                    masteryLevel: ritualState.masteryLevel,
                    masteryLevelName: ritualState.masteryLevelName,
                    totalCompletions: ritualState.totalCompletions,
                    discoveredRituals: Array.from(ritualState.discoveredRituals),
                    ritualHistory: ritualState.ritualHistory,
                    ritualCompletionsByType: Object.keys(ritualState.rituals).reduce((acc, key) => {
                        const ritual = ritualState.rituals[key];
                        if (ritual.discovered) {
                            acc[ritual.name] = ritual.completions;
                        }
                        return acc;
                    }, {})
                }
            }, null, 2);

            // ... rest of existing code ...
        }
```

### 5.3: Add event listener for ritual toggle button

Find the section where other event listeners are added (around line 11500-12000) and add:

```javascript
        // Ritual Mode toggle
        const ritualToggleBtn = document.getElementById('ritualToggle');
        if (ritualToggleBtn) {
            ritualToggleBtn.addEventListener('click', toggleRitualMode);
        }

        // Close ritual book on escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                const modal = document.getElementById('ritualBookModal');
                if (modal && modal.classList.contains('visible')) {
                    closeRitualBook();
                }
            }
        });
```

### 5.4: Initialize ritual mastery display on load

Find the initialization code section (around line 12500-12800) and add:

```javascript
        // Initialize ritual mastery display if rituals were already discovered
        if (ritualState.discoveredRituals.size > 0) {
            updateRitualMasteryDisplay();
            const ritualMasteryDisplay = document.getElementById('ritualMasteryDisplay');
            if (ritualMasteryDisplay && ritualState.enabled) {
                ritualMasteryDisplay.style.display = 'block';
            }
        }
```

---

## Testing the Implementation

After adding all the code:

1. **Open the application** in a modern browser (Chrome, Firefox, or Edge)
2. **Click "Begin Observation"**
3. **Enable Ritual Mode** by clicking the ritual toggle button
4. **Test each ritual**:
   - **Circle 3x**: Move cursor in 3 clockwise circles
   - **Spiral inward**: Start at edge and spiral toward center
   - **Pentagram**: Draw a star shape with 5 points
   - **Figure-8**: Draw a figure-eight pattern
   - **Swipe out**: Start at center, swipe outward quickly
   - **Hold still**: Don't move for 5+ seconds
   - **Zigzag**: Make quick erratic zigzag movements
   - **Sine wave**: Move cursor in smooth wave pattern
   - **Secret rituals**: Trigger specific emotional states

5. **Check the Ritual Book** by clicking "View Ritual Book"
6. **Export data** to verify ritual history is included

---

## Troubleshooting

- **Patterns not detecting**: Try making more exaggerated movements
- **Ceremony not appearing**: Check browser console for errors
- **Audio not working**: Click anywhere on page first to enable audio context
- **Styles not showing**: Verify CSS was added in correct location
- **Functions not working**: Check for JavaScript syntax errors in console

---

## Notes

- The implementation is approximately **1,200 lines of code** total
- All rituals are saved to localStorage automatically
- Mastery levels unlock as you complete more rituals
- Secret rituals require specific emotional states detected by the existing emotion tracking system
- The ritual system integrates seamlessly with existing features (shadow self, time dilation, existential crisis, etc.)

---

## File Locations Summary

1. **CSS**: Before line 3843 (before `</style>`)
2. **HTML (sidebar)**: After line 4868 (after shadow personality panel)
3. **HTML (viewport)**: Around line 3565-3600 (inside simulation-viewport)
4. **HTML (modal)**: Before line 4995 (before `</body>`)
5. **JavaScript state**: After line 5223 (after shadow state)
6. **JavaScript functions**: After state definitions (around line 5400)
7. **Integration points**: Various locations as specified in Step 5

---

## Completion

Once all code is added, you'll have a fully functional Ritual Mode with:
- ✅ 10 unique rituals with gesture detection
- ✅ Ancient mystical visual aesthetic
- ✅ Candle particles and rune animations
- ✅ Web Audio chanting sounds
- ✅ System effects that modify application behavior
- ✅ Ritual Book UI showing progress
- ✅ Mastery level tracking
- ✅ Secret emotional rituals
- ✅ Complete data persistence and export

**The Ritual Mode is now complete!**
