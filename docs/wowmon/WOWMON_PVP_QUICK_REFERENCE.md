# WoWmon Competitive PvP - Quick Reference Guide

**Agent 6: Competitive Strategy - Executive Summary**

---

## Overview

This document outlines a complete competitive multiplayer system for WoWmon.html focused on balanced PvP battles, team building, ranking systems, tournaments, and fair play enforcement.

---

## Key Features

### 1. TEAM BUILDER SYSTEM
- **Drag-and-drop team composition** with 6 creatures max
- **Tier system**: Uber, OU, UU, RU, NU, Little Cup
- **Meta analysis dashboard** showing usage stats, win rates, threat lists
- **Type coverage analyzer** highlighting weaknesses
- **Team validation** with legality checker
- **Import/Export** in Showdown format + QR codes

**Example Team Roles**:
- Physical Sweeper (high Attack + Speed)
- Special Wall (high Sp. Defense + HP)
- Pivot (good defenses, U-turn/Volt Switch)
- Lead (entry hazards, screens)
- Revenge Killer (Choice Scarf, priority moves)
- Win Condition (setup sweeper)

---

### 2. BATTLE SYSTEM (Competitive Mechanics)

#### Advanced Damage Formula
```
Base = ((2 * Level / 5 + 2) * Power * Attack / Defense / 50) + 2
Final = Base × Weather × Critical × Random × STAB × Effectiveness × Items × Abilities × Screens
```

**Key Mechanics**:
- **STAB**: 1.5× damage for same-type moves
- **Critical hits**: 12.5% base chance, 1.5× damage
- **Random variance**: 85-100% for each hit
- **Type effectiveness**: 0×, 0.5×, 1×, 2× multipliers
- **Weather effects**: Sun boosts Fire, Rain boosts Water
- **Status conditions**: Burn, Poison, Toxic, Paralysis, Sleep, Freeze
- **Entry hazards**: Stealth Rock, Spikes, Toxic Spikes, Sticky Web
- **Screens**: Reflect (physical), Light Screen (special)

#### Status Conditions
- **Burn**: Halves Attack, 1/16 max HP damage per turn
- **Poison**: 1/8 max HP damage per turn
- **Toxic**: 1/16, 2/16, 3/16... increasing damage
- **Paralysis**: Halves Speed, 25% chance to be fully paralyzed
- **Sleep**: Can't move for 1-3 turns
- **Freeze**: Can't move, 20% chance to thaw each turn

---

### 3. RANKING & MATCHMAKING

#### ELO System
| Rank | Min ELO | Icon |
|------|---------|------|
| Master | 2000+ | 👑 |
| Diamond | 1800+ | 💎 |
| Platinum | 1600+ | 🏆 |
| Gold | 1400+ | 🥇 |
| Silver | 1200+ | 🥈 |
| Bronze | 1000+ | 🥉 |
| Beginner | 0+ | 🌱 |

**ELO Formula**:
```
Change = K × (Actual Score - Expected Score)
Expected Score = 1 / (1 + 10^((Opp Rating - Your Rating) / 400))
```

#### Matchmaking Algorithm
1. Initial search: ±200 ELO difference
2. Expansion: +50 ELO every 30 seconds
3. Max wait time: 5 minutes
4. Prioritize: Low latency > Same region > Similar wait time

**Anti-Smurf Detection**:
- High win rate on new account
- Consistently beating higher-rated opponents
- Advanced strategies at low rating
- Perfect prediction accuracy
- → Action: Boost hidden MMR, increase K-factor

---

### 4. TOURNAMENT SYSTEM

#### Tournament Formats
- **Single Elimination**: Lose once = out
- **Double Elimination**: Winners + losers brackets
- **Swiss System**: Round-robin, no elimination
- **Round Robin**: Everyone plays everyone
- **Battle Royale**: 100 players, last team standing

#### Tournament Rules
- **Species Clause**: No duplicate creatures
- **Item Clause**: No duplicate items (optional)
- **Sleep Clause**: Can't put 2+ opponent creatures to sleep
- **OHKO Clause**: One-hit KO moves banned
- **Endless Clause**: Prevent infinite battles
- **Team Lock**: Can't change team after registration

#### Prize Distribution
| Place | Prize % |
|-------|---------|
| 1st | 50% |
| 2nd | 25% |
| 3rd-4th | 12.5% each |

---

### 5. REPLAY & ANALYSIS

#### Replay Features
- **Save/Load/Share**: JSON, QR code, embed code
- **Playback controls**: Speed (0.5x-2x), pause, seek
- **Critical moments**: Auto-highlight important turns
- **Turn-by-turn analysis**: Damage, switches, predictions
- **Mistake identification**: Suboptimal plays with suggestions
- **Performance stats**: Damage dealt/taken, KOs, MVP

#### Post-Battle Statistics
- Total damage dealt/taken
- Creature performance (MVP calculation)
- Move usage breakdown
- Prediction accuracy
- Effective switches
- Momentum chart

#### Replay Validation
- Server-side damage recalculation
- Seeded RNG verification
- Stat change validation
- Prevents replay tampering

---

### 6. ANTI-CHEAT & FAIR PLAY

#### Detection Methods
1. **Server-side validation**: All damage, moves, stats
2. **Timing analysis**: Detect instant decisions (bots)
3. **Pattern detection**: Perfect predictions, automated inputs
4. **Packet validation**: Real-time action verification
5. **Replay validation**: Reconstruct battle from seed

