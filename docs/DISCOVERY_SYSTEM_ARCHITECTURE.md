# Advanced Discovery System Architecture
## Local First Tools Gallery

**Version:** 2.0
**Date:** 2025-10-12
**Status:** Design Specification

---

## Executive Summary

This document outlines the design for an intelligent discovery system that transforms the current random "stumble" feature into a sophisticated recommendation engine that learns from user behavior, understands tool relationships, and provides multiple discovery modes to help users find tools they'll love.

### Current State Analysis

**Existing Implementation:**
- Simple random selection from filtered apps
- Basic category filtering
- Linear history tracking (last 10 items)
- Recent stumbles avoid list (prevents immediate repeats)
- localStorage-based persistence

**Key Limitations:**
- No personalization or learning
- No relationship understanding between tools
- Single discovery mode (random only)
- No preference tracking
- No quality/relevance scoring

---

## System Architecture Overview

### High-Level Components

```
┌─────────────────────────────────────────────────────────┐
│                    Discovery Engine                      │
│  ┌────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │ User       │  │ Tool        │  │ Recommendation  │  │
│  │ Profile    │──│ Relationship│──│ Algorithm       │  │
│  │ Manager    │  │ Graph       │  │ Engine          │  │
│  └────────────┘  └─────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                   ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ localStorage │  │   Session    │  │   Analytics  │
│   Persistent │  │   Temporary  │  │   Metrics    │
│    Profile   │  │     Data     │  │   Tracking   │
└──────────────┘  └──────────────┘  └──────────────┘
```

---

## 1. Data Structures

### 1.1 User Profile Schema

```javascript
{
  version: "2.0",
  userId: "uuid-v4",                    // Anonymous user ID
  created: "2025-10-12T00:00:00Z",      // Profile creation date
  lastUpdated: "2025-10-12T00:00:00Z",  // Last activity

  // User Preferences
  preferences: {
    favoriteCategories: {
      "3d_immersive": 0.85,              // Affinity scores 0-1
      "games_puzzles": 0.72,
      "visual_art": 0.45
    },
    favoriteTags: {
      "3d": 0.90,
      "game": 0.75,
      "animation": 0.65
    },
    complexityPreference: {
      "simple": 0.2,
      "intermediate": 0.5,
      "advanced": 0.3
    },
    interactionTypePreference: {
      "game": 0.6,
      "visual": 0.3,
      "interactive": 0.1
    },

    // Temporal preferences
    timeOfDayPatterns: {
      morning: ["educational_tools", "creative_tools"],
      afternoon: ["games_puzzles", "3d_immersive"],
      evening: ["visual_art", "audio_music"]
    },

    // Behavioral preferences
    discoveryStyle: "explorer",         // explorer, focused, serendipitous
    diversityPreference: 0.5,           // 0 = similar, 1 = diverse
    noveltyPreference: 0.7              // 0 = familiar, 1 = novel
  },

  // Interaction History
  interactions: {
    // Tool filename as key
    "gameoflife.html": {
      viewCount: 15,                     // Number of times viewed
      totalTimeSpent: 3600,              // Seconds
      lastViewed: "2025-10-12T00:00:00Z",
      firstViewed: "2025-10-01T00:00:00Z",
      rated: 5,                          // 1-5 stars (optional)
      pinned: true,                      // User-pinned
      voted: true,                       // Upvoted
      bookmarked: false,                 // Bookmarked
      shared: 2,                         // Times shared

      // Session data
      sessions: [
        {
          timestamp: "2025-10-12T00:00:00Z",
          duration: 300,
          source: "stumble",             // stumble, search, browse, direct
          completed: true                // Did user engage meaningfully?
        }
      ],

      // Engagement signals
      engagement: {
        quickBounce: false,              // <10s view
        deepDive: true,                  // >5min view
        repeatedReturn: true,            // Came back 3+ times
        recommendedToOthers: false
      }
    }
  },

  // Discovery Sessions
  discoverySessions: [
    {
      sessionId: "uuid",
      startTime: "2025-10-12T00:00:00Z",
      endTime: "2025-10-12T01:00:00Z",
      mode: "similar",                   // random, similar, trending, favorites
      theme: "3d_exploration",           // Auto-detected or user-selected
      toolsDiscovered: ["snake3.html", "gameoflife.html"],
      toolsEngaged: ["gameoflife.html"],
      satisfaction: 0.8                  // Inferred from behavior
    }
  ],

  // Favorites & Collections
  favorites: ["gameoflife.html", "drone-simulator.html"],
  collections: {
    "Weekend Projects": ["workshop.html", "physics-playground-lab.html"],
    "Quick Fun": ["snake3.html", "wowMon.html"]
  },

  // Learning & Adaptation
  learningMetrics: {
    explorationScore: 0.75,              // How much they explore
    loyaltyScore: 0.45,                  // How much they revisit
    diversityScore: 0.60,                // How diverse their interests
    engagementScore: 0.80,               // Overall engagement level
    lastCalibration: "2025-10-12T00:00:00Z"
  }
}
```

### 1.2 Tool Relationship Graph

