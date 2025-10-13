# WoWmon Competitive PvP - System Architecture

**Agent 6: Competitive Strategy - Technical Architecture**

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        WOWMON PVP SYSTEM                            │
│                     (Competitive Multiplayer)                        │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
        ▼                         ▼                         ▼
┌──────────────┐        ┌──────────────────┐      ┌──────────────┐
│ TEAM BUILDER │        │  BATTLE ENGINE   │      │   RANKING    │
│              │        │                  │      │              │
│ • Composer   │───────▶│ • Damage Calc   │      │ • ELO System │
│ • Validator  │        │ • Turn Logic    │      │ • Tiers      │
│ • Meta Tools │        │ • Status Effects│◀─────│ • Leaderboard│
└──────────────┘        └──────────────────┘      └──────────────┘
        │                         │                         │
        │                         │                         │
        ▼                         ▼                         ▼
┌──────────────┐        ┌──────────────────┐      ┌──────────────┐
│ MATCHMAKING  │◀──────▶│  MULTIPLAYER     │      │   REPLAY     │
│              │        │                  │      │              │
│ • Queue      │        │ • WebSocket     │      │ • Save/Load  │
│ • ELO Match  │        │ • P2P Protocol  │      │ • Analysis   │
│ • Anti-Smurf │        │ • Sync Engine   │      │ • Sharing    │
└──────────────┘        └──────────────────┘      └──────────────┘
        │                         │                         │
        └─────────────────────────┼─────────────────────────┘
                                  │
                                  ▼
                        ┌──────────────────┐
                        │   ANTI-CHEAT     │
                        │                  │
                        │ • Server Verify  │
                        │ • Pattern Detect │
                        │ • Fair Play Score│
                        └──────────────────┘
```

---

## Component Architecture

### 1. Team Builder Flow

```
┌─────────────┐
│   USER      │
│  SELECTS    │
│  CREATURES  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│         TEAM COMPOSITION                │
│                                         │
│  ┌────┐ ┌────┐ ┌────┐                 │
│  │ C1 │ │ C2 │ │ C3 │ ... (max 6)     │
│  └────┘ └────┘ └────┘                 │
└──────┬──────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│       VALIDATION ENGINE                 │
│                                         │
│  1. Species Clause Check                │
│  2. Tier Legality Check                 │
│  3. Type Coverage Analysis              │
│  4. Team Balance Scoring                │
└──────┬──────────────────────────────────┘
       │
       ├───▶ [LEGAL] ──────┐
       │                   │
       └───▶ [ILLEGAL] ────┼──▶ Show Errors
                           │
                           ▼
                 ┌──────────────────┐
                 │   READY FOR      │
                 │   BATTLE         │
                 └──────────────────┘
```

### 2. Battle Turn Flow

```
       PLAYER 1              SERVER              PLAYER 2
          │                    │                    │
          │  Submit Action 1   │                    │
          ├───────────────────▶│                    │
          │                    │  Submit Action 2   │
          │                    │◀───────────────────┤
          │                    │                    │
          │                    ▼                    │
          │           ┌──────────────┐             │
          │           │ DETERMINE    │             │
          │           │ ACTION ORDER │             │
          │           │              │             │
          │           │ 1. Switches  │             │
          │           │ 2. Priority  │             │
          │           │ 3. Speed     │             │
          │           └──────┬───────┘             │
          │                    │                    │
          │                    ▼                    │
          │           ┌──────────────┐             │
          │           │ EXECUTE      │             │
          │           │ ACTIONS      │             │
          │           │              │             │
          │           │ • Damage Calc│             │
          │           │ • Status FX  │             │
          │           │ • Field FX   │             │
          │           └──────┬───────┘             │
          │                    │                    │
          │                    ▼                    │
          │           ┌──────────────┐             │
          │           │ VALIDATE     │             │
          │           │ RESULTS      │             │
          │           │              │             │
          │           │ (Anti-Cheat) │             │
          │           └──────┬───────┘             │
          │                    │                    │
          │   Battle State     │   Battle State     │
          │◀───────────────────┼───────────────────▶│
          │                    │                    │
          ▼                    ▼                    ▼
      [UPDATE UI]         [LOG TURN]          [UPDATE UI]
