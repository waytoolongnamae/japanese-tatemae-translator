# 建前 Translator Web App

A simple, mobile-friendly web interface for the Japanese Hedging Translator.

> ⚠️ **Important**: This is an educational and satirical tool. The translations exaggerate communication patterns for learning purposes. Not recommended for real professional or personal use. See the [main README](../README.md) for full disclaimer.

## Features

- 📱 **Mobile-First Design**: Optimized for smartphones and tablets
- ⚡ **Fast & Responsive**: Instant translations with smooth animations
- 📋 **Easy Sharing**: Copy or share translations with one tap
- 🎯 **Simple Interface**: Clean, intuitive design
- 🔄 **PWA Support**: Install as an app on your device
- 💾 **Offline Ready**: Service worker for fast loading

## Quick Start

### Local Development

```bash
# From root directory, configure API key first
cp .env.example .env
# Add your DEEPSEEK_API_KEY_CHAT to .env

# Navigate to web directory
cd web

# Using uv (Recommended - Faster)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements-web.txt

# OR using pip
pip install -r requirements-web.txt

# Run the server (uses root .env file)
python app.py
```

**Note**: The web app uses the `.env` file from the **root directory**, not from `web/.env`. This is because it imports the translator module from the parent directory.

Open [http://localhost:8000](http://localhost:8000) in your browser.

Troubleshooting:
- If you see an "operation not permitted" bind error, try a different port:
  `PORT=8081 HOST=127.0.0.1 python app.py`
- Check local firewall or security software blocking localhost binds.

### Using Docker

```bash
# Build and run
docker build -t tatemae-web .
docker run -p 8000:8000 --env-file .env tatemae-web
```

## Deployment

For detailed deployment instructions to various platforms (Vercel, Railway, Fly.io, Heroku, DigitalOcean, AWS, GCP, Docker, etc.), see the comprehensive **[Deployment Guide](../docs/DEPLOYMENT.md)**.

### Quick Deploy Options

**Railway (Easiest):**
```bash
# Push to GitHub, then:
# 1. Visit railway.app
# 2. Connect GitHub repo
# 3. Add DEEPSEEK_API_KEY_CHAT
# 4. Deploy!
```

**Fly.io (Best Free Tier):**
```bash
curl -L https://fly.io/install.sh | sh
fly auth login
fly launch
fly secrets set DEEPSEEK_API_KEY_CHAT=your_key
fly deploy
```

See [docs/DEPLOYMENT.md](../docs/DEPLOYMENT.md) for complete instructions and more platforms.

## API Endpoints

### `POST /api/translate`

Translate a message to Japanese tatemae.

**Request:**
```json
{
  "text": "I'm not interested in this job.",
  "level": "business",
  "context": "recruiter"
}
```

**Response:**
```json
{
  "tatemae_text": "大変興味深いお話をいただきまして...",
  "intent": "disinterest",
  "confidence": 0.98,
  "detected_language": "en",
  "level": "business",
  "context": "recruiter"
}
```

### `GET /api/examples`

Get example translations.

**Response:**
```json
{
  "examples": [
    {
      "input": "I'm not interested in this job.",
      "intent": "disinterest",
      "description": "Politely declining a job offer"
    }
  ]
}
```

### `GET /health`

Health check endpoint.

## Project Structure

```
web/
├── app.py                 # FastAPI application
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── style.css         # Styles
│   ├── app.js            # JavaScript logic
│   ├── sw.js             # Service worker
│   └── manifest.json     # PWA manifest
├── requirements-web.txt  # Python dependencies
├── Procfile              # Deployment config
├── runtime.txt           # Python version
└── README.md             # This file
```

## Configuration

Edit `.env`:

```bash
# Required
DEEPSEEK_API_KEY_CHAT=your_key_here

# Optional
PORT=8000              # Server port
HOST=0.0.0.0          # Server host
ENVIRONMENT=production # Environment name
```

## Sharing the App

Once deployed, share your app URL:

```
https://your-app.vercel.app
```

Users can:
- Access directly in browser
- Add to home screen (PWA)
- Share translations via native share dialog
- Copy translations to clipboard

## Development

### Adding New Features

1. **Backend**: Edit [app.py](app.py) to add API endpoints
2. **Frontend**: Edit files in `static/` and `templates/`
3. **Styles**: Modify [static/style.css](static/style.css)
4. **Logic**: Update [static/app.js](static/app.js)

### Testing

```bash
# Test the API
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "I disagree", "level": "business"}'

# Check health
curl http://localhost:8000/health
```

## Browser Support

- ✅ Chrome/Edge (latest)
- ✅ Safari (latest)
- ✅ Firefox (latest)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## Performance

- Initial load: < 100ms
- Translation: ~ 1-3s (depends on API)
- Offline: Cached assets load instantly

## License

See parent repository LICENSE file.

## Support

For issues or questions, see the main [README](../README.md).
