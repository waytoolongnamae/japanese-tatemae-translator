"""
LangGraph workflow nodes for Japanese Hedging Translator
"""
import random
import logging
from typing import Dict, Any
from openai import OpenAI
from config.settings import (
    DEEPSEEK_API_KEY_CHAT,
    DEEPSEEK_BASE_URL,
    DEFAULT_MODEL,
    TEMPERATURE,
    INTENT_CATEGORIES,
    TEMPLATES,
    SOFTENERS,
    HONORIFIC_MODIFIERS
)
from models.state import TranslationState

logger = logging.getLogger(__name__)

# Initialize DeepSeek client (using OpenAI-compatible API)
client = OpenAI(
    api_key=DEEPSEEK_API_KEY_CHAT,
    base_url=DEEPSEEK_BASE_URL
) if DEEPSEEK_API_KEY_CHAT else None


def intent_detector_node(state: TranslationState) -> Dict[str, Any]:
    """
    Detect the intent/sentiment of the input message.
    Categories: refusal, disagreement, delay, disinterest, criticism, neutral_polite
    """
    input_text = state["input_text"]
    logger.info(f"Detecting intent for: {input_text}")

    # Create prompt for LLM
    prompt = f"""Analyze the following message and classify its intent into one of these categories:
- refusal: The speaker is declining or rejecting something
- disagreement: The speaker disagrees with a statement or idea
- delay: The speaker is postponing or delaying something
- disinterest: The speaker is not interested in an opportunity
- criticism: The speaker is criticizing or pointing out flaws
- neutral_polite: The speaker is making a neutral or polite statement

Message: "{input_text}"

Respond with ONLY the category name and a confidence score (0-1) in this format:
category: <category_name>
confidence: <score>

Example:
category: refusal
confidence: 0.95"""

    try:
        if client and DEEPSEEK_API_KEY_CHAT and len(DEEPSEEK_API_KEY_CHAT) > 20:
            response = client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing communication intent."},
                    {"role": "user", "content": prompt}
                ],
                temperature=TEMPERATURE
            )
            result = response.choices[0].message.content.strip()

            # Parse result
            lines = result.split('\n')
            intent = None
            confidence = 0.8

            for line in lines:
                if line.startswith("category:"):
                    intent = line.split(":", 1)[1].strip()
                elif line.startswith("confidence:"):
                    try:
                        confidence = float(line.split(":", 1)[1].strip())
                    except ValueError:
                        confidence = 0.8

            # Validate intent
            if intent not in INTENT_CATEGORIES:
                logger.warning(f"Invalid intent detected: {intent}, defaulting to neutral_polite")
                intent = "neutral_polite"
        else:
            # Fallback: Simple keyword-based detection
            logger.debug("Using keyword-based detection (no valid API key)")
            intent, confidence = _keyword_based_intent_detection(input_text)

    except Exception as e:
        logger.debug(f"Error in intent detection, using fallback: {e}")
        intent, confidence = _keyword_based_intent_detection(input_text)

    logger.info(f"Detected intent: {intent} (confidence: {confidence})")

    return {
        "intent": intent,
        "confidence": confidence
    }


def _keyword_based_intent_detection(text: str) -> tuple[str, float]:
    """Fallback keyword-based intent detection"""
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
    Adjust politeness level and ensure grammatical correctness using LLM.
    Levels: business (1), ultra_polite (2), casual (3)
    """
    filled_template = state["filled_template"]
    input_text = state["input_text"]
    intent = state["intent"]
    level = state.get("level", "business")

    logger.info(f"Tuning politeness to level: {level}")

    # Use LLM to refine the translation and ensure grammatical correctness
    try:
        if client and DEEPSEEK_API_KEY_CHAT and len(DEEPSEEK_API_KEY_CHAT) > 20:
            level_descriptions = {
                "business": "標準的なビジネス敬語（普通の丁寧さ）",
                "ultra_polite": "非常に丁寧で改まった敬語（上司や重要な取引先向け）",
                "casual": "カジュアルだが礼儀正しい表現（社内チーム向け）"
            }

            prompt = f"""あなたは京都の老舗の商人のような、日本語の建前表現の達人です。

【重要】元のメッセージの具体的な内容やニュアンスを保ちながら、表面的には非常に丁寧で間接的な表現に変換してください。

元のメッセージ: "{input_text}"
意図カテゴリ: {intent}
希望する丁寧さ: {level_descriptions[level]}

【京都スタイルの建前表現の原則】:
1. 表面的には最大限に丁寧で謙虚に見える
2. しかし、元のメッセージの具体的な意味や文脈は保持する
3. 批判や拒否は「褒める」形式で表現する（例：「さすがお考えですね」「勉強になります」など、実は皮肉）
4. 直接的な「NO」は絶対に言わず、遠回しに不可能性を示唆する
5. 「検討させていただきます」「参考にさせていただきます」は「やらない」という意味
6. 元のメッセージが具体的な対象について言及している場合、その対象を曖昧にしつつも残す
7. 文法的に完璧な日本語にする（重複表現禁止）
8. 皮肉や本音が表面的には絶対に気づかれないようにする

【例】:
- 元: "Your proposal is inefficient" → "大変興味深いご提案ですね。ぜひ今後の参考とさせていただきます」（= やらない）
- 元: "I'm not interested in this job" → "大変魅力的なお話でございます。現在の状況を鑑みますと、慎重に検討させていただきたく存じます」（= 断る）
- 元: "That's impossible" → "たいへん貴重なご意見をいただきありがとうございます。様々な角度から検討させていただきます」（= 無理）

元のメッセージの具体的な内容を反映させた、京都風の建前表現のみを出力してください:"""

            response = client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=[
                    {"role": "system", "content": "あなたは京都の老舗商人のような建前表現の達人です。表面的には完璧に丁寧ですが、巧妙に本音を隠します。元のメッセージの具体的な内容は必ず保持してください。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7  # Higher temperature for more varied, context-specific responses
            )

            tatemae_text = response.choices[0].message.content.strip()
            # Remove any quotes if the model wrapped the response
            tatemae_text = tatemae_text.strip('"').strip("'").strip("「").strip("」")

            logger.info(f"LLM refined tatemae text: {tatemae_text}")
        else:
            # Fallback: use template as-is with basic cleanup
            logger.debug("Using template-based output (no API key)")
            tatemae_text = filled_template

            # Basic cleanup of doubled phrases
            import re
            # Remove doubled verb endings like させていただきますさせていただきます
            tatemae_text = re.sub(r'(させていただきます|いたします|ございます)(\1)+', r'\1', tatemae_text)
            # Remove doubled particles
            tatemae_text = re.sub(r'(ため|という状況|でして)(ため|という状況|でして)', r'\1', tatemae_text)

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

    # Simple heuristic: check if text contains Japanese characters
    has_hiragana = any('\u3040' <= char <= '\u309f' for char in input_text)
    has_katakana = any('\u30a0' <= char <= '\u30ff' for char in input_text)
    has_kanji = any('\u4e00' <= char <= '\u9faf' for char in input_text)

    if has_hiragana or has_katakana or has_kanji:
        detected_language = "ja"
        logger.info("Detected language: Japanese")
        return {"detected_language": detected_language}

    # Check for Chinese
    has_chinese = any('\u4e00' <= char <= '\u9fff' for char in input_text)
    if has_chinese:
        detected_language = "zh"
    else:
        detected_language = "en"

    logger.info(f"Detected language: {detected_language}")

    # For now, we'll work with the original text
    # In production, you might want to translate to Japanese first
    return {
        "detected_language": detected_language,
        "intermediate_translation": None  # Could add translation here
    }