```

### 3. Damage Calculation Pipeline

```
INPUT:
┌──────────────────────────────────────────┐
│ Attacker: { level, attack, types }      │
│ Defender: { defense, hp, types }        │
│ Move: { power, type, category }         │
│ Field: { weather, terrain, hazards }    │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│ STEP 1: BASE DAMAGE                     │
│ = ((2×Lvl/5+2) × Pow × Atk/Def / 50)+2 │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│ STEP 2: WEATHER MODIFIER                │
│ × 1.5 (Sun+Fire, Rain+Water)           │
│ × 0.5 (Sun+Water, Rain+Fire)           │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│ STEP 3: CRITICAL HIT                    │
│ × 1.5 (12.5% chance)                    │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│ STEP 4: RANDOM FACTOR                   │
│ × (0.85 to 1.00)                        │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│ STEP 5: STAB                            │
│ × 1.5 (same type)                       │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│ STEP 6: TYPE EFFECTIVENESS              │
│ × 2.0 (super effective)                 │
│ × 0.5 (not very effective)              │
│ × 0.0 (no effect)                       │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│ STEP 7: ITEM MODIFIERS                  │
│ × 1.3 (Life Orb)                        │
│ × 1.5 (Choice Band/Specs)              │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│ STEP 8: SCREENS                         │
│ × 0.5 (Reflect/Light Screen)           │
└──────────┬───────────────────────────────┘
           │
           ▼
OUTPUT:
┌──────────────────────────────────────────┐
│ Final Damage = max(1, calculated)       │
│ + Metadata: effectiveness, crit, etc.   │
└──────────────────────────────────────────┘
```

### 4. Matchmaking Flow

```
PLAYER JOINS QUEUE
       │
       ▼
┌─────────────────────┐
│ QUEUE ENTRY         │
│                     │
│ • Player ID         │
│ • Rating: 1500      │
│ • Hidden MMR: 1520  │
│ • Region: NA        │
│ • Latency: 40ms     │
│ • Team: [...]       │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│ SEARCH FOR MATCH (Every 2 sec)         │
│                                         │
│ Time = 0s:   ±200 ELO                  │
│ Time = 30s:  ±250 ELO                  │
│ Time = 60s:  ±300 ELO                  │
│ Time = 90s:  ±350 ELO                  │
│ ...                                     │
│ Time = 300s: TIMEOUT                   │
└──────┬──────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│ SCORE OPPONENTS                         │
│                                         │
│ For each candidate:                     │
│   score = 1000 - rating_diff            │
│   if low_latency: score += 200          │
│   if same_region: score += 100          │
│   score -= wait_time_diff / 1000        │
└──────┬──────────────────────────────────┘
       │
       ├─▶ [MATCH FOUND] ──┐
       │                   │
       └─▶ [NO MATCH] ─────┼─▶ Continue searching
                           │
                           ▼
                 ┌──────────────────┐
                 │ CREATE BATTLE    │
                 │                  │
                 │ P1 vs P2         │
                 │ Format: Singles  │
                 │ Server: US-WEST  │
                 └──────────────────┘
```

### 5. Tournament Bracket (Single Elimination)

```
ROUND 1          ROUND 2       FINALS        WINNER

P1  ┐
    ├─► W1  ┐
P2  ┘       │
            ├─► W5  ┐
P3  ┐       │       │
    ├─► W2  ┘       │
P4  ┘               ├─► W7  ──────► CHAMPION
                    │
P5  ┐               │
    ├─► W3  ┐       │
P6  ┘       │       │
            ├─► W6  ┘
P7  ┐       │
    ├─► W4  ┘
P8  ┘

