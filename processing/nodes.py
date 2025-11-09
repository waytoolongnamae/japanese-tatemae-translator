"""
LangGraph workflow nodes for Japanese Hedging Translator
"""
import random
import logging
from typing import Dict, Any
from config.settings import (
    INTENT_CATEGORIES,
    TEMPLATES,
    SOFTENERS,
    HONORIFIC_MODIFIERS
)
from models.state import TranslationState
from providers import DeepSeekProvider, FallbackProvider

logger = logging.getLogger(__name__)

# Initialize provider with fallback
try:
    _primary_provider = DeepSeekProvider()
    if _primary_provider.is_available():
        provider = _primary_provider
        logger.info("Using DeepSeek provider")
    else:
        provider = FallbackProvider()
        logger.info("DeepSeek unavailable, using fallback provider")
except Exception as e:
    logger.warning(f"Error initializing DeepSeek provider: {e}, using fallback")
    provider = FallbackProvider()


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
    Adjust politeness level and ensure grammatical correctness using provider abstraction.
    Levels: business (1), ultra_polite (2), casual (3)
    """
    filled_template = state["filled_template"]
    input_text = state["input_text"]
    intent = state["intent"]
    level = state.get("level", "business")

    logger.info(f"Tuning politeness to level: {level}")

    try:
        tatemae_text = provider.refine_text(
            input_text=input_text,
            filled_template=filled_template,
            intent=intent,
            level=level
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
