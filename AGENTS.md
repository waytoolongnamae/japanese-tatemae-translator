# Repository Guidelines

## Project Structure & Module Organization
- Core logic lives at the repo root (`translator.py`, `cli.py`, `main.py`, `tatemae`).
- `config/` holds settings and templates, `models/` defines state, `processing/` contains LangGraph workflow nodes, and `providers/` implements LLM backends.
- `tests/` contains pytest suites; `docs/` holds longer-form guides.
- `web/` is the FastAPI web app with `templates/` and `static/` assets.

## Build, Test, and Development Commands
- Install dependencies (CLI/API): `uv venv && source .venv/bin/activate && uv pip install -r requirements.txt` or `pip install -r requirements.txt`.
- Run CLI: `python cli.py` (interactive) or `python cli.py -m "message" -l ultra_polite -f high`.
- Run web app: `cd web && pip install -r requirements-web.txt && python app.py` (uses root `.env`).
- Run tests: `pytest` or `pytest --cov`; example: `pytest tests/test_translator.py -v`.

## Coding Style & Naming Conventions
- Python uses 4-space indentation and conventional naming: `snake_case` for functions/modules, `CapWords` for classes.
- Tests follow pytest discovery: files `test_*.py`, classes `Test*`, functions `test_*`.
- No formatter/linter is enforced; keep edits consistent with surrounding code.

## Testing Guidelines
- Framework: pytest with coverage enforcement in `pytest.ini` (`--cov-fail-under=80`).
- Coverage reports: `htmlcov/` for HTML output.
- Tests rely on mocked providers, so API keys are not required for test runs.

## Commit & Pull Request Guidelines
- Commit subjects are short, imperative, and capitalized (e.g., “Add fidelity dimension support”, “Fix copy button”).
- PRs should include a concise summary and the tests run. Add screenshots or GIFs for UI changes and link related issues when applicable.

## Configuration & Security Tips
- Copy `.env.example` to `.env` and set `DEEPSEEK_API_KEY_CHAT`; keep secrets out of git.
- The web app reads the root `.env` (not `web/.env`).
- For security reporting guidance, see `docs/SECURITY.md`.
