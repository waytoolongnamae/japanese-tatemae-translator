# Project Structure

Clean, organized structure for the Japanese Hedging Translator (建前 Translator).

## Directory Overview

```
winwin/
├── 📄 Core Files (Root)
├── 📁 config/          # Configuration and settings
├── 📁 models/          # Data models and state definitions
├── 📁 processing/      # LangGraph workflow processing
├── 📁 providers/       # LLM provider abstractions
├── 📁 tests/           # Test suite
├── 📁 web/             # Web application
└── 📁 docs/            # Documentation
```

## 📄 Root Directory Files

### Essential Files
```
├── translator.py       # Main API - Public interface for translations
├── cli.py             # Command-line interface
├── main.py            # Example runner (demo script)
├── tatemae            # CLI wrapper script (chmod +x)
├── requirements.txt   # Python dependencies
├── pytest.ini         # Pytest configuration
├── .env.example       # Environment variables template
└── .gitignore         # Git ignore rules
```

### Documentation
```
├── README.md          # Main project documentation
├── LICENSE            # MIT License
└── QUICKSTART_WEB.md  # Web app quick start guide
```

### Configuration Files (Hidden)
```
├── .env               # Environment variables (gitignored)
├── .claude/           # Claude Code settings (gitignored)
├── .mcp.json          # MCP configuration (gitignored)
└── .vscode/           # VSCode settings (gitignored)
```

## 📁 Core Application Structure

### 1. `config/` - Configuration and Settings
```
config/
├── __init__.py        # Package initialization
└── settings.py        # All configuration settings
    ├── API configuration (DeepSeek)
    ├── Intent categories
    ├── Politeness levels
    ├── Template database
    ├── Softening phrases
    └── Honorific modifiers
```

**Purpose**: Centralized configuration management.

### 2. `models/` - Data Models
```
models/
├── __init__.py        # Package initialization
└── state.py           # TranslationState TypedDict
```

**Purpose**: Type definitions for state management in LangGraph workflow.

### 3. `processing/` - Workflow Logic
```
processing/
├── __init__.py        # Package initialization
├── nodes.py           # Workflow nodes (functions)
│   ├── language_detector_node()
│   ├── intent_detector_node()
│   ├── tatemae_generator_node()
│   └── politeness_tuner_node()
└── graph.py           # LangGraph workflow builder
```

**Purpose**: Core translation workflow using LangGraph.

### 4. `providers/` - LLM Abstractions
```
providers/
├── __init__.py        # Package initialization and exports
├── base.py            # LLMProvider abstract base class
├── deepseek.py        # DeepSeek API implementation
└── fallback.py        # Keyword-based fallback provider
```

**Purpose**: Pluggable LLM provider system with automatic fallback.

### 5. `tests/` - Test Suite
```
tests/
├── __init__.py        # Package initialization
├── conftest.py        # Pytest fixtures and mocks
├── test_translator.py # Translator API tests
├── test_nodes.py      # Workflow node tests
├── test_integration.py # End-to-end workflow tests
└── test_edge_cases.py # Edge cases and error handling
```

**Purpose**: Comprehensive test coverage (90%+) with mocked providers.

### 6. `web/` - Web Application
```
web/
├── 📄 Backend
│   ├── app.py              # FastAPI application
│   ├── requirements-web.txt # Web dependencies
│   └── .env                 # Web environment config
├── 📁 templates/
│   └── index.html          # Main HTML template
├── 📁 static/
│   ├── style.css           # Mobile-first styles
│   ├── app.js              # Interactive JavaScript
│   ├── sw.js               # Service worker (PWA)
│   └── manifest.json       # PWA manifest
├── 📄 Deployment
│   ├── Dockerfile          # Docker containerization
│   ├── Procfile           # Heroku/Railway config
│   ├── runtime.txt        # Python version
│   └── run.sh             # Quick start script
└── 📄 Documentation
    ├── README.md          # Web app guide
    └── DEPLOYMENT.md      # Deployment for 8+ platforms
```

**Purpose**: Mobile-friendly web interface with REST API.

### 7. `docs/` - Documentation
```
docs/
├── INDEX.md           # Complete documentation index
├── QUICKSTART.md      # Quick start guide
├── USAGE.md           # Detailed CLI usage
├── KYOTO_STYLE.md     # Cultural communication guide
├── TESTING.md         # Testing guide
├── SECURITY.md        # Security best practices
├── CHANGELOG.md       # Version history
└── IMPROVEMENTS.md    # Future enhancements
```

**Purpose**: Comprehensive documentation for all use cases.

## 🔄 Data Flow

### Translation Pipeline

```
Input Text
    ↓
┌─────────────────────┐
│ Language Detector   │ (processing/nodes.py)
└─────────────────────┘
    ↓
┌─────────────────────┐
│ Intent Detector     │ (providers/deepseek.py or fallback.py)
└─────────────────────┘
    ↓
┌─────────────────────┐
│ Tatemae Generator   │ (config/settings.py templates)
└─────────────────────┘
    ↓
┌─────────────────────┐
│ Politeness Tuner    │ (providers/deepseek.py)
└─────────────────────┘
    ↓
Output (建前 Text)
```

