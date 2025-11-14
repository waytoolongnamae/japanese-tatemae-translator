"""
Configuration settings for Japanese Hedging Translator
"""
import os
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

# API Configuration
DEEPSEEK_API_KEY_CHAT = os.getenv("DEEPSEEK_API_KEY_CHAT", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

# Model Provider Selection
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "deepseek")  # Options: "deepseek", "openai"
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "deepseek-chat")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# Log Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = "logs"

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
