#!/bin/bash
# Run Lean backtest with selected algorithm

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================"
echo "Lean Backtesting Runner"
echo -e "========================================${NC}"
echo ""

# Check if algorithm argument provided
if [ -z "$1" ]; then
    echo -e "${YELLOW}Available algorithms:${NC}"
    echo ""
    echo "  1. SimpleBuyAndHold      - Basic buy and hold SPY strategy"
    echo "  2. DemoMomentumStrategy  - Moving average crossover strategy"
    echo ""
    echo "Usage: $0 <algorithm-name>"
    echo "Example: $0 SimpleBuyAndHold"
    echo ""
    exit 1
fi

ALGORITHM=$1
ALGO_FILE="./algorithms/${ALGORITHM}.py"

# Check if algorithm file exists
if [ ! -f "$ALGO_FILE" ]; then
    echo -e "${YELLOW}Error: Algorithm file not found: $ALGO_FILE${NC}"
    echo ""
    echo "Available algorithms:"
    ls -1 ./algorithms/*.py 2>/dev/null | xargs -n1 basename | sed 's/.py$//' | sed 's/^/  - /'
    exit 1
fi

echo -e "${GREEN}Running backtest for: $ALGORITHM${NC}"
echo ""

# Run Lean in Docker with the selected algorithm
echo "Starting Lean engine..."
echo ""

# Copy algorithm to a location Lean can access
sudo docker cp "$ALGO_FILE" trading-system-ci-lean-1:/Lean/Algorithm.Python/${ALGORITHM}.py

# Run Lean with the algorithm
sudo docker exec -it trading-system-ci-lean-1 \
    dotnet /Lean/Launcher/bin/Release/QuantConnect.Lean.Launcher.dll \
    --algorithm-type-name "$ALGORITHM" \
    --algorithm-language "Python" \
    --algorithm-location "../../../Algorithm.Python/${ALGORITHM}.py"

echo ""
echo -e "${GREEN}Backtest complete!${NC}"
echo ""

# Create results directory if it doesn't exist
mkdir -p ./results/${ALGORITHM}

# Copy results from container to host
echo "Copying results to ./results/${ALGORITHM}/ ..."
sudo docker cp trading-system-ci-lean-1:/Lean/log.txt ./results/${ALGORITHM}/backtest.log 2>/dev/null || echo "No log file found"
sudo docker exec trading-system-ci-lean-1 find /Lean -name "*.json" -o -name "*.html" -o -name "*.csv" 2>/dev/null | while read file; do
    sudo docker cp trading-system-ci-lean-1:"$file" ./results/${ALGORITHM}/ 2>/dev/null
done

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Results Summary:${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Show log output
if [ -f "./results/${ALGORITHM}/backtest.log" ]; then
    echo "📊 Backtest Log (last 50 lines):"
    echo ""
    tail -50 "./results/${ALGORITHM}/backtest.log"
    echo ""
else
    echo "⚠️  No log file generated"
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo "📁 All results saved to: ./results/${ALGORITHM}/"
echo ""
echo "Files created:"
ls -lh ./results/${ALGORITHM}/ 2>/dev/null || echo "  (no files)"
echo ""
echo -e "${BLUE}========================================${NC}"
