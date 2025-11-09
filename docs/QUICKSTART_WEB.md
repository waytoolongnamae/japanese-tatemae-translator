# Quick Start: Web App

The easiest way to use and share the Japanese Hedging Translator.

## 🚀 Run Locally (1 Minute)

```bash
# 1. Navigate to web directory
cd web

# 2. Copy environment file
cp .env.example .env
# Add your DEEPSEEK_API_KEY_CHAT to .env (or skip for keyword-based fallback)

# 3. Install dependencies
pip install -r requirements-web.txt

# 4. Start the server
python app.py
```

Open [http://localhost:8000](http://localhost:8000) 🎉

## 📱 Using the App

1. **Type your direct message** (e.g., "I'm not interested")
2. **Choose politeness level** (Casual, Business, Ultra Polite)
3. **Click "Translate to 建前"**
4. **Copy or share** the translation!

## 🌐 Deploy for Public Access

Want to share this with others? See **[DEPLOYMENT.md](DEPLOYMENT.md)** for complete deployment instructions on:

- **Railway** (easiest, free tier)
- **Fly.io** (best free tier, global CDN)
- **Vercel** (simple, generous free tier)
- **Heroku, DigitalOcean, AWS, GCP** (production options)
- **Docker** (self-hosted)

Quick deploy commands available for each platform!

## 🎨 Features

- ✅ **Mobile-optimized**: Perfect for phones and tablets
- ✅ **PWA**: Install as an app on any device
- ✅ **Share**: One-tap sharing to any app
- ✅ **Copy**: Quick clipboard copy
- ✅ **Examples**: Pre-loaded examples to try
- ✅ **Fast**: Instant UI, ~2s translations
- ✅ **Offline-ready**: Service worker caching

## 🔧 Customization

### Change Port

```bash
PORT=3000 python app.py
```

### Add Custom Examples

Edit [web/app.py](web/app.py) - look for the `get_examples()` function.

### Customize Colors

Edit [web/static/style.css](web/static/style.css) - see `:root` variables.

### Add App Icon

Replace `web/static/icon.png` with your icon (PNG, 512x512px recommended).

## 📊 API Usage

Your deployed app includes a REST API:

```bash
# Translate
curl -X POST https://your-app.vercel.app/api/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I disagree with that",
    "level": "business"
  }'

# Get examples
curl https://your-app.vercel.app/api/examples
```

Full API docs at: `https://your-app.vercel.app/docs`

## 🐛 Troubleshooting

### Port already in use
```bash
# Change port
PORT=8001 python app.py
```

### Dependencies fail to install
```bash
# Upgrade pip
pip install --upgrade pip

# Retry
pip install -r requirements-web.txt
```

### API key not working
- Check `.env` file exists in `web/` directory
- Verify key starts with `DEEPSEEK_API_KEY_CHAT=`
- No quotes needed around the key
- Restart the server after changing `.env`

### Translation fails
The app has automatic fallback to keyword-based detection if the API fails. Check:
- API key is correct
- You have API credits
- Network connection is working

## 🎯 Next Steps

- Share your deployed URL with colleagues!
- Add app to home screen (iOS: Share → Add to Home Screen)
- Check full docs: [web/README.md](web/README.md)

## 💡 Tips

- **Mobile**: Best experience on phones - optimized for one-handed use
- **Sharing**: Use the native share dialog to send to any app
- **Examples**: Click any example card to auto-fill the input
- **Keyboard**: Press Enter to translate (Shift+Enter for newline)

Enjoy! 🎌