### Component Interactions

```
┌──────────────┐
│  translator  │ (Main API)
│  .py         │
└──────┬───────┘
       │
       ├──> processing/graph.py (Workflow Builder)
       │     └──> processing/nodes.py (Workflow Steps)
       │           ├──> providers/ (LLM Calls)
       │           │    ├──> deepseek.py
       │           │    └──> fallback.py
       │           └──> config/settings.py (Templates)
       │
       └──> models/state.py (Type Definitions)
```

## 📦 Entry Points

### For Users

1. **Web App**: `web/app.py`
   ```bash
   cd web && python app.py
   ```

2. **CLI**: `cli.py`
   ```bash
   python cli.py
   ```

3. **Python API**: `translator.py`
   ```python
   from translator import JapaneseTatemaeTranslator
   ```

### For Developers

1. **Run Tests**: `pytest`
2. **Run Coverage**: `pytest --cov`
3. **Run Demo**: `python main.py`

## 🗂️ File Categories

### Source Code (`.py`)
- `translator.py` - Main API
- `cli.py` - CLI interface
- `main.py` - Demo script
- `config/settings.py` - Configuration
- `models/state.py` - Type definitions
- `processing/*.py` - Workflow logic
- `providers/*.py` - LLM providers
- `tests/*.py` - Test suite
- `web/app.py` - Web server

### Configuration (`.ini`, `.txt`, `.json`)
- `pytest.ini` - Test configuration
- `requirements.txt` - Dependencies
- `.env.example` - Environment template
- `web/manifest.json` - PWA config

### Documentation (`.md`)
- Root: `README.md`, `QUICKSTART_WEB.md`, `LICENSE`
- `docs/*.md` - All documentation files
- `web/README.md`, `web/DEPLOYMENT.md` - Web docs

### Web Assets (`.html`, `.css`, `.js`)
- `web/templates/*.html` - HTML templates
- `web/static/*.css` - Stylesheets
- `web/static/*.js` - JavaScript

### Deployment (Various)
- `web/Dockerfile` - Docker config
- `web/Procfile` - Platform config
- `web/runtime.txt` - Python version
- `web/run.sh` - Start script
- `tatemae` - CLI wrapper

## 🚫 Ignored Files (`.gitignore`)

### Always Ignored
- `__pycache__/` - Python bytecode cache
- `*.pyc`, `*.pyo`, `*.pyd` - Compiled Python
- `.env` - Environment variables (keep `.env.example`)
- `.coverage`, `htmlcov/` - Test coverage reports
- `.pytest_cache/` - Pytest cache
- `logs/` - Log files
- `.DS_Store` - macOS files
- `.vscode/`, `.idea/` - IDE settings
- `.claude/`, `.mcp.json` - Tool configs

### Generated Files
- `build/`, `dist/`, `*.egg-info/` - Build artifacts
- `env/`, `venv/`, `ENV/` - Virtual environments

## 📝 Maintenance Guidelines

### Adding New Features

1. **Configuration**: Add to `config/settings.py`
2. **Processing Logic**: Add nodes to `processing/nodes.py`
3. **Workflow Changes**: Update `processing/graph.py`
4. **New Provider**: Create in `providers/`, extend `base.py`
5. **Tests**: Add to appropriate test file in `tests/`
6. **Documentation**: Update relevant docs in `docs/`

### Before Committing

1. **Clean Cache**: Remove `__pycache__/` directories
2. **Run Tests**: `pytest`
3. **Check Coverage**: `pytest --cov`
4. **Update Docs**: If API or behavior changed
5. **Update CHANGELOG**: Add entry to `docs/CHANGELOG.md`

### Project Health Checklist

- [ ] No `__pycache__/` directories committed
- [ ] No `.pyc` files committed
- [ ] `.env` not committed (only `.env.example`)
- [ ] Tests passing (`pytest`)
- [ ] Coverage above 90% (`pytest --cov`)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated

## 🎯 Design Principles

1. **Separation of Concerns**
   - Configuration: `config/`
   - Models: `models/`
   - Logic: `processing/`
   - Providers: `providers/`
   - Tests: `tests/`

2. **Single Responsibility**
   - Each module has one clear purpose
   - Files are focused and maintainable

3. **DRY (Don't Repeat Yourself)**
   - Configuration centralized in `config/settings.py`
   - Provider abstraction in `providers/base.py`
   - Shared fixtures in `tests/conftest.py`

4. **Extensibility**
   - Easy to add new providers
   - Easy to add new workflow nodes
   - Easy to add new templates

5. **Testability**
   - All components have unit tests
   - Integration tests cover workflows
   - Mocked providers avoid API calls

## 📊 Metrics

### Code Organization
- **Total Python Files**: 15 source + 4 tests
- **Lines of Code**: ~1500 (excluding tests, docs)
- **Test Coverage**: 90%+
- **Documentation Files**: 12 markdown files

### Structure Cleanliness
- ✅ No circular dependencies
- ✅ Clear import hierarchy
- ✅ Logical grouping
- ✅ Minimal root clutter

---

**Last Updated**: 2025-11-08 (v3.0.0)

**See Also**: [README.md](../README.md) | [INDEX.md](INDEX.md)
