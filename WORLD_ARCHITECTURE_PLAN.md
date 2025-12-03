# World Architecture Refactor Plan

## Current Problem
The game engine has **hardcoded content** mixed with **world seed overrides**. This creates:
- Constant "skip if customOnly" checks scattered everywhere
- Lane towers, creeps, structures spawning even when disabled
- Custom worlds fighting against default behavior instead of defining their own

## Vision
**The game engine should be a blank canvas.** ALL content comes from world seeds:
- No hardcoded lanes, towers, creeps, structures
- Default gameplay is just another world seed (`default-world.json`)
- Custom worlds define 100% of their content
- Engine only renders what the seed specifies

---

## Phase 1: Immediate Fix (Nexus Plaza Working)
**Goal:** Make `customOnly: true` actually work by preventing ALL hardcoded spawning

### Tasks:
1. [ ] Add master guard at game initialization that checks `WORLD_SYSTEMS`
2. [ ] Create `CONTENT_SYSTEMS` object that tracks what should spawn
3. [ ] Guard ALL spawning functions:
   - `spawnInitialLaneTowers()`
   - `initCreepWaveSystem()`
   - `spawnShip()`
   - `createBarracks()`
   - `spawnPlatforms()`
   - `generateProps()` (trees, rocks)
   - `initializeLaneSupport()`
4. [ ] Ensure custom objects spawn AFTER all cleanup passes
5. [ ] Test Nexus Plaza shows ONLY fountain

---

## Phase 2: Extract Default Content to Seed
**Goal:** Move all hardcoded content to `default-world.json`

### Create `data/public-worlds/seeds/default-world.json`:
```json
{
  "worldId": "default-world",
  "config": {
    "name": "Procedural World",
    "biome": "Terra"
  },
  "systems": {
    "mobs": true,
    "creeps": true,
    "towerDefense": true,
    "creepWaves": true,
    "ship": true,
    "trees": true,
    "rocks": true,
    "water": true
  },
  "lanes": {
    "top": {
      "color": "#00ff00",
      "waypoints": [...],
      "towers": {
        "robot": [{ "segment": 0, "offset": 0.2 }, ...],
        "hostile": [{ "segment": 5, "offset": 0.7 }, ...]
      }
    },
    "mid": { ... },
    "bot": { ... }
  },
  "creepWaves": {
    "interval": 30000,
    "types": ["basic", "fast", "tank"],
    "scaling": { "healthPerWave": 1.1, "countPerWave": 1 }
  },
  "structures": {
    "ship": { "position": { "x": 0, "y": 5, "z": 0 } },
    "barracks": [...],
    "spawnPlatforms": [...]
  },
  "terrain": {
    "heightScale": 1.0,
    "water": true,
    "props": { "treeDensity": 0.04, "rockDensity": 0.04 }
  }
}
```

### Tasks:
1. [ ] Create `default-world.json` with current hardcoded values
2. [ ] Create lane schema in world seeds
3. [ ] Create creep wave schema in world seeds
4. [ ] Create structure placement schema
5. [ ] Load default seed when no custom seed is active

---

## Phase 3: Refactor Engine to be Content-Agnostic
**Goal:** Engine reads ALL content from active world seed

### Architecture:
```
┌─────────────────────────────────────────────────────────┐
│                    GAME ENGINE                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Renderer  │  │   Physics   │  │   Input     │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│                         │                               │
│              ┌──────────▼──────────┐                   │
│              │   WORLD LOADER      │                   │
│              │  (reads seed JSON)  │                   │
│              └──────────┬──────────┘                   │
│                         │                               │
│    ┌────────────────────┼────────────────────┐         │
│    ▼                    ▼                    ▼         │
│ ┌──────┐          ┌──────────┐         ┌─────────┐    │
│ │Terrain│          │Structures│         │Entities │    │
│ │Spawner│          │ Spawner  │         │ Spawner │    │
│ └──────┘          └──────────┘         └─────────┘    │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │    WORLD SEED       │
              │   (JSON config)     │
              │                     │
              │ - terrain config    │
              │ - custom objects    │
              │ - lanes (optional)  │
              │ - waves (optional)  │
              │ - structures        │
              │ - agents/NPCs       │
              │ - lore/secrets      │
              └─────────────────────┘
```

### Tasks:
1. [ ] Create `WorldLoader` class that parses seed and spawns content
2. [ ] Move lane definitions from code to seed
3. [ ] Move creep wave logic to read from seed
4. [ ] Move structure spawning to read from seed
5. [ ] Move prop generation to read from seed
6. [ ] Remove all hardcoded content from main game loop

---

## Phase 4: World Seed Schema
**Goal:** Define complete schema for world customization