```javascript
{
  version: "1.0",
  lastUpdated: "2025-10-12T00:00:00Z",

  // Tool nodes with enhanced metadata
  tools: {
    "gameoflife.html": {
      // Core metadata (from vibe_gallery_config.json)
      title: "Life Architect: 3D Conway Challenge",
      category: "3d_immersive",
      tags: ["3d", "canvas", "svg", "animation", "game"],
      complexity: "advanced",
      interactionType: "game",
      featured: true,

      // Computed metadata
      popularity: 0.85,                  // Global popularity score
      quality: 0.90,                     // Quality score (from votes, engagement)
      trendingScore: 0.75,               // Recent popularity spike

      // Relationship scores (computed)
      relatedTools: {
        "physics-playground-lab.html": 0.85,  // Similarity score
        "snake3.html": 0.70,
        "feedShyworm4.html": 0.65
      },

      // Feature vectors (for ML-style similarity)
      features: {
        hasWebGL: true,
        hasPhysics: true,
        hasAnimation: true,
        isMultiplayer: false,
        requiresInput: true,
        isEducational: true
      },

      // User statistics (aggregated)
      stats: {
        totalViews: 1250,
        avgSessionDuration: 420,         // Seconds
        returnRate: 0.35,                // % of users who return
        completionRate: 0.65,            // % who spend >5min
        shareRate: 0.12,                 // % who share
        voteCount: 45,
        avgRating: 4.5
      }
    }
  },

  // Precomputed relationship clusters
  clusters: {
    "3d_games": ["gameoflife.html", "snake3.html", "feedShyworm4.html"],
    "physics_simulations": ["physics-playground-lab.html", "gameoflife.html"],
    "retro_gaming": ["gameboy-clone.html", "windows95-emulator.html"]
  },

  // Discovery paths (curated journeys)
  paths: {
    "beginner_3d": {
      name: "3D Graphics Journey",
      description: "Start with simple 3D and progress to complex",
      tools: ["rainbow-svg-path.html", "tile-room-3d.html", "snake3.html", "gameoflife.html"],
      difficulty: "progressive"
    }
  }
}
```

### 1.3 Discovery History

```javascript
{
  version: "1.0",

  // Global discovery history (all users, anonymized)
  globalHistory: {
    "gameoflife.html": {
      discoveryCount: 450,               // Times discovered via stumble
      engagementRate: 0.65,              // % who engaged after discovery
      lastDiscovered: "2025-10-12T00:00:00Z",
      trendingWindows: {
        "hourly": 12,                    // Discoveries in last hour
        "daily": 45,                     // Discoveries today
        "weekly": 180                    // Discoveries this week
      }
    }
  },

  // User-specific discovery history
  userHistory: [
    {
      toolId: "gameoflife.html",
      discoveredAt: "2025-10-12T00:00:00Z",
      discoveryMode: "similar",          // How it was discovered
      discoveryContext: {
        previousTool: "physics-playground-lab.html",
        sessionTheme: "physics_exploration",
        categoryFilter: "3d_immersive"
      },
      outcome: {
        engaged: true,
        duration: 600,
        rated: 5,
        bookmarked: true
      }
    }
  ],

  // Recent context (short-term memory)
  recentContext: {
    lastViewed: ["gameoflife.html", "snake3.html"],
    currentMood: "exploratory",          // Inferred from behavior
    sessionStartTime: "2025-10-12T00:00:00Z",
    toolsInSession: 5,
    avgEngagement: 0.8
  }
}
```

### 1.4 Recommendation Scores

```javascript
{
  // Per-tool recommendation score for current user
  recommendations: {
    "gameoflife.html": {
      score: 0.92,                       // Overall recommendation score
      confidence: 0.85,                  // Confidence in recommendation

      // Score components (for explainability)
      components: {
        contentSimilarity: 0.85,         // Similar to liked content
        collaborativeSignal: 0.75,       // Similar users liked it
        popularityBoost: 0.65,           // Popular globally
        noveltyBoost: 0.90,              // New to user
        diversityPenalty: -0.05,         // Recently saw similar
        qualityBoost: 0.85,              // High quality tool
        contextBoost: 0.70,              // Fits current context
        temporalBoost: 0.60              // Good for time of day
      },

      // Reasoning (for user explanation)
      reasoning: [
        "You enjoyed physics-playground-lab.html",
        "Similar users loved this",
        "High ratings and engagement",
        "Trending this week"
      ],

      // Metadata for display
      expectedEngagement: 0.85,          // Predicted engagement
      estimatedDuration: 420,            // Expected session length
      matchReason: "similar_interests"   // Primary match reason
    }
  }
}
```

---

## 2. Discovery Modes

### 2.1 Random Mode (Enhanced)

**Description:** Improved random discovery with smart filtering

**Algorithm:**
```javascript
function getRandomRecommendation(filters) {
  // 1. Filter available tools
  let candidates = filterTools({
    category: filters.category,
    excludeRecent: true,               // Avoid last 10
    minQuality: 0.3,                   // Quality threshold
    excludeViewed: filters.freshOnly   // Optional: only unseen
  });

  // 2. Apply soft preferences (weighted random)
  let weighted = candidates.map(tool => ({
    tool,
    weight: calculateRandomWeight(tool, userProfile)
  }));

  // 3. Weighted random selection
  return weightedRandomSelect(weighted);
}

function calculateRandomWeight(tool, profile) {
  let weight = 1.0;

  // Boost preferred categories
  if (profile.preferences.favoriteCategories[tool.category]) {
    weight *= (1 + profile.preferences.favoriteCategories[tool.category] * 0.5);
  }

  // Boost preferred complexity
  if (profile.preferences.complexityPreference[tool.complexity]) {
    weight *= (1 + profile.preferences.complexityPreference[tool.complexity] * 0.3);
  }

  // Novelty boost (never seen)
  if (!profile.interactions[tool.filename]) {
    weight *= (1 + profile.preferences.noveltyPreference * 0.8);
  }

  // Quality boost
  weight *= (0.5 + tool.quality * 0.5);

  return weight;
}
```

### 2.2 Similar Mode

**Description:** Find tools similar to what you like

**Algorithm:**
```javascript
function getSimilarRecommendation(options) {
  // 1. Get user's favorite tools
  let favorites = getUserFavoriteTools(userProfile, topN = 10);

  // 2. Get similar tools for each favorite
  let similarSets = favorites.map(fav =>
    toolGraph.relatedTools[fav.filename]
  );

  // 3. Aggregate and score
  let candidates = aggregateSimilarTools(similarSets);

  // 4. Filter and rank
  let ranked = candidates
    .filter(tool => !recentlyViewed(tool))
    .map(tool => ({
      tool,
      score: calculateSimilarityScore(tool, favorites, userProfile)
    }))
    .sort((a, b) => b.score - a.score);

  // 5. Select with controlled randomness
  return selectWithVariety(ranked, temperature = 0.3);
}

function calculateSimilarityScore(tool, favorites, profile) {
  let score = 0;

  // Content-based similarity
  favorites.forEach(fav => {
    let similarity = toolGraph.relatedTools[fav.filename][tool.filename] || 0;
    let favWeight = profile.interactions[fav.filename].engagementScore || 1;
    score += similarity * favWeight;
  });

  // Normalize
  score /= favorites.length;

  // Apply modifiers
  score *= (0.7 + tool.quality * 0.3);              // Quality boost
  score *= (1 - profile.learningMetrics.diversityScore * 0.2); // Diversity adjustment

  return score;
}
```

