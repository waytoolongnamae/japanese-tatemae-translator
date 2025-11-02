"""
Fallback provider for offline/no-API scenarios
"""
import logging
import re
from typing import Tuple
from providers.base import LLMProvider

logger = logging.getLogger(__name__)


class FallbackProvider(LLMProvider):
    """
    Fallback provider using keyword-based intent detection and regex-based cleanup.

    Used when no API key is available or when API calls fail.
    """

    def detect_intent(self, text: str) -> Tuple[str, float]:
        """
        Keyword-based intent detection fallback.

        Args:
            text: Input text to analyze

        Returns:
            Tuple of (intent, confidence)
        """
        text_lower = text.lower()

        # Refusal keywords
        if any(word in text_lower for word in ["not interested", "decline", "pass", "no thanks", "reject", "興味ない"]):
            return "refusal", 0.7

        # Disagreement keywords
        if any(word in text_lower for word in ["disagree", "don't think", "wrong", "incorrect", "反対", "違う"]):
            return "disagreement", 0.7

        # Delay keywords
        if any(word in text_lower for word in ["later", "postpone", "delay", "can't meet", "busy", "後で", "延期"]):
            return "delay", 0.7

        # Disinterest keywords
        if any(word in text_lower for word in ["not interested", "don't want", "not for me", "興味ない"]):
            return "disinterest", 0.7

        # Criticism keywords
        if any(word in text_lower for word in ["inefficient", "bad", "poor", "needs improvement", "問題", "改善"]):
            return "criticism", 0.7

        return "neutral_polite", 0.6

    def refine_text(
        self,
        input_text: str,
        filled_template: str,
        intent: str,
        level: str
    ) -> str:
        """
        Basic regex-based text cleanup fallback.

        Args:
            input_text: Original input (unused in fallback)
            filled_template: Template-generated text
            intent: Detected intent (unused in fallback)
            level: Politeness level (unused in fallback)

        Returns:
            Cleaned text
        """
        text = filled_template

        # Remove doubled verb endings
        text = re.sub(r'(させていただきます|いたします|ございます)(\1)+', r'\1', text)

        # Remove doubled particles
        text = re.sub(r'(ため|という状況|でして)(ため|という状況|でして)', r'\1', text)

        # Remove tripled or more particles
        text = re.sub(r'(ため|という状況|でして){3,}', r'\1', text)

        logger.info(f"Fallback text refinement applied")
        return text

    def is_available(self) -> bool:
        """Fallback provider is always available"""
        return True
