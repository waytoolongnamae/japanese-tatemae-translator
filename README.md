# Japanese Hedging Translator (建前 Translator)

A natural language style conversion tool that transforms direct, explicit, or assertive statements into indirect, polite, and vague Japanese-style expressions (建前 language) suitable for business or social communication in Japan.

## Overview

This tool helps convert straightforward messages into appropriately indirect Japanese business communication style, automatically detecting intent and applying culturally appropriate hedging patterns. **Now featuring Kyoto-style communication** - the art of being polite on the surface while subtly conveying your true meaning underneath.

## Features

- **Kyoto-Style Tatemae (京都風建前)**: Subtle sarcasm hidden beneath polite language - praise while criticizing, say "yes" while meaning "no"
- **Context Preservation**: Each translation maintains specific details from your input - no generic responses
- **Intent Detection**: Automatically classifies messages into categories (refusal, disagreement, delay, disinterest, criticism, neutral)
- **Grammar Refinement**: LLM-powered grammar checking ensures natural, correct Japanese output
- **Politeness Levels**: Three levels of formality (business, ultra_polite, casual)
- **LangGraph Workflow**: Structured multi-stage processing pipeline
- **LLM-Powered**: Uses DeepSeek API for intent detection and grammar refinement (with keyword fallback)

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Add your DeepSeek API key to .env
DEEPSEEK_API_KEY_CHAT=your_deepseek_key_here
```

## Quick Start

### Command Line (Recommended)

```bash
# Interactive mode (default)
python cli.py

# Translate a single message
python cli.py -m "I'm not interested in this job."

# With custom politeness level
python cli.py -m "That's not possible." -l ultra_polite

# Using the wrapper script
./tatemae -m "I disagree with that idea."
```

### Python API

```python
from translator import JapaneseTatemaeTranslator

# Initialize translator
translator = JapaneseTatemaeTranslator()

# Translate a message
result = translator.translate(
    "I'm not interested in this job.",
    level="business"
)

print(result["tatemae_text"])
# Output: 現在は別のテーマに注力しており、今回は情報として参考にさせていただきます。
```

## Kyoto-Style Examples (京都風建前)

The translator uses **Kyoto-style communication** - polite on the surface, but with hidden meaning underneath:

```bash
# Criticism disguised as praise
$ python cli.py -m "Your code is terrible" -q
大変興味深いコードのご提案を拝見いたしました。
私どもには大変勉強になる斬新なアプローチでございます。

# "Interesting" = bad, "Educational" = what not to do

# Refusal disguised as consideration
$ python cli.py -m "I don't want to work with John anymore" -q
ジョンさんには大変お世話になっております。ただ、今後のプロジェクトにつきましては、
より多様なスキルセットをお持ちの方々との協働も検討させていただきたく存じます。

# "Thank you John" + "considering others" = done with John

# Disagreement disguised as learning
$ python cli.py -m "Your proposal will never work" -q
さすがに独創的なご提案で、大変勉強になります。
現実の様々な事情を考慮いたしますと、実現にはさらなる工夫が必要かもしれませんね。

# "Original" = impractical, "needs work" = won't happen
```

**Key feature**: Each translation preserves the specific context (code, John, proposal) while applying Kyoto-style indirectness.

📖 **Full Guide**: See [KYOTO_STYLE.md](KYOTO_STYLE.md) for comprehensive examples and cultural background.

## Usage Examples

### Example 1: Refusal
```python
input_text = "I'm not interested in this job."
result = translator.translate(input_text, level="business")
print(result["tatemae_text"])
# 大変興味深いお話をいただきまして、誠にありがとうございます。
# 慎重に検討させていただきましたが、今回は見送らせていただきますこととなりました。
```

### Example 2: Criticism
```python
input_text = "Your proposal is inefficient."
result = translator.translate(input_text, level="business")
print(result["tatemae_text"])
# 誠に素晴らしいご提案と拝見いたしました。さすがに独創的なお考えで、
# 大変勉強になる内容でございます。
```

### Example 3: Delay
```python
input_text = "I can't meet this week."
result = translator.translate(input_text, level="business")
print(result["tatemae_text"])
# 誠に申し訳ございませんが、今週中は調整が難しそうでございまして、
# 日程を改めてご相談させていただけますと幸いです。
```

### Example 4: Disagreement
```python
input_text = "I disagree with that idea."
result = translator.translate(input_text, level="business")
print(result["tatemae_text"])
# お考えはよく理解いたしましたが、別の観点もございますので、
# 少しご提案させていただければと存じます。
```

## Politeness Levels

- **business** (Level 1): Standard business keigo - appropriate for most professional contexts
- **ultra_polite** (Level 2): Heavy honorific usage - for formal situations or senior stakeholders
- **casual** (Level 3): Light polite form - for internal teams or casual professional settings

## Command Line Interface

### Interactive Mode

Start interactive mode (default):
```bash
python cli.py
```

In interactive mode:
- Type your message and press Enter to translate
- `:level <business|ultra_polite|casual>` - Change politeness level
- `:help` - Show help
- `:quit` or `:q` - Exit

Example session:
```
> I'm not interested in this job.
⏳ Translating...
================================================================================
📝 Translation Result:
================================================================================
貴重な情報をありがとうございます。魅力的なご提案ですが、今回は今後の参考とさせていただきます。

