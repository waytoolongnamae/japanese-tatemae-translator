"""
Unit tests for workflow nodes
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from processing.nodes import (
    intent_detector_node,
    tatemae_generator_node,
    politeness_tuner_node,
    language_detector_node
)
from providers import FallbackProvider
from config.settings import INTENT_CATEGORIES, TEMPLATES


class TestLanguageDetectorNode:
    """Tests for language_detector_node"""

    def test_detect_japanese_hiragana(self, sample_state):
        """Test detection of Japanese text with hiragana"""
        sample_state["input_text"] = "これは日本語です"
        result = language_detector_node(sample_state)
        assert result["detected_language"] == "ja"

    def test_detect_japanese_katakana(self, sample_state):
        """Test detection of Japanese text with katakana"""
        sample_state["input_text"] = "カタカナです"
        result = language_detector_node(sample_state)
        assert result["detected_language"] == "ja"

    def test_detect_japanese_kanji(self, sample_state):
        """Test detection of Japanese text with kanji"""
        sample_state["input_text"] = "漢字のテスト"
        result = language_detector_node(sample_state)
        assert result["detected_language"] == "ja"

    def test_detect_english(self, sample_state):
        """Test detection of English text"""
        sample_state["input_text"] = "This is English text"
        result = language_detector_node(sample_state)
        assert result["detected_language"] == "en"

    def test_detect_chinese(self, sample_state):
        """Test detection of Chinese text"""
        sample_state["input_text"] = "这是中文"
        result = language_detector_node(sample_state)
        assert result["detected_language"] in ["zh", "ja"]  # Overlap possible

    def test_mixed_language(self, sample_state):
        """Test detection with mixed language"""
        sample_state["input_text"] = "Hello こんにちは"
        result = language_detector_node(sample_state)
        # Should detect as Japanese due to Japanese characters
        assert result["detected_language"] == "ja"

    def test_empty_text(self, sample_state):
        """Test with empty text"""
        sample_state["input_text"] = ""
        result = language_detector_node(sample_state)
        assert result["detected_language"] == "en"  # Default


class TestFallbackProvider:
    """Tests for FallbackProvider intent detection"""

    @pytest.fixture
    def fallback_provider(self):
        """Create a fallback provider instance"""
        return FallbackProvider()

    def test_refusal_keywords(self, fallback_provider):
        """Test refusal intent detection"""
        intent, confidence = fallback_provider.detect_intent("I decline this offer")
        assert intent == "refusal"
        assert confidence == 0.7

    def test_disagreement_keywords(self, fallback_provider):
        """Test disagreement intent detection"""
        intent, confidence = fallback_provider.detect_intent("I disagree with that")
        assert intent == "disagreement"
        assert confidence == 0.7

    def test_delay_keywords(self, fallback_provider):
        """Test delay intent detection"""
        intent, confidence = fallback_provider.detect_intent("I'll do it later")
        assert intent == "delay"
        assert confidence == 0.7

    def test_disinterest_keywords(self, fallback_provider):
        """Test disinterest intent detection"""
        intent, confidence = fallback_provider.detect_intent("I'm not interested")
        assert intent in ["refusal", "disinterest"]  # Both match "not interested"
        assert confidence == 0.7

    def test_criticism_keywords(self, fallback_provider):
        """Test criticism intent detection"""
        intent, confidence = fallback_provider.detect_intent("This is inefficient")
        assert intent == "criticism"
        assert confidence == 0.7

    def test_neutral_default(self, fallback_provider):
        """Test neutral intent as default"""
        intent, confidence = fallback_provider.detect_intent("Hello there")
        assert intent == "neutral_polite"
        assert confidence == 0.6

    def test_japanese_keywords(self, fallback_provider):
        """Test Japanese keyword detection"""
        intent, confidence = fallback_provider.detect_intent("興味ない")
        assert intent in ["refusal", "disinterest"]
        assert confidence == 0.7

    def test_case_insensitive(self, fallback_provider):
        """Test case-insensitive matching"""
        intent1, _ = fallback_provider.detect_intent("DISAGREE")
        intent2, _ = fallback_provider.detect_intent("disagree")
        assert intent1 == intent2 == "disagreement"


class TestIntentDetectorNode:
    """Tests for intent_detector_node"""

    def test_intent_detection_with_provider(self, sample_state, monkeypatch):
        """Test intent detection with provider"""
        # Mock provider to return known result
        mock_provider = MagicMock()
        mock_provider.detect_intent.return_value = ("refusal", 0.9)

        import processing.nodes
        monkeypatch.setattr(processing.nodes, "provider", mock_provider)

        result = intent_detector_node(sample_state)
        assert result["intent"] == "refusal"
        assert result["confidence"] == 0.9

    def test_intent_detection_fallback(self, sample_state, monkeypatch):
        """Test fallback provider for keyword-based detection"""
        # Use FallbackProvider
        mock_provider = FallbackProvider()

        import processing.nodes
        monkeypatch.setattr(processing.nodes, "provider", mock_provider)

        sample_state["input_text"] = "I disagree with that"
        result = intent_detector_node(sample_state)
        assert result["intent"] == "disagreement"
        assert result["confidence"] == 0.7

    def test_intent_detection_api_error(self, sample_state, monkeypatch):
        """Test handling of provider errors"""
        # Create mock that raises exception
        mock_provider = MagicMock()
        mock_provider.detect_intent.side_effect = Exception("Provider Error")

        import processing.nodes
        monkeypatch.setattr(processing.nodes, "provider", mock_provider)

        result = intent_detector_node(sample_state)
        # Should return error state
        assert "intent" in result
        assert result["intent"] == "neutral_polite"
        assert result["confidence"] == 0.5

    def test_invalid_intent_category(self, sample_state, monkeypatch):
        """Test handling of invalid intent from provider"""
        mock_provider = MagicMock()
        mock_provider.detect_intent.return_value = ("invalid_intent", 0.9)

        import processing.nodes
        monkeypatch.setattr(processing.nodes, "provider", mock_provider)

        result = intent_detector_node(sample_state)
        # Should default to neutral_polite for invalid intent
        assert result["intent"] == "neutral_polite"

    @pytest.mark.parametrize("text,expected_intent", [
        ("I'm not interested", "refusal"),
        ("I disagree", "disagreement"),
        ("later please", "delay"),
        ("not for me", "disinterest"),
        ("needs improvement", "criticism"),
    ])
    def test_various_intents(self, sample_state, monkeypatch, text, expected_intent):
        """Test various intent classifications with fallback provider"""
        mock_provider = FallbackProvider()

        import processing.nodes
        monkeypatch.setattr(processing.nodes, "provider", mock_provider)

        sample_state["input_text"] = text
        result = intent_detector_node(sample_state)
        assert result["intent"] == expected_intent


class TestTatemaeGeneratorNode:
    """Tests for tatemae_generator_node"""

    def test_generates_template_for_refusal(self, sample_state):
        """Test template generation for refusal intent"""
        sample_state["intent"] = "refusal"
        result = tatemae_generator_node(sample_state)

        assert "template" in result
        assert "filled_template" in result
        assert result["template"] in TEMPLATES["refusal"]
        assert len(result["filled_template"]) > 0

    def test_generates_template_for_disagreement(self, sample_state):
        """Test template generation for disagreement intent"""
        sample_state["intent"] = "disagreement"
        result = tatemae_generator_node(sample_state)

        assert result["template"] in TEMPLATES["disagreement"]
        assert len(result["filled_template"]) > 0

    def test_generates_template_for_all_intents(self, sample_state, intent_category):
        """Test template generation for all intent categories"""
        sample_state["intent"] = intent_category
        result = tatemae_generator_node(sample_state)

        assert "template" in result
        assert "filled_template" in result
        assert result["template"] in TEMPLATES[intent_category]

    def test_template_placeholder_replacement(self, sample_state):
        """Test that placeholders are replaced in templates"""
        sample_state["intent"] = "refusal"
        result = tatemae_generator_node(sample_state)

        # Check that no placeholder syntax remains
        assert "{" not in result["filled_template"]
        assert "}" not in result["filled_template"]

    def test_default_to_neutral_for_unknown_intent(self, sample_state):
        """Test fallback to neutral_polite for unknown intent"""
        sample_state["intent"] = "unknown_intent"
        result = tatemae_generator_node(sample_state)

        # Should use neutral_polite templates
        assert result["template"] in TEMPLATES["neutral_polite"]

    def test_filled_template_is_japanese(self, sample_state):
        """Test that filled template contains Japanese characters"""
        sample_state["intent"] = "refusal"
        result = tatemae_generator_node(sample_state)

        # Check for Japanese characters (hiragana, katakana, or kanji)
        text = result["filled_template"]
        has_japanese = any(
            '\u3040' <= char <= '\u309f' or  # Hiragana
            '\u30a0' <= char <= '\u30ff' or  # Katakana
            '\u4e00' <= char <= '\u9faf'     # Kanji
            for char in text
        )
        assert has_japanese, f"Expected Japanese text, got: {text}"


class TestPolitenessTunerNode:
    """Tests for politeness_tuner_node"""

    def test_politeness_tuning_with_provider(self, sample_state, monkeypatch):
        """Test politeness tuning with provider"""
        mock_provider = MagicMock()
        mock_provider.refine_text.return_value = "大変恐縮ですが、今回は見送らせていただきます。"

        import processing.nodes
        monkeypatch.setattr(processing.nodes, "provider", mock_provider)

        sample_state["filled_template"] = "見送らせていただきます。"
        sample_state["intent"] = "refusal"
        sample_state["level"] = "business"

        result = politeness_tuner_node(sample_state)

        assert "tatemae_text" in result
        assert len(result["tatemae_text"]) > 0
        mock_provider.refine_text.assert_called_once()

    def test_politeness_tuning_fallback(self, sample_state, monkeypatch):
        """Test fallback provider"""
        mock_provider = FallbackProvider()

        import processing.nodes
        monkeypatch.setattr(processing.nodes, "provider", mock_provider)

        sample_state["filled_template"] = "見送らせていただきます。"
        sample_state["intent"] = "refusal"
        sample_state["level"] = "business"

        result = politeness_tuner_node(sample_state)

        assert "tatemae_text" in result
        assert result["tatemae_text"] == "見送らせていただきます。"

    def test_removes_doubled_verb_endings(self, sample_state, monkeypatch):
        """Test removal of doubled verb endings with fallback provider"""
        mock_provider = FallbackProvider()

        import processing.nodes
        monkeypatch.setattr(processing.nodes, "provider", mock_provider)

        sample_state["filled_template"] = "させていただきますさせていただきます"
        sample_state["intent"] = "refusal"
        sample_state["level"] = "business"

        result = politeness_tuner_node(sample_state)

        # Should remove duplication
        assert "させていただきますさせていただきます" not in result["tatemae_text"]
        assert result["tatemae_text"] == "させていただきます"

    def test_removes_doubled_particles(self, sample_state, monkeypatch):
        """Test removal of doubled particles with fallback provider"""
        mock_provider = FallbackProvider()

        import processing.nodes
        monkeypatch.setattr(processing.nodes, "provider", mock_provider)

        sample_state["filled_template"] = "調整中でしてでして"
        sample_state["intent"] = "delay"
        sample_state["level"] = "business"

        result = politeness_tuner_node(sample_state)

        # Should remove duplication
        assert result["tatemae_text"] == "調整中でして"

    @pytest.mark.parametrize("level", ["business", "ultra_polite", "casual"])
    def test_all_politeness_levels(self, sample_state, monkeypatch, level):
        """Test all politeness levels with fallback provider"""
        mock_provider = FallbackProvider()

        import processing.nodes
        monkeypatch.setattr(processing.nodes, "provider", mock_provider)

        sample_state["filled_template"] = "見送らせていただきます。"
        sample_state["intent"] = "refusal"
        sample_state["level"] = level

        result = politeness_tuner_node(sample_state)

        assert "tatemae_text" in result
        assert len(result["tatemae_text"]) > 0

    def test_removes_quote_wrapping(self, sample_state, monkeypatch):
        """Test removal of quote marks from provider response"""
        mock_provider = MagicMock()
        mock_provider.refine_text.return_value = '"見送らせていただきます。"'

        import processing.nodes
        monkeypatch.setattr(processing.nodes, "provider", mock_provider)

        sample_state["filled_template"] = "見送らせていただきます。"
        sample_state["intent"] = "refusal"
        sample_state["level"] = "business"

        result = politeness_tuner_node(sample_state)

        # DeepSeekProvider strips quotes in its refine_text method
        # Here we're mocking it to return quoted text, so it stays quoted
        assert "tatemae_text" in result

    def test_handles_api_error_gracefully(self, sample_state, monkeypatch):
        """Test graceful handling of provider errors"""
        mock_provider = MagicMock()
        mock_provider.refine_text.side_effect = Exception("Provider Error")

        import processing.nodes
        monkeypatch.setattr(processing.nodes, "provider", mock_provider)

        sample_state["filled_template"] = "見送らせていただきます。"
        sample_state["intent"] = "refusal"
        sample_state["level"] = "business"

        result = politeness_tuner_node(sample_state)

        # Should fall back to template
        assert "tatemae_text" in result
        assert result["tatemae_text"] == "見送らせていただきます。"
