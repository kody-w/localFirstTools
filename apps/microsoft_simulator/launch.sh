#!/bin/bash

# Macrohard AI Simulation Launcher
# Autonomous Microsoft Simulation Based on Elon Musk's Vision

echo "════════════════════════════════════════════════════════════"
echo "           MACROHARD AI SIMULATION LAUNCHER                 "
echo "    Autonomous Microsoft Simulation • 100% AI-Powered       "
echo "════════════════════════════════════════════════════════════"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 detected: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip --quiet

# Install requirements
echo "📦 Installing dependencies..."
pip install -r requirements.txt --quiet

echo ""
echo "════════════════════════════════════════════════════════════"
echo "                    STARTING SIMULATION                      "
echo "════════════════════════════════════════════════════════════"
echo ""
echo "🚀 Starting Macrohard AI Backend Server..."
echo "   API Server: http://localhost:5000"
echo ""

# Start the Python backend in background
python3 macrohard_agents.py &
BACKEND_PID=$!
echo "✅ Backend server started (PID: $BACKEND_PID)"

# Wait for backend to initialize
sleep 3

echo ""
echo "🌐 Opening Web Interface..."
echo "   Dashboard: file://$(pwd)/index.html"
echo ""

# Open the HTML file in default browser
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open index.html
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open index.html 2>/dev/null || firefox index.html 2>/dev/null || google-chrome index.html 2>/dev/null
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows
    start index.html
fi

echo "════════════════════════════════════════════════════════════"
echo "              SIMULATION RUNNING SUCCESSFULLY!               "
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📊 Dashboard: Open index.html in your browser"
echo "🔌 API Server: http://localhost:5000/api/status"
echo "⚡ Speed: 10x (adjustable in UI)"
echo ""
echo "Commands:"
echo "  • Press Ctrl+C to stop the simulation"
echo "  • Use the web interface for full control"
echo ""
echo "Features:"
echo "  • 18 Autonomous AI Agents working in parallel"
echo "  • Real-time product development and launches"
echo "  • Live inter-agent communication transcripts"
echo "  • Export/Import simulation state"
echo "  • Adjustable simulation speed (1x-100x)"
echo ""
echo "════════════════════════════════════════════════════════════"

# Wait for user to stop
echo ""
echo "Press Ctrl+C to stop the simulation..."
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping simulation..."
    kill $BACKEND_PID 2>/dev/null
    echo "✅ Simulation stopped"
    echo "Thank you for using Macrohard AI!"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT

# Keep script running
wait $BACKEND_PID