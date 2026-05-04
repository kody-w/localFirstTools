#!/bin/bash

echo "🤖 Installing Agent Browser..."
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Make CLI executable
echo "🔧 Setting up CLI..."
chmod +x src/cli.js

# Link globally (optional)
read -p "Install CLI globally? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]
then
    npm link
    echo "✓ CLI installed globally as 'agent-browser'"
else
    echo "ℹ️  Run with: node src/cli.js"
fi

# Create directories
echo "📁 Creating directories..."
mkdir -p sessions screenshots pdfs downloads

echo ""
echo "✅ Installation complete!"
echo ""
echo "Quick Start:"
echo "  Interactive mode:  agent-browser"
echo "  OR:                node src/cli.js"
echo ""
echo "  First command:     agent-browser goto 'https://example.com' --extract"
echo ""
echo "  Examples:          node examples/simple-navigation.js"
echo ""
echo "Documentation:"
echo "  README.md          - Overview and features"
echo "  QUICKSTART.md      - Get started in 5 minutes"
echo "  docs/AGENT_GUIDE.md - Building AI agents"
echo "  docs/API.md        - Complete API reference"
echo ""
echo "Happy browsing! 🚀"
