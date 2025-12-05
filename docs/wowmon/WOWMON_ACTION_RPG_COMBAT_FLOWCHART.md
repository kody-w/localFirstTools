# WoWMon Action RPG - Combat System Flowchart

## Real-Time Combat State Machine

```
┌─────────────────────────────────────────────────────────────────┐
│                        COMBAT LOOP                              │
│                     (60 FPS / 16ms per frame)                   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   NEUTRAL STATE       │◄──────────────┐
                    │   (Can act freely)    │               │
                    └───────────────────────┘               │
                                │                           │
                    ┌───────────┴───────────┐              │
                    │                       │               │
            ┌───────▼────────┐      ┌──────▼──────┐       │
            │  PLAYER INPUT  │      │ UPDATE      │       │
            │   - Attack     │      │ - Stamina   │       │
            │   - Dodge      │      │ - I-frames  │       │
            │   - Block      │      │ - Position  │       │
            └────────────────┘      └─────────────┘       │
                    │                                      │
                    ▼                                      │
        ┌───────────────────────┐                        │
        │   ACTION SELECTED     │                        │
        └───────────────────────┘                        │
                    │                                      │
        ┌───────────┴────────────┐                       │
        │                        │                        │
    ┌───▼────┐  ┌────▼─────┐  ┌─▼──────┐  ┌─────▼────┐ │
    │ATTACK  │  │  DODGE   │  │ BLOCK  │  │ SPECIAL  │ │
    └────────┘  └──────────┘  └────────┘  └──────────┘ │
        │             │             │            │        │
        └─────────────┴─────────────┴────────────┘       │
                    │                                      │
                    ▼                                      │
        ┌──────────────────────┐                         │
        │  STAMINA CHECK       │                         │
        │  Enough? ────Yes────►│──────────────┐         │
        │    │                 │              │          │
        │    No                │              │          │
        │    │                 │              │          │
        │    ▼                 │              │          │
        │  FAIL               │              │          │
        └───────┬──────────────┘              │          │
                │                             │          │
                └─────────────────────────────┼──────────┘
                                              │
                                              ▼
                                    ┌─────────────────┐
                                    │ EXECUTE ACTION  │
                                    └─────────────────┘
                                              │
                    ┌─────────────────────────┼────────────────────┐
                    │                         │                    │
            ┌───────▼────────┐      ┌────────▼────────┐  ┌───────▼──────┐
            │  ATTACKING     │      │   DODGING       │  │  BLOCKING    │
            │                │      │                 │  │              │
            │ Startup: 100ms │      │ Duration: 600ms │  │ Continuous   │
            │ Active: 150ms  │      │ I-frames: 200ms │  │ -5 STA/sec   │
            │ Recovery: 150ms│      │                 │  │              │
            └────────────────┘      └─────────────────┘  └──────────────┘
                    │                         │                    │
                    │                         │                    │
                    └─────────────────────────┼────────────────────┘
                                              │
                                              ▼
                                    ┌──────────────────┐
                                    │  HITBOX CHECK    │
                                    └──────────────────┘
                                              │
                    ┌─────────────────────────┼───────────────────┐
                    │                         │                   │
            ┌───────▼──────┐         ┌───────▼──────┐    ┌──────▼──────┐
            │   HIT!       │         │   MISS       │    │   BLOCKED   │
            │              │         │              │    │             │
            │ Apply Damage │         │ No Effect    │    │ Reduce DMG  │
            │ Hitstun      │         │              │    │ Drain STA   │
            │ Knockback    │         │              │    │             │
            └──────────────┘         └──────────────┘    └─────────────┘
                    │                         │                   │
                    └─────────────────────────┼───────────────────┘
                                              │
                                              ▼
                                    ┌──────────────────┐
                                    │  RETURN TO       │
                                    │  NEUTRAL STATE   │
                                    └──────────────────┘
```

## Attack Frame Data Breakdown

