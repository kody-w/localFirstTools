#!/bin/bash
# DOTA 3 LEGACY Ralph Loop Launcher

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
PROMPT_FILE="$SCRIPT_DIR/ralph-loop-prompt.md"
STATE_FILE="$SCRIPT_DIR/ralph-loop.local.md"

echo "========================================="
echo "  DOTA 3 LEGACY - Ralph Loop Launcher"
echo "========================================="
echo ""
echo "Target: dota3-legacy.html"
echo "Max Iterations: 150"
echo "Estimated Duration: 24 hours"
echo "Promise: DOTA3_LEGACY_COMPLETE_ALL_FEATURES_POLISHED"
echo ""
echo "Initial State:"
/Users/kodywildfeuer/Documents/GitHub/m365-agents-for-python/localFirstTools/.claude/verify-dota3.sh
echo ""
echo "========================================="
echo ""
read -p "Launch Ralph loop? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Launching Ralph loop..."
    echo "Press Ctrl+C to cancel at any time"
    echo ""

    cd "$PROJECT_DIR"

    # Update state file with start time
    START_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    echo "Started at: $START_TIME"

    # Launch Claude Code with the prompt
    claude --prompt-file "$PROMPT_FILE" --max-iterations 150

    echo ""
    echo "========================================="
    echo "Ralph loop completed or interrupted"
    echo "Final State:"
    /Users/kodywildfeuer/Documents/GitHub/m365-agents-for-python/localFirstTools/.claude/verify-dota3.sh
else
    echo "Launch cancelled"
    exit 0
fi
