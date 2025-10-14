#!/bin/bash

# Automated Meeting Notes Emailer - Test Script
# This script tests the Power Automate flow with sample data

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Automated Meeting Notes Emailer - Test Script            ║${NC}"
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo ""

# Check if FLOW_URL is set
if [ -z "$FLOW_URL" ]; then
    echo -e "${YELLOW}⚠️  FLOW_URL environment variable not set${NC}"
    echo ""
    echo "Please set your flow trigger URL:"
    echo ""
    echo -e "${GREEN}export FLOW_URL=\"https://prod-XX.logic.azure.com:443/workflows/...\"${NC}"
    echo ""
    echo "You can find this URL after importing the flow in Power Automate:"
    echo "1. Open the flow in edit mode"
    echo "2. Click on the 'manual' trigger step"
    echo "3. Copy the 'HTTP POST URL'"
    echo ""
    exit 1
fi

# Function to test with a payload file
test_flow() {
    local payload_file=$1
    local test_name=$2

    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}Testing: ${test_name}${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    if [ ! -f "$payload_file" ]; then
        echo -e "${RED}❌ Payload file not found: $payload_file${NC}"
        return 1
    fi

    echo -e "${YELLOW}📄 Payload:${NC}"
    cat "$payload_file" | python3 -m json.tool
    echo ""

    echo -e "${YELLOW}🚀 Sending request to flow...${NC}"

    response=$(curl -s -w "\n%{http_code}" -X POST "$FLOW_URL" \
        -H "Content-Type: application/json" \
        -d @"$payload_file")

    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    echo ""
    echo -e "${YELLOW}📥 Response:${NC}"
    echo -e "HTTP Status: ${http_code}"

    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✅ Success!${NC}"
        echo ""
        echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
    elif [ "$http_code" = "202" ]; then
        echo -e "${GREEN}✅ Accepted! (Flow triggered successfully)${NC}"
        echo ""
        echo "$body"
    else
        echo -e "${RED}❌ Failed!${NC}"
        echo ""
        echo "$body"
    fi

    echo ""
}

# Main menu
echo "Select a test option:"
echo ""
echo "1. Test with full sample payload (with action items)"
echo "2. Test with minimal sample payload (no action items)"
echo "3. Test with custom JSON file"
echo "4. Interactive mode (enter JSON manually)"
echo ""
read -p "Enter option (1-4): " option
echo ""

case $option in
    1)
        test_flow "sample_payload.json" "Full Sample with Action Items"
        ;;
    2)
        test_flow "sample_payload_minimal.json" "Minimal Sample"
        ;;
    3)
        read -p "Enter path to JSON file: " custom_file
        test_flow "$custom_file" "Custom Payload"
        ;;
    4)
        echo "Enter your JSON payload (press Ctrl+D when done):"
        temp_file=$(mktemp)
        cat > "$temp_file"
        test_flow "$temp_file" "Interactive Payload"
        rm "$temp_file"
        ;;
    *)
        echo -e "${RED}Invalid option${NC}"
        exit 1
        ;;
esac

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Test complete!${NC}"
echo ""
echo "Check your email inbox for the meeting notes."
echo "If you don't see it, check:"
echo "  • Spam/Junk folder"
echo "  • Flow run history in Power Automate portal"
echo "  • Office 365 connection status"
echo ""
echo -e "${BLUE}For troubleshooting, see: AutomatedMeetingNotesEmailer_README.md${NC}"
echo ""