```
LIGHT ATTACK TIMELINE (400ms total)
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  STARTUP     │    ACTIVE      │      RECOVERY             │
│  (100ms)     │    (150ms)     │      (150ms)              │
│              │                │                           │
│  Vulnerable  │  Hitbox Active │  Can Roll Cancel (last 100ms) │
│              │                │                           │
│  ░░░░░░░░░░  │  █████████████ │  ░░░░░░░░░░░░░░          │
│              │                │                           │
│  Can't act   │  Damage window │  Can buffer next input    │
│              │                │                           │
└────────────────────────────────────────────────────────────┘
     0ms         100ms          250ms                   400ms


HEAVY ATTACK TIMELINE (750ms total)
┌────────────────────────────────────────────────────────────┐
│                                                            │
│     STARTUP         │       ACTIVE      │   RECOVERY      │
│     (250ms)         │       (200ms)     │   (300ms)       │
│                     │                   │                 │
│   Long wind-up      │   Hitbox Active   │   Long recovery │
│   VERY Vulnerable   │   High damage     │   Vulnerable    │
│                     │                   │                 │
│   ░░░░░░░░░░░░░░░   │   █████████████   │   ░░░░░░░░░░   │
│                     │                   │                 │
│   Enemy can         │   Guard Break     │   Get punished  │
│   interrupt         │   Poise Break     │   if you miss   │
│                     │                   │                 │
└────────────────────────────────────────────────────────────┘
     0ms              250ms              450ms          750ms


DODGE ROLL TIMELINE (600ms total)
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  I-FRAMES (200ms)    │         VULNERABLE (400ms)         │
│                      │                                    │
│  INVINCIBLE!         │         Can be hit                 │
│                      │                                    │
│  █████████████████   │         ░░░░░░░░░░░░░░░░░░░░░░    │
│                      │                                    │
│  Dodge through       │         Recovery period            │
│  attacks safely      │                                    │
│                      │                                    │
└────────────────────────────────────────────────────────────┘
     0ms              200ms                              600ms
```

## Parry Timing Window

```
ENEMY ATTACK INCOMING
│
│  ┌──────────────────────────────────────────────┐
│  │                                              │
│  │         ENEMY TELEGRAPH                      │
│  │         (400-800ms warning)                  │
│  │                                              │
│  └──────────────────────────────────────────────┘
│                      │
│                      ▼
│         ┌────────────────────────┐
│         │  ENEMY HITBOX ACTIVE   │
│         └────────────────────────┘
│                      │
│     ┌────────────────┼────────────────┐
│     │                │                │
│     ▼                ▼                ▼
│  ┌──────┐      ┌──────────┐     ┌──────┐
│  │ TOO  │      │ PERFECT  │     │ TOO  │
│  │EARLY │      │  PARRY!  │     │ LATE │
│  │      │      │ (150ms)  │     │      │
│  │Block │      │ +30 STA  │     │ Hit! │
│  └──────┘      └──────────┘     └──────┘
│                      │
│                      ▼
│              ┌──────────────┐
│              │   RIPOSTE    │
│              │  WINDOW      │
│              │  (2000ms)    │
│              └──────────────┘
│                      │
│                      ▼
│              ┌──────────────┐
│              │   CRITICAL   │
│              │   DAMAGE     │
│              │   (3x DMG)   │
│              └──────────────┘
```

## Stamina Management Flow

