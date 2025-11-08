# Changelog

## v3.0.0 - Web App Release (2025-11-08)

### 🌐 Major Features

#### Mobile Web Application
- **FastAPI Backend**: RESTful API with automatic documentation
- **Mobile-First UI**: Responsive design optimized for smartphones
- **PWA Support**: Install as an app, offline-ready with service worker
- **Easy Sharing**: One-tap share to any app, copy to clipboard
- **Simple Deployment**: Ready for Vercel, Railway, Fly.io, Heroku, etc.

#### Key Features
1. **User-Friendly Interface**
   - Clean, minimalist design
   - Interactive politeness level selector
   - Real-time character counter
   - Smooth animations and transitions
   - Example cards to try instantly

2. **REST API**
   - POST `/api/translate` - Translate messages
   - GET `/api/examples` - Get example translations
   - GET `/health` - Health check endpoint
   - Auto-generated Swagger/ReDoc documentation

3. **Easy Deployment**
   - Docker support with Dockerfile
   - Platform configs (Procfile, runtime.txt)
   - One-command deployment scripts
   - Comprehensive deployment guides

### 📱 Web App Structure

```
web/
├── app.py              # FastAPI backend
├── templates/          # HTML templates
│   └── index.html     # Main interface
├── static/            # Frontend assets
│   ├── style.css      # Responsive styles
│   ├── app.js         # Interactive logic
│   ├── sw.js          # Service worker
│   └── manifest.json  # PWA manifest
├── README.md          # Web app documentation
├── DEPLOYMENT.md      # Deployment guides
└── requirements-web.txt
```

### 🚀 Quick Start

```bash
cd web
pip install -r requirements-web.txt
python app.py
# Open http://localhost:8000
```

### 📚 New Documentation

- **[web/README.md](../web/README.md)**: Complete web app guide
- **[web/DEPLOYMENT.md](../web/DEPLOYMENT.md)**: Deployment for 8+ platforms
- **[QUICKSTART_WEB.md](../QUICKSTART_WEB.md)**: Quick start for web app
- Updated main **[README.md](../README.md)** with web app section

### 🔧 Technical Additions

- FastAPI + Uvicorn web server
- Jinja2 templating
- CORS middleware for API access
- Service worker for offline functionality
- PWA manifest for app installation
- Docker containerization
- Multi-platform deployment configs

### 📦 Dependencies Added

```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
jinja2>=3.1.0
pydantic>=2.0.0
```

### 🎯 Use Cases

1. **Personal Use**: Simple web interface for quick translations
2. **Team Sharing**: Deploy once, share URL with team
3. **Mobile Access**: Use on phone via browser or install as app
4. **API Integration**: Embed in other applications via REST API
5. **Learning Tool**: Interactive way to learn Kyoto-style communication

---

## v2.0.0 - Kyoto-Style Update (2025-10-22)

### 🎌 Major Features

#### Kyoto-Style Tatemae (京都風建前)
- **Subtle Sarcasm**: Praise on the surface, criticism underneath
- **Context Preservation**: Each translation maintains specific details from input
- **Varied Outputs**: No more generic "one translation for many" responses
- **Cultural Authenticity**: Based on real Kyoto merchant communication patterns

#### Key Improvements
1. **Context-Aware Translation**
   - Mentions specific subjects (code, design, proposals, people)
   - Preserves original meaning while applying indirectness
   - Different inputs produce unique outputs

2. **Hidden Meanings**
   - "勉強になります" (educational) = useless/wrong
   - "参考にさせていただきます" (will reference) = won't use
   - "さすがですね" (impressive) = terrible
   - "検討させていただきます" (will consider) = not happening

3. **Plausible Deniability**
   - Sarcasm is subtle and cannot be used as evidence
   - Surface meaning is always polite and professional
   - True intent hidden beneath layers of courtesy

### 📝 Examples

