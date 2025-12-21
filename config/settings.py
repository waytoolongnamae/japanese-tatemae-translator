"""
Configuration settings for Japanese Hedging Translator
"""
import logging
import os
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()


def _get_bool_env(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _get_int_env(name: str, default: int, min_value: int = None, max_value: int = None) -> int:
    raw = os.getenv(name)
    try:
        value = int(raw) if raw is not None else default
    except ValueError:
        value = default
    if min_value is not None and value < min_value:
        value = min_value
    if max_value is not None and value > max_value:
        value = max_value
    return value


def _get_float_env(name: str, default: float, min_value: float = None, max_value: float = None) -> float:
    raw = os.getenv(name)
    try:
        value = float(raw) if raw is not None else default
    except ValueError:
        value = default
    if min_value is not None and value < min_value:
        value = min_value
    if max_value is not None and value > max_value:
        value = max_value
    return value


def _get_csv_env(name: str, default: str = "") -> List[str]:
    raw = os.getenv(name, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


# API Configuration
DEEPSEEK_API_KEY_CHAT = os.getenv("DEEPSEEK_API_KEY_CHAT", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

# Model Provider Selection
ALLOWED_MODEL_PROVIDERS = ("deepseek", "openai")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "deepseek").lower()
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "deepseek-chat")
TEMPERATURE = _get_float_env("TEMPERATURE", 0.7, min_value=0.0, max_value=2.0)
API_TIMEOUT_SECONDS = _get_float_env("API_TIMEOUT_SECONDS", 30.0, min_value=1.0, max_value=120.0)
MAX_API_RETRIES = _get_int_env("MAX_API_RETRIES", 3, min_value=0, max_value=10)

# Log Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_DIR = os.getenv("LOG_DIR", "logs")
LOG_TO_FILE = _get_bool_env("LOG_TO_FILE", True)
LOG_FILE_NAME = os.getenv("LOG_FILE_NAME", "translator.log")
LOG_FILE_MAX_BYTES = _get_int_env("LOG_FILE_MAX_BYTES", 5 * 1024 * 1024, min_value=1024)
LOG_FILE_BACKUPS = _get_int_env("LOG_FILE_BACKUPS", 5, min_value=0, max_value=20)

# Request/Validation Limits
MIN_INPUT_LENGTH = _get_int_env("MIN_INPUT_LENGTH", 1, min_value=1, max_value=1000)
MAX_INPUT_LENGTH = _get_int_env("MAX_INPUT_LENGTH", 5000, min_value=1, max_value=100000)
MAX_REQUEST_BYTES = _get_int_env("MAX_REQUEST_BYTES", 65536, min_value=1024, max_value=10 * 1024 * 1024)

# Web Security/Network Configuration
CORS_ALLOWED_ORIGINS = _get_csv_env("CORS_ALLOWED_ORIGINS")
ALLOWED_HOSTS = _get_csv_env("ALLOWED_HOSTS")

# Intent Categories
INTENT_CATEGORIES = [
    "refusal",
    "disagreement",
    "delay",
    "disinterest",
    "criticism",
    "neutral_polite"
]

# Politeness Levels
POLITENESS_LEVELS = {
    "business": 1,  # Neutral Business
    "ultra_polite": 2,  # Ultra Polite
    "casual": 3  # Casual Social
}

# Fidelity Levels (closeness to original meaning)
FIDELITY_LEVELS = {
    "high": 1,      # Stay close to original meaning, minimal embellishment
    "medium": 2,    # Balanced tatemae style (default)
    "low": 3        # Maximum Kyoto-style indirection, can deviate for politeness
}

# Template Database
TEMPLATES: Dict[str, List[str]] = {
    "refusal": [
        "現在は{soft_reason}、今回は{neutral_action}させていただきます。",
        "誠に恐縮ですが、現在{soft_reason}ため、{neutral_action}させていただければと存じます。",
        "{soft_reason}という状況でございまして、{neutral_action}させていただきたく存じます。"
    ],
    "disagreement": [
        "{acknowledge}が、{soft_negation}と思っております。",
        "{acknowledge}。ただ、{soft_negation}という見方もあるかもしれません。",
        "ご意見も理解いたしますが、{soft_negation}と考えております。"
    ],
    "delay": [
        "現時点では{soft_constraint}ため、{future_intent}。",
        "現在{soft_constraint}という状況でして、{future_intent}と考えております。",
        "申し訳ございませんが、{soft_constraint}ため、{future_intent}させていただければと思います。"
    ],
    "criticism": [
        "もう少し{neutral_term}の余地があるかもしれません。",
        "{neutral_term}について、改善の余地があるかもしれないと感じました。",
        "今後{neutral_term}を検討いただけますと幸いです。"
    ],
    "disinterest": [
        "{interest_phrase}。今回は{reference_action}。",
        "貴重な情報をありがとうございます。{interest_phrase}が、今回は{reference_action}させていただきます。",
        "{interest_phrase}。ただ、現在は{reference_action}という状況でございます。"
    ],
    "neutral_polite": [
        "承知いたしました。{polite_acknowledgment}。",
        "ご連絡ありがとうございます。{polite_acknowledgment}。",
        "かしこまりました。{polite_acknowledgment}させていただきます。"
    ]
}

# Softening Phrases Database
SOFTENERS = {
    "soft_reason": [
        "別のテーマに注力しており",
        "他の案件を優先しておりまして",
        "スケジュールの都合上",
        "現在の体制では",
        "諸般の事情により"
    ],
    "neutral_action": [
        "情報として参考にさせていただきます",
        "見送らせていただきます",
        "今後の参考とさせていただきます",
        "お断りさせていただきます",
        "辞退させていただきます"
    ],
    "acknowledge": [
        "おっしゃることはわかります",
        "ご意見ごもっともです",
        "そのお考えも理解できます",
        "確かにそういう見方もあります"
    ],
    "soft_negation": [
        "少し異なる見方をしております",
        "別の観点から検討が必要かもしれません",
        "もう少し慎重に考えたいと思っております",
        "若干異なる印象を持っております"
    ],
    "soft_constraint": [
        "スケジュールが立て込んでおり",
        "調整が必要な状況でして",
        "確認事項がございまして",
        "社内調整中でして"
    ],
    "future_intent": [
        "改めてご連絡させていただきます",
        "後日あらためてご相談させてください",
        "追って調整させていただきます",
        "別の機会にご相談できればと存じます"
    ],
    "neutral_term": [
        "検討",
        "精査",
        "調整",
        "改善",
        "ブラッシュアップ"
    ],
    "interest_phrase": [
        "興味深いお話です",
        "貴重な機会をいただきありがとうございます",
        "魅力的なご提案です",
        "大変光栄なお話です"
    ],
    "reference_action": [
        "情報として参考にさせていただきます",
        "今後の参考とさせていただきます",
        "別の機会にさせていただきたく存じます",
        "今回は見送らせていただきます"
    ],
    "polite_acknowledgment": [
        "対応させていただきます",
        "確認させていただきます",
        "検討させていただきます",
        "承りました"
    ]
}

# Honorific Modifiers by Level
HONORIFIC_MODIFIERS = {
    1: {  # Business - Standard keigo
        "verb_endings": ["ます", "ております", "させていただきます"],
        "sentence_starters": ["", ""],
        "closings": ["。", "と存じます。"]
    },
    2: {  # Ultra Polite - Heavy keigo
        "verb_endings": ["いたします", "させていただきます", "申し上げます"],
        "sentence_starters": ["誠に恐縮ですが、", "大変恐れ入りますが、"],
        "closings": ["と存じます。", "させていただければ幸いです。", "いただけますと幸いです。"]
    },
    3: {  # Casual - Light polite
        "verb_endings": ["ます", "と思います"],
        "sentence_starters": ["", "すみませんが、"],
        "closings": ["。", "ね。", "と思います。"]
    }
}


def validate_settings() -> Dict[str, List[str]]:
    """
    Validate configuration values and return warnings/errors.

    Returns:
        Dict with "errors" and "warnings" lists
    """
    errors: List[str] = []
    warnings: List[str] = []

    if MODEL_PROVIDER not in ALLOWED_MODEL_PROVIDERS:
        warnings.append(
            f"MODEL_PROVIDER='{MODEL_PROVIDER}' not in {ALLOWED_MODEL_PROVIDERS}; defaulting to fallback behavior."
        )

    if LOG_LEVEL not in logging._nameToLevel:
        warnings.append(f"LOG_LEVEL='{LOG_LEVEL}' is not a standard logging level.")

    if MIN_INPUT_LENGTH > MAX_INPUT_LENGTH:
        errors.append("MIN_INPUT_LENGTH cannot be greater than MAX_INPUT_LENGTH.")

    if API_TIMEOUT_SECONDS <= 0:
        errors.append("API_TIMEOUT_SECONDS must be greater than 0.")

    if MAX_API_RETRIES < 0:
        errors.append("MAX_API_RETRIES must be zero or greater.")

    if MODEL_PROVIDER == "deepseek" and not DEEPSEEK_API_KEY_CHAT:
        warnings.append("DEEPSEEK_API_KEY_CHAT is not set; DeepSeek calls will fall back.")

    if MODEL_PROVIDER == "openai" and not OPENAI_API_KEY:
        warnings.append("OPENAI_API_KEY is not set; OpenAI calls will fall back.")

    return {"errors": errors, "warnings": warnings}
