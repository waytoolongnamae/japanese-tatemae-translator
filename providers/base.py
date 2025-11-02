"""
Base LLM Provider interface
"""
from abc import ABC, abstractmethod
from typing import Tuple, Optional


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.

    This allows swapping between different LLM providers (DeepSeek, OpenAI, Anthropic, local models)
    without changing the core translation logic.
    """

    @abstractmethod
    def detect_intent(self, text: str) -> Tuple[str, float]:
        """
        Detect the intent/sentiment of the input message.

        Args:
            text: Input text to analyze

        Returns:
            Tuple of (intent_category, confidence_score)
            - intent_category: One of the INTENT_CATEGORIES
            - confidence_score: Float between 0 and 1

        Example:
            >>> provider = DeepSeekProvider()
            >>> intent, confidence = provider.detect_intent("I'm not interested")
            >>> print(f"{intent}: {confidence}")
            refusal: 0.95
        """
        pass

    @abstractmethod
    def refine_text(
        self,
        input_text: str,
        filled_template: str,
        intent: str,
        level: str
    ) -> str:
        """
        Refine and adjust the generated tatemae text for grammar and politeness.

        Args:
            input_text: Original input text
            filled_template: Template-generated text to refine
            intent: Detected intent category
            level: Desired politeness level

        Returns:
            Refined Japanese tatemae text

        Example:
            >>> provider = DeepSeekProvider()
            >>> refined = provider.refine_text(
            ...     "I disagree",
            ...     "ご意見も理解いたしますが、少し異なる見方をしております。",
            ...     "disagreement",
            ...     "business"
            ... )
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the provider is available and configured.

        Returns:
            True if provider can be used, False otherwise
        """
        pass

    def get_provider_name(self) -> str:
        """
        Get the name of this provider.

        Returns:
            Provider name (e.g., "deepseek", "openai", "anthropic")
        """
        return self.__class__.__name__.replace("Provider", "").lower()
