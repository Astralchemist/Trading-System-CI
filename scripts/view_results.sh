#!/bin/bash
# View backtest results

BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}========================================"
echo "Backtest Results Viewer"
echo -e "========================================${NC}"
echo ""

if [ -z "$1" ]; then
    echo "Available results:"
    echo ""
    for dir in ./results/*/; do
        if [ -d "$dir" ]; then
            algo=$(basename "$dir")
            echo "  📊 $algo"
            if [ -f "$dir/backtest.log" ]; then
                # Show last line which usually has summary
                echo "      $(tail -1 "$dir/backtest.log" | head -c 100)"
            fi
            echo ""
        fi
    done
    echo ""
    echo "Usage: $0 <algorithm-name>"
    echo "Example: $0 SimpleBuyAndHold"
    exit 0
fi

ALGORITHM=$1
RESULTS_DIR="./results/${ALGORITHM}"

if [ ! -d "$RESULTS_DIR" ]; then
    echo -e "${YELLOW}No results found for: $ALGORITHM${NC}"
    echo ""
    echo "Run a backtest first:"
    echo "  ./scripts/run_backtest.sh $ALGORITHM"
    exit 1
fi

echo -e "${GREEN}Results for: $ALGORITHM${NC}"
echo ""
echo -e "${BLUE}Files:${NC}"
ls -lh "$RESULTS_DIR"
echo ""

if [ -f "$RESULTS_DIR/backtest.log" ]; then
    echo -e "${BLUE}========================================${NC}"
    echo -e "${GREEN}Backtest Log:${NC}"
    echo -e "${BLUE}========================================${NC}"
    cat "$RESULTS_DIR/backtest.log"
    echo ""
fi

# Show JSON files if they exist
for json_file in "$RESULTS_DIR"/*.json; do
    if [ -f "$json_file" ]; then
        echo -e "${BLUE}========================================${NC}"
        echo -e "${GREEN}$(basename "$json_file"):${NC}"
        echo -e "${BLUE}========================================${NC}"
        cat "$json_file" | python3 -m json.tool 2>/dev/null || cat "$json_file"
        echo ""
    fi
done

echo ""
echo -e "${GREEN}✅ Results location: $RESULTS_DIR${NC}"
