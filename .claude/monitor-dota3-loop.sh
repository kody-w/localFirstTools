#!/bin/bash
# DOTA 3 LEGACY - Ralph Loop Monitor
# Check current progress of the running loop

STATE_FILE="/Users/kodywildfeuer/Documents/GitHub/m365-agents-for-python/localFirstTools/.claude/ralph-loop.local.md"
PROJECT_DIR="/Users/kodywildfeuer/Documents/GitHub/m365-agents-for-python/localFirstTools"

echo "========================================="
echo "  DOTA 3 LEGACY - Loop Monitor"
echo "========================================="
echo ""

# Check if state file exists
if [ ! -f "$STATE_FILE" ]; then
    echo "✗ Loop state file not found. Has the loop been initialized?"
    exit 1
fi

# Extract key info from state file
echo "LOOP STATUS:"
grep "^status:" "$STATE_FILE" | head -1
grep "^current_iteration:" "$STATE_FILE" | head -1
grep "^max_iterations:" "$STATE_FILE" | head -1
grep "^started_at:" "$STATE_FILE" | head -1

echo ""
echo "RECENT GIT COMMITS:"
cd "$PROJECT_DIR"
git log --oneline --grep="dota3\|DOTA" -10 2>/dev/null || echo "No dota3-related commits yet"

echo ""
echo "CURRENT FILE STATE:"
/Users/kodywildfeuer/Documents/GitHub/m365-agents-for-python/localFirstTools/.claude/verify-dota3.sh

echo ""
echo "LAST 10 LINES OF STATE FILE:"
tail -10 "$STATE_FILE"

echo ""
echo "========================================="
