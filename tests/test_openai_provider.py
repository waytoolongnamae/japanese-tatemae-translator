"""
Tests for OpenAI Provider
"""
import pytest
from unittest.mock import MagicMock, Mock, patch
from providers.openai import OpenAIProvider
from config.settings import INTENT_CATEGORIES


class TestOpenAIProviderInitialization:
    """Test OpenAI provider initialization"""

    def test_provider_initializes_with_valid_key(self):
        """Test that provider initializes successfully with valid API key"""
        # Use conftest environment which has valid test key
        provider = OpenAIProvider()

        # Should use the test key from conftest
        assert provider.api_key is not None
        assert len(provider.api_key) > 20
        assert provider.client is not None

    def test_provider_handles_missing_key(self, monkeypatch):
        """Test that provider handles missing API key gracefully"""
        # Need to reload the module to apply new env vars
        import importlib
        import providers.openai as openai_module

        monkeypatch.setattr(openai_module, "OPENAI_API_KEY", "")
        provider = openai_module.OpenAIProvider()
        provider.api_key = ""
        provider.client = None

        assert not provider.is_available()

    def test_provider_handles_short_key(self, monkeypatch):
        """Test that provider handles invalid short API key"""
        import providers.openai as openai_module

        provider = openai_module.OpenAIProvider()
        provider.api_key = "short"
        provider.client = MagicMock()  # Has client but key is short

        assert not provider.is_available()

    def test_is_available_returns_true_with_valid_setup(self, monkeypatch):
        """Test that is_available returns True with valid configuration"""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key-that-is-long-enough-to-pass-validation")
        monkeypatch.setenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

        provider = OpenAIProvider()

        assert provider.is_available()

    def test_get_provider_name(self, monkeypatch):
        """Test that provider returns correct name"""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key-that-is-long-enough-to-pass-validation")

        provider = OpenAIProvider()

        assert provider.get_provider_name() == "openai"


class TestOpenAIIntentDetection:
    """Test intent detection with OpenAI provider"""

    @pytest.fixture
    def mock_provider(self, monkeypatch):
        """Create a mocked OpenAI provider"""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key-that-is-long-enough-to-pass-validation")
        return OpenAIProvider()

    def test_detect_intent_refusal(self, mock_provider, monkeypatch):
        """Test intent detection for refusal"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "category: refusal\nconfidence: 0.95"

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_provider.client = mock_client

        intent, confidence = mock_provider.detect_intent("I'm not interested")

        assert intent == "refusal"
        assert confidence == 0.95

    def test_detect_intent_disagreement(self, mock_provider, monkeypatch):
        """Test intent detection for disagreement"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "category: disagreement\nconfidence: 0.88"

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_provider.client = mock_client

        intent, confidence = mock_provider.detect_intent("I disagree with that")

        assert intent == "disagreement"
        assert confidence == 0.88

    def test_detect_intent_delay(self, mock_provider):
        """Test intent detection for delay"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "category: delay\nconfidence: 0.82"

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_provider.client = mock_client

        intent, confidence = mock_provider.detect_intent("Can we talk later?")

        assert intent == "delay"
        assert confidence == 0.82

    def test_detect_intent_disinterest(self, mock_provider):
        """Test intent detection for disinterest"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "category: disinterest\nconfidence: 0.91"

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_provider.client = mock_client

        intent, confidence = mock_provider.detect_intent("Not interested in this job")

        assert intent == "disinterest"
        assert confidence == 0.91

    def test_detect_intent_criticism(self, mock_provider):
        """Test intent detection for criticism"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "category: criticism\nconfidence: 0.87"

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_provider.client = mock_client

        intent, confidence = mock_provider.detect_intent("This code is poorly written")

        assert intent == "criticism"
        assert confidence == 0.87

    def test_detect_intent_neutral_polite(self, mock_provider):
        """Test intent detection for neutral/polite"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "category: neutral_polite\nconfidence: 0.93"

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_provider.client = mock_client

        intent, confidence = mock_provider.detect_intent("Thank you for the information")

        assert intent == "neutral_polite"
        assert confidence == 0.93

    def test_detect_intent_with_invalid_category_defaults_to_neutral(self, mock_provider):
        """Test that invalid intent category defaults to neutral_polite"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "category: invalid_category\nconfidence: 0.80"

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_provider.client = mock_client

        intent, confidence = mock_provider.detect_intent("Some text")

        assert intent == "neutral_polite"
        assert confidence == 0.80

    def test_detect_intent_with_malformed_confidence(self, mock_provider):
        """Test that malformed confidence defaults to 0.8"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "category: refusal\nconfidence: invalid"

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_provider.client = mock_client

        intent, confidence = mock_provider.detect_intent("No thanks")

        assert intent == "refusal"
        assert confidence == 0.8

    def test_detect_intent_raises_error_when_unavailable(self):
        """Test that detect_intent raises error when provider is unavailable"""
        provider = OpenAIProvider()
        provider.client = None  # Simulate unavailable provider

        with pytest.raises(RuntimeError, match="OpenAI provider not available"):
            provider.detect_intent("Some text")

    def test_detect_intent_handles_api_error(self, mock_provider):
        """Test that detect_intent handles API errors"""
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_provider.client = mock_client

        with pytest.raises(Exception, match="API Error"):
            mock_provider.detect_intent("Some text")


