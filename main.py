"""
Main entry point for Japanese Hedging Translator
Demonstrates usage with example inputs
"""
import logging
from translator import JapaneseTatemaeTranslator
from config.logging import configure_logging
from config.settings import validate_settings

configure_logging()

logger = logging.getLogger(__name__)


def main():
    """Run example translations"""
    settings_issues = validate_settings()
    if settings_issues["errors"]:
        for error in settings_issues["errors"]:
            logger.error(error)
        raise SystemExit(1)
    for warning in settings_issues["warnings"]:
        logger.warning(warning)
    print("=== Japanese Hedging Translator (建前 Translator) ===\n")

    # Initialize translator
    translator = JapaneseTatemaeTranslator()

    # Example test cases
    test_cases = [
        {
            "input": "I'm not interested in this job.",
            "level": "business",
            "description": "Refusal (recruiter message)"
        },
        {
            "input": "Your proposal is inefficient.",
            "level": "business",
            "description": "Criticism (work context)"
        },
        {
            "input": "I can't meet this week.",
            "level": "business",
            "description": "Delay (scheduling)"
        },
        {
            "input": "I disagree with that idea.",
            "level": "business",
            "description": "Disagreement"
        },
        {
            "input": "That's not possible.",
            "level": "ultra_polite",
            "description": "Refusal (ultra polite)"
        },
        {
            "input": "I don't want to attend this meeting.",
            "level": "business",
            "description": "Disinterest"
        },
        {
            "input": "This code needs more work.",
            "level": "casual",
            "description": "Criticism (casual)"
        }
    ]

    print("Running example translations:\n")
    print("=" * 80)

    for i, test in enumerate(test_cases, 1):
        print(f"\n[Example {i}] {test['description']}")
        print(f"Level: {test['level']}")
        print(f"Input:  \"{test['input']}\"")

        result = translator.translate(test['input'], level=test['level'])

        print(f"Output: \"{result['tatemae_text']}\"")
        print(f"Intent: {result['intent']} (confidence: {result.get('confidence', 0):.2f})")
        print("-" * 80)

    print("\n=== Translation Complete ===")
    print("\nTo use in your code:")
    print("  from translator import JapaneseTatemaeTranslator")
    print("  translator = JapaneseTatemaeTranslator()")
    print("  result = translator.translate('Your message here', level='business')")
    print("  print(result['tatemae_text'])")


if __name__ == "__main__":
    main()
