"""
State definitions for LangGraph workflow
"""
from typing import TypedDict, Optional


class TranslationState(TypedDict):
    """State object that flows through the graph"""
    # Input
    input_text: str
    level: str  # business, ultra_polite, casual
    fidelity: Optional[str]  # high, medium, low (closeness to original meaning)
    context: Optional[str]  # business / personal / recruiter

    # Processing
    intent: Optional[str]
    confidence: Optional[float]
    template: Optional[str]
    filled_template: Optional[str]

    # Output
    tatemae_text: Optional[str]

    # Metadata
    detected_language: Optional[str]
    intermediate_translation: Optional[str]
