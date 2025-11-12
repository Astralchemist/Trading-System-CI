"""
AI-Powered Trading Strategy Code Generator
Generates and validates QuantConnect Lean trading strategies using AI
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

try:
    from anthropic import Anthropic
except ImportError:
    print("Warning: anthropic library not installed. Using mock mode.")
    Anthropic = None


class StrategyGenerator:
    """Generates trading strategies using AI and validates them"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=self.api_key) if Anthropic and self.api_key else None
        self.output_dir = Path("/app/generated")
        self.output_dir.mkdir(exist_ok=True)

    def generate_strategy(self, prompt: str, language: str = "python") -> Dict[str, str]:
        """
        Generate a trading strategy based on a natural language prompt

        Args:
            prompt: Description of the trading strategy to generate
            language: Programming language (python or csharp)

        Returns:
            Dictionary with 'code' and 'description' keys
        """
        if not self.client:
            return self._generate_mock_strategy(prompt, language)

        system_prompt = f"""You are an expert QuantConnect Lean trading strategy developer.
Generate clean, production-ready {language} trading strategies that follow QuantConnect best practices.

Include:
- Proper initialization and configuration
- Clear variable names and comments
- Risk management (position sizing, stop losses)
- Performance tracking
- Error handling

The strategy should be complete and runnable in the QuantConnect Lean engine."""

        user_prompt = f"""Generate a QuantConnect Lean trading strategy in {language} based on this description:

{prompt}

Provide only the code without explanation."""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                messages=[{
                    "role": "user",
                    "content": user_prompt
                }],
                system=system_prompt
            )

            code = message.content[0].text

            # Clean up code blocks if present
            if "```" in code:
                code = code.split("```")[1]
                if code.startswith("python") or code.startswith("csharp"):
                    code = "\n".join(code.split("\n")[1:])

            return {
                "code": code.strip(),
                "description": prompt,
                "language": language,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error generating strategy: {e}")
            return self._generate_mock_strategy(prompt, language)

    def _generate_mock_strategy(self, prompt: str, language: str) -> Dict[str, str]:
        """Generate a simple mock strategy for testing"""
        if language == "python":
            code = '''from AlgorithmImports import *

class GeneratedStrategy(QCAlgorithm):
    """
    Auto-generated trading strategy
    Description: {description}
    """

    def Initialize(self):
        self.SetStartDate(2023, 1, 1)
        self.SetEndDate(2024, 1, 1)
        self.SetCash(100000)

        # Add equity
        self.symbol = self.AddEquity("SPY", Resolution.Daily).Symbol

        # Set up indicators
        self.sma_fast = self.SMA(self.symbol, 20, Resolution.Daily)
        self.sma_slow = self.SMA(self.symbol, 50, Resolution.Daily)

    def OnData(self, data):
        if not self.sma_fast.IsReady or not self.sma_slow.IsReady:
            return

        # Simple moving average crossover strategy
        if self.sma_fast.Current.Value > self.sma_slow.Current.Value:
            if not self.Portfolio[self.symbol].Invested:
                self.SetHoldings(self.symbol, 1.0)
        else:
            if self.Portfolio[self.symbol].Invested:
                self.Liquidate(self.symbol)
'''.format(description=prompt)
        else:
            code = f'''// Auto-generated C# strategy
// Description: {prompt}

namespace QuantConnect.Algorithm.CSharp
{{
    public class GeneratedStrategy : QCAlgorithm
    {{
        private Symbol _symbol;

        public override void Initialize()
        {{
            SetStartDate(2023, 1, 1);
            SetEndDate(2024, 1, 1);
            SetCash(100000);

            _symbol = AddEquity("SPY", Resolution.Daily).Symbol;
        }}

        public override void OnData(Slice data)
        {{
            if (!Portfolio[_symbol].Invested)
            {{
                SetHoldings(_symbol, 1.0);
            }}
        }}
    }}
}}'''

        return {
            "code": code,
            "description": prompt,
            "language": language,
            "timestamp": datetime.now().isoformat()
        }

    def validate_strategy(self, code: str, language: str) -> Dict[str, any]:
        """
        Validate strategy code using linting and basic checks

        Args:
            code: Strategy code to validate
            language: Programming language

        Returns:
            Dictionary with validation results
        """
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "score": 100
        }

        # Basic validation checks
        if language == "python":
            # Check for required imports
            if "AlgorithmImports" not in code and "QCAlgorithm" not in code:
                results["errors"].append("Missing QuantConnect imports")
                results["valid"] = False

            # Check for required methods
            if "def Initialize(" not in code:
                results["errors"].append("Missing Initialize method")
                results["valid"] = False

            if "def OnData(" not in code:
                results["warnings"].append("Missing OnData method")
                results["score"] -= 20

            # Try pylint if available
            temp_file = self.output_dir / "temp_validate.py"
            try:
                temp_file.write_text(code)
                result = subprocess.run(
                    ["pylint", str(temp_file), "--score=yes"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode != 0:
                    results["warnings"].append("Linting issues found")
            except Exception:
                pass
            finally:
                if temp_file.exists():
                    temp_file.unlink()

        elif language == "csharp":
            if "QCAlgorithm" not in code:
                results["errors"].append("Missing QCAlgorithm base class")
                results["valid"] = False

            if "Initialize()" not in code:
                results["errors"].append("Missing Initialize method")
                results["valid"] = False

        return results

    def save_strategy(self, strategy: Dict[str, str], filename: str) -> Path:
        """Save generated strategy to file"""
        ext = "py" if strategy["language"] == "python" else "cs"
        filepath = self.output_dir / f"{filename}.{ext}"

        filepath.write_text(strategy["code"])

        # Save metadata
        meta_path = self.output_dir / f"{filename}.json"
        meta_path.write_text(json.dumps({
            "description": strategy["description"],
            "language": strategy["language"],
            "timestamp": strategy["timestamp"],
            "filename": str(filepath)
        }, indent=2))

        return filepath


def main():
    """Main entry point for strategy generator"""
    print("=" * 60)
    print("AI Trading Strategy Generator")
    print("=" * 60)

    generator = StrategyGenerator()

    # Example: Generate a simple strategy
    prompts = [
        "Create a momentum strategy using RSI indicator with 30/70 thresholds",
        "Generate a mean reversion strategy using Bollinger Bands",
        "Build a trend following strategy using MACD crossovers"
    ]

    for i, prompt in enumerate(prompts, 1):
        print(f"\n[{i}/{len(prompts)}] Generating: {prompt}")

        strategy = generator.generate_strategy(prompt, language="python")
        validation = generator.validate_strategy(strategy["code"], strategy["language"])

        if validation["valid"]:
            filepath = generator.save_strategy(strategy, f"strategy_{i}")
            print(f" Generated and saved to: {filepath}")
            print(f"  Validation score: {validation['score']}/100")
        else:
            print(f" Validation failed:")
            for error in validation["errors"]:
                print(f"  - {error}")

    print("\n" + "=" * 60)
    print("Strategy generation complete!")
    print(f"Output directory: {generator.output_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
