"""
LangGraph workflow nodes for Japanese Hedging Translator
"""
import random
import logging
from typing import Dict, Any, Optional
from config.settings import (
    INTENT_CATEGORIES,
    TEMPLATES,
    SOFTENERS,
    HONORIFIC_MODIFIERS,
    MODEL_PROVIDER
)
from models.state import TranslationState
from providers import DeepSeekProvider, FallbackProvider
from providers.openai import OpenAIProvider

logger = logging.getLogger(__name__)

# Global provider variable
provider = None
_provider_name = None


def _get_provider_instance(provider_type: str):
    """Get provider instance based on type"""
    if provider_type == "openai":
        return OpenAIProvider()
    elif provider_type == "deepseek":
        return DeepSeekProvider()
    else:
        logger.warning(f"Unknown provider type: {provider_type}, defaulting to deepseek")
        return DeepSeekProvider()


def initialize_provider(provider_type: Optional[str] = None):
    """
    Initialize the LLM provider based on configuration or parameter.

    Args:
        provider_type: Optional provider type override ("openai" or "deepseek")
    """
    global provider, _provider_name

    selected_provider = provider_type or MODEL_PROVIDER

    try:
        _primary_provider = _get_provider_instance(selected_provider)
        if _primary_provider.is_available():
            provider = _primary_provider
            _provider_name = selected_provider
            model_info = getattr(provider, 'model', 'unknown')
            logger.info(f"Using {selected_provider} provider with model: {model_info}")
        else:
            provider = FallbackProvider()
            _provider_name = "fallback"
            logger.info(f"{selected_provider} unavailable, using fallback provider")
    except Exception as e:
        logger.warning(f"Error initializing {selected_provider} provider: {e}, using fallback")
        provider = FallbackProvider()
        _provider_name = "fallback"


def get_provider_info() -> Dict[str, str]:
    """
    Get information about the current provider.

    Returns:
        Dictionary with provider name and model information
    """
    global provider, _provider_name
    if provider is None:
        initialize_provider()

    return {
        "provider": _provider_name or "unknown",
        "model": getattr(provider, 'model', 'unknown') if provider else "unknown"
    }


# Initialize provider on module load
initialize_provider()


def intent_detector_node(state: TranslationState) -> Dict[str, Any]:
    """
    Detect the intent/sentiment of the input message using provider abstraction.
    Categories: refusal, disagreement, delay, disinterest, criticism, neutral_polite
    """
    input_text = state["input_text"]
    logger.info(f"Detecting intent for: {input_text}")

    try:
        intent, confidence = provider.detect_intent(input_text)

        # Validate intent
        if intent not in INTENT_CATEGORIES:
            logger.warning(f"Invalid intent detected: {intent}, defaulting to neutral_polite")
            intent = "neutral_polite"

    except Exception as e:
        logger.error(f"Error in intent detection: {e}")
        intent = "neutral_polite"
        confidence = 0.5

    logger.info(f"Detected intent: {intent} (confidence: {confidence})")

    return {
        "intent": intent,
        "confidence": confidence
    }


def tatemae_generator_node(state: TranslationState) -> Dict[str, Any]:
    """
    Generate tatemae (建前) text based on detected intent using templates.
    """
    intent = state["intent"]
    logger.info(f"Generating tatemae for intent: {intent}")

    # Select template
    templates = TEMPLATES.get(intent, TEMPLATES["neutral_polite"])
    template = random.choice(templates)

    # Fill template with softeners
    filled_template = template
    for placeholder, options in SOFTENERS.items():
        if f"{{{placeholder}}}" in filled_template:
            selected = random.choice(options)
            filled_template = filled_template.replace(f"{{{placeholder}}}", selected)

    logger.info(f"Selected template: {template}")
    logger.info(f"Filled template: {filled_template}")

    return {
        "template": template,
        "filled_template": filled_template
    }


def politeness_tuner_node(state: TranslationState) -> Dict[str, Any]:
    """
    Adjust politeness level and fidelity, ensuring grammatical correctness using provider abstraction.
    Politeness levels: business (1), ultra_polite (2), casual (3)
    Fidelity levels: high (1), medium (2), low (3) - closeness to original meaning
    """
    filled_template = state["filled_template"]
    input_text = state["input_text"]
    intent = state["intent"]
    level = state.get("level", "business")
    fidelity = state.get("fidelity", "medium")

    logger.info(f"Tuning with politeness: {level}, fidelity: {fidelity}")

    try:
        tatemae_text = provider.refine_text(
            input_text=input_text,
            filled_template=filled_template,
            intent=intent,
            level=level,
            fidelity=fidelity
        )
        logger.info(f"Provider refined tatemae text: {tatemae_text}")

    except Exception as e:
        logger.warning(f"Error in politeness tuning, using template: {e}")
        tatemae_text = filled_template

    logger.info(f"Final tatemae text: {tatemae_text}")

    return {
        "tatemae_text": tatemae_text
    }


def language_detector_node(state: TranslationState) -> Dict[str, Any]:
    """
    Detect input language and translate to Japanese if needed.
    This is an optional pre-processing step.
    """
    input_text = state["input_text"]

    # Check for Japanese-specific characters (Hiragana and Katakana)
    has_hiragana = any('\u3040' <= char <= '\u309f' for char in input_text)
    has_katakana = any('\u30a0' <= char <= '\u30ff' for char in input_text)

    # If Japanese-specific characters are present, it's definitely Japanese
    if has_hiragana or has_katakana:
        detected_language = "ja"
        logger.info("Detected language: Japanese (has kana)")
        return {"detected_language": detected_language}

    # Check for CJK characters (used by both Chinese and Japanese)
    has_cjk = any('\u4e00' <= char <= '\u9fff' for char in input_text)

    if has_cjk:
        # If there are CJK characters but no kana, assume Chinese
        # (Pure Japanese text almost always contains at least some hiragana)
        detected_language = "zh"
        logger.info("Detected language: Chinese (has CJK without kana)")
    else:
        # No CJK or kana characters, assume English
        detected_language = "en"
        logger.info("Detected language: English")

    # For now, we'll work with the original text
    # In production, you might want to translate to Japanese first
    return {
        "detected_language": detected_language,
        "intermediate_translation": None  # Could add translation here
    }
