#!/bin/bash
# Interactive menu for running backtests

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

clear
echo -e "${BLUE}╔════════════════════════════════════════╗"
echo "║   Trading System - Backtest Menu      ║"
echo -e "╚════════════════════════════════════════╝${NC}"
echo ""

echo -e "${YELLOW}Select an algorithm to backtest:${NC}"
echo ""
echo "  1) SimpleBuyAndHold      - Buy SPY and hold (2020-2023)"
echo "  2) DemoMomentumStrategy  - SMA crossover strategy"
echo "  3) List generated strategies"
echo "  4) Exit"
echo ""
read -p "Enter your choice [1-4]: " choice

case $choice in
    1)
        echo ""
        echo -e "${GREEN}Running SimpleBuyAndHold strategy...${NC}"
        echo ""
        ./scripts/run_backtest.sh SimpleBuyAndHold
        ;;
    2)
        echo ""
        echo -e "${GREEN}Running DemoMomentumStrategy...${NC}"
        echo ""
        ./scripts/run_backtest.sh DemoMomentumStrategy
        ;;
    3)
        echo ""
        echo -e "${YELLOW}Generated strategies:${NC}"
        ls -la ./services/strategy/generated/ 2>/dev/null || echo "No generated strategies found"
        echo ""
        ;;
    4)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