#### Violations
| Severity | Examples | Action |
|----------|----------|--------|
| Critical | Damage manipulation, impossible moves | Immediate ban |
| High | Perfect predictions (>90%), packet manipulation | Temp ban + review |
| Medium | Suspicious timing, rapid inputs | Warning + monitoring |

#### Fair Play Score
- Base: 100 points
- Deductions: Warnings (-5), temp bans (-15), forfeits (-20), toxic chat (-10)
- Bonuses: Sportsmanship (+5), valid reports (+2)
- **Score < 40**: Restricted from ranked play

---

### 7. ADDITIONAL FEATURES

#### Draft Mode
- Ban phase: 2 bans per player
- Pick phase: 6 picks per player
- Snake draft: Alternating picks (1-2-2-1-1-2-2-1...)
- Real-time creature pool with stats

#### Seasonal System
- **Duration**: 3 months per season
- **Rewards**: Titles, cosmetics, currency, exclusive skins
- **Soft reset**: Rating moves toward 1500 at season end
- **Leaderboards**: Global, regional, seasonal

#### Spectator Mode
- Full battle state visibility
- Live statistics dashboard
- AI commentary (optional)
- Replay generation
- Spectator chat

---

## Balance Recommendations

### Nerfs Needed
| Creature | Issue | Fix |
|----------|-------|-----|
| Dragon | BST too high (400+) | Reduce by 10-15% |
| Infernal | Explosion (250 power) | Reduce to 200, add drawback |
| Phoenix | Speed 100 too fast | Reduce to 90 |

### Buffs Needed
| Creature | Issue | Fix |
|----------|-------|-----|
| Murloc | Too weak early | HP 45 → 50 |
| Skeleton | No evolution, weak | Add evolution or +10% stats |
| Kobold | Very limited use | Attack 35 → 45 |

### Move Balance
- **Hyper Beam**: Add recharge turn
- **Explosion**: User faints after use
- **Quick Attack**: Fine as-is

---

## Implementation Roadmap

### Phase 1: Core PvP (Weeks 1-4)
- Enhanced battle mechanics
- Team builder UI
- Multiplayer networking (WebSocket)
- Basic matchmaking

### Phase 2: Competitive (Weeks 5-8)
- Tier system
- Ranking and leaderboards
- Replay system
- Tournament infrastructure

### Phase 3: Advanced (Weeks 9-12)
- Anti-cheat system
- Advanced analytics
- Draft mode
- Balance patches

### Phase 4: Launch (Weeks 13-16)
- Beta testing
- First tournament
- Community features
- Official Season 1

**Total Timeline**: 16 weeks (4 months)
**Team Required**: 2-3 developers + 1 balance designer

---

## Technical Stack

- **Frontend**: HTML5 Canvas, WebSocket client
- **Backend**: Node.js + WebSocket server
- **Storage**: IndexedDB (local), MongoDB (cloud)
- **Validation**: Server-side battle engine
- **Matchmaking**: Redis queue + ELO algorithm
- **Anti-cheat**: Server-side calculation verification

---

## Competitive Meta Predictions

### Tier List (Launch Meta)
**S-Tier** (Must-ban):
- Murloc King (versatile, strong coverage)
- Orc Warlord (high damage, good typing)
- Ancient Wisp (speed control, healing)

**A-Tier** (Top picks):
- Dire Wolf (speed + power)
- Phoenix (speed + rebirth)
- Naga (water/magic coverage)
- Drake (balanced stats)

**B-Tier** (Situational):
- Felguard (demon typing)
- Nerubian (poison/shadow)
- Abomination (tank)

**C-Tier** (Niche):
- Gnoll (outclassed)
- Spider (weak to common threats)
- Ghoul (better evolutions exist)

### Predicted Team Archetypes
1. **Hyper Offense** (35% usage): Fast sweepers, minimal defense
2. **Balance** (30% usage): Mix of offense and defense
3. **Stall** (15% usage): Walls + recovery moves
4. **Weather** (10% usage): Sun/Rain teams
5. **Trick Room** (10% usage): Slow + powerful

---

## Key Success Metrics

### Competitive Health Indicators
- **Creature diversity**: Top 20 creatures should be <60% of usage
- **Win rate spread**: No creature with >55% win rate when used
- **Match duration**: Average 8-15 turns (not too fast/slow)
- **Player retention**: >60% of players play 10+ matches per season
- **Fair play score**: <5% of players below 60 score

### Anti-Cheat Effectiveness
- **False positive rate**: <1%
- **Detection speed**: Flagged within 5 matches
- **Ban accuracy**: >95% confirmed cheaters

---

## Quick Start Guide for Developers

1. **Read full design**: `/WOWMON_COMPETITIVE_PVP_DESIGN.md`
2. **Set up WebSocket server**: Node.js + Socket.io
3. **Implement damage calculator**: Copy formula from design doc
4. **Build team builder UI**: Start with drag-drop interface
5. **Add basic matchmaking**: Queue system + ELO
6. **Test with beta users**: 10-20 competitive players
7. **Iterate based on data**: Monthly balance patches

---

## Contact & Resources

- **Full Design Document**: `/WOWMON_COMPETITIVE_PVP_DESIGN.md`
- **Current WoWmon File**: `/wowMon.html`
- **Balance Spreadsheet**: (TBD - create for tracking)
- **Discord/Community**: (TBD - for competitive scene)

---

**Version**: 1.0
**Last Updated**: 2025-10-12
**Author**: Agent 6 - Competitive Strategy