### Schema Categories:

#### 1. Config (basic world settings)
```json
{
  "config": {
    "name": "string",
    "biome": "Terra|Desert|Ice|Volcanic|Alien|Ocean",
    "gravity": 1.0,
    "timeOfDay": 0.5,
    "timeFrozen": false,
    "maxPlayers": 20,
    "pvpEnabled": false
  }
}
```

#### 2. Systems (feature toggles)
```json
{
  "systems": {
    "mobs": true,
    "creeps": true,
    "towerDefense": true,
    "creepWaves": true,
    "combat": true,
    "building": true,
    "resources": true,
    "customOnly": false
  }
}
```

#### 3. Terrain
```json
{
  "terrain": {
    "seed": "string",
    "heightScale": 1.0,
    "flattenAll": false,
    "noWater": false,
    "baseHeight": 2,
    "props": {
      "trees": true,
      "rocks": true,
      "treeDensity": 0.04,
      "rockDensity": 0.04
    }
  }
}
```

#### 4. Visuals
```json
{
  "visuals": {
    "skyColor": "#87CEEB",
    "fogColor": "#ffffff",
    "fogDensity": 0.01,
    "ambientColor": "#404040",
    "ambientIntensity": 0.6,
    "sunColor": "#ffffff",
    "sunIntensity": 1.0
  }
}
```

#### 5. Custom Objects
```json
{
  "customObjects": [
    {
      "type": "cylinder|sphere|box|cone|torus|plane|light-point|light-spot",
      "position": { "x": 0, "y": 0, "z": 0 },
      "rotation": { "x": 0, "y": 0, "z": 0 },
      "scale": { "x": 1, "y": 1, "z": 1 },
      "color": "#ffffff",
      "emissive": "#000000",
      "emissiveIntensity": 0,
      "opacity": 1.0,
      "metalness": 0.1,
      "roughness": 0.5
    }
  ]
}
```

#### 6. Lanes (Tower Defense)
```json
{
  "lanes": {
    "top": {
      "enabled": true,
      "color": "#00ff00",
      "waypoints": [
        { "x": -100, "z": -80 },
        { "x": 100, "z": -80 }
      ],
      "towers": {
        "teamA": [{ "segment": 0, "offset": 0.2, "type": "basic" }],
        "teamB": [{ "segment": 5, "offset": 0.7, "type": "basic" }]
      }
    }
  }
}
```

#### 7. Creep Waves
```json
{
  "creepWaves": {
    "enabled": true,
    "interval": 30000,
    "waves": [
      { "count": 5, "type": "basic", "lane": "all" },
      { "count": 3, "type": "fast", "lane": "mid" }
    ],
    "scaling": {
      "healthMultiplier": 1.1,
      "countIncrease": 1
    }
  }
}
```

#### 8. Agents/NPCs
```json
{
  "agents": [
    {
      "name": "The Greeter",
      "position": { "x": 10, "y": 2, "z": 10 },
      "personality": "friendly",
      "dialogue": ["Welcome, traveler!", "This is the Nexus Plaza."],
      "appearance": { "color": "#gold", "scale": 1.2 }
    }
  ]
}
```

---

## Phase 5: Planet Builder Tool
**Goal:** Visual editor for creating world seeds

### Features:
1. [ ] 3D preview of world
2. [ ] All config options with visual controls
3. [ ] Drag-and-drop custom object placement
4. [ ] Lane editor with waypoint drawing
5. [ ] Import/export JSON
6. [ ] Template presets (Flat Plaza, Tower Defense, Mars Desert, etc.)
7. [ ] Validation before export
8. [ ] GitHub sharing instructions

---

## Implementation Order

### Sprint 1: Make Custom Worlds Work (TODAY)
1. Add master `WORLD_SYSTEMS` guard to all spawners
2. Fix custom object spawning
3. Test Nexus Plaza

### Sprint 2: Extract Default Content
1. Create `default-world.json`
2. Move lane definitions to seed
3. Move tower positions to seed
4. Move creep wave config to seed

### Sprint 3: Engine Refactor
1. Create `WorldLoader` class
2. Refactor spawners to read from seed
3. Remove hardcoded content

### Sprint 4: Planet Builder
1. Create HTML tool
2. Add 3D preview
3. Add all editors
4. Test full workflow

---

## Success Criteria

- [ ] Nexus Plaza loads with ONLY the fountain (no towers, no lanes, no creeps)
- [ ] Crimson Wastes loads with Mars terrain (no water, red sky)
- [ ] Default world loads with full tower defense gameplay
- [ ] Planet Builder can create and export valid world seeds
- [ ] Exported seeds load correctly in game