### 2.3 Trending Mode

**Description:** Discover what's hot right now

**Algorithm:**
```javascript
function getTrendingRecommendation(timeWindow = "daily") {
  // 1. Get trending tools
  let trending = getTrendingTools(timeWindow)
    .filter(tool => !recentlyViewed(tool))
    .map(tool => ({
      tool,
      score: calculateTrendingScore(tool, timeWindow, userProfile)
    }))
    .sort((a, b) => b.score - a.score);

  // 2. Select with personalization
  return selectWithPersonalization(trending);
}

function calculateTrendingScore(tool, timeWindow, profile) {
  let score = tool.trendingScore;

  // Adjust for user preferences
  if (profile.preferences.favoriteCategories[tool.category]) {
    score *= (1 + profile.preferences.favoriteCategories[tool.category] * 0.5);
  }

  // Adjust for quality
  score *= (0.6 + tool.quality * 0.4);

  // Novelty bonus (if unseen)
  if (!profile.interactions[tool.filename]) {
    score *= 1.3;
  }

  return score;
}
```

### 2.4 Favorites Mode

**Description:** Rediscover your favorites and similar gems

**Algorithm:**
```javascript
function getFavoritesRecommendation() {
  // 1. Get user's top tools
  let topTools = Object.entries(profile.interactions)
    .filter(([_, data]) => data.engagementScore > 0.7)
    .sort((a, b) => b[1].engagementScore - a[1].engagementScore)
    .slice(0, 20);

  // 2. Mix of revisit + similar
  let recommendations = [];

  // 30% chance to revisit a favorite (if not recent)
  if (Math.random() < 0.3) {
    let revisit = topTools
      .filter(([file, data]) => !wasRecentlyViewed(file, days = 7))
      .map(([file, data]) => ({
        tool: getToolData(file),
        score: data.engagementScore,
        reason: "revisit_favorite"
      }));
    recommendations.push(...revisit);
  }

  // 70% chance to find similar to favorites
  let similar = topTools.flatMap(([file, data]) =>
    toolGraph.relatedTools[file]
      .filter(relFile => !profile.interactions[relFile])
      .map(relFile => ({
        tool: getToolData(relFile),
        score: toolGraph.relatedTools[file][relFile] * data.engagementScore,
        reason: `similar_to_${file}`
      }))
  );
  recommendations.push(...similar);

  // 3. Sort and select
  return recommendations
    .sort((a, b) => b.score - a.score)
    .slice(0, 1)[0];
}
```

### 2.5 Discovery Paths (Guided Mode)

**Description:** Curated journeys through related tools

**Algorithm:**
```javascript
function getPathRecommendation(pathId = null) {
  // 1. If no path specified, find best path
  if (!pathId) {
    pathId = findBestPath(userProfile);
  }

  // 2. Get path data
  let path = toolGraph.paths[pathId];

  // 3. Find next tool in path
  let completedTools = path.tools.filter(tool =>
    profile.interactions[tool]?.completed
  );

  let nextTool = path.tools[completedTools.length];

  // 4. Return with context
  return {
    tool: getToolData(nextTool),
    context: {
      pathName: path.name,
      pathDescription: path.description,
      progress: completedTools.length / path.tools.length,
      remainingTools: path.tools.length - completedTools.length
    }
  };
}

function findBestPath(profile) {
  // Find path that matches user interests and has some progress
  let paths = Object.entries(toolGraph.paths)
    .map(([id, path]) => ({
      id,
      path,
      score: scorePathRelevance(path, profile)
    }))
    .sort((a, b) => b.score - a.score);

  return paths[0].id;
}
```

### 2.6 Surprise Me Mode

**Description:** Wildcard recommendations outside comfort zone

**Algorithm:**
```javascript
function getSurpriseRecommendation() {
  // 1. Find underexplored categories
  let unexplored = findUnexploredCategories(userProfile);

  // 2. Select random underexplored category
  let category = unexplored[Math.floor(Math.random() * unexplored.length)];

  // 3. Get high-quality tool from that category
  let candidates = getToolsByCategory(category)
    .filter(tool => !profile.interactions[tool.filename])
    .filter(tool => tool.quality > 0.6)
    .sort((a, b) => b.quality - a.quality);

  // 4. Select from top candidates
  return candidates[Math.floor(Math.random() * Math.min(5, candidates.length))];
}

function findUnexploredCategories(profile) {
  let allCategories = Object.keys(vibeGalleryConfig.categories);

  return allCategories.filter(cat => {
    let affinity = profile.preferences.favoriteCategories[cat] || 0;
    return affinity < 0.3;  // Low exposure
  });
}
```

---

## 3. Recommendation Algorithm Core

### 3.1 Master Recommendation Engine

