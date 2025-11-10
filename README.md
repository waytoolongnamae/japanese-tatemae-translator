# 建前 Translator

Transform direct messages into polite Japanese business communication with Kyoto-style 建前 (tatemae) - the art of subtle, indirect expression.

> ⚠️ **Educational & Satirical Tool**: This exaggerates communication patterns for learning purposes. Not recommended for actual professional use.

---

## 🚀 Quick Start

**Web App (Recommended):**
```bash
cd web && pip install -r requirements-web.txt && python app.py
```
Open [localhost:8000](http://localhost:8000) - Mobile-friendly, PWA-enabled, shareable!

**CLI:**
```bash
python cli.py -m "I'm not interested in this job."
```

**Python:**
```python
from translator import JapaneseTatemaeTranslator
translator = JapaneseTatemaeTranslator()
result = translator.translate("Not possible", level="business")
```

📖 **Full Guide**: [docs/QUICKSTART.md](docs/QUICKSTART.md) | [docs/QUICKSTART_WEB.md](docs/QUICKSTART_WEB.md)

---

## ✨ What It Does

**Criticism → Praise**
```
Input:  "Your code is terrible"
Output: 大変興味深いコードのご提案を拝見いたしました。私どもには大変勉強になる斬新なアプローチでございます。
        ("Interesting" = bad, "Educational" = what not to do)
```

**Refusal → Consideration**
```
Input:  "I don't want to work with John anymore"
Output: ジョンさんには大変お世話になっております。ただ、今後のプロジェクトにつきましては、
        より多様なスキルセットをお持ちの方々との協働も検討させていただきたく存じます。
        (Politely indicating you're done with John)
```

**Key Feature**: Context preserved (names, topics) + Kyoto-style indirectness applied.

📖 [Kyoto-Style Guide](docs/KYOTO_STYLE.md)

---

## 📦 Installation

**Using uv (faster):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
```

**Using pip:**
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

**Configure:**
```bash
cp .env.example .env
# Add your DeepSeek API key to .env
```

Get API key: [platform.deepseek.com](https://platform.deepseek.com)

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| **Kyoto-Style 建前** | Say "yes" while meaning "no", praise while criticizing |
| **Context Preservation** | Maintains names, topics, specific details |
| **Intent Detection** | Refusal, disagreement, delay, disinterest, criticism, neutral |
| **3 Politeness Levels** | business, ultra_polite, casual |
| **Multi-line Input** | CLI handles pasted text (Esc+Enter to submit) |
| **Web + API** | Mobile UI + REST endpoints |
| **Auto-Fallback** | Keyword-based when API unavailable |
| **90%+ Test Coverage** | Comprehensive unit/integration tests |

---

## 💻 Usage

**CLI:**
```bash
python cli.py                                    # Interactive mode
python cli.py -m "I disagree" -l ultra_polite   # With politeness level
echo "No thanks" | python cli.py --stdin        # Pipe input
python cli.py -m "Not interested" -q            # Quiet mode (text only)
```

**Python API:**
```python
result = translator.translate(
    "Your proposal is inefficient.",
    level="business",
    context="business"
)
print(result["tatemae_text"])
print(f"Intent: {result['intent']} ({result['confidence']:.0%})")
```

**Politeness Levels:**
- `business`: Standard business keigo (default)
- `ultra_polite`: Heavy honorifics (formal, senior stakeholders)
- `casual`: Light polite (internal teams)

---

## 🌐 Deploy

| Platform | Difficulty | Free Tier | Guide |
|----------|-----------|-----------|-------|
| Railway | ⭐ Easiest | ✅ Yes | Push to GitHub → Connect → Deploy |
| Fly.io | ⭐⭐ Easy | ✅ 3 VMs | `fly launch && fly deploy` |
| Vercel | ⭐ Easiest | ✅ Generous | Import from GitHub |
| Docker | ⭐⭐ Moderate | Self-host | `docker build && docker run` |

**Complete Guide**: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

## 📖 Documentation

| Topic | Link |
|-------|------|
| 📚 Complete Index | [docs/INDEX.md](docs/INDEX.md) |
| 🚀 Quick Start | [docs/QUICKSTART.md](docs/QUICKSTART.md) |
| 📱 Web App | [docs/QUICKSTART_WEB.md](docs/QUICKSTART_WEB.md) |
| 💻 CLI Usage | [docs/USAGE.md](docs/USAGE.md) |
| 🎌 Kyoto-Style | [docs/KYOTO_STYLE.md](docs/KYOTO_STYLE.md) |
| 🌐 Deployment | [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) |
| 🧪 Testing | [docs/TESTING.md](docs/TESTING.md) |
| 🔒 Security | [docs/SECURITY.md](docs/SECURITY.md) |
| 📝 Changelog | [docs/CHANGELOG.md](docs/CHANGELOG.md) |

---

## 🏗️ Architecture

```
Input → Language Detection → Intent Detection → Template Generation → Politeness Tuning → Output
```

**Tech Stack:**
- LangGraph (workflow orchestration)
- DeepSeek API (LLM with keyword fallback)
- FastAPI (web + REST API)
- pytest (90%+ coverage)

**Project Structure:**
```
winwin/
├── config/       # Templates & settings
├── processing/   # Workflow nodes
├── providers/    # LLM abstraction
├── web/          # FastAPI app
├── docs/         # Documentation
└── tests/        # Test suite
```

Full details: [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)

---

## 🧪 Testing

```bash
pytest                           # Run all tests
pytest --cov                     # With coverage
pytest tests/test_translator.py  # Specific test
```

---

## 🤝 Contributing

Contributions welcome! Check:
1. [docs/IMPROVEMENTS.md](docs/IMPROVEMENTS.md) - Roadmap
2. [docs/TESTING.md](docs/TESTING.md) - Testing requirements
3. [GitHub Issues](https://github.com/yourusername/winwin/issues)

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/winwin/issues)
- **Security**: [docs/SECURITY.md](docs/SECURITY.md)
- **Docs**: [docs/INDEX.md](docs/INDEX.md)

---

**Built with**: DeepSeek • LangGraph • FastAPI • Python 3.12+
**Version**: 3.0.0 - [Changelog](docs/CHANGELOG.md)
