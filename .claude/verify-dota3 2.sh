#!/bin/bash
# DOTA 3 LEGACY - Verification Script
# Checks if critical features are implemented

FILE="/Users/kodywildfeuer/Documents/GitHub/m365-agents-for-python/localFirstTools/dota3-legacy.html"

echo "=== DOTA 3 LEGACY Feature Verification ==="
echo ""

# Check file exists and size
if [ -f "$FILE" ]; then
    SIZE=$(wc -l < "$FILE")
    echo "✓ File exists: $SIZE lines"
else
    echo "✗ File not found!"
    exit 1
fi

# Critical Features
echo ""
echo "CRITICAL FEATURES:"

# Ability System
if grep -q "castAbility\|useAbility" "$FILE" && grep -q "cooldown" "$FILE" && grep -q "manaCost" "$FILE"; then
    echo "✓ Ability system with cooldowns and mana"
else
    echo "✗ Ability system incomplete"
fi

# Jungle Camps
if grep -q "jungleCamp\|neutralCamp\|spawnCamp" "$FILE"; then
    echo "✓ Jungle camp system"
else
    echo "✗ Jungle camps missing"
fi

# Item Shop
if grep -q "shop\|buyItem\|purchaseItem" "$FILE"; then
    ITEM_COUNT=$(grep -c "itemId\|item:" "$FILE")
    echo "✓ Item shop ($ITEM_COUNT item references)"
else
    echo "✗ Item shop incomplete"
fi

# Sound Effects
if grep -q "AudioContext\|createOscillator\|playSound" "$FILE"; then
    echo "✓ Sound system (Web Audio API)"
else
    echo "✗ Sound effects missing"
fi

# AI Enemies
if grep -q "enemyAI\|AIController\|botControl" "$FILE"; then
    echo "✓ AI enemy system"
else
    echo "✗ AI enemies missing"
fi

# Visual Effects
if grep -q "particle\|ParticleSystem\|createEffect" "$FILE"; then
    echo "✓ Visual effects system"
else
    echo "✗ Visual effects incomplete"
fi

echo ""
echo "IMPORTANT FEATURES:"

# Tooltips
if grep -q "tooltip\|showTooltip" "$FILE"; then
    echo "✓ UI tooltips"
else
    echo "✗ Tooltips missing"
fi

# Kill Feed
if grep -q "killFeed\|combatLog" "$FILE"; then
    echo "✓ Kill feed"
else
    echo "✗ Kill feed missing"
fi

# AI Teammates
if grep -q "teammate.*AI\|allyAI\|friendlyBot" "$FILE"; then
    echo "✓ AI teammates"
else
    echo "✗ AI teammates missing"
fi

echo ""
echo "=== Verification Complete ==="
