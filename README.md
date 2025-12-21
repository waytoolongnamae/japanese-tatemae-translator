# Japanese Hedging Translator (建前 Translator)

![Coverage](https://img.shields.io/badge/coverage-82%25-brightgreen)

Transform direct messages into polite Japanese business communication with Kyoto-style 建前 (tatemae) - the art of subtle, indirect expression.

## ⚠️ Important Disclaimer

**This tool is a satirical and educational project exploring Japanese communication patterns.**

The "Kyoto-style" expressions generated represent an **exaggerated, sarcastic interpretation** of high-context communication for **educational and entertainment purposes**.

**I do not endorse using this communication style in real professional interactions.** Direct, honest communication is always preferable. This tool demonstrates:

- Cultural communication differences (high-context vs. low-context)
- Linguistic creativity and satire
- NLP and prompt engineering techniques
- Linguistic indirection as an academic subject

Use responsibly and with cultural sensitivity.

---

## 🚀 Quick Start

### 📱 Web App (Recommended)

```bash
cd web
pip install -r requirements-web.txt
python app.py
```

Open [http://localhost:8000](http://localhost:8000) - Mobile-friendly, PWA-enabled, easy to share!

**Deploy:** See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for Railway, Fly.io, Vercel, Heroku, AWS, GCP, Docker options.

### 💻 Command Line

```bash
# Interactive mode
python cli.py

# Direct translation
python cli.py -m "I'm not interested in this job."

# With politeness level
python cli.py -m "That's not possible." -l ultra_polite

# With fidelity level (closeness to original meaning)
python cli.py -m "I disagree" -f high  # Direct and frank
python cli.py -m "I disagree" -f low   # Maximum indirection

# With specific model provider
python cli.py --model openai  # Use OpenAI
python cli.py --model deepseek  # Use DeepSeek (default)
```

### 🐍 Python API

```python
from translator import JapaneseTatemaeTranslator

translator = JapaneseTatemaeTranslator()

# With fidelity control
result = translator.translate(
    "I'm not interested in this job.",
    level="business",
    fidelity="medium"  # high, medium, or low
)
print(result["tatemae_text"])
# Medium fidelity: 現在は別のテーマに注力しており、今回は情報として参考にさせていただきます。

# High fidelity (more direct)
result = translator.translate(
    "I'm not interested in this job.",
    level="business",
    fidelity="high"
)
# High fidelity: 興味がございません。
```

---

## ✨ Features

- **Two-Dimensional Control**: Adjust both politeness level AND fidelity (closeness to original meaning)
- **Fidelity Levels**:
  - **High**: Direct and frank with polite language, minimal tatemae
  - **Medium**: Balanced tatemae expression (default)
  - **Low**: Maximum Kyoto-style indirection
- **Kyoto-Style 建前**: Praise while criticizing, say "yes" while meaning "no"
- **Context Preservation**: Maintains specific details from your input (names, topics, etc.)
- **Intent Detection**: Classifies messages (refusal, disagreement, delay, disinterest, criticism, neutral)
- **3 Politeness Levels**: business, ultra_polite, casual
- **Multi-line Support**: CLI handles pasted text with line breaks
- **Web & API**: Mobile-friendly web UI with fidelity selector + REST API
- **Multiple LLM Providers**: DeepSeek (default) and OpenAI with automatic fallback
- **Model Selection**: Choose your preferred provider via CLI argument or environment variable
- **Model Info Display**: See current provider and model in both CLI and web interface
- **82% Test Coverage**: 158 tests with comprehensive unit and integration coverage

---

## ✅ Tests

```bash
pytest
```

Last run: 158 tests, 82% coverage.

---

## 🎌 Kyoto-Style Examples

Polite on the surface, with hidden meaning underneath:

```bash
# Criticism → Praise
$ python cli.py -m "Your code is terrible" -q
大変興味深いコードのご提案を拝見いたしました。
私どもには大変勉強になる斬新なアプローチでございます。
# "Interesting" = bad, "Educational" = what not to do

# Refusal → Consideration
$ python cli.py -m "I don't want to work with John anymore" -q
ジョンさんには大変お世話になっております。ただ、今後のプロジェクトにつきましては、
より多様なスキルセットをお持ちの方々との協働も検討させていただきたく存じます。
# "Thank you John" + "considering others" = done with John

# Disagreement → Learning
$ python cli.py -m "Your proposal will never work" -q
さすがに独創的なご提案で、大変勉強になります。
現実の様々な事情を考慮いたしますと、実現にはさらなる工夫が必要かもしれませんね。
# "Original" = impractical, "needs work" = won't happen
```

**Key Feature**: Context is preserved (code, John, proposal) while applying Kyoto-style indirectness.

📖 **Full Guide**: [docs/KYOTO_STYLE.md](docs/KYOTO_STYLE.md)

---

## 📦 Installation

### Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

```bash
# Clone repository
git clone https://github.com/yourusername/winwin.git
cd winwin

# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Add your DeepSeek API key to .env
```

### Using pip

```bash
# Clone repository
git clone https://github.com/yourusername/winwin.git
cd winwin

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Add your DeepSeek API key to .env
```

Get your API key: [platform.deepseek.com](https://platform.deepseek.com)

---

## 📖 Documentation

### Complete Guide
**[docs/INDEX.md](docs/INDEX.md)** - Full documentation index with learning paths

### Quick Links
| Topic | Documentation |
|-------|---------------|
| 🚀 Quick Start | [docs/QUICKSTART.md](docs/QUICKSTART.md) |
| 📱 Web App Setup | [docs/QUICKSTART_WEB.md](docs/QUICKSTART_WEB.md) |
| 🌐 Deployment | [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) |
| 🧭 Runbook | [docs/RUNBOOK.md](docs/RUNBOOK.md) |
| 💻 CLI Usage | [docs/USAGE.md](docs/USAGE.md) |
| 🎌 Kyoto-Style Guide | [docs/KYOTO_STYLE.md](docs/KYOTO_STYLE.md) |
| 🔒 Security | [docs/SECURITY.md](docs/SECURITY.md) |
| 🧪 Testing | [docs/TESTING.md](docs/TESTING.md) |
| 📝 Changelog | [docs/CHANGELOG.md](docs/CHANGELOG.md) |
| 🔧 Project Structure | [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) |

---

## 🎯 Usage

### Fidelity Levels (Closeness to Original Meaning)

- **high**: Direct and frank translation with polite language, minimal tatemae techniques
- **medium**: Balanced tatemae expression with moderate indirection (default)
- **low**: Maximum Kyoto-style indirection, meaning can deviate for politeness

### Politeness Levels

- **business**: Standard business keigo (most professional contexts)
- **ultra_polite**: Heavy honorifics (formal situations, senior stakeholders)
- **casual**: Light polite form (internal teams, casual professional)

### Intent Categories

- **refusal**: Declining/rejecting
- **disagreement**: Opposing an idea
- **delay**: Postponing/deferring
- **disinterest**: Not interested
- **criticism**: Pointing out flaws
- **neutral_polite**: Neutral acknowledgment

### CLI Examples

```bash
# Interactive mode with multi-line support
python cli.py
# Type message, press Esc+Enter to submit
# Use :fidelity high/medium/low to change fidelity level

# Single translation
python cli.py -m "I disagree with that idea."

# Custom level and fidelity
python cli.py -m "Not possible" -l ultra_polite -f high

# Fidelity comparison
python cli.py -m "I'm not interested" -f high    # More direct
python cli.py -m "I'm not interested" -f medium  # Balanced
python cli.py -m "I'm not interested" -f low     # Maximum tatemae

# Pipe input
echo "I can't attend" | python cli.py --stdin

# Quiet mode (text only)
python cli.py -m "No thanks" -q

# With context
python cli.py -m "I'm not interested" -c recruiter
```

### Python API

```python
# Full metadata with fidelity control
result = translator.translate(
    "Your proposal is inefficient.",
    level="business",
    fidelity="high",  # high, medium, or low
    context="business"
)
print(result["tatemae_text"])
print(f"Intent: {result['intent']} ({result['confidence']:.0%} confidence)")

# Simple interface (text only)
text = translator.translate_simple("I disagree", level="casual", fidelity="medium")
```

---

## 🏗️ Architecture

### Workflow Stages

```
Input → Language Detection → Intent Detection → Template Generation → Politeness Tuning → Output
```

1. **Language Detector**: Identifies input language (EN/JP/ZH)
2. **Intent Detector**: LLM-powered intent classification
3. **Tatemae Generator**: Template selection and filling
4. **Politeness Tuner**: Grammar refinement and level adjustment

### Tech Stack

- **Framework**: LangGraph workflow orchestration
- **LLM**: DeepSeek API (with keyword fallback)
- **Web**: FastAPI + vanilla JS (PWA-enabled)
- **Testing**: pytest with 90%+ coverage
- **Deployment**: Docker, Railway, Fly.io, Vercel, etc.

### Project Structure

```
winwin/
├── config/           # Settings and templates
├── models/           # State definitions
├── processing/       # Workflow nodes and graph
├── providers/        # LLM provider abstraction
├── web/              # FastAPI web app
├── docs/             # Documentation
├── tests/            # Test suite
├── translator.py     # Main API
└── cli.py            # CLI interface
```

Full structure: [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)

---

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov

# Specific test file
pytest tests/test_translator.py -v

# Watch mode
pytest tests/ -v --tb=short
```

**Test Categories**:
- Unit tests: Individual components
- Integration tests: Full workflow
- Edge cases: Boundary conditions and error handling

All tests use mocked providers (no API calls needed).

---

## 🔒 Security & Robustness

### Input Validation
- Type checking and length limits (1-5000 chars)
- Empty/whitespace detection
- Automatic correction for invalid parameters

### API Resilience
- Automatic retry with exponential backoff (up to 3 attempts)
- 30-second timeout
- Graceful fallback to keyword matching when API unavailable
- Rate limit handling

### Provider Abstraction
- Pluggable architecture for multiple LLM providers
- Comprehensive error logging

See [docs/SECURITY.md](docs/SECURITY.md) for security best practices.

---

## 🚀 Deployment

Deploy your own instance for public access:

### Recommended Options

| Platform | Difficulty | Cost | Best For |
|----------|-----------|------|----------|
| **Railway** | ⭐ Easiest | Free tier | Quick deploy, low traffic |
| **Fly.io** | ⭐⭐ Easy | Free (3 VMs) | Production, global CDN |
| **Vercel** | ⭐ Easiest | Free tier | Serverless, simple |
| **Docker** | ⭐⭐ Moderate | Self-hosted | Full control |

**Complete Guide**: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

Quick deploy to Railway:
```bash
# 1. Push to GitHub
# 2. Visit railway.app
# 3. Connect repo
# 4. Add DEEPSEEK_API_KEY_CHAT
# 5. Deploy!
```

---

## 🔮 Future Improvements

- [ ] Multi-language translation support
- [ ] Fine-tuned intent classification model
- [ ] Context-aware template selection
- [ ] Relationship hierarchy awareness
- [ ] LangGraph Studio visualization

See [docs/IMPROVEMENTS.md](docs/IMPROVEMENTS.md) for full roadmap.

---

## 📄 License

This project is for educational and professional use.

---

## 🤝 Contributing

Contributions welcome! Please:
1. Check [docs/IMPROVEMENTS.md](docs/IMPROVEMENTS.md) for wanted features
2. Review [docs/TESTING.md](docs/TESTING.md) for testing requirements
3. Submit issues or pull requests on GitHub

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/winwin/issues)
- **Security**: See [docs/SECURITY.md](docs/SECURITY.md) for reporting
- **Documentation**: Start with [docs/INDEX.md](docs/INDEX.md)

---

**Built with**: DeepSeek API • LangGraph • FastAPI • Python 3.12+

**Version**: 3.1.0 (Fidelity Dimension Release) - See [docs/CHANGELOG.md](docs/CHANGELOG.md)