```javascript
class RecommendationEngine {
  constructor(userProfile, toolGraph, discoveryHistory) {
    this.profile = userProfile;
    this.graph = toolGraph;
    this.history = discoveryHistory;
  }

  /**
   * Get next recommendation based on mode and context
   */
  getRecommendation(mode, options = {}) {
    switch (mode) {
      case 'random':
        return this.getRandomRecommendation(options);
      case 'similar':
        return this.getSimilarRecommendation(options);
      case 'trending':
        return this.getTrendingRecommendation(options);
      case 'favorites':
        return this.getFavoritesRecommendation(options);
      case 'path':
        return this.getPathRecommendation(options);
      case 'surprise':
        return this.getSurpriseRecommendation(options);
      default:
        return this.getSmartRecommendation(options);
    }
  }

  /**
   * Smart mode: Auto-select best discovery mode
   */
  getSmartRecommendation(options) {
    let context = this.analyzeContext();

    // Decide mode based on context
    let mode;
    if (context.isNewUser) {
      mode = 'random';                   // Explore widely
    } else if (context.hasStrongPreferences) {
      mode = 'similar';                  // Cater to preferences
    } else if (context.isBoredSignals) {
      mode = 'surprise';                 // Shake things up
    } else if (context.hasActivePath) {
      mode = 'path';                     // Continue journey
    } else {
      mode = this.selectBalancedMode();  // Balanced exploration
    }

    return this.getRecommendation(mode, options);
  }

  /**
   * Analyze user context
   */
  analyzeContext() {
    return {
      isNewUser: Object.keys(this.profile.interactions).length < 5,
      hasStrongPreferences: this.profile.learningMetrics.loyaltyScore > 0.7,
      isBoredSignals: this.detectBoredSignals(),
      hasActivePath: this.hasActiveDiscoveryPath(),
      sessionDuration: this.getCurrentSessionDuration(),
      toolsInSession: this.getToolsViewedInSession(),
      timeOfDay: this.getTimeOfDay(),
      dayOfWeek: this.getDayOfWeek()
    };
  }

  /**
   * Detect if user is showing bored signals
   */
  detectBoredSignals() {
    let recentSessions = this.history.userHistory.slice(-5);

    // Check for quick bounces
    let quickBounces = recentSessions.filter(s => s.outcome.duration < 30).length;

    // Check for repetitive behavior
    let uniqueCategories = new Set(
      recentSessions.map(s => this.graph.tools[s.toolId].category)
    ).size;

    return quickBounces > 3 || uniqueCategories < 2;
  }

  /**
   * Select mode with balanced exploration-exploitation
   */
  selectBalancedMode() {
    let explorationScore = this.profile.learningMetrics.explorationScore;
    let noveltyPref = this.profile.preferences.noveltyPreference;

    // Weighted random mode selection
    let modes = [
      { mode: 'similar', weight: 0.4 + (1 - explorationScore) * 0.2 },
      { mode: 'trending', weight: 0.2 },
      { mode: 'random', weight: 0.2 + explorationScore * 0.2 },
      { mode: 'surprise', weight: 0.1 + noveltyPref * 0.2 },
      { mode: 'favorites', weight: 0.1 }
    ];

    return weightedRandomSelect(modes);
  }
}
```

### 3.2 Personalization Engine

```javascript
class PersonalizationEngine {
  /**
   * Update user profile based on interaction
   */
  recordInteraction(toolId, interaction) {
    // 1. Update interaction record
    if (!this.profile.interactions[toolId]) {
      this.profile.interactions[toolId] = this.createInteractionRecord();
    }

    let record = this.profile.interactions[toolId];
    this.updateInteractionRecord(record, interaction);

    // 2. Update preferences
    this.updatePreferences(toolId, interaction);

    // 3. Update learning metrics
    this.updateLearningMetrics();

    // 4. Persist to storage
    this.saveProfile();
  }

  /**
   * Update user preferences based on engagement
   */
  updatePreferences(toolId, interaction) {
    let tool = this.graph.tools[toolId];
    let engagementScore = this.calculateEngagementScore(interaction);

    // Update category affinity
    let categoryAffinity = this.profile.preferences.favoriteCategories[tool.category] || 0;
    this.profile.preferences.favoriteCategories[tool.category] =
      this.updateAffinity(categoryAffinity, engagementScore, learningRate = 0.1);

    // Update tag affinities
    tool.tags.forEach(tag => {
      let tagAffinity = this.profile.preferences.favoriteTags[tag] || 0;
      this.profile.preferences.favoriteTags[tag] =
        this.updateAffinity(tagAffinity, engagementScore, learningRate = 0.1);
    });

    // Update complexity preference
    let complexityAffinity = this.profile.preferences.complexityPreference[tool.complexity] || 0;
    this.profile.preferences.complexityPreference[tool.complexity] =
      this.updateAffinity(complexityAffinity, engagementScore, learningRate = 0.05);
  }

  /**
   * Update affinity score with exponential moving average
   */
  updateAffinity(currentAffinity, signal, learningRate) {
    return currentAffinity * (1 - learningRate) + signal * learningRate;
  }

  /**
   * Calculate engagement score from interaction
   */
  calculateEngagementScore(interaction) {
    let score = 0;

    // Duration score (0-1)
    let durationScore = Math.min(interaction.duration / 600, 1); // 10min = full score
    score += durationScore * 0.4;

    // Completion score
    if (interaction.completed) score += 0.3;

    // Rating score
    if (interaction.rated) score += (interaction.rated / 5) * 0.2;

    // Action score (bookmark, share, pin)
    if (interaction.bookmarked) score += 0.1;
    if (interaction.shared) score += 0.1;
    if (interaction.pinned) score += 0.1;

    return Math.min(score, 1);
  }
}
```

### 3.3 Diversity & Novelty Balancing

```javascript
class DiversityManager {
  /**
   * Ensure recommendations maintain diversity
   */
  ensureDiversity(recommendations, context) {
    let recentCategories = this.getRecentCategories(lookback = 5);
    let recentTags = this.getRecentTags(lookback = 10);

    // Apply diversity penalties
    return recommendations.map(rec => {
      let penalty = 0;

      // Category diversity
      let categoryRepetition = recentCategories.filter(
        cat => cat === rec.tool.category
      ).length;
      penalty += categoryRepetition * 0.1;

      // Tag diversity
      let tagOverlap = rec.tool.tags.filter(
        tag => recentTags.includes(tag)
      ).length;
      penalty += (tagOverlap / rec.tool.tags.length) * 0.15;

      // Apply user's diversity preference
      penalty *= this.profile.preferences.diversityPreference;

      return {
        ...rec,
        score: rec.score * (1 - penalty)
      };
    }).sort((a, b) => b.score - a.score);
  }

  /**
   * Balance novelty vs familiarity
   */
  balanceNovelty(recommendations) {
    let noveltyPref = this.profile.preferences.noveltyPreference;

    return recommendations.map(rec => {
      let isNovel = !this.profile.interactions[rec.tool.filename];

      // Apply novelty boost/penalty based on preference
      let noveltyModifier = isNovel ?
        (1 + noveltyPref * 0.3) :        // Boost novel if preferred
        (1 - noveltyPref * 0.2);         // Boost familiar if not preferred

      return {
        ...rec,
        score: rec.score * noveltyModifier
      };
    });
  }
}
```

