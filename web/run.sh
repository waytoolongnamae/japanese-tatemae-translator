#!/bin/bash
# Simple script to run the web app

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Parse arguments
MODEL=""
PORT="8000"

while [[ $# -gt 0 ]]; do
    case $1 in
        --model|-M)
            MODEL="$2"
            shift 2
            ;;
        --port|-p)
            PORT="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: ./run.sh [options]"
            echo ""
            echo "Options:"
            echo "  --model, -M MODEL      LLM provider (deepseek or openai)"
            echo "  --port, -p PORT        Port to run on (default: 8000)"
            echo "  --help, -h             Show this help message"
            echo ""
            echo "Examples:"
            echo "  ./run.sh                    # Run with default model"
            echo "  ./run.sh --model openai     # Run with OpenAI model"
            echo "  ./run.sh -M deepseek        # Run with DeepSeek model"
            echo "  ./run.sh -p 3000            # Run on port 3000"
            echo ""
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}🎌 Starting Japanese Hedging Translator Web App${NC}"
if [ -n "$MODEL" ]; then
    echo -e "${GREEN}Model: $MODEL${NC}"
fi
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

# Set MODEL_PROVIDER environment variable if specified
if [ -n "$MODEL" ]; then
    export MODEL_PROVIDER="$MODEL"
fi

python app.py
