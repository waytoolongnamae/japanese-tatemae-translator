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

        prompt = f"""You are an expert linguist specializing in pragmatics and speech act theory. Analyze the communicative intent of the following message.

**Task**: Classify the primary communicative intent into ONE of these categories:

1. **refusal** - Speaker declines, rejects, or turns down a request/offer/invitation
   - Examples: "No thanks", "I can't do that", "I'm not available"

2. **disagreement** - Speaker expresses opposition to an idea, opinion, or statement
   - Examples: "I don't think so", "That's not correct", "I see it differently"

3. **delay** - Speaker postpones, defers, or requests more time
   - Examples: "Let me think about it", "Can we discuss this later?", "Not right now"

4. **disinterest** - Speaker lacks interest in an opportunity, topic, or proposal
   - Examples: "I'm not interested", "This isn't for me", "I'll pass"

5. **criticism** - Speaker identifies flaws, problems, or negative aspects
   - Examples: "This has issues", "That approach won't work", "There are problems with this"

6. **neutral_polite** - Neutral, informative, or genuinely polite communication
   - Examples: "Thank you", "I appreciate that", "Here's an update"

**Input Message**: "{text}"

**Instructions**:
- Focus on the speaker's primary communicative goal, not surface politeness
- Consider implicit meaning and pragmatic context
- Assign confidence based on clarity of intent (0.7-0.9 for clear, 0.5-0.6 for ambiguous)

**Output Format** (respond with ONLY these two lines):
category: <category_name>
confidence: <0.00-1.00>"""

        try:
            response = self._call_api(
                messages=[
                    {"role": "system", "content": "You are an expert linguist and pragmatics specialist. You analyze communicative intent with precision, distinguishing between surface form and underlying meaning. You provide clear, justified classifications based on speech act theory."},
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
        level: str,
        fidelity: str = "medium"
    ) -> str:
        """
        Refine text using DeepSeek API.

        Args:
            input_text: Original input text
            filled_template: Template-generated text
            intent: Detected intent
            level: Politeness level
            fidelity: Fidelity level (closeness to original meaning)

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

        fidelity_descriptions = {
            "high": "元の意味とトーンに可能な限り忠実で、不適切にならない程度に直接的な表現を保つ",
            "medium": "バランスの取れた建前表現（標準）",
            "low": "最大限の京都風間接表現、意味の乖離を許容して礼儀を優先"
        }

        prompt = f"""# 役割定義
あなたは日本の伝統的な高文脈コミュニケーションの専門家です。特に、京都の老舗商家に伝わる「建前（たてまえ）」の技法に精通しています。

# タスク
以下の直接的なメッセージを、日本の伝統的な「建前表現」に変換してください。

**元のメッセージ**: "{input_text}"
**意図カテゴリ**: {intent}
**丁寧さレベル**: {level_descriptions[level]}
**忠実度レベル**: {fidelity_descriptions[fidelity]}

# 建前表現の本質的原則

## 核心思想
建前とは、社会的調和（和）を保つために、本音を間接的・暗示的に伝える日本独特の高文脈コミュニケーション技法です。

## 具体的手法

### 1. 表層と深層の二重構造
- **表層**: 極めて丁寧で肯定的な言葉遣い
- **深層**: 本来の否定的・批判的な意図を巧妙に埋め込む
- **重要**: 表層が完璧すぎることで、深層の意図を察知させる

### 2. 京都風の間接表現技法
a) **婉曲的拒絶**:
   - 直接「NO」は絶対に言わない
   - 「検討させていただきます」= 実行しない
   - 「参考にさせていただきます」= 採用しない
   - 「前向きに」「慎重に」= 実際には否定的

b) **逆説的褒め言葉**:
   - 批判を褒め言葉の形式で包む
   - 「さすがですね」= あり得ない/理解できない
   - 「勉強になります」= 間違っている
   - 「興味深いですね」= 実行不可能

c) **状況依存の責任回避**:
   - 「現在の状況を鑑みますと」= 私の意思ではなく状況のせい
   - 「諸般の事情により」= 説明したくない理由
   - 「タイミングが」= 永遠に来ない適切な時期

