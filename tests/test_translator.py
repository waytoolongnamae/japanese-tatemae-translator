"""
Basic smoke tests for Japanese Hedging Translator
"""
import pytest
from translator import JapaneseTatemaeTranslator


class TestBasicTranslation:
    """Basic translation smoke tests"""

    def test_refusal_intent(self, translator):
        """Test basic refusal translation"""
        result = translator.translate("I'm not interested in this job.", level="business")
        assert result["tatemae_text"] is not None
        assert result["intent"] in ["refusal", "disinterest", "neutral_polite"]
        assert len(result["tatemae_text"]) > 0

    def test_disagreement_intent(self, translator):
        """Test basic disagreement translation"""
        result = translator.translate("I disagree with that idea.", level="business")
        assert result["tatemae_text"] is not None
        assert len(result["tatemae_text"]) > 0

    def test_delay_intent(self, translator):
        """Test basic delay translation"""
        result = translator.translate("I can't meet this week.", level="business")
        assert result["tatemae_text"] is not None
        assert len(result["tatemae_text"]) > 0


class TestPolitenessLevels:
    """Test different politeness levels"""

    def test_business_level(self, translator):
        """Test business politeness level"""
        result = translator.translate("That's not possible.", level="business")
        assert result["tatemae_text"] is not None
        assert result["level"] == "business"

    def test_ultra_polite_level(self, translator):
        """Test ultra_polite politeness level"""
        result = translator.translate("That's not possible.", level="ultra_polite")
        assert result["tatemae_text"] is not None
        assert result["level"] == "ultra_polite"

    def test_casual_level(self, translator):
        """Test casual politeness level"""
        result = translator.translate("That's not possible.", level="casual")
        assert result["tatemae_text"] is not None
        assert result["level"] == "casual"


class TestSimpleInterface:
    """Test simplified translation interface"""

    def test_translate_simple_returns_string(self, translator):
        """Test that translate_simple returns a string"""
        text = translator.translate_simple("Your proposal is inefficient.")
        assert text is not None
        assert isinstance(text, str)
        assert len(text) > 0

    def test_translate_simple_with_level(self, translator):
        """Test translate_simple with custom level"""
        text = translator.translate_simple("I can't meet.", level="ultra_polite")
        assert isinstance(text, str)
        assert len(text) > 0


class TestAllIntents:
    """Test all intent categories"""

    @pytest.mark.parametrize("intent,text", [
        ("refusal", "I'm not interested."),
        ("disagreement", "I disagree."),
        ("delay", "I can't do it now."),
        ("disinterest", "Not interested in this opportunity."),
        ("criticism", "This is inefficient."),
        ("neutral_polite", "Thank you for your message."),
    ])
    def test_intent_translation(self, translator, intent, text):
        """Test translation for each intent category"""
        result = translator.translate(text)
        assert result["tatemae_text"] is not None
        assert len(result["tatemae_text"]) > 0
