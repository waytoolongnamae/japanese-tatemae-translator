#!/bin/bash
# Simple script to run the web app

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🎌 Starting Japanese Hedging Translator Web App${NC}"
echo ""

# Check if root .env exists (web app uses parent directory's .env)
if [ ! -f ../.env ]; then
    echo "⚠️  No .env file found in root directory"
    echo "Creating .env from .env.example..."
    cp ../.env.example ../.env
    echo -e "${GREEN}✓${NC} Created .env file in root directory"
    echo "⚠️  Please edit ../env and add your DEEPSEEK_API_KEY_CHAT"
    echo ""
fi

# Detect package manager
if command -v uv &> /dev/null; then
    PACKAGE_MANAGER="uv"
    echo -e "${YELLOW}Using uv (faster package manager)${NC}"
else
    PACKAGE_MANAGER="pip"
    echo -e "${YELLOW}Using pip${NC}"
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -d ".venv" ]; then
        echo "Activating virtual environment..."
        source .venv/bin/activate
        echo -e "${GREEN}✓${NC} Virtual environment activated"
    else
        echo "Creating virtual environment..."
        if [ "$PACKAGE_MANAGER" = "uv" ]; then
            uv venv
        else
            python -m venv .venv
        fi
        source .venv/bin/activate
        echo -e "${GREEN}✓${NC} Virtual environment created and activated"
    fi
    echo ""
fi

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "Installing dependencies..."
    if [ "$PACKAGE_MANAGER" = "uv" ]; then
        uv pip install -r requirements-web.txt
    else
        pip install -r requirements-web.txt
    fi
    echo -e "${GREEN}✓${NC} Dependencies installed"
    echo ""
fi

# Run the app
echo -e "${GREEN}Starting server...${NC}"
echo ""
python app.py
