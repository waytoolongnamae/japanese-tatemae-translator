"""
Main API interface for Japanese Hedging Translator
"""
import logging
from typing import Optional, Dict, Any, Tuple
from models.state import TranslationState
from processing.graph import build_workflow

logger = logging.getLogger(__name__)

# Configuration constants
MAX_INPUT_LENGTH = 5000  # Maximum characters allowed
MIN_INPUT_LENGTH = 1     # Minimum meaningful input
VALID_LEVELS = ["business", "ultra_polite", "casual"]
VALID_CONTEXTS = ["business", "personal", "recruiter", None]


class InputValidationError(ValueError):
    """Raised when input validation fails"""
    pass


class JapaneseTatemaeTranslator:
    """
    Main translator class providing the public API.
    """

    def __init__(self):
        """Initialize the translator with the LangGraph workflow."""
        logger.info("Initializing Japanese Tatemae Translator")
        self.workflow = build_workflow()
        logger.info("Translator initialized successfully")

    def _validate_input(
        self,
        input_text: str,
        level: str,
        context: Optional[str]
    ) -> Tuple[str, Optional[str]]:
        """
        Validate input parameters.

        Args:
            input_text: Text to validate
            level: Politeness level to validate
            context: Context to validate

        Returns:
            Tuple of (validated_level, validated_context)

        Raises:
            InputValidationError: If validation fails
        """
        # Validate input_text type
        if not isinstance(input_text, str):
            raise InputValidationError(
                f"input_text must be a string, got {type(input_text).__name__}"
            )

        # Validate input_text is not empty
        if not input_text or not input_text.strip():
            raise InputValidationError(
                "input_text cannot be empty or whitespace only"
            )

        # Validate input length
        if len(input_text) < MIN_INPUT_LENGTH:
            raise InputValidationError(
                f"input_text too short (minimum {MIN_INPUT_LENGTH} character)"
            )

        if len(input_text) > MAX_INPUT_LENGTH:
            raise InputValidationError(
                f"input_text too long (maximum {MAX_INPUT_LENGTH} characters, got {len(input_text)})"
            )

        # Validate level - default to business if invalid
        validated_level = level
        if level not in VALID_LEVELS:
            logger.warning(
                f"Invalid level '{level}'. Must be one of: {', '.join(VALID_LEVELS)}. Defaulting to 'business'."
            )
            validated_level = "business"

        # Validate context - default to None if invalid
        validated_context = context
        if context is not None and context not in VALID_CONTEXTS:
            logger.warning(
                f"Invalid context '{context}'. Must be one of: {', '.join(str(c) for c in VALID_CONTEXTS if c)}. Defaulting to None."
            )
            validated_context = None

        return validated_level, validated_context

    def translate(
        self,
        input_text: str,
        level: str = "business",
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Translate direct text into Japanese tatemae (建前) style.

        Args:
            input_text: The input message to translate (1-5000 characters)
            level: Politeness level - "business", "ultra_polite", or "casual"
            context: Optional context tag - "business", "personal", or "recruiter"

        Returns:
            Dictionary containing:
                - tatemae_text: The translated tatemae text
                - intent: Detected intent category
                - confidence: Confidence score for intent detection
                - detected_language: Input language detected
                - level: Politeness level used
                - error: Error message if validation/processing fails

        Raises:
            InputValidationError: If input validation fails

        Example:
            >>> translator = JapaneseTatemaeTranslator()
            >>> result = translator.translate("I'm not interested in this job.", level="business")
            >>> print(result["tatemae_text"])
            現在は別のテーマに注力しており、今回は情報として参考にさせていただきます。
        """
        # Validate inputs and get validated values
        try:
            validated_level, validated_context = self._validate_input(input_text, level, context)
        except InputValidationError as e:
            logger.error(f"Input validation failed: {e}")
            return {
                "tatemae_text": "申し訳ございません。入力内容を確認してください。",
                "intent": "error",
                "confidence": 0.0,
                "detected_language": None,
                "level": level,
                "context": context,
                "error": str(e)
            }

        # Create initial state with validated values
        initial_state: TranslationState = {
            "input_text": input_text,
            "level": validated_level,
            "context": validated_context,
            "intent": None,
            "confidence": None,
            "template": None,
            "filled_template": None,
            "tatemae_text": None,
            "detected_language": None,
            "intermediate_translation": None
        }

        logger.info(f"Translating: '{input_text}' with level: {validated_level}")

        # Run workflow
        try:
            final_state = self.workflow.invoke(initial_state)

            # Extract result
            result = {
                "tatemae_text": final_state.get("tatemae_text", ""),
                "intent": final_state.get("intent"),
                "confidence": final_state.get("confidence"),
                "detected_language": final_state.get("detected_language"),
                "level": validated_level,
                "context": validated_context
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