Seeding Order: 1v8, 4v5, 2v7, 3v6
```

### 6. Replay System Architecture

```
                    BATTLE IN PROGRESS
                           │
                           ▼
                 ┌──────────────────┐
                 │ LOG EVERY TURN   │
                 │                  │
                 │ • Actions        │
                 │ • Damage         │
                 │ • RNG Seed       │
                 │ • Timestamps     │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ COMPRESS DATA    │
                 │                  │
                 │ Delta Encoding   │
                 │ (Only Changes)   │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ SAVE REPLAY      │
                 │                  │
                 │ IndexedDB /      │
                 │ LocalStorage     │
                 └────────┬─────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   PLAYBACK   │  │   ANALYSIS   │  │    SHARE     │
│              │  │              │  │              │
│ • Controls   │  │ • Stats      │  │ • QR Code    │
│ • Speed      │  │ • Mistakes   │  │ • Link       │
│ • Seek       │  │ • Critical   │  │ • Embed      │
└──────────────┘  └──────────────┘  └──────────────┘
```

### 7. Anti-Cheat Validation Flow

```
           CLIENT SUBMITS ACTION
                    │
                    ▼
           ┌──────────────────┐
           │ SERVER RECEIVES  │
           │ ACTION PACKET    │
           └────────┬─────────┘
                    │
                    ▼
           ┌──────────────────────────────┐
           │ VALIDATION CHECKS            │
           │                              │
           │ ✓ Is move legal?             │
           │ ✓ Is PP available?           │
           │ ✓ Is timing normal?          │
           │ ✓ Is action possible?        │
           └────────┬─────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
   [VALID]                 [INVALID]
        │                       │
        ▼                       ▼
┌──────────────┐      ┌──────────────────┐
│ EXECUTE      │      │ FLAG VIOLATION   │
│ ACTION       │      │                  │
│              │      │ • Log incident   │
└──────┬───────┘      │ • Increment count│
       │              │ • Possible ban   │
       ▼              └──────────────────┘
┌──────────────┐
│ CALCULATE    │
│ RESULT       │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────┐
│ RE-VALIDATE RESULT           │
│                              │
│ • Recalculate damage         │
│ • Compare with claimed       │
│ • Check against range        │
└──────┬───────────────────────┘
       │
       ├─▶ [MATCH] ──────┐
       │                 │
       └─▶ [MISMATCH] ───┼──▶ BAN PLAYER
                         │
                         ▼
                ┌─────────────────┐
                │ SEND RESULT     │
                │ TO BOTH PLAYERS │
                └─────────────────┘
