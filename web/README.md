# 建前 Translator Web App

A simple, mobile-friendly web interface for the Japanese Hedging Translator.

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
# Navigate to web directory
cd web

# Install dependencies
pip install -r requirements-web.txt

# Create .env file
cp .env.example .env
# Add your DEEPSEEK_API_KEY_CHAT to .env

# Run the server
python app.py
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

### Using Docker

```bash
# Build and run
docker build -t tatemae-web .
docker run -p 8000:8000 --env-file .env tatemae-web
```

## Deployment

### Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/winwin)

1. Fork this repository
2. Sign up at [Vercel](https://vercel.com)
3. Import your forked repository
4. Add environment variable: `DEEPSEEK_API_KEY_CHAT`
5. Deploy!

### Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

1. Click the button above
2. Add environment variable: `DEEPSEEK_API_KEY_CHAT`
3. Deploy!

### Deploy to Fly.io

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Launch app
fly launch

# Set secret
fly secrets set DEEPSEEK_API_KEY_CHAT=your_key_here

# Deploy
fly deploy
```

### Deploy to Heroku

```bash
# Login
heroku login

# Create app
heroku create your-app-name

# Set config
heroku config:set DEEPSEEK_API_KEY_CHAT=your_key_here

# Deploy
git push heroku main
```

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