---

## 4. User Interface Flows

### 4.1 Discovery Button States

```
┌─────────────────────────────────────┐
│   Primary Discovery Button          │
│                                      │
│   Default:  "Stumble"                │
│   Active:   Shows current mode       │
│             "Stumble (Similar)"      │
│                                      │
│   [ Stumble ▼ ]                      │
│                                      │
│   Dropdown Menu:                     │
│   ✓ Smart Discovery                  │
│     Random                           │
│     Similar to Favorites             │
│     Trending Now                     │
│     Continue Path                    │
│     Surprise Me                      │
│   ────────────────                   │
│     Discovery Settings               │
│                                      │
└─────────────────────────────────────┘
```

### 4.2 Enhanced Discovery Modal

```
┌──────────────────────────────────────────────┐
│  ×                                    [Mode] │
│                                              │
│              🎮                              │
│                                              │
│      Life Architect: 3D Conway Challenge     │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │ "You might like this because:"         │ │
│  │ • You enjoyed physics-playground-lab   │ │
│  │ • Similar users rated this highly      │ │
│  │ • Trending in 3D Immersive category    │ │
│  └────────────────────────────────────────┘ │
│                                              │
│  3D Immersive • Advanced • gameoflife.html  │
│                                              │
│  Enhanced Conway's Game of Life with 3D...  │
│                                              │
│  [3d] [canvas] [svg] [animation] [game]     │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │ Match Score: ●●●●●○○○○○ 85%         │   │
│  │ Estimated Time: ~7 minutes           │   │
│  └──────────────────────────────────────┘   │
│                                              │
│  Actions:                                    │
│  [Open]  [Next]  [Bookmark]  [Not Interested]│
│                                              │
│  Quick Actions:                              │
│  [❤️ Love] [👍 Like] [👎 Pass] [⏭️ Skip]    │
│                                              │
└──────────────────────────────────────────────┘
```

### 4.3 Discovery Session View

```
┌──────────────────────────────────────────────┐
│  Discovery Session: Physics Exploration       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━ 60% Complete      │
│                                              │
│  Tools Discovered: 5                         │
│  Tools Engaged: 3                            │
│  Session Time: 28 minutes                    │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │ Session Path:                          │ │
│  │                                        │ │
│  │ ✓ Physics Playground ─→               │ │
│  │ ✓ Game of Life ─→                     │ │
│  │ ✓ 3D Worm ─→                          │ │
│  │ ○ Drone Simulator ─→                  │ │
│  │ ○ AI Assembly Line                    │ │
│  └────────────────────────────────────────┘ │
│                                              │
│  [Continue Session]  [End & Save]  [Reset]   │
│                                              │
└──────────────────────────────────────────────┘
```

### 4.4 Discovery Settings Panel

```
┌──────────────────────────────────────────────┐
│  Discovery Preferences                        │
│                                              │
│  Discovery Style:                            │
│  ○ Focused (More similar)                    │
│  ● Balanced (Mix of both)                    │
│  ○ Adventurous (More diverse)                │
│                                              │
│  Novelty Preference:                         │
│  Familiar ━━━━●━━━━━ Novel                   │
│                                              │
│  Complexity Preference:                      │
│  Simple   ━━●━━━━━━━ Advanced                │
│                                              │
│  Show Explanations:                          │
│  [✓] Why this was recommended                │
│  [✓] Match scores                            │
│  [✓] Estimated engagement time               │
│                                              │
│  Quick Actions:                              │
│  [✓] Enable swipe gestures                   │
│  [✓] Auto-advance after rating               │
│  [ ] Skip seen tools automatically           │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │ Your Discovery Stats:                  │ │
│  │ Tools Discovered: 127                  │ │
│  │ Avg Engagement: 85%                    │ │
│  │ Favorite Category: 3D Immersive        │ │
│  │ Discovery Style: Explorer              │ │
│  └────────────────────────────────────────┘ │
│                                              │
│  [Reset Preferences]  [Export Data]  [Save]  │
│                                              │
└──────────────────────────────────────────────┘
```

---

## 5. localStorage Schema

### 5.1 Storage Keys

```javascript
{
  // User profile (main data)
  "lft_user_profile": UserProfile,              // See section 1.1

  // Discovery session (temporary)
  "lft_discovery_session": CurrentSession,

  // Tool relationship cache (computed)
  "lft_tool_graph": ToolRelationshipGraph,      // See section 1.2

  // Recent history (quick access)
  "lft_recent_history": RecentHistory,          // Last 20 interactions

  // Preferences cache
  "lft_preferences_cache": PreferencesCache,

  // Analytics (opt-in)
  "lft_analytics": AnalyticsData,               // Anonymized usage data

  // Legacy support
  "lft_recent_stumbles": Array,                 // Old format
  "lft_stumble_history": Array                  // Old format
}
```

### 5.2 Storage Management