**Before (Generic)**:
```
Input: "Your code is terrible"
Output: もう少し検討の余地があるかもしれません。

Input: "Your design is ugly"
Output: もう少し検討の余地があるかもしれません。
```
❌ Same generic response

**After (Context-Aware Kyoto-Style)**:
```
Input: "Your code is terrible"
Output: 誠に興味深いコードのご提案を拝見いたしました。
        大変勉強になるご発想で、さすがお考えがお深いと感服いたしております。

Input: "Your design is ugly"
Output: 誠に素敵なデザインでございますね。大変ユニークなご発想と拝見いたしました。
        私どもの狭い了見では、このような独創的なお考えに至るのは難しく...
```
✅ Each unique, context-specific, with hidden sarcasm

### 🔧 Technical Changes

#### Prompt Engineering
- Completely rewritten system prompt
- Japanese instructions for better LLM understanding
- Explicit Kyoto-style communication principles
- Temperature increased to 0.7 for more variety

#### Processing Pipeline
```
Input → Intent Detection → Template → Kyoto-Style Refinement → Output
                                              ↓
                                    - Preserve context
                                    - Add subtle sarcasm
                                    - Ensure grammar
                                    - Vary expression
```

### 📚 New Documentation

- **[KYOTO_STYLE.md](KYOTO_STYLE.md)**: Comprehensive guide to Kyoto-style communication
- **[IMPROVEMENTS.md](IMPROVEMENTS.md)**: Grammar improvement details
- Updated **[README.md](README.md)** with Kyoto-style examples
- Updated **[USAGE.md](USAGE.md)** with context-aware examples

### 🧪 Testing

All tests pass with new Kyoto-style translations:
```bash
python test_translator.py
# ALL TESTS PASSED! ✓
```

### 💡 Usage

No changes to CLI interface - improvements are automatic:

```bash
# Each produces unique, context-aware output
python cli.py -m "Your code is terrible"
python cli.py -m "Your design is ugly"
python cli.py -m "Your deadline is unrealistic"
```

---

## v1.0.0 - Initial Release

### Features
- Basic intent detection
- Template-based generation
- Three politeness levels
- Grammar refinement
- CLI interface
- Interactive mode
- Python API

### Components
- LangGraph workflow
- DeepSeek API integration
- Keyword-based fallback
- Command-line tool

---

## Comparison: v1.0 vs v2.0

| Aspect | v1.0 | v2.0 |
|--------|------|------|
| **Context** | Generic responses | Specific, context-aware |
| **Variety** | Repetitive | Unique for each input |
| **Style** | Simple polite | Kyoto-style subtle sarcasm |
| **Sarcasm** | None | Hidden beneath politeness |
| **Detail** | Lost specifics | Preserves all details |
| **Temperature** | 0.3 (consistent) | 0.7 (varied) |

## Migration Notes

### From v1.0 to v2.0

**No breaking changes** - all existing code continues to work.

The improvements are in the quality of translations:
- More context-aware
- More varied outputs
- Subtle Kyoto-style sarcasm
- Better preservation of original meaning

Simply update the code and enjoy better translations!

```bash
git pull origin main
# That's it - no code changes needed
```

## Future Roadmap

### Planned Features
- [ ] Language auto-translation (EN/ZH → JA)
- [ ] Fine-tuned intent classification
- [ ] Relationship context (上司/同僚/部下)
- [ ] Industry-specific templates
- [ ] LangGraph Studio visualization
- [ ] Web interface
- [ ] API service

### Under Consideration
- [ ] Reverse translation (建前 → 本音)
- [ ] Sarcasm intensity control
- [ ] Regional style variations (関西弁 etc.)
- [ ] Historical formality levels (古語 etc.)
- [ ] Audio output (TTS integration)

---

**Full documentation**: [README.md](README.md) | [KYOTO_STYLE.md](KYOTO_STYLE.md) | [USAGE.md](USAGE.md)