```
STARTING STAMINA: 100
│
├──► LIGHT ATTACK (-15)
│    │
│    ├─ Success: 85 stamina remaining
│    └─ Continue?
│         │
│         ├──► YES: LIGHT ATTACK (-15)
│         │    │
│         │    ├─ Success: 70 stamina remaining
│         │    └─ Continue?
│         │         │
│         │         ├──► YES: LIGHT ATTACK (-15)
│         │         │    │
│         │         │    ├─ Success: 55 stamina remaining
│         │         │    └─ Continue?
│         │         │         │
│         │         │         ├──► YES: DODGE (-25)
│         │         │         │    │
│         │         │         │    ├─ Success: 30 stamina (SAFE)
│         │         │         │    └─ Retreat to regenerate
│         │         │         │
│         │         │         └──► NO: Retreat (SMART!)
│         │         │              Regen: +25/sec
│         │         │              After 1 sec: 80 stamina
│         │         │              After 2 sec: 100 stamina (FULL)
│         │         │
│         │         └──► RECKLESS: HEAVY ATTACK (-30)
│         │              │
│         │              ├─ 40 stamina left
│         │              └─ Enemy attacks!
│         │                   │
│         │                   ├──► Try to dodge (-25)?
│         │                   │    │
│         │                   │    ├─ Success: 15 stamina (DANGER!)
│         │                   │    └─ Can't attack, can't dodge again
│         │                   │         │
│         │                   │         └──► Enemy hits = DEAD
│         │                   │
│         │                   └──► Try to block (-5/sec)?
│         │                        │
│         │                        └─ Hit during block
│         │                             │
│         │                             ├─ Stamina drains: 40→35→30→25
│         │                             └─ STAMINA BROKEN!
│         │                                  │
│         │                                  └─► Stunned for 2 seconds
│         │                                       │
│         │                                       └─► DEAD
│         │
│         └──► NO: Retreat (SMART PLAY)
│              │
│              └─► Regenerate stamina
│                   │
│                   └─► Re-engage at full resources
│
└──► GOOD PLAYER PATH:
     │
     Attack x2 (-30 total)
     │
     Dodge out (-25)
     │
     45 stamina remaining (SAFE)
     │
     Regen while spacing
     │
     Back to 100 stamina
     │
     Repeat (sustainable)
```

## Boss Fight Decision Tree

```
                    ┌─────────────────┐
                    │  BOSS ENCOUNTER │
                    └─────────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
        ┌───────▼────────┐      ┌──────▼──────┐
        │  PHASE 1       │      │   PLAYER    │
        │  (100-50% HP)  │      │   STATE     │
        └────────────────┘      └─────────────┘
                │                       │
                ▼                       ▼
    ┌──────────────────┐    ┌──────────────────┐
    │ Boss AI State    │    │ HP:   █████░░    │
    │                  │    │ STA:  ████████   │
    │ - Idle (1s)      │    │ Estus: 5/5       │
    │ - Telegraph      │    └──────────────────┘
    │ - Attack         │                │
    │ - Recovery       │                ▼
    └──────────────────┘        DECISION POINT
                │                       │
                ▼               ┌───────┴────────┐
    ┌──────────────────┐        │                │
    │ Boss Chooses:    │    ┌───▼────┐    ┌─────▼─────┐
    │                  │    │OFFENSE │    │  DEFENSE  │
    │ - Claw Swipe     │    │        │    │           │
    │ - Leap           │    │ Attack │    │  Dodge    │
    │ - Howl (buff)    │    │ back   │    │  & Wait   │
    └──────────────────┘    └────────┘    └───────────┘
                │               │               │
                ▼               │               │
    ┌──────────────────┐        │               │
    │ TELEGRAPH        │        │               │
    │ (Yellow → Red)   │        │               │
    │ Duration: 0.4s   │        │               │
    └──────────────────┘        │               │
                │               │               │
                ▼               │               │
        PLAYER REACTION         │               │
                │               │               │
    ┌───────────┴────────┐      │               │
    │                    │      │               │
┌───▼────┐      ┌────────▼────┐ │               │
│ DODGE  │      │   PARRY     │ │               │
│        │      │             │ │               │
│ I-frames│     │ +30 STA    │ │               │
│ Safe   │      │ → Riposte  │ │               │
└────────┘      └─────────────┘ │               │
    │                   │        │               │
    └───────────────────┼────────┘               │
                        │                        │
                        ▼                        ▼
            ┌──────────────────┐      ┌─────────────────┐
            │  PUNISH WINDOW   │      │  SAFE SPACING   │
            │                  │      │                 │
            │ Boss Recovery    │      │ Wait for next   │
            │ 2-3 hit combo    │      │ attack          │
            │ (-45 stamina)    │      │ Regen stamina   │
            └──────────────────┘      └─────────────────┘
                        │                        │
                        ▼                        │
            ┌──────────────────┐                 │
            │  BOSS HP: 75%    │                 │
            └──────────────────┘                 │
                        │                        │
                        │                        │
            ┌───────────┴────────────────────────┘
            │
            ▼
    REPEAT CYCLE
    │
    ▼
┌──────────────────┐
│ BOSS HP: 50%     │ ──► PHASE 2 TRANSITION
│                  │
│ - Heals 25%      │
│ - New attacks    │
│ - Summons adds   │
└──────────────────┘
```