```javascript
class StorageManager {
  constructor() {
    this.namespace = 'lft_';
    this.version = '2.0';
  }

  /**
   * Save user profile
   */
  saveProfile(profile) {
    profile.version = this.version;
    profile.lastUpdated = new Date().toISOString();

    localStorage.setItem(
      this.namespace + 'user_profile',
      JSON.stringify(profile)
    );
  }

  /**
   * Load user profile (with migration)
   */
  loadProfile() {
    let stored = localStorage.getItem(this.namespace + 'user_profile');

    if (!stored) {
      return this.createNewProfile();
    }

    let profile = JSON.parse(stored);

    // Migrate old version
    if (profile.version !== this.version) {
      profile = this.migrateProfile(profile);
    }

    return profile;
  }

  /**
   * Migrate from old version
   */
  migrateProfile(oldProfile) {
    // Migrate from 1.0 to 2.0
    if (oldProfile.version === '1.0' || !oldProfile.version) {
      return {
        version: '2.0',
        userId: this.generateUserId(),
        created: oldProfile.created || new Date().toISOString(),
        lastUpdated: new Date().toISOString(),

        // Migrate old stumble history to interactions
        interactions: this.migrateStumbleHistory(oldProfile),

        // Initialize new fields
        preferences: this.initializePreferences(),
        discoverySessions: [],
        favorites: oldProfile.favorites || [],
        collections: {},
        learningMetrics: this.calculateInitialMetrics(oldProfile)
      };
    }

    return oldProfile;
  }

  /**
   * Create new user profile
   */
  createNewProfile() {
    return {
      version: '2.0',
      userId: this.generateUserId(),
      created: new Date().toISOString(),
      lastUpdated: new Date().toISOString(),
      preferences: this.initializePreferences(),
      interactions: {},
      discoverySessions: [],
      favorites: [],
      collections: {},
      learningMetrics: {
        explorationScore: 0.5,
        loyaltyScore: 0.5,
        diversityScore: 0.5,
        engagementScore: 0.5,
        lastCalibration: new Date().toISOString()
      }
    };
  }

  /**
   * Export user data (GDPR compliance)
   */
  exportUserData() {
    let profile = this.loadProfile();
    let history = this.loadHistory();
    let sessions = this.loadSessions();

    return {
      exported: new Date().toISOString(),
      version: this.version,
      profile,
      history,
      sessions
    };
  }

  /**
   * Clear user data (GDPR compliance)
   */
  clearUserData() {
    Object.keys(localStorage)
      .filter(key => key.startsWith(this.namespace))
      .forEach(key => localStorage.removeItem(key));
  }
}
```

---

## 6. API Specifications

### 6.1 Discovery Service API

```javascript
class DiscoveryService {
  /**
   * Get next recommendation
   *
   * @param {string} mode - Discovery mode
   * @param {object} options - Additional options
   * @returns {object} Recommendation
   */
  async getRecommendation(mode = 'smart', options = {}) {
    // Implementation
  }

  /**
   * Record user interaction
   *
   * @param {string} toolId - Tool filename
   * @param {object} interaction - Interaction data
   */
  async recordInteraction(toolId, interaction) {
    // Implementation
  }

  /**
   * Get user preferences
   *
   * @returns {object} User preferences
   */
  async getPreferences() {
    // Implementation
  }

  /**
   * Update user preferences
   *
   * @param {object} preferences - New preferences
   */
  async updatePreferences(preferences) {
    // Implementation
  }

  /**
   * Get discovery session
   *
   * @param {string} sessionId - Session ID (optional)
   * @returns {object} Session data
   */
  async getSession(sessionId = null) {
    // Implementation
  }

  /**
   * Start new discovery session
   *
   * @param {object} options - Session options
   * @returns {object} New session
   */
  async startSession(options = {}) {
    // Implementation
  }

  /**
   * End discovery session
   *
   * @param {string} sessionId - Session ID
   * @param {object} summary - Session summary
   */
  async endSession(sessionId, summary) {
    // Implementation
  }

  /**
   * Get discovery history
   *
   * @param {object} filters - Filter options
   * @returns {array} History items
   */
  async getHistory(filters = {}) {
    // Implementation
  }

  /**
   * Get tool recommendations batch
   *
   * @param {number} count - Number of recommendations
   * @param {object} options - Options
   * @returns {array} Recommendations
   */
  async getBatchRecommendations(count = 5, options = {}) {
    // Implementation
  }

  /**
   * Get discovery insights
   *
   * @returns {object} User insights
   */
  async getInsights() {
    // Implementation
  }

  /**
   * Provide feedback on recommendation
   *
   * @param {string} toolId - Tool ID
   * @param {string} feedback - positive, negative, neutral
   * @param {string} reason - Reason for feedback
   */
  async provideFeedback(toolId, feedback, reason = null) {
    // Implementation
  }
}
```

### 6.2 Event System

```javascript
// Event types
const DiscoveryEvents = {
  RECOMMENDATION_SHOWN: 'discovery:recommendation:shown',
  RECOMMENDATION_ACCEPTED: 'discovery:recommendation:accepted',
  RECOMMENDATION_REJECTED: 'discovery:recommendation:rejected',
  SESSION_STARTED: 'discovery:session:started',
  SESSION_ENDED: 'discovery:session:ended',
  PREFERENCE_UPDATED: 'discovery:preference:updated',
  PROFILE_SYNCED: 'discovery:profile:synced'
};

// Event emitter
class DiscoveryEventEmitter extends EventEmitter {
  emitRecommendation(recommendation) {
    this.emit(DiscoveryEvents.RECOMMENDATION_SHOWN, {
      toolId: recommendation.tool.filename,
      mode: recommendation.mode,
      score: recommendation.score,
      timestamp: new Date().toISOString()
    });
  }

  emitInteraction(toolId, interaction) {
    if (interaction.engaged) {
      this.emit(DiscoveryEvents.RECOMMENDATION_ACCEPTED, {
        toolId,
        interaction,
        timestamp: new Date().toISOString()
      });
    } else {
      this.emit(DiscoveryEvents.RECOMMENDATION_REJECTED, {
        toolId,
        reason: interaction.reason,
        timestamp: new Date().toISOString()
      });
    }
  }
}
```

---

## 7. Testing Strategy

### 7.1 Unit Tests

