# Deployment Guide

Quick reference for deploying the 建前 Translator web app.

## Prerequisites

- Python 3.12+
- DeepSeek API key (optional but recommended)
- Git repository

## Local Development

```bash
cd web
cp .env.example .env
# Edit .env and add your DEEPSEEK_API_KEY_CHAT
pip install -r requirements-web.txt
python app.py
```

Visit: http://localhost:8000

## Deployment Options

### 1. Vercel (Recommended - Easiest)

**Best for:** Static sites with serverless functions

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd web
vercel

# Set environment variable in dashboard
# DEEPSEEK_API_KEY_CHAT=your_key
```

**Or use GitHub integration:**
1. Push to GitHub
2. Import at [vercel.com/new](https://vercel.com/new)
3. Set environment variable
4. Deploy!

### 2. Railway

**Best for:** Simple deployment with database support

1. Visit [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Select your repository
4. Add environment variable: `DEEPSEEK_API_KEY_CHAT`
5. Railway will auto-detect and deploy

**CLI:**
```bash
npm i -g @railway/cli
railway login
railway init
railway add
railway up
```

### 3. Fly.io

**Best for:** Edge deployment, multiple regions

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Deploy
cd web
fly launch
fly secrets set DEEPSEEK_API_KEY_CHAT=your_key
fly deploy
```

**Configuration (fly.toml):**
```toml
app = "your-app-name"

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8000"

[[services]]
  http_checks = []
  internal_port = 8000
  protocol = "tcp"

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

### 4. Heroku

**Best for:** Traditional PaaS deployment

```bash
# Login
heroku login

# Create app
heroku create your-app-name

# Set environment
heroku config:set DEEPSEEK_API_KEY_CHAT=your_key

# Deploy
git push heroku main
```

**Required files (already included):**
- `Procfile`
- `runtime.txt`
- `requirements-web.txt`

### 5. Google Cloud Run

**Best for:** Containerized deployment, Google Cloud ecosystem

```bash
# Build image
docker build -t gcr.io/YOUR_PROJECT/tatemae-web .

# Push to registry
docker push gcr.io/YOUR_PROJECT/tatemae-web

# Deploy
gcloud run deploy tatemae-web \
  --image gcr.io/YOUR_PROJECT/tatemae-web \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DEEPSEEK_API_KEY_CHAT=your_key
```

### 6. AWS (Elastic Beanstalk)

**Best for:** AWS ecosystem integration

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.12 tatemae-web

# Create environment
eb create tatemae-web-env

# Set environment variable
eb setenv DEEPSEEK_API_KEY_CHAT=your_key

# Deploy
eb deploy
```

### 7. DigitalOcean App Platform

**Best for:** Simple deployment with databases

1. Visit [cloud.digitalocean.com/apps](https://cloud.digitalocean.com/apps)
2. Create App → GitHub
3. Select repository and branch
4. DigitalOcean auto-detects Python
5. Add environment variable
6. Deploy!

**Or use doctl:**
```bash
doctl apps create --spec .do/app.yaml
```

### 8. Docker (Self-hosted)

**Best for:** Own infrastructure, any cloud provider

```bash
# Build
docker build -t tatemae-web .

# Run
docker run -d \
  -p 8000:8000 \
  -e DEEPSEEK_API_KEY_CHAT=your_key \
  --name tatemae \
  tatemae-web

# Or with docker-compose
docker-compose up -d
```

**docker-compose.yml:**
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: unless-stopped
```

## Environment Variables

Required:
- `DEEPSEEK_API_KEY_CHAT` - Your DeepSeek API key

Optional:
- `PORT` - Server port (default: 8000)
- `HOST` - Server host (default: 0.0.0.0)
- `ENVIRONMENT` - Environment name (default: production)

## Custom Domain

### Vercel
1. Go to Project Settings → Domains
2. Add your domain
3. Update DNS records as instructed

### Fly.io
```bash
fly certs add yourdomain.com
fly certs show yourdomain.com
# Update DNS with provided values
```

### Railway
1. Go to Settings → Domains
2. Add custom domain
3. Update DNS records

## SSL/HTTPS

All deployment platforms provide automatic HTTPS via Let's Encrypt.

## Monitoring

### Health Check
All platforms support health checks at: `/health`

### Logs

**Vercel:**
```bash
vercel logs
```

**Railway:**
```bash
railway logs
```

**Fly.io:**
```bash
fly logs
```

**Heroku:**
```bash
heroku logs --tail
```

## Performance Tips

1. **Enable caching:** Service worker is already configured
2. **Use CDN:** Most platforms include CDN automatically
3. **Optimize images:** Replace placeholder icon with optimized PNG
4. **Monitor API usage:** Check DeepSeek API dashboard
5. **Rate limiting:** Consider adding rate limits for public deployments

## Security

1. **Environment variables:** Never commit API keys
2. **HTTPS:** Always use HTTPS in production
3. **CORS:** Configured for all origins by default (adjust in `app.py` if needed)
4. **Input validation:** Already implemented in backend

## Costs

**Free tier options:**
- Vercel: 100GB bandwidth, unlimited requests
- Railway: $5 credit/month (enough for moderate usage)
- Fly.io: 3 shared VMs free
- Heroku: Free tier discontinued (start at $7/month)

**DeepSeek API:**
- Very affordable compared to OpenAI
- Check current pricing at [deepseek.com](https://deepseek.com)

## Troubleshooting

### Build fails
- Check `requirements-web.txt` is present
- Verify Python version in `runtime.txt`
- Check logs for specific errors

### App crashes on startup
- Verify environment variables are set
- Check PORT is correct for platform
- Review application logs

### Translations fail
- Check API key is valid
- Verify network connectivity
- App will fallback to keyword detection if API unavailable

### Slow performance
- Check API response times
- Consider enabling caching
- Use CDN for static assets

## Scaling

Most platforms auto-scale. For manual scaling:

**Fly.io:**
```bash
fly scale count 3
```

**Heroku:**
```bash
heroku ps:scale web=3
```

## Updates

```bash
# Pull latest changes
git pull origin main

# Redeploy (varies by platform)
vercel --prod          # Vercel
railway up             # Railway
fly deploy             # Fly.io
git push heroku main   # Heroku
```

## Support

For platform-specific issues:
- Vercel: [vercel.com/support](https://vercel.com/support)
- Railway: [railway.app/help](https://railway.app/help)
- Fly.io: [fly.io/docs](https://fly.io/docs)

For app issues: See main [README.md](../README.md)