### 3. 文脈保持の原則
- 元のメッセージの**具体的な対象・内容**は必ず保持
- ただし、直接性を和らげ、間接的に言及する
- 固有名詞や具体的事項は「そちら」「その件」などに置き換え可能だが、文脈から特定できる程度に残す

### 4. 言語美学
- 文法的に完璧な日本語（「いただく」の重複などを避ける）
- 適度な謙譲語・尊敬語の使用
- 季節感や時候の挨拶を適宜織り込む（長文の場合）
- リズムと調和を重視

## 丁寧さレベル別の調整

**business（標準ビジネス）**:
- 「〜と存じます」「〜いただければ」レベル
- 適度な距離感を保つ

**ultra_polite（超丁寧）**:
- 「恐れ入りますが」「恐縮ではございますが」
- 書簡形式（拝啓〜敬具）の採用も検討
- 最大限の謙譲表現

**casual（カジュアル）**:
- 「〜と思います」「〜ですね」
- 親しみやすいが礼儀は保つ
- 過度な敬語は避ける

## 忠実度レベル別の調整

**high（高忠実度）**:
- 元の意味とトーンを最大限保持する
- 直接的な表現をできるだけ維持し、不適切にならない程度の最小限の調整のみ
- 婉曲表現や間接表現は基本的に使わない
- 具体的な内容を削除したり置き換えたりしない
- 元の言葉遣いに近い日本語表現を選ぶ
- 「礼儀正しいが率直」な表現を目指す
- 建前技法は最小限（社交辞令的なクッションや導入フレーズ程度）
- 例: "I'm not interested" → 「興味がございません」（×「魅力的ですが今回は見送ります」）

**medium（中忠実度・標準）**:
- バランスの取れた建前表現
- 適度な間接表現と意味の保持
- 伝統的な建前技法を適切に使用
- 文脈から意図が十分に読み取れる程度

**low（低忠実度）**:
- 最大限の京都風間接表現を使用
- 礼儀と社交辞令を最優先
- 元の意味からの乖離を許容
- 「表層的には極めて肯定的だが、深層では否定的」な表現
- 高度な文脈理解が必要な表現も可

# 変換例

**例1 - 批判的フィードバック**
- 元: "Your code has too many bugs and is poorly structured"
- 建前: 「コードを拝見いたしました。大変興味深い実装アプローチですね。いくつか改善の余地がある箇所も見受けられましたので、今後のご参考までに別途お伝えできればと存じます。」
- 分析: 「興味深い」=標準的ではない、「改善の余地」=多くの問題、「今後のご参考」=直ちに修正すべき

**例2 - 求人の辞退**
- 元: "I'm not interested in this position"
- 建前: 「大変魅力的なポジションのご紹介、誠にありがとうございます。現在の業務に注力している状況でございまして、今回は情報として頂戴させていただきたく存じます。」
- 分析: 「魅力的」=社交辞令、「注力している」=他を考える余地なし、「情報として」=応募しない

**例3 - 提案の却下**
- 元: "That proposal won't work"
- 建前: 「ご提案の内容、慎重に拝見させていただきました。様々な角度から検討させていただきましたところ、現段階では実現に向けた課題も多く、もう少しお時間をいただきたく存じます。」
- 分析: 「慎重に」=否定的に、「課題も多く」=実現困難、「お時間を」=無期限延期

# 出力指示
上記の原則に従い、元のメッセージを建前表現に変換した**日本語テキストのみ**を出力してください。
説明・注釈・引用符は一切不要です。自然な日本語として成立する文章を生成してください。"""

        try:
            response = self._call_api(
                messages=[
                    {"role": "system", "content": "あなたは日本の高文脈コミュニケーションの専門家であり、特に京都の伝統的な建前表現に精通しています。表層では極めて丁寧で肯定的な表現を用いながら、深層では本音を巧妙に暗示する技法を習得しています。言語学的な洗練と文化的な深みを備えた、自然で美しい日本語を生成します。元のメッセージの具体的な内容・文脈は必ず保持しつつ、間接的な表現に変換します。"},
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
