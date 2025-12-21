# Japanese Hedging Translator (建前 Translator)

![CI](https://github.com/waytoolongnamae/japanese-tatemae-translator/actions/workflows/ci.yml/badge.svg?branch=main)
![Coverage](https://img.shields.io/badge/coverage-82%25-brightgreen)

Transform direct messages into polite Japanese business communication with Kyoto-style 建前 (tatemae).

## ⚠️ Disclaimer

This is a satirical, educational project that exaggerates high-context communication styles.
Do not use it for real professional interactions.

## 🚀 Quick Start

### Web App

```bash
cd web
pip install -r requirements-web.txt
python app.py
```

Open http://localhost:8000

### CLI

```bash
cp .env.example .env
python cli.py -m "I'm not interested in this job."
```

### Python API

```python
from translator import JapaneseTatemaeTranslator

translator = JapaneseTatemaeTranslator()
result = translator.translate("I disagree", level="business", fidelity="medium")
print(result["tatemae_text"])
```

## ✨ Features

- Two-dimensional control: politeness + fidelity
- Kyoto-style indirectness with context preservation
- Intent detection across common categories
- Web UI + REST API + CLI
- Multiple providers with automatic fallback

## 📖 Docs & Links

- Full docs index: docs/INDEX.md
- Deployment: docs/DEPLOYMENT.md
- Web app setup: docs/QUICKSTART_WEB.md
- CLI usage: docs/USAGE.md
- Kyoto-style guide: docs/KYOTO_STYLE.md

## ✅ Tests

```bash
pytest
```