```javascript
describe('RecommendationEngine', () => {
  describe('Random Mode', () => {
    it('should return different tools on subsequent calls', () => {
      // Test
    });

    it('should avoid recently viewed tools', () => {
      // Test
    });

    it('should respect category filter', () => {
      // Test
    });

    it('should weight by user preferences', () => {
      // Test
    });
  });

  describe('Similar Mode', () => {
    it('should recommend tools similar to favorites', () => {
      // Test
    });

    it('should avoid tools already viewed', () => {
      // Test
    });

    it('should adjust for quality', () => {
      // Test
    });
  });

  describe('Trending Mode', () => {
    it('should return currently trending tools', () => {
      // Test
    });

    it('should personalize trending results', () => {
      // Test
    });
  });
});

describe('PersonalizationEngine', () => {
  it('should update category affinities after interaction', () => {
    // Test
  });

  it('should update learning metrics', () => {
    // Test
  });

  it('should calculate engagement scores correctly', () => {
    // Test
  });
});
```

### 7.2 Integration Tests

```javascript
describe('Discovery Flow Integration', () => {
  it('should complete full discovery session', async () => {
    // 1. Get recommendation
    let rec = await service.getRecommendation('smart');
    expect(rec).toBeDefined();

    // 2. Simulate interaction
    await service.recordInteraction(rec.tool.filename, {
      duration: 300,
      completed: true,
      rated: 5
    });

    // 3. Get next recommendation
    let next = await service.getRecommendation('smart');
    expect(next.tool.filename).not.toBe(rec.tool.filename);

    // 4. Check preferences updated
    let prefs = await service.getPreferences();
    expect(prefs.favoriteCategories[rec.tool.category]).toBeGreaterThan(0);
  });

  it('should maintain session continuity', async () => {
    // Test session flow
  });
});
```

### 7.3 A/B Testing Framework

```javascript
class ABTestingFramework {
  constructor() {
    this.experiments = {
      'recommendation_algorithm': {
        variants: ['content_based', 'collaborative', 'hybrid'],
        distribution: [0.33, 0.33, 0.34],
        metrics: ['engagement_rate', 'session_duration', 'return_rate']
      },
      'modal_layout': {
        variants: ['classic', 'compact', 'detailed'],
        distribution: [0.5, 0.25, 0.25],
        metrics: ['conversion_rate', 'bounce_rate']
      }
    };
  }

  /**
   * Assign user to experiment variant
   */
  assignVariant(experimentId, userId) {
    // Consistent hash-based assignment
    let hash = this.hashUserId(userId, experimentId);
    let rand = hash % 100 / 100;

    let cumulative = 0;
    for (let i = 0; i < this.experiments[experimentId].variants.length; i++) {
      cumulative += this.experiments[experimentId].distribution[i];
      if (rand < cumulative) {
        return this.experiments[experimentId].variants[i];
      }
    }
  }

  /**
   * Track experiment metric
   */
  trackMetric(experimentId, userId, metric, value) {
    // Track in analytics
  }
}
```

### 7.4 Performance Testing

```javascript
describe('Performance Tests', () => {
  it('should get recommendation in <100ms', async () => {
    let start = performance.now();
    await service.getRecommendation('smart');
    let duration = performance.now() - start;
    expect(duration).toBeLessThan(100);
  });

  it('should handle 100 tools efficiently', async () => {
    // Test with large dataset
  });

  it('should not degrade with large interaction history', async () => {
    // Test with 1000+ interactions
  });
});
```

---

## 8. Analytics & Metrics

### 8.1 Key Performance Indicators

**Discovery Effectiveness:**
- **Recommendation Acceptance Rate**: % of recommendations that user engages with
- **Average Engagement Score**: Quality of engagement after discovery
- **Session Completion Rate**: % of discovery sessions completed
- **Return Rate**: % of users who return to discovered tools

**Personalization Quality:**
- **Preference Accuracy**: How well predictions match actual preferences
- **Diversity Score**: Variety in recommendations
- **Novelty Score**: Balance of new vs familiar content
- **Satisfaction Score**: User-reported satisfaction

**System Health:**
- **Recommendation Latency**: Time to generate recommendation
- **Cache Hit Rate**: Efficiency of precomputed data
- **Storage Usage**: localStorage consumption
- **Error Rate**: Failed recommendations

### 8.2 Analytics Events

```javascript
// Track recommendation shown
analytics.track('recommendation_shown', {
  toolId: string,
  mode: string,
  score: number,
  position: number,
  sessionId: string,
  context: object
});

// Track recommendation outcome
analytics.track('recommendation_outcome', {
  toolId: string,
  accepted: boolean,
  engagementScore: number,
  duration: number,
  sessionId: string
});

// Track preference update
analytics.track('preference_updated', {
  category: string,
  oldValue: number,
  newValue: number,
  trigger: string
});

// Track session metrics
analytics.track('session_completed', {
  sessionId: string,
  duration: number,
  toolsDiscovered: number,
  toolsEngaged: number,
  avgEngagement: number,
  mode: string
});
```

### 8.3 User Insights Dashboard

```javascript
class InsightsDashboard {
  /**
   * Generate user insights
   */
  generateInsights(profile, history) {
    return {
      // Behavioral insights
      behavior: {
        discoveryStyle: this.classifyDiscoveryStyle(profile),
        topCategories: this.getTopCategories(profile, limit = 3),
        topTags: this.getTopTags(profile, limit = 5),
        explorationPattern: this.analyzeExplorationPattern(history),
        engagementPattern: this.analyzeEngagementPattern(history)
      },

      // Temporal insights
      temporal: {
        bestTimeOfDay: this.getBestTimeOfDay(history),
        bestDayOfWeek: this.getBestDayOfWeek(history),
        avgSessionDuration: this.getAvgSessionDuration(history),
        peakEngagementTime: this.getPeakEngagementTime(history)
      },

      // Content insights
      content: {
        favoriteTools: this.getFavoriteTools(profile, limit = 10),
        hiddenGems: this.findHiddenGems(profile),
        underexploredCategories: this.findUnderexploredCategories(profile),
        recommendedPaths: this.recommendPaths(profile)
      },

      // Achievement insights
      achievements: {
        toolsDiscovered: Object.keys(profile.interactions).length,
        categoriesExplored: this.countCategoriesExplored(profile),
        totalEngagementTime: this.getTotalEngagementTime(profile),
        streakDays: this.calculateStreak(history),
        level: this.calculateUserLevel(profile)
      }
    };
  }
}
```

