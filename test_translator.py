"""
Simple test script for Japanese Hedging Translator
"""
import os
import sys

# Suppress OpenAI warnings for testing without API key
os.environ.setdefault("OPENAI_API_KEY", "test_key")

from translator import JapaneseTatemaeTranslator


def test_basic_translation():
    """Test basic translation functionality"""
    print("Testing basic translation...")

    translator = JapaneseTatemaeTranslator()

    # Test refusal
    result = translator.translate("I'm not interested in this job.", level="business")
    assert result["tatemae_text"] is not None
    assert result["intent"] in ["refusal", "disinterest", "neutral_polite"]
    print(f"✓ Refusal test passed: {result['tatemae_text']}")

    # Test disagreement
    result = translator.translate("I disagree with that idea.", level="business")
    assert result["tatemae_text"] is not None
    print(f"✓ Disagreement test passed: {result['tatemae_text']}")

    # Test delay
    result = translator.translate("I can't meet this week.", level="business")
    assert result["tatemae_text"] is not None
    print(f"✓ Delay test passed: {result['tatemae_text']}")

    print("\nAll basic tests passed!")


def test_politeness_levels():
    """Test different politeness levels"""
    print("\nTesting politeness levels...")

    translator = JapaneseTatemaeTranslator()
    input_text = "That's not possible."

    # Test each level
    for level in ["business", "ultra_polite", "casual"]:
        result = translator.translate(input_text, level=level)
        assert result["tatemae_text"] is not None
        assert result["level"] == level
        print(f"✓ {level} level test passed: {result['tatemae_text']}")

    print("\nAll politeness level tests passed!")


def test_simple_interface():
    """Test simplified translation interface"""
    print("\nTesting simple interface...")

    translator = JapaneseTatemaeTranslator()

    text = translator.translate_simple("Your proposal is inefficient.")
    assert text is not None
    assert len(text) > 0
    print(f"✓ Simple interface test passed: {text}")

    print("\nSimple interface test passed!")


def test_all_intents():
    """Test all intent categories"""
    print("\nTesting all intent categories...")

    translator = JapaneseTatemaeTranslator()

    test_cases = {
        "refusal": "I'm not interested.",
        "disagreement": "I disagree.",
        "delay": "I can't do it now.",
        "disinterest": "Not interested in this opportunity.",
        "criticism": "This is inefficient.",
        "neutral_polite": "Thank you for your message."
    }

    for intent, text in test_cases.items():
        result = translator.translate(text)
        assert result["tatemae_text"] is not None
        print(f"✓ {intent} test passed")

    print("\nAll intent tests passed!")


def main():
    """Run all tests"""
    print("=" * 80)
    print("Japanese Hedging Translator - Test Suite")
    print("=" * 80)

    try:
        test_basic_translation()
        test_politeness_levels()
        test_simple_interface()
        test_all_intents()

        print("\n" + "=" * 80)
        print("ALL TESTS PASSED!")
        print("=" * 80)

    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
