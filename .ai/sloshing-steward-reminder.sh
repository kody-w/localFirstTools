#!/bin/bash

# Sloshing Steward Weekly Reminder
# This script sends a notification reminder to run the Sloshing Steward

# Send macOS notification
osascript -e 'display notification "Time to optimize your data sloshing systems! Open the repo in Claude Code and run the steward." with title "🌊 Sloshing Steward Reminder" sound name "Glass"'

# Optional: Open the repo in your default editor (uncomment if desired)
# open -a "Cursor" "/Users/kodyw/Documents/GitHub/localFirstTools3"

# Log the reminder
echo "[$(date)] Sloshing Steward reminder sent" >> /Users/kodyw/Documents/GitHub/localFirstTools3/.ai/steward-reminders.log

# Optional: Open Claude Code in browser (uncomment if desired)
# open "https://claude.ai/code"
