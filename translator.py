"""
Main API interface for Japanese Hedging Translator
"""
import logging
from typing import Optional, Dict, Any
from models.state import TranslationState
from processing.graph import build_workflow

logger = logging.getLogger(__name__)


class JapaneseTatemaeTranslator:
    """
    Main translator class providing the public API.
    """

    def __init__(self):
        """Initialize the translator with the LangGraph workflow."""
        logger.info("Initializing Japanese Tatemae Translator")
        self.workflow = build_workflow()
        logger.info("Translator initialized successfully")

    def translate(
        self,
        input_text: str,
        level: str = "business",
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Translate direct text into Japanese tatemae (建前) style.

        Args:
            input_text: The input message to translate
            level: Politeness level - "business", "ultra_polite", or "casual"
            context: Optional context tag - "business", "personal", or "recruiter"

        Returns:
            Dictionary containing:
                - tatemae_text: The translated tatemae text
                - intent: Detected intent category
                - confidence: Confidence score for intent detection
                - detected_language: Input language detected
                - level: Politeness level used

        Example:
            >>> translator = JapaneseTatemaeTranslator()
            >>> result = translator.translate("I'm not interested in this job.", level="business")
            >>> print(result["tatemae_text"])
            現在は別のテーマに注力しており、今回は情報として参考にさせていただきます。
        """
        # Validate level
        valid_levels = ["business", "ultra_polite", "casual"]
        if level not in valid_levels:
            logger.warning(f"Invalid level '{level}', defaulting to 'business'")
            level = "business"

        # Create initial state
        initial_state: TranslationState = {
            "input_text": input_text,
            "level": level,
            "context": context,
            "intent": None,
            "confidence": None,
            "template": None,
            "filled_template": None,
            "tatemae_text": None,
            "detected_language": None,
            "intermediate_translation": None
        }

        logger.info(f"Translating: '{input_text}' with level: {level}")

        # Run workflow
        try:
            final_state = self.workflow.invoke(initial_state)

            # Extract result
            result = {
                "tatemae_text": final_state.get("tatemae_text", ""),
                "intent": final_state.get("intent"),
                "confidence": final_state.get("confidence"),
                "detected_language": final_state.get("detected_language"),
                "level": level,
                "context": context
            }

            logger.info(f"Translation completed: {result['tatemae_text']}")
            return result

        except Exception as e:
            logger.error(f"Error during translation: {e}", exc_info=True)
            return {
                "tatemae_text": "申し訳ございません。現在処理できない状況です。",
                "intent": "error",
                "confidence": 0.0,
                "detected_language": None,
                "level": level,
                "context": context,
                "error": str(e)
            }

    def translate_simple(self, input_text: str, level: str = "business") -> str:
        """
        Simplified translation interface that returns only the tatemae text.

        Args:
            input_text: The input message to translate
            level: Politeness level - "business", "ultra_polite", or "casual"

        Returns:
            The translated tatemae text as a string

        Example:
            >>> translator = JapaneseTatemaeTranslator()
            >>> print(translator.translate_simple("I disagree with that idea."))
            ご意見も理解いたしますが、少し異なる見方をしております。
        """
        result = self.translate(input_text, level)
        return result["tatemae_text"]


# Convenience function for quick usage
def quick_translate(input_text: str, level: str = "business") -> str:
    """
    Quick translation function that creates a translator and returns the result.

    Args:
        input_text: The input message to translate
        level: Politeness level

    Returns:
        The translated tatemae text

    Example:
        >>> from translator import quick_translate
        >>> print(quick_translate("Your proposal is inefficient."))
        もう少し検討の余地があるかもしれません。
    """
    translator = JapaneseTatemaeTranslator()
    return translator.translate_simple(input_text, level)