class TestOpenAITextRefinement:
    """Test text refinement with OpenAI provider"""

    @pytest.fixture
    def mock_provider(self, monkeypatch):
        """Create a mocked OpenAI provider"""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key-that-is-long-enough-to-pass-validation")
        return OpenAIProvider()

    def test_refine_text_business_level(self, mock_provider):
        """Test text refinement with business politeness level"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "現在は別のテーマに注力しておりまして、今回は見送らせていただきます。"

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_provider.client = mock_client

        result = mock_provider.refine_text(
            input_text="I'm not interested",
            filled_template="現在は{soft_reason}、今回は{neutral_action}させていただきます。",
            intent="refusal",
            level="business"
        )

        # Check that result is valid Japanese text (not empty and contains expected patterns)
        assert len(result) > 0
        assert any(word in result for word in ["ます", "おり", "いただ"])

    def test_refine_text_ultra_polite_level(self, mock_provider):
        """Test text refinement with ultra_polite politeness level"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "誠に恐縮ではございますが、現在は別の案件に注力している状況でございまして、今回は見送らせていただければと存じます。"

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_provider.client = mock_client

        result = mock_provider.refine_text(
            input_text="I'm not interested",
            filled_template="Template text",
            intent="refusal",
            level="ultra_polite"
        )

        assert len(result) > 0
        assert "ございます" in result or "存じます" in result

    def test_refine_text_casual_level(self, mock_provider):
        """Test text refinement with casual politeness level"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "今回は見送らせていただきますね。"

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_provider.client = mock_client

        result = mock_provider.refine_text(
            input_text="I'm not interested",
            filled_template="Template text",
            intent="refusal",
            level="casual"
        )

        assert len(result) > 0

    def test_refine_text_strips_quotes(self, mock_provider):
        """Test that refine_text strips surrounding quotes"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '"今回は見送らせていただきます。"'

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_provider.client = mock_client

        result = mock_provider.refine_text(
            input_text="No thanks",
            filled_template="Template",
            intent="refusal",
            level="business"
        )

        assert not result.startswith('"')
        assert not result.endswith('"')

    def test_refine_text_strips_japanese_quotes(self, mock_provider):
        """Test that refine_text strips Japanese quotation marks"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "「今回は見送らせていただきます。」"

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_provider.client = mock_client

        result = mock_provider.refine_text(
            input_text="No thanks",
            filled_template="Template",
            intent="refusal",
            level="business"
        )

        assert not result.startswith("「")
        assert not result.endswith("」")

    def test_refine_text_raises_error_when_unavailable(self):
        """Test that refine_text raises error when provider is unavailable"""
        provider = OpenAIProvider()
        provider.client = None  # Simulate unavailable provider

        with pytest.raises(RuntimeError, match="OpenAI provider not available"):
            provider.refine_text("Input", "Template", "refusal", "business")

    def test_refine_text_handles_api_error(self, mock_provider):
        """Test that refine_text handles API errors"""
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_provider.client = mock_client

        with pytest.raises(Exception, match="API Error"):
            mock_provider.refine_text("Input", "Template", "refusal", "business")

    def test_refine_text_for_all_intents(self, mock_provider):
        """Test text refinement for all intent categories"""
        intents = ["refusal", "disagreement", "delay", "disinterest", "criticism", "neutral_polite"]

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "適切な日本語表現です。"

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_provider.client = mock_client

        for intent in intents:
            result = mock_provider.refine_text(
                input_text="Test input",
                filled_template="Template",
                intent=intent,
                level="business"
            )
            assert len(result) > 0
            assert isinstance(result, str)


class TestOpenAIProviderRetry:
    """Test retry logic in OpenAI provider"""

    @pytest.fixture
    def mock_provider(self, monkeypatch):
        """Create a mocked OpenAI provider"""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key-that-is-long-enough-to-pass-validation")
        return OpenAIProvider()

    def test_call_api_raises_error_when_client_not_initialized(self, mock_provider):
        """Test that _call_api raises error when client is not initialized"""
        mock_provider.client = None

        with pytest.raises(RuntimeError, match="OpenAI client not initialized"):
            mock_provider._call_api([{"role": "user", "content": "test"}])


class TestOpenAIProviderIntegration:
    """Integration tests for OpenAI provider with processing nodes"""

    def test_provider_can_be_imported_in_nodes(self):
        """Test that OpenAI provider can be imported and used in nodes module"""
        from processing.nodes import _get_provider_instance

        provider = _get_provider_instance("openai")
        assert provider is not None
        assert isinstance(provider, OpenAIProvider)

    def test_initialize_provider_with_openai(self, monkeypatch):
        """Test initializing provider system with OpenAI"""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key-that-is-long-enough-to-pass-validation")
        monkeypatch.setenv("MODEL_PROVIDER", "openai")

        from processing.nodes import initialize_provider, get_provider_info

        initialize_provider("openai")
        info = get_provider_info()

        # Note: Will use fallback if actual API key is invalid
        assert info["provider"] in ["openai", "fallback"]

    def test_get_provider_info_returns_correct_structure(self, monkeypatch):
        """Test that get_provider_info returns correct data structure"""
        from processing.nodes import get_provider_info

        info = get_provider_info()

        assert "provider" in info
        assert "model" in info
        assert isinstance(info["provider"], str)
        assert isinstance(info["model"], str)
