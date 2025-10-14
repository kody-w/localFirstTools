# Time-Gap Aware Briefing Examples

The AI briefing system calibrates its tone, priorities, and guidance based on **how long it's been since the last briefing**. Here are examples showing the dramatic differences:

---

## 🕐 Scenario 1: Same Day (3 hours ago)

**Gap:** 3 hours
**Category:** `continuing_session`
**Tone:** Casual, check-in style

```json
{
  "timeGapContext": {
    "lastBriefingTimestamp": 1736917200000,
    "lastBriefingDate": "2025-01-15",
    "daysSinceLastBriefing": 0,
    "hoursSinceLastBriefing": 3,
    "gapCategory": "same_day",
    "gapDescription": "3 hours since last briefing"
  },

  "todaysAgenda": {
    "greeting": "Welcome back! You were here this morning. Let's continue your day.",
    "primaryFocus": "Continuing momentum from this morning",
    "keyPriorities": [
      "✅ Complete tasks started this morning",
      "📋 Review progress so far",
      "🎯 Finish your afternoon goals"
    ],
    "aiGuidance": "You're in the middle of your workday. Keep the momentum going. You completed 2 tasks this morning - stay focused."
  },

  "insights": {
    "morningStats": {
      "windowsOpened": 5,
      "tasksCompleted": 2,
      "productiveTime": "2.5 hours",
      "currentMomentum": "strong"
    },
    "suggestions": [
      "You're on a roll - 2 tasks done already",
      "Keep Notepad open like you had it this morning",
      "You were most focused between 9-10 AM"
    ]
  }
}
```

**Briefing Window Title:** "✨ Afternoon Check-In - Continuing Your Day"

---

## 📅 Scenario 2: Yesterday (1 day ago)

**Gap:** 1 day
**Category:** `daily_continuation`
**Tone:** Standard daily briefing, energetic

```json
{
  "timeGapContext": {
    "lastBriefingTimestamp": 1736841600000,
    "lastBriefingDate": "2025-01-14",
    "daysSinceLastBriefing": 1,
    "gapCategory": "normal_daily",
    "gapDescription": "1 day since last briefing"
  },

  "todaysAgenda": {
    "greeting": "Good morning! Ready for another productive day?",
    "primaryFocus": "Deep work and project completion",
    "keyPriorities": [
      "📝 Finish project proposal (80% done yesterday)",
      "🎨 Create design mockups",
      "📞 Follow up with team",
      "🧹 Organize workspace"
    ],
    "aiGuidance": "You made great progress yesterday. Today is about finishing strong and maintaining momentum."
  },

  "insights": {
    "yesterdayStats": {
      "tasksCompleted": 7,
      "productiveHours": 4.5,
      "mostUsedProgram": "Notepad"
    },
    "achievements": [
      "🏆 Completed 7 tasks yesterday",
      "⚡ 4.5 hours of focused work",
      "📝 Drafted 3 documents"
    ],
    "suggestions": [
      "Keep using your 9-11 AM productivity window",
      "You work well with Notepad + Calculator combo"
    ]
  }
}
```

**Briefing Window Title:** "☀️ Daily Intelligence Briefing - January 15, 2025"

---

## 📆 Scenario 3: Weekend Break (3 days ago)

**Gap:** 3 days
**Category:** `weekend_return`
**Tone:** Fresh start, re-energized

```json
{
  "timeGapContext": {
    "lastBriefingTimestamp": 1736668800000,
    "lastBriefingDate": "2025-01-12",
    "daysSinceLastBriefing": 3,
    "gapCategory": "weekend_break",
    "gapDescription": "3 days since last briefing (weekend)"
  },

  "todaysAgenda": {
    "greeting": "Welcome back after the weekend! Hope you're refreshed.",
    "primaryFocus": "Week planning and momentum building",
    "keyPriorities": [
      "📅 Plan this week's goals",
      "📋 Review last Friday's progress",
      "🎯 Set 3 main objectives for the week",
      "🚀 Start with one quick win"
    ],
    "aiGuidance": "Monday energy! Use this fresh start to plan your week strategically. Start with something easy to build momentum."
  },

  "insights": {
    "lastWeekStats": {
      "tasksCompleted": 15,
      "productiveHours": 18.5,
      "strongDays": ["Tuesday", "Thursday"]
    },
    "achievements": [
      "🏆 Strong week last week - 15 tasks completed",
      "💪 Tuesday was your best day"
    ],
    "suggestions": [
      "Last week you peaked on Tuesdays - replicate that",
      "You were most productive in morning sessions"
    ]
  }
}
```

**Briefing Window Title:** "💼 Monday Briefing - Fresh Week Ahead"

---

## 🗓️ Scenario 4: Week Away (7 days ago)

**Gap:** 7 days
**Category:** `week_return`
**Tone:** Catch-up mode, gentle reintroduction

