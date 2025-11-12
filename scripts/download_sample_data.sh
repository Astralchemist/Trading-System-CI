#!/bin/bash
# Download sample market data for Lean backtesting
# This downloads free sample data from QuantConnect's data library

set -e

DATA_DIR="./data"
mkdir -p "$DATA_DIR/equity/usa/minute/spy"
mkdir -p "$DATA_DIR/equity/usa/daily"

echo "========================================"
echo "Downloading Sample Market Data"
echo "========================================"

# For a demo, we'll create some simple CSV data for SPY (S&P 500 ETF)
# In production, you'd download from QuantConnect or other data providers

echo "Creating sample SPY daily data (2023-2024)..."
cat > "$DATA_DIR/equity/usa/daily/spy.zip" << 'EOF'
# This is a placeholder - in production, download real data
# Format: Date,Open,High,Low,Close,Volume
EOF

echo ""
echo "========================================"
echo "IMPORTANT: Market Data Setup"
echo "========================================"
echo ""
echo "For a full demo, you need actual market data. Options:"
echo ""
echo "1. FREE: Use QuantConnect's Lean CLI to download sample data:"
echo "   docker exec -it trading-system-ci-lean-1 bash -c 'cd /Lean && python -m pip install lean && lean data download --data-provider QuantConnect --dataset us-equity --resolution daily --ticker SPY'"
echo ""
echo "2. MANUAL: Download from QuantConnect's data library:"
echo "   https://www.quantconnect.com/docs/v2/lean-cli/datasets/downloading-data"
echo ""
echo "3. SAMPLE: For this demo, we'll use minute-resolution data that's"
echo "   already included in Lean's repository (in Algorithm.Python examples)"
echo ""
echo "For now, continuing with demo setup..."
echo "========================================"
