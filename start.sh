#!/bin/bash
# AI Hiring Agent - Full Stack Startup Script

echo "╔════════════════════════════════════════════════════════════╗"
echo "║          AI HIRING AGENT - STARTUP SCRIPT                 ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Set project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo -e "${BLUE}Project Directory:${NC} $PROJECT_DIR"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv .venv
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source .venv/bin/activate

# Install/Update dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -q -r requirements.txt

# Check .env file
echo -e "${BLUE}Checking .env configuration...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${RED}✗ .env file not found!${NC}"
    echo "Please create .env file with:"
    echo "  GROQ_API_KEY=your_actual_key"
    exit 1
fi

if ! grep -q "GROQ_API_KEY" .env; then
    echo -e "${RED}✗ GROQ_API_KEY not found in .env!${NC}"
    echo "Please add GROQ_API_KEY=your_actual_key to .env"
    exit 1
fi

echo -e "${GREEN}✓ .env configured${NC}"
echo ""

# Run tests (if test file exists)
if [ -f "backend/explainability/test_explainability.py" ]; then
    echo -e "${BLUE}Running tests...${NC}"
    python backend/explainability/test_explainability.py > /tmp/test_output.txt 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ All tests passed${NC}"
    else
        echo -e "${YELLOW}⚠ Tests had issues (non-blocking)${NC}"
        # Don't exit, allow startup to continue
    fi
else
    echo -e "${YELLOW}⚠ No tests found, skipping test run${NC}"
fi
echo ""

echo "╔════════════════════════════════════════════════════════════╗"
echo "║              STARTUP INSTRUCTIONS                         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${BLUE}Option 1: Run both backend and frontend in one terminal${NC}"
echo "  → This will run sequentially (backend first, then frontend)"
echo ""
echo -e "${BLUE}Option 2: Run in separate terminals (RECOMMENDED)${NC}"
echo "  → Terminal 1: python backend/main.py"
echo "  → Terminal 2: streamlit run frontend/app.py"
echo ""
read -p "Choose option (1 or 2): " option

if [ "$option" = "1" ]; then
    echo ""
    echo -e "${YELLOW}Starting backend...${NC}"
    python backend/main.py &
    BACKEND_PID=$!
    
    echo "Waiting for backend to start..."
    sleep 3
    
    # Check if backend is running
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo -e "${RED}✗ Backend failed to start${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Backend running (PID: $BACKEND_PID)${NC}"
    echo ""
    echo -e "${YELLOW}Starting frontend...${NC}"
    streamlit run frontend/app.py
    
    # Kill backend when frontend exits
    kill $BACKEND_PID
    
elif [ "$option" = "2" ]; then
    echo ""
    echo -e "${BLUE}Starting backend in new terminal...${NC}"
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        open -a Terminal "$PROJECT_DIR/start_backend.sh"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        gnome-terminal -- bash "$PROJECT_DIR/start_backend.sh" &
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        # Windows
        start cmd /k "cd $PROJECT_DIR && python backend/main.py"
    fi
    
    echo "Waiting for backend to start..."
    sleep 3
    
    echo -e "${BLUE}Starting frontend...${NC}"
    streamlit run frontend/app.py
else
    echo -e "${RED}Invalid option${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}Application stopped${NC}"