```json
{
  "timeGapContext": {
    "lastBriefingTimestamp": 1736323200000,
    "lastBriefingDate": "2025-01-08",
    "daysSinceLastBriefing": 7,
    "gapCategory": "weekly_return",
    "gapDescription": "1 week since last briefing"
  },

  "todaysAgenda": {
    "greeting": "Welcome back! It's been a week. Let's ease back in.",
    "primaryFocus": "Catching up and reorienting",
    "keyPriorities": [
      "🔍 Review what happened last week",
      "📋 Check for urgent items",
      "🎯 Set fresh priorities",
      "📝 One catch-up task"
    ],
    "aiGuidance": "After a week away, don't try to do everything at once. Spend the first hour just reviewing and reorienting. Then pick ONE thing to work on."
  },

  "insights": {
    "gapAnalysis": "Week-long gap detected. Old priorities may be stale.",
    "suggestions": [
      "Start by checking what's changed",
      "Don't assume last week's tasks are still relevant",
      "Take an hour to just catch up before diving in",
      "Your old momentum is gone - rebuild it slowly"
    ],
    "recommendations": "Treat today like a mini 'first day back' - low pressure, focus on reorientation"
  }
}
```

**Briefing Window Title:** "🔄 Welcome Back - 1 Week Catch-Up"

---

## 📅 Scenario 5: Month Away (30 days ago)

**Gap:** 30 days
**Category:** `monthly_return`
**Tone:** Fresh start, reset expectations

```json
{
  "timeGapContext": {
    "lastBriefingTimestamp": 1734336000000,
    "lastBriefingDate": "2024-12-16",
    "daysSinceLastBriefing": 30,
    "gapCategory": "monthly_return",
    "gapDescription": "1 month since last briefing"
  },

  "todaysAgenda": {
    "greeting": "Welcome back! It's been a month. Things have probably changed.",
    "primaryFocus": "Fresh start and goal setting",
    "keyPriorities": [
      "🗑️ Clear out old mental models",
      "🎯 Set NEW goals (old ones likely irrelevant)",
      "📋 One simple task to rebuild confidence",
      "🔍 Explore and reacquaint yourself"
    ],
    "aiGuidance": "A month is long enough that your old patterns don't apply. Treat this as a fresh start. Don't try to remember where you left off - start new."
  },

  "insights": {
    "gapAnalysis": "Month-long absence. Significant reset needed.",
    "oldDataNote": "Your last session was December 16th. That data is likely obsolete.",
    "suggestions": [
      "Assume nothing from your last session applies",
      "Set completely fresh goals for this new period",
      "No pressure to be productive immediately",
      "Spend today just getting comfortable again"
    ]
  }
}
```

**Briefing Window Title:** "🌟 Welcome Back - Fresh Start After 1 Month"

---

## 🎉 Scenario 6: Years Away (5 years ago)

**Gap:** 1836 days (5 years)
**Category:** `long_absence`
**Tone:** Extremely gentle, no pressure, celebration of return

```json
{
  "timeGapContext": {
    "lastBriefingTimestamp": 1578268800000,
    "lastBriefingDate": "2020-01-06",
    "daysSinceLastBriefing": 1836,
    "gapCategory": "long_absence",
    "gapDescription": "5 years since last briefing"
  },

  "todaysAgenda": {
    "greeting": "🎉 Welcome back! It's been 5 YEARS since your last session (January 6, 2020).",
    "primaryFocus": "Gentle reintroduction and exploration",
    "contextualNote": "The world has changed dramatically since 2020. No need to be productive today - just get comfortable.",
    "keyPriorities": [
      "🔍 Just explore - Click around, no goals",
      "🧹 Fresh start - Forget old workflows",
      "📝 Open Notepad if you want (totally optional)",
      "🎯 No tasks today - just be present"
    ],
    "aiGuidance": "After 5 years, productivity is NOT the goal. Just explore. Click things. Open programs. Get comfortable. Everything else can wait."
  },

  "insights": {
    "whatHappenedSince2020": [
      "COVID-19 pandemic changed everything",
      "Remote work became the norm",
      "AI assistants (like this one) got dramatically better",
      "Your entire context has probably shifted"
    ],
    "emotionalSupport": "You might feel rusty, lost, or overwhelmed. That's completely normal after 5 years. The goal today is just to show up. You've already succeeded by being here."
  },

  "achievements": [
    "✨ You came back after 5 years - that's huge!",
    "🏆 Every click today is a win"
  ]
}
```

**Briefing Window Title:** "🎉 Welcome Back! It's Been 5 Years..."

---

## Time Gap Calibration Chart

| Gap | Category | Tone | Primary Focus | Pressure Level |
|-----|----------|------|---------------|----------------|
| < 6 hours | `same_day` | Casual check-in | Continue momentum | Medium |
| 1 day | `normal_daily` | Standard energetic | Daily productivity | Medium-High |
| 2-4 days | `weekend_return` | Fresh start | Week planning | Medium |
| 5-14 days | `weekly_return` | Gentle catch-up | Reorientation | Low-Medium |
| 15-60 days | `monthly_return` | Reset mode | New goals | Low |
| 60+ days | `long_absence` | Extremely gentle | Exploration only | None |

---

## Key Principle

**The longer the gap, the gentler the tone and lower the expectations.**

- **Hours ago** = "Let's keep going!"
- **Yesterday** = "New day, let's be productive!"
- **Days ago** = "Welcome back, let's catch up"
- **Weeks ago** = "Fresh start, rebuild slowly"
- **Months+ ago** = "Just explore, no pressure"

This ensures the AI always meets users where they are, not where it thinks they should be.