---

## 9. Implementation Phases

### Phase 1: Foundation (Week 1)
- [ ] Implement enhanced data structures
- [ ] Create StorageManager with migration
- [ ] Build PersonalizationEngine core
- [ ] Add basic interaction tracking
- [ ] Unit tests for core components

### Phase 2: Discovery Modes (Week 2)
- [ ] Implement Random mode (enhanced)
- [ ] Implement Similar mode
- [ ] Implement Trending mode
- [ ] Build RecommendationEngine
- [ ] Add mode switching UI

### Phase 3: Advanced Features (Week 3)
- [ ] Implement Favorites mode
- [ ] Implement Surprise mode
- [ ] Add Discovery Paths
- [ ] Build DiversityManager
- [ ] Enhanced discovery modal

### Phase 4: Personalization (Week 4)
- [ ] Implement Smart mode
- [ ] Add preference learning
- [ ] Build context analyzer
- [ ] Session tracking
- [ ] User insights dashboard

### Phase 5: Polish & Testing (Week 5)
- [ ] Integration testing
- [ ] Performance optimization
- [ ] A/B testing setup
- [ ] Analytics implementation
- [ ] Documentation

### Phase 6: Launch (Week 6)
- [ ] User acceptance testing
- [ ] Bug fixes
- [ ] Migration from old system
- [ ] Launch announcement
- [ ] Monitor metrics

---

## 10. Success Metrics

### Launch Criteria
- **Recommendation Acceptance Rate**: >50%
- **Average Engagement Score**: >0.6
- **System Latency**: <100ms (p95)
- **Error Rate**: <1%
- **Storage Usage**: <5MB per user

### 30-Day Goals
- **User Adoption**: >70% of active users try new discovery
- **Engagement Increase**: +25% in discovery engagement
- **Session Length**: +15% in discovery session duration
- **Return Rate**: +20% of users revisit discovered tools

### 90-Day Goals
- **Preference Accuracy**: >75%
- **Diversity Score**: 0.6-0.8 (balanced)
- **User Satisfaction**: >4.0/5.0
- **Discovery Contribution**: >40% of tool views from discovery

---

## 11. Future Enhancements

### Phase 2 Features (Post-Launch)
- **Social Discovery**: Share discovery sessions with friends
- **Collaborative Filtering**: Learn from similar users globally
- **Smart Playlists**: Auto-generated tool playlists
- **Voice Commands**: "Stumble on 3D games"
- **Ambient Discovery**: Background recommendations while browsing
- **Discovery Challenges**: Gamified exploration goals

### Advanced ML Features
- **Deep Learning Embeddings**: Neural network-based tool embeddings
- **Multi-Armed Bandits**: Optimized exploration-exploitation
- **Reinforcement Learning**: Self-improving recommendation
- **Natural Language**: Text-based discovery queries
- **Image Recognition**: Visual similarity matching

### Integration Features
- **Cross-Device Sync**: Cloud-based profile sync
- **Export/Import**: Share profiles between devices
- **API Access**: Third-party integrations
- **Webhook Events**: Real-time discovery notifications
- **Browser Extension**: Discover tools across the web

---

## Appendix A: Algorithms Reference

### A.1 Weighted Random Selection

```javascript
function weightedRandomSelect(items) {
  let totalWeight = items.reduce((sum, item) => sum + item.weight, 0);
  let random = Math.random() * totalWeight;

  let cumulative = 0;
  for (let item of items) {
    cumulative += item.weight;
    if (random < cumulative) {
      return item;
    }
  }

  return items[items.length - 1];
}
```

### A.2 Cosine Similarity

```javascript
function cosineSimilarity(vecA, vecB) {
  let dotProduct = 0;
  let normA = 0;
  let normB = 0;

  for (let key in vecA) {
    if (vecB[key]) {
      dotProduct += vecA[key] * vecB[key];
    }
    normA += vecA[key] * vecA[key];
  }

  for (let key in vecB) {
    normB += vecB[key] * vecB[key];
  }

  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}
```

### A.3 Exponential Moving Average

```javascript
function updateEMA(current, newValue, alpha = 0.1) {
  return current * (1 - alpha) + newValue * alpha;
}
```

---

## Appendix B: Data Migration Guide

### Migrating from v1.0 to v2.0

```javascript
function migrateV1ToV2(oldData) {
  // Old stumble history format
  let oldHistory = JSON.parse(
    localStorage.getItem('lft_stumble_history') || '[]'
  );

  // Convert to new interactions format
  let interactions = {};
  oldHistory.forEach(item => {
    interactions[item.filename] = {
      viewCount: 1,
      totalTimeSpent: 0,
      lastViewed: item.timestamp,
      firstViewed: item.timestamp,
      sessions: [{
        timestamp: item.timestamp,
        duration: 0,
        source: 'stumble',
        completed: false
      }],
      engagement: {
        quickBounce: false,
        deepDive: false,
        repeatedReturn: false,
        recommendedToOthers: false
      }
    };
  });

  // Create new profile
  return {
    version: '2.0',
    userId: generateUserId(),
    created: new Date().toISOString(),
    lastUpdated: new Date().toISOString(),
    preferences: initializePreferences(),
    interactions,
    discoverySessions: [],
    favorites: [],
    collections: {},
    learningMetrics: calculateInitialMetrics(interactions)
  };
}
```

---

## Appendix C: Privacy & Ethics

### Data Privacy
- All data stored locally in browser localStorage
- No server-side tracking or profiling
- User data never leaves the device
- Anonymous usage analytics (opt-in only)
- GDPR-compliant data export/deletion

### Ethical Considerations
- Transparent recommendation reasoning
- User control over personalization
- No manipulative dark patterns
- Diversity promotion (avoid filter bubbles)
- Quality over engagement metrics

### User Control
- Clear preference settings
- Easy reset/delete options
- Explainable recommendations
- Opt-out of tracking
- Data portability

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-12 | Discovery System Agent | Initial architecture design |

---

**End of Document**
