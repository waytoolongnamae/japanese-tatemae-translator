#!/usr/bin/env python3
"""
Test script for fidelity levels
Tests how different fidelity levels affect translation output
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from translator import JapaneseTatemaeTranslator

def test_fidelity_levels():
    """Test translation with different fidelity levels"""
    translator = JapaneseTatemaeTranslator()

    # Test cases with direct messages
    test_cases = [
        "I'm not interested in this job.",
        "Your proposal won't work.",
        "I can't meet this week.",
        "I disagree with that idea.",
        "That's not possible.",
        "This code has too many bugs.",
        "I don't want to attend this meeting.",
        "Your design is poorly structured."
    ]

    print("=" * 80)
    print("FIDELITY LEVEL TEST")
    print("=" * 80)
    print()

    for i, test_input in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"Test Case {i}: {test_input}")
        print(f"{'='*80}\n")

        for fidelity in ["high", "medium", "low"]:
            print(f"{fidelity.upper()} FIDELITY:")
            print("-" * 40)

            result = translator.translate(
                test_input,
                level="business",
                fidelity=fidelity
            )

            print(f"Translation: {result['tatemae_text']}")
            print(f"Intent: {result['intent']}")
            print(f"Confidence: {result['confidence']:.2f}")
            print()

    print("=" * 80)
    print("Test complete. Review the outputs above.")
    print()
    print("Expected behavior:")
    print("- HIGH: Should be direct and frank, minimal euphemisms")
    print("- MEDIUM: Balanced tatemae with moderate indirection")
    print("- LOW: Maximum Kyoto-style indirection and politeness")
    print("=" * 80)

if __name__ == "__main__":
    test_fidelity_levels()
