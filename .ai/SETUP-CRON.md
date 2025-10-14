# 🌊 Setup Sloshing Steward Cron Job

## Quick Setup

Run this command to add the weekly reminder to your crontab:

```bash
(crontab -l 2>/dev/null; echo "# Sloshing Steward Weekly Reminder - Every Friday at 5 PM"; echo "0 17 * * 5 /Users/kodyw/Documents/GitHub/localFirstTools3/.ai/sloshing-steward-reminder.sh") | crontab -
```

---

## What This Does

- ⏰ **When**: Every Friday at 5:00 PM
- 🔔 **Action**: Sends macOS notification reminder
- 📝 **Logs**: Writes to `.ai/steward-reminders.log`

---

## Custom Schedule Options

### Every Friday at 5 PM (recommended)
```bash
0 17 * * 5 /Users/kodyw/Documents/GitHub/localFirstTools3/.ai/sloshing-steward-reminder.sh
```

### Every Monday at 9 AM
```bash
0 9 * * 1 /Users/kodyw/Documents/GitHub/localFirstTools3/.ai/sloshing-steward-reminder.sh
```

### First day of every month at 10 AM
```bash
0 10 1 * * /Users/kodyw/Documents/GitHub/localFirstTools3/.ai/sloshing-steward-reminder.sh
```

### Every Sunday at 8 PM
```bash
0 20 * * 0 /Users/kodyw/Documents/GitHub/localFirstTools3/.ai/sloshing-steward-reminder.sh
```

---

## Cron Schedule Format

```
* * * * * command
│ │ │ │ │
│ │ │ │ └─── Day of week (0-7, Sunday=0 or 7)
│ │ │ └───── Month (1-12)
│ │ └─────── Day of month (1-31)
│ └───────── Hour (0-23)
└─────────── Minute (0-59)
```

---

## Verify Cron Job

Check that it was added:
```bash
crontab -l
```

You should see:
```
# Sloshing Steward Weekly Reminder - Every Friday at 5 PM
0 17 * * 5 /Users/kodyw/Documents/GitHub/localFirstTools3/.ai/sloshing-steward-reminder.sh
```

---

## Test the Reminder

Run the script manually to test:
```bash
/Users/kodyw/Documents/GitHub/localFirstTools3/.ai/sloshing-steward-reminder.sh
```

You should see a macOS notification pop up.

---

## Check Reminder Log

View reminder history:
```bash
cat /Users/kodyw/Documents/GitHub/localFirstTools3/.ai/steward-reminders.log
```

---

## Remove Cron Job

If you want to remove the reminder:
```bash
crontab -l | grep -v "sloshing-steward-reminder" | crontab -
```

---

## The Workflow

1. 📅 **Friday 5 PM**: Cron sends notification
2. 🔔 **You see reminder**: "Time to optimize!"
3. 💻 **Open repo**: In Claude Code
4. ⌨️ **Run command**: "Run the sloshing steward"
5. ⏳ **Wait 25-30 min**: Agent optimizes everything
6. ✅ **Review report**: See improvements
7. 🎉 **Done!**: System is optimized for next week

---

**Recommended**: Friday at 5 PM (end of week cleanup)
**Alternative**: Sunday evening (prepare for Monday)
**Frequency**: Weekly (7 days between runs)
