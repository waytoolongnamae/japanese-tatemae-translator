"""
Pytest configuration and shared fixtures
"""
import os
import pytest
from unittest.mock import MagicMock, Mock
from openai import OpenAI

# Set test environment variables before imports
os.environ["DEEPSEEK_API_KEY_CHAT"] = "sk-test-key-for-testing-only"
os.environ["DEEPSEEK_BASE_URL"] = "https://api.deepseek.com"
os.environ["DEFAULT_MODEL"] = "deepseek-chat"
os.environ["TEMPERATURE"] = "0.7"
os.environ["LOG_LEVEL"] = "ERROR"  # Suppress logs during testing

from translator import JapaneseTatemaeTranslator
from models.state import TranslationState


@pytest.fixture
def translator():
    """Create a translator instance for testing"""
    return JapaneseTatemaeTranslator()


@pytest.fixture
def sample_state():
    """Create a sample translation state for testing"""
    return {
        "input_text": "I'm not interested in this job.",
        "level": "business",
        "context": None,
        "intent": None,
        "confidence": None,
        "template": None,
        "filled_template": None,
        "tatemae_text": None,
        "detected_language": None,
        "intermediate_translation": None
    }


@pytest.fixture
def mock_openai_client(monkeypatch):
    """Mock provider for testing without API calls"""
    mock_provider = MagicMock()
    mock_provider.detect_intent.return_value = ("refusal", 0.95)
    mock_provider.refine_text.return_value = "大変恐縮ですが、今回は見送らせていただきます。"

    # Patch the provider in the nodes module
    import processing.nodes
    monkeypatch.setattr(processing.nodes, "provider", mock_provider)

    return mock_provider


@pytest.fixture
def mock_openai_client_factory():
    """Factory to create mock providers with custom responses"""
    def _create_mock(intent_response=None, grammar_response=None):
        mock_provider = MagicMock()

        # Default responses
        if intent_response is None:
            mock_provider.detect_intent.return_value = ("neutral_polite", 0.8)
        else:
            # Parse intent_response string for backwards compatibility
            lines = intent_response.split('\n')
            intent = "neutral_polite"
            confidence = 0.8
            for line in lines:
                if line.startswith("category:"):
                    intent = line.split(":", 1)[1].strip()
                elif line.startswith("confidence:"):
                    try:
                        confidence = float(line.split(":", 1)[1].strip())
                    except ValueError:
                        pass
            mock_provider.detect_intent.return_value = (intent, confidence)

        if grammar_response is None:
            mock_provider.refine_text.return_value = "承知いたしました。"
        else:
            mock_provider.refine_text.return_value = grammar_response

        return mock_provider

    return _create_mock


@pytest.fixture(params=["business", "ultra_polite", "casual"])
def politeness_level(request):
    """Parametrized fixture for politeness levels"""
    return request.param


@pytest.fixture(params=[
    "refusal",
    "disagreement",
    "delay",
    "disinterest",
    "criticism",
    "neutral_polite"
])
def intent_category(request):
    """Parametrized fixture for intent categories"""
    return request.param


@pytest.fixture
def sample_translations():
    """Sample test inputs for each intent category"""
    return {
        "refusal": "I'm not interested in this job.",
        "disagreement": "I disagree with that idea.",
        "delay": "I can't meet this week.",
        "disinterest": "Not interested in this opportunity.",
        "criticism": "Your proposal is inefficient.",
        "neutral_polite": "Thank you for your message."
    }


@pytest.fixture
def japanese_texts():
    """Sample Japanese text inputs"""
    return [
        "この仕事には興味がありません。",
        "その意見には賛成できません。",
        "今週は会えません。",
    ]


@pytest.fixture
def edge_case_inputs():
    """Edge case test inputs"""
    return {
        "empty": "",
        "whitespace": "   ",
        "single_char": "a",
        "very_long": "a" * 5000,
        "special_chars": "!@#$%^&*()",
        "mixed_language": "Hello こんにちは 你好",
        "emoji": "I'm not interested 😊🎌",
        "newlines": "I disagree\nwith that\nidea",
        "tabs": "I can't\tmeet\ttoday",
    }
