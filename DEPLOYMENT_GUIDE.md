# Deployment Guide - 建前 Translator

This guide covers multiple deployment options for making the Japanese Hedging Translator publicly accessible.

## Quick Comparison

| Platform | Cost | Difficulty | Best For |
|----------|------|------------|----------|
| **Railway** | Free tier available | ⭐ Easiest | Quick deployment, low traffic |
| **Fly.io** | Free tier (3 VMs) | ⭐⭐ Easy | Production apps, global CDN |
| **Render** | Free tier available | ⭐ Easiest | Simple static + backend |
| **DigitalOcean App Platform** | $5/month | ⭐⭐ Moderate | Scalable production |
| **AWS/GCP/Azure** | Pay-as-you-go | ⭐⭐⭐ Complex | Enterprise, full control |

---

## Option 1: Railway (Recommended - Easiest)

Railway offers the simplest deployment with automatic Docker builds and free tier.

### Steps:

1. **Prepare your repository**
   ```bash
   # Ensure your code is committed
   git add .
   git commit -m "Ready for deployment"
   ```

2. **Sign up at Railway**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

3. **Deploy**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will automatically detect the Dockerfile

4. **Configure Environment Variables**
   - In Railway dashboard, go to "Variables"
   - Add: `DEEPSEEK_API_KEY_CHAT=your_key_here`

5. **Set Custom Domain (Optional)**
   - Railway provides a `.railway.app` domain automatically
   - Or add your custom domain in Settings → Domains

### Railway Configuration

Railway auto-detects the Dockerfile, but you can customize with `railway.json`:

```json
{
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "web/Dockerfile"
  },
  "deploy": {
    "startCommand": "cd web && uvicorn app:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

**Estimated Cost:** Free for hobby projects (500 hours/month)

---

## Option 2: Fly.io

Fly.io offers excellent global CDN and free tier with 3 shared VMs.

### Steps:

1. **Install flyctl**
   ```bash
   # macOS
   brew install flyctl

   # Or use install script
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login**
   ```bash
   flyctl auth login
   ```

3. **Create fly.toml**

   Create `/Users/chouheisei/Repos/winwin/fly.toml`:

   ```toml
   app = "tatemae-translator"  # Change to your preferred name
   primary_region = "nrt"  # Tokyo region (or "sjc" for San Jose)

   [build]
     dockerfile = "web/Dockerfile"

   [env]
     PORT = "8080"

   [http_service]
     internal_port = 8080
     force_https = true
     auto_stop_machines = true
     auto_start_machines = true
     min_machines_running = 0

   [[vm]]
     cpu_kind = "shared"
     cpus = 1
     memory_mb = 256
   ```

4. **Set Secrets**
   ```bash
   flyctl secrets set DEEPSEEK_API_KEY_CHAT=your_key_here
   ```

5. **Deploy**
   ```bash
   flyctl launch
   flyctl deploy
   ```

6. **Access your app**
   ```bash
   flyctl open
   ```

**Estimated Cost:** Free for 3 shared VMs (perfect for this app)

---

## Option 3: Render

Render provides simple deployment with free tier for web services.

### Steps:

1. **Sign up at Render**
   - Go to [render.com](https://render.com)
   - Connect your GitHub account

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your repository
   - Configure:
     - **Name:** tatemae-translator
     - **Region:** Choose closest to your users
     - **Branch:** main
     - **Root Directory:** `web`
     - **Runtime:** Python
     - **Build Command:** `pip install -r requirements-web.txt`
     - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`

3. **Add Environment Variable**
   - In dashboard, go to "Environment"
   - Add: `DEEPSEEK_API_KEY_CHAT`

4. **Deploy**
   - Render automatically deploys on git push

**Estimated Cost:** Free tier available (with sleep after 15 min inactivity)

---

## Option 4: DigitalOcean App Platform

For more serious production deployments with better uptime guarantees.

### Steps:

1. **Sign up at DigitalOcean**
   - Go to [digitalocean.com](https://www.digitalocean.com/products/app-platform)

2. **Create App**
   - Click "Create" → "Apps"
   - Connect GitHub repository
   - Choose branch: `main`

3. **Configure**
   ```yaml
   name: tatemae-translator
   services:
   - name: web
     dockerfile_path: web/Dockerfile
     github:
       repo: your-username/winwin
       branch: main
     http_port: 8000
     instance_count: 1
     instance_size_slug: basic-xxs
     routes:
     - path: /
     envs:
     - key: DEEPSEEK_API_KEY_CHAT
       scope: RUN_TIME
       type: SECRET
   ```

4. **Deploy**
   - DigitalOcean builds and deploys automatically

**Estimated Cost:** Starting at $5/month for basic tier

---

## Option 5: Self-Hosted (VPS)

For complete control, deploy on your own VPS (Ubuntu example).

### Prerequisites:
- A VPS (DigitalOcean Droplet, AWS EC2, Linode, etc.)
- Domain name (optional)

### Steps:

1. **SSH into your server**
   ```bash
   ssh root@your-server-ip
   ```

2. **Install dependencies**
   ```bash
   # Update system
   apt update && apt upgrade -y

   # Install Python and pip
   apt install python3 python3-pip nginx certbot python3-certbot-nginx -y

   # Install Docker (optional, for containerized deployment)
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   ```

3. **Clone repository**
   ```bash
   cd /opt
   git clone https://github.com/your-username/winwin.git
   cd winwin/web
   ```

4. **Create systemd service**

   Create `/etc/systemd/system/tatemae.service`:

   ```ini
   [Unit]
   Description=Tatemae Translator Web App
   After=network.target

   [Service]
   Type=simple
   User=www-data
   WorkingDirectory=/opt/winwin/web
   Environment="DEEPSEEK_API_KEY_CHAT=your_key_here"
   ExecStart=/usr/bin/python3 -m uvicorn app:app --host 0.0.0.0 --port 8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

5. **Start service**
   ```bash
   systemctl daemon-reload
   systemctl enable tatemae
   systemctl start tatemae
   ```

6. **Configure Nginx reverse proxy**

   Create `/etc/nginx/sites-available/tatemae`:

   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

7. **Enable site and SSL**
   ```bash
   ln -s /etc/nginx/sites-available/tatemae /etc/nginx/sites-enabled/
   nginx -t
   systemctl restart nginx

   # Get SSL certificate
   certbot --nginx -d your-domain.com
   ```

**Estimated Cost:** $5-10/month for VPS

---

## Environment Variables

All deployment methods require this environment variable:

```bash
DEEPSEEK_API_KEY_CHAT=your_deepseek_api_key_here
```

**Get your API key:**
1. Go to [DeepSeek Platform](https://platform.deepseek.com)
2. Sign up/login
3. Navigate to API Keys
4. Create new key

---

## Post-Deployment Checklist

- [ ] Test the web app at your deployed URL
- [ ] Verify API endpoint: `curl https://your-url.com/api/translate -X POST -H "Content-Type: application/json" -d '{"text":"test","level":"business"}'`
- [ ] Check logs for any errors
- [ ] Test on mobile devices
- [ ] Set up monitoring (optional): [UptimeRobot](https://uptimerobot.com)
- [ ] Add custom domain (if desired)
- [ ] Enable HTTPS (most platforms do this automatically)

---

## Monitoring & Maintenance

### Health Check Endpoint
The app includes a health check at `/`:
```bash
curl https://your-url.com/
```

### View Logs

**Railway:** Dashboard → Logs tab
**Fly.io:** `flyctl logs`
**Render:** Dashboard → Logs tab
**Self-hosted:** `journalctl -u tatemae -f`

### Update Deployment

Most platforms auto-deploy on `git push`:
```bash
git add .
git commit -m "Update"
git push origin main
```

---

## Troubleshooting

### Issue: "Failed to fetch" error
**Solution:** Ensure the backend is running and API_KEY is set correctly

### Issue: 502 Bad Gateway
**Solution:** Check if the app is listening on the correct port (usually `$PORT` environment variable)

### Issue: High API costs
**Solution:** Implement rate limiting (see below)

### Adding Rate Limiting

Add to `web/app.py`:
```python
from fastapi import Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/translate")
@limiter.limit("10/minute")  # 10 requests per minute per IP
async def translate(request: Request, req: TranslateRequest):
    # existing code
```

---

## Recommended Setup for Public Access

**For beginners:** Railway (easiest setup, free tier)
**For serious projects:** Fly.io (better performance, still free)
**For production:** DigitalOcean App Platform (reliable, scalable)
**For full control:** Self-hosted VPS (most flexible, requires maintenance)

All options work well for this app. Choose based on your comfort level and budget!
