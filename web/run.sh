#!/bin/bash
# Simple script to run the web app

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🎌 Starting Japanese Hedging Translator Web App${NC}"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo -e "${GREEN}✓${NC} Created .env file"
    echo "⚠️  Please edit .env and add your DEEPSEEK_API_KEY_CHAT"
    echo ""
fi

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements-web.txt
    echo -e "${GREEN}✓${NC} Dependencies installed"
    echo ""
fi

# Run the app
echo -e "${GREEN}Starting server...${NC}"
echo ""
python app.py