```

---

## Data Flow

### Battle State Synchronization

```
CLIENT A                  SERVER                  CLIENT B
    │                        │                        │
    │    Move: Hydro Pump    │                        │
    ├───────────────────────▶│                        │
    │                        │    Move: Thunder       │
    │                        │◀───────────────────────┤
    │                        │                        │
    │                        ▼                        │
    │              ┌──────────────────┐              │
    │              │ PROCESS TURN     │              │
    │              │                  │              │
    │              │ 1. Order: Speed  │              │
    │              │ 2. Execute Moves │              │
    │              │ 3. Validate      │              │
    │              └────────┬─────────┘              │
    │                        │                        │
    │    Turn Result         │         Turn Result    │
    │◀───────────────────────┼───────────────────────▶│
    │                        │                        │
    │    {                   │                     {  │
    │      turn: 5,          │                turn: 5,│
    │      p1_action: {...}, │          p1_action: {..│
    │      p2_action: {...}, │          p2_action: {..│
    │      damage: 85,       │                damage: │
    │      status: ...       │                status: │
    │    }                   │                     }  │
    │                        │                        │
    ▼                        ▼                        ▼
[UPDATE UI]            [LOG TURN]              [UPDATE UI]
```

### ELO Rating Update

```
                    BATTLE ENDS
                         │
                         ▼
              ┌──────────────────────┐
              │ COLLECT RATINGS      │
              │                      │
              │ Player 1: 1500       │
              │ Player 2: 1600       │
              │ Result: P1 Wins      │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ CALCULATE ELO        │
              │                      │
              │ Expected: 36% chance │
              │ Actual: Win (100%)   │
              │ K-Factor: 32         │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ APPLY CHANGES        │
              │                      │
              │ P1: 1500 → 1520 (+20)│
              │ P2: 1600 → 1580 (-20)│
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ UPDATE LEADERBOARD   │
              │                      │
              │ • Global Rank        │
              │ • Regional Rank      │
              │ • Seasonal Rank      │
              └──────────────────────┘
```

---

## Database Schema

### Player Profile

```
Player {
  id: String (UUID)
  username: String
  rating: Number (ELO)
  hiddenMMR: Number
  rd: Number (Glicko-2)
  volatility: Number (Glicko-2)

  stats: {
    totalBattles: Number
    wins: Number
    losses: Number
    winRate: Number
    currentStreak: Number
    longestStreak: Number
  }

  seasonal: {
    seasonNumber: Number
    seasonRating: Number
    seasonRank: Number
    peakRating: Number
  }

  teams: Array[Team]
  replays: Array[ReplayID]

  fairPlay: {
    score: Number (0-100)
    warnings: Number
    tempBans: Number
    violations: Array[Violation]
  }

  preferences: {
    region: String
    language: String
    notifications: Boolean
  }
}
```

### Team

```
Team {
  id: String (UUID)
  name: String
  format: String (singles/doubles/triples)
  tier: String (OU/UU/RU/NU)

  creatures: Array[6] {
    id: String
    nickname: String
    level: Number
    moves: Array[4] (move IDs)
    item: String
    ability: String
    nature: String
    evs: { hp, atk, def, spa, spd, spe }
    ivs: { hp, atk, def, spa, spd, spe }
  }

  stats: {
    gamesPlayed: Number
    wins: Number
    losses: Number
    avgTurns: Number
  }

  created: Timestamp
  lastUsed: Timestamp
}
```

### Battle

```
Battle {
  id: String (UUID)
  format: String
  tier: String

  players: {
    player1: {
      id: String
      rating: Number
      team: Team
    }
    player2: {
      id: String
      rating: Number
      team: Team
    }
  }

  state: {
    turn: Number
    player1Active: CreatureID
    player2Active: CreatureID
    field: {
      weather: String
      terrain: String
      hazards: Object
    }
  }

  turnHistory: Array[Turn]
  randomSeed: Number

  result: {
    winner: PlayerID
    duration: Number
    turns: Number
    eloChange: { p1: Number, p2: Number }
  }

  validation: {
    isValid: Boolean
    violations: Array
  }

  timestamp: Timestamp
}
```

### Replay

```
Replay {
  id: String (UUID)
  battleId: String

  metadata: {
    date: Timestamp
    format: String
    tier: String
    duration: Number
    turns: Number
  }

  players: {
    player1: { name, rating, team }
    player2: { name, rating, team }
  }

  winner: String

  data: Array[CompressedTurn]
  seed: Number

  stats: {
    views: Number
    rating: Number
    featured: Boolean
  }

  analysis: {
    criticalMoments: Array
    mistakes: Array
    mvp: Object
  }
}
```

---

## Network Protocol

### WebSocket Messages

```javascript
// Client → Server
{
  type: "SUBMIT_ACTION",
  battleId: "battle_123",
  playerId: "player_456",
  turn: 5,
  action: {
    type: "move", // or "switch"
    moveId: "hydro_pump",
    target: 1
  },
  timestamp: 1234567890
}

// Server → Client
{
  type: "TURN_RESULT",
  battleId: "battle_123",
  turn: 5,
  actions: [
    {
      player: 1,
      action: "move",
      moveId: "hydro_pump",
      damage: 85,
      effectiveness: 2.0,
      isCrit: false
    },
    {
      player: 2,
      action: "switch",
      from: "creature_a",
      to: "creature_b"
    }
  ],
  state: {
    player1Active: { hp: 120, status: null },
    player2Active: { hp: 85, status: "burn" },
    field: { weather: "rain", turns: 3 }
  }
}

// Server → Client (Match Found)
{
  type: "MATCH_FOUND",
  battleId: "battle_789",
  opponent: {
    id: "player_999",
    name: "Rival",
    rating: 1550
  },
  server: "US-WEST",
  format: "singles",
  tier: "OU"
}
```

---

## Performance Considerations

### Optimization Targets

```
Metric                  Target          Critical
─────────────────────────────────────────────────
Damage Calculation      < 1ms           < 5ms
Turn Processing         < 100ms         < 500ms
Matchmaking             < 30s           < 5min
UI Update               60 FPS          30 FPS
Network Latency         < 100ms         < 300ms
Replay Load             < 2s            < 10s
Anti-Cheat Validation   < 50ms          < 200ms
```

### Scaling Strategy

```
                    ┌──────────────┐
                    │ LOAD BALANCER│
                    └──────┬───────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ BATTLE       │  │ BATTLE       │  │ BATTLE       │
│ SERVER 1     │  │ SERVER 2     │  │ SERVER 3     │
│              │  │              │  │              │
│ 100 battles  │  │ 100 battles  │  │ 100 battles  │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ CENTRAL DATABASE │
                 │                  │
                 │ • Player Data    │
                 │ • Replay Storage │
                 │ • Leaderboards   │
                 └──────────────────┘
```

---

## Security Measures

### Cheat Prevention Layers

```
LAYER 1: Client-Side          LAYER 2: Server-Side      LAYER 3: Post-Battle
─────────────────────────────────────────────────────────────────────────────
• Input validation            • Action validation       • Replay validation
• Rate limiting               • Damage recalculation    • Pattern analysis
• Obfuscation                 • State verification      • Anomaly detection
                              • Real-time monitoring    • Statistical review
                                                        • Human review (flagged)
```

### Validation Checkpoints

```
 ACTION SUBMITTED
       │
       ▼
 ✓ Is action format valid?
       │
       ▼
 ✓ Is player's turn?
       │
       ▼
 ✓ Is move/switch legal?
       │
       ▼
 ✓ Is PP available?
       │
       ▼
 ✓ Is timing reasonable?
       │
       ▼
 EXECUTE ACTION
       │
       ▼
 ✓ Recalculate damage
       │
       ▼
 ✓ Compare with claimed
       │
       ▼
 ✓ Log for post-analysis
       │
       ▼
 SEND TO CLIENTS
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      PRODUCTION                          │
└─────────────────────────────────────────────────────────┘

┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│   REGION:    │       │   REGION:    │       │   REGION:    │
│   US-WEST    │       │   US-EAST    │       │   EU-WEST    │
│              │       │              │       │              │
│ • Battle Srv │       │ • Battle Srv │       │ • Battle Srv │
│ • WebSocket  │       │ • WebSocket  │       │ • WebSocket  │
│ • 50ms avg   │       │ • 50ms avg   │       │ • 55ms avg   │
└──────┬───────┘       └──────┬───────┘       └──────┬───────┘
       │                      │                      │
       └──────────────────────┼──────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ GLOBAL DATABASE  │
                    │                  │
                    │ MongoDB Cluster  │
                    │ (3 Replicas)     │
                    └──────────────────┘
                              │
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
            ┌──────────────┐    ┌──────────────┐
            │ REDIS CACHE  │    │  S3 STORAGE  │
            │              │    │              │
            │ • Queue      │    │ • Replays    │
            │ • Sessions   │    │ • Backups    │
            └──────────────┘    └──────────────┘
```

---

**Version**: 1.0
**Last Updated**: 2025-10-12
**Author**: Agent 6 - Competitive Strategy