--------------------------------------------------------------------------------
Intent:     disinterest
Confidence: 98.00%
Level:      business
Language:   en
================================================================================

> :level ultra_polite
✓ Politeness level changed to: ultra_polite

> That's not possible.
...
```

### Single Translation Mode

Translate a message directly:
```bash
# Basic usage
python cli.py -m "I'm not interested in this job."

# With politeness level
python cli.py -m "That's not possible." -l ultra_polite

# With context
python cli.py -m "I disagree" -l business -c business

# Quiet mode (output only translated text)
python cli.py -m "I can't meet" -q
```

### Pipe Input

```bash
# From echo
echo "I disagree with that idea." | python cli.py --stdin

# From file
cat message.txt | python cli.py --stdin -l ultra_polite

# With other commands
curl -s https://example.com/message | python cli.py --stdin -q
```

### Wrapper Script

Use the `tatemae` wrapper for shorter commands:
```bash
./tatemae -m "Your proposal is inefficient."
./tatemae -m "I can't attend" -l casual
```

### CLI Options

```
-m, --message TEXT          Message to translate
-l, --level LEVEL          Politeness level: business, ultra_polite, casual
-c, --context CONTEXT      Context: business, personal, recruiter
--stdin                    Read input from stdin
-q, --quiet                Output only translated text
-i, --interactive          Run in interactive mode
-h, --help                 Show help message
```

## API Reference

### `JapaneseTatemaeTranslator`

Main translator class.

#### Methods

##### `translate(input_text: str, level: str = "business", context: Optional[str] = None) -> Dict`

Full translation with metadata.

**Parameters:**
- `input_text`: The direct message to convert
- `level`: Politeness level ("business", "ultra_polite", "casual")
- `context`: Optional context tag ("business", "personal", "recruiter")

**Returns:**
```python
{
    "tatemae_text": str,      # Translated text
    "intent": str,            # Detected intent category
    "confidence": float,      # Confidence score (0-1)
    "detected_language": str, # Input language
    "level": str,            # Politeness level used
    "context": str           # Context tag
}
```

##### `translate_simple(input_text: str, level: str = "business") -> str`

Simplified interface returning only the translated text.

### `quick_translate(input_text: str, level: str = "business") -> str`

Convenience function for one-off translations.

## Architecture

### Workflow Stages

1. **Language Detector**: Detects input language (EN/JP/ZH)
2. **Intent Detector**: Classifies message intent using LLM
3. **Tatemae Generator**: Selects and fills appropriate templates
4. **Politeness Tuner**: Adjusts formality level

### Project Structure

```
winwin/
├── config/
│   └── settings.py          # Configuration and templates
├── models/
│   └── state.py            # State definitions
├── processing/
│   ├── nodes.py            # Workflow nodes
│   └── graph.py            # LangGraph workflow
├── logs/                   # Log files
├── translator.py           # Main API
├── main.py                 # Example runner
├── requirements.txt        # Dependencies
├── .env.example           # Environment template
└── README.md              # This file
```

## Running Examples

```bash
# Run example translations
python main.py
```

This will demonstrate various translation scenarios with different intents and politeness levels.

## Intent Categories

- **refusal**: Declining or rejecting something
- **disagreement**: Disagreeing with a statement
- **delay**: Postponing or delaying
- **disinterest**: Not interested in an opportunity
- **criticism**: Pointing out flaws or issues
- **neutral_polite**: Neutral acknowledgment

## Configuration

Edit [config/settings.py](config/settings.py) to customize:
- Templates for each intent category
- Softening phrases database
- Honorific modifiers by level
- LLM model and parameters

## Advanced Usage

### Custom Context

```python
result = translator.translate(
    "I don't think this will work",
    level="business",
    context="recruiter"
)
```

### Accessing Metadata

```python
result = translator.translate("Not interested")
print(f"Detected intent: {result['intent']}")
print(f"Confidence: {result['confidence']}")
print(f"Language: {result['detected_language']}")
```

## Limitations

- Currently optimized for English/Japanese input
- Requires DeepSeek API key for best intent detection
- Fallback to keyword matching when API unavailable
- Does not perform language translation (preserves Japanese input)

## Future Enhancements

- [ ] Multi-language translation support
- [ ] Fine-tuned intent classification model
- [ ] Context-aware template selection
- [ ] Tone adjustment based on relationship hierarchy
- [ ] LangGraph Studio visualization support

## License

This project is for educational and professional use.

## Contributing

Contributions welcome! Please feel free to submit issues or pull requests.

## Support

For questions or issues, please open a GitHub issue.
