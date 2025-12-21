# Operations Runbook

## Service Overview
- **Service**: Japanese Hedging Translator
- **Interfaces**: CLI (`cli.py`) and Web API (`web/app.py`)
- **Health**: `GET /health`

## Required Configuration
- Copy `.env.example` to `.env`
- Set at least one provider API key:
  - `DEEPSEEK_API_KEY_CHAT` or `OPENAI_API_KEY`
- Optional hardening:
  - `ALLOWED_HOSTS` (comma-separated hostnames)
  - `CORS_ALLOWED_ORIGINS` (comma-separated origins)

## Startup
- Web: `uvicorn web.app:app --host 0.0.0.0 --port 8000`
- CLI: `python cli.py -m "message"`

## Health Checks
- **Liveness**: `GET /health`
- **Expected**: `status=healthy`
- **Notes**: `uptime_seconds` should be present after startup

## Logs
- Default to stdout; optional file logs when `LOG_TO_FILE=true`.
- File location controlled by `LOG_DIR` and `LOG_FILE_NAME`.

## Troubleshooting
- **Startup fails**: check `LOG_LEVEL`, provider keys, and `MODEL_PROVIDER`.
- **All translations fallback**: provider key missing or invalid.
- **413 errors**: request exceeds `MAX_REQUEST_BYTES` or `MAX_INPUT_LENGTH`.

## Deployment Tips
- Run behind a reverse proxy with TLS termination.
- Set `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS` for production.
- Use container health checks or external probes hitting `/health`.
