"""
LangGraph workflow builder for Japanese Hedging Translator
"""
import logging
from langgraph.graph import StateGraph, END
from models.state import TranslationState
from processing.nodes import (
    language_detector_node,
    intent_detector_node,
    tatemae_generator_node,
    politeness_tuner_node
)

logger = logging.getLogger(__name__)


def build_workflow() -> StateGraph:
    """
    Build the LangGraph workflow for Japanese Hedging Translation.

    Flow:
    1. language_detector: Detect input language (optional pre-processing)
    2. intent_detector: Classify the intent of the message
    3. tatemae_generator: Generate 建前 text using templates
    4. politeness_tuner: Adjust politeness level
    """
    # Initialize graph
    workflow = StateGraph(TranslationState)

    # Add nodes
    workflow.add_node("language_detector", language_detector_node)
    workflow.add_node("intent_detector", intent_detector_node)
    workflow.add_node("tatemae_generator", tatemae_generator_node)
    workflow.add_node("politeness_tuner", politeness_tuner_node)

    # Define edges
    workflow.set_entry_point("language_detector")
    workflow.add_edge("language_detector", "intent_detector")
    workflow.add_edge("intent_detector", "tatemae_generator")
    workflow.add_edge("tatemae_generator", "politeness_tuner")
    workflow.add_edge("politeness_tuner", END)

    logger.info("Workflow built successfully")

    return workflow.compile()