## Combo System Flowchart

```
COMBO SYSTEM
│
├─► Input: Light Attack (X)
│   │
│   ├─ Stamina: 100 → 85
│   ├─ Damage: 1.0x
│   ├─ Animation: Slash Right (400ms)
│   │
│   └─► Combo Window: 500ms to continue
│       │
│       ├─► Input within 500ms: Light Attack (X)
│       │   │
│       │   ├─ Stamina: 85 → 70
│       │   ├─ Damage: 1.0x
│       │   ├─ Combo Counter: 2
│       │   ├─ Animation: Slash Left (400ms)
│       │   │
│       │   └─► Combo Window: 500ms to continue
│       │       │
│       │       ├─► Input: Light Attack (X)
│       │       │   │
│       │       │   ├─ Stamina: 70 → 55
│       │       │   ├─ Damage: 1.2x (combo bonus!)
│       │       │   ├─ Combo Counter: 3
│       │       │   ├─ Animation: Thrust (500ms)
│       │       │   │
│       │       │   └─► Combo Window: 500ms for finisher
│       │       │       │
│       │       │       ├─► Input: Light Attack (X)
│       │       │       │   │
│       │       │       │   ├─ Stamina: 55 → 40
│       │       │       │   ├─ Damage: 1.5x (FINISHER!)
│       │       │       │   ├─ Combo Counter: 4
│       │       │       │   ├─ Animation: Overhead Slam (600ms)
│       │       │       │   ├─ Knockdown enemy
│       │       │       │   │
│       │       │       │   └─► Combo complete!
│       │       │       │        Stamina: 40 (can still dodge)
│       │       │       │
│       │       │       └─► Input: Heavy Attack (Y)
│       │       │           │
│       │       │           ├─ Stamina: 55 → 25
│       │       │           ├─ Damage: 2.0x (HEAVY FINISHER!)
│       │       │           ├─ Guard Break
│       │       │           ├─ Poise Break: +20
│       │       │           │
│       │       │           └─► High damage, but low stamina!
│       │       │                Risk/Reward decision
│       │       │
│       │       └─► Input: Dodge (B)
│       │           │
│       │           ├─ Cancel combo
│       │           ├─ Stamina: 70 → 45
│       │           ├─ I-frames: 200ms
│       │           │
│       │           └─► Safety first!
│       │                Reset combo counter
│       │
│       └─► No input (timeout after 500ms)
│           │
│           └─► Combo reset
│                Combo counter: 0
│                Back to neutral
│
└─► Advanced: Mix Light + Heavy
    │
    ├─► Light → Light → Heavy
    │   │
    │   ├─ Total damage: 1.0 + 1.0 + 2.0 = 4.0x
    │   ├─ Total stamina: 15 + 15 + 30 = 60
    │   └─ Guard break on finisher
    │
    └─► Heavy → Light → Light
        │
        ├─ Total damage: 1.5 + 0.8 + 1.5 = 3.8x
        ├─ Total stamina: 30 + 15 + 15 = 60
        └─ Different combo properties
```

## Legend

```
█████  Active/Safe state
░░░░░  Vulnerable state
───►   Flow direction
┌───┐  Decision point
│   │  State/Action
▼     Direction indicator
```

---

These flowcharts visualize the **real-time decision making** that makes Souls-like combat engaging. Every choice has consequences, every action has risk, and mastery comes from understanding these systems.
