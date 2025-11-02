"""
DeepSeek LLM Provider implementation
"""
import logging
from typing import Tuple
from openai import OpenAI
from openai import APIError, RateLimitError, APIConnectionError, APITimeoutError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)
from providers.base import LLMProvider
from config.settings import (
    DEEPSEEK_API_KEY_CHAT,
    DEEPSEEK_BASE_URL,
    DEFAULT_MODEL,
    TEMPERATURE,
    INTENT_CATEGORIES
)

logger = logging.getLogger(__name__)


class DeepSeekProvider(LLMProvider):
    """
    DeepSeek API provider for intent detection and text refinement.
    """

    def __init__(self):
        """Initialize DeepSeek client"""
        self.client = None
        self.api_key = DEEPSEEK_API_KEY_CHAT
        self.base_url = DEEPSEEK_BASE_URL
        self.model = DEFAULT_MODEL

        if self.api_key and len(self.api_key) > 20:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=30.0,
                max_retries=0  # We handle retries with tenacity
            )
            logger.info("DeepSeek provider initialized successfully")
        else:
            logger.warning("DeepSeek API key not configured or invalid")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((RateLimitError, APIConnectionError, APITimeoutError)),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True
    )
    def _call_api(self, messages: list, temperature: float = None):
        """Call DeepSeek API with retry logic"""
        if not self.client:
            raise RuntimeError("DeepSeek client not initialized")

        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature or TEMPERATURE
        )

    def detect_intent(self, text: str) -> Tuple[str, float]:
        """
        Detect intent using DeepSeek API.

        Args:
            text: Input text to analyze

        Returns:
            Tuple of (intent, confidence)
        """
        if not self.is_available():
            raise RuntimeError("DeepSeek provider not available")

        prompt = f"""Analyze the following message and classify its intent into one of these categories:
- refusal: The speaker is declining or rejecting something
- disagreement: The speaker disagrees with a statement or idea
- delay: The speaker is postponing or delaying something
- disinterest: The speaker is not interested in an opportunity
- criticism: The speaker is criticizing or pointing out flaws
- neutral_polite: The speaker is making a neutral or polite statement

Message: "{text}"

Respond with ONLY the category name and a confidence score (0-1) in this format:
category: <category_name>
confidence: <score>

Example:
category: refusal
confidence: 0.95"""

        try:
            response = self._call_api(
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing communication intent."},
                    {"role": "user", "content": prompt}
                ]
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

            return intent, confidence

        except Exception as e:
            logger.error(f"Error detecting intent with DeepSeek: {e}")
            raise

    def refine_text(
        self,
        input_text: str,
        filled_template: str,
        intent: str,
        level: str
    ) -> str:
        """
        Refine text using DeepSeek API.

        Args:
            input_text: Original input text
            filled_template: Template-generated text
            intent: Detected intent
            level: Politeness level

        Returns:
            Refined Japanese text
        """
        if not self.is_available():
            raise RuntimeError("DeepSeek provider not available")

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

        try:
            response = self._call_api(
                messages=[
                    {"role": "system", "content": "あなたは京都の老舗商人のような建前表現の達人です。表面的には完璧に丁寧ですが、巧妙に本音を隠します。元のメッセージの具体的な内容は必ず保持してください。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            tatemae_text = response.choices[0].message.content.strip()
            # Remove any quotes if the model wrapped the response
            tatemae_text = tatemae_text.strip('"').strip("'").strip("「").strip("」")

            return tatemae_text

        except Exception as e:
            logger.error(f"Error refining text with DeepSeek: {e}")
            raise

    def is_available(self) -> bool:
        """Check if DeepSeek provider is available"""
        return self.client is not None and self.api_key is not None and len(self.api_key) > 20
