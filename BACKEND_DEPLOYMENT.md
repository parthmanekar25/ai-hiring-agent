# Render.com Deployment Guide for AI Hiring Agent Backend

## Step-by-Step Deployment to Render

### Prerequisites
- Render account: https://render.com (sign up free)
- GitHub account with the repository
- Groq API key

### Step 1: Create a Render Account
1. Go to https://render.com
2. Sign up with GitHub
3. Authorize the connection

### Step 2: Create a New Web Service
1. Click "New +" button
2. Select "Web Service"
3. Click "Connect a repository"
4. Find and select `parthmanekar25/ai-hiring-agent`
5. Click "Connect"

### Step 3: Configure the Service

**Basic Settings:**
- **Name:** `ai-hiring-agent-backend` (or your preferred name)
- **Environment:** Python 3
- **Region:** Choose closest to your users
- **Branch:** main

**Build & Deploy:**
- **Root Directory:** (leave empty)
- **Build Command:** 
  ```
  pip install -r requirements.txt
  ```
- **Start Command:**
  ```
  uvicorn backend.main:app --host 0.0.0.0 --port 8000
  ```

### Step 4: Add Environment Variables
In the "Environment" section, add:

| Key | Value |
|-----|-------|
| `GROQ_API_KEY` | your-actual-groq-api-key |
| `PORT` | 8000 |
| `PYTHONUNBUFFERED` | 1 |

### Step 5: Deploy
- Click "Create Web Service"
- Wait for deployment (usually 2-5 minutes)
- Get the URL (e.g., `https://ai-hiring-agent-backend.onrender.com`)

### Step 6: Update Streamlit Frontend
1. Go to your Streamlit app settings
2. Click the settings icon (⚙️)
3. Go to "Secrets"
4. Update `BACKEND_URL`:
   ```
   BACKEND_URL = "https://ai-hiring-agent-backend.onrender.com"
   ```
5. Save - the app will auto-restart

---

## **Option 2: Deploy Backend Locally (For Testing)**

If you want to test locally first:

```bash
# Terminal 1: Start Backend
cd /Users/parth/Projects/ai-hiring-agent
source .venv/bin/activate
python backend/main.py

# Terminal 2: Check if it's running
curl http://localhost:8000/health
```

Output should be:
```json
{"status": "healthy"}
```

---

## **Option 3: Alternative Cloud Platforms**

### Railway.app (Also Free)
1. Go to https://railway.app
2. Click "New Project"
3. Click "Deploy from GitHub"
4. Select repository
5. Add same environment variables
6. Deploy

### AWS/Azure/GCP
More complex but highly scalable options.

---

## **Verify Deployment**

Once deployed, test the backend URL:

```bash
curl https://your-backend-url.com/health
```

Should return:
```json
{"status": "healthy"}
```

---

## **Troubleshooting**

### Backend won't start
- Check logs in Render dashboard
- Verify `GROQ_API_KEY` is set
- Check Python version compatibility

### Streamlit can't connect to backend
- Verify `BACKEND_URL` in secrets is correct
- Add `/health` endpoint test
- Check CORS settings in backend

### Slow response times
- Might need paid tier on Render (free tier is slower)
- Consider Railway or AWS for better performance

---

## **Costs**

| Platform | Free Tier | Cost |
|----------|-----------|------|
| Render | Yes (limited) | $7/month for paid |
| Railway | Yes (limited) | Pay-as-you-go |
| Streamlit Cloud | Yes | Free |

---

## **Quick Links**

- Render: https://render.com
- Railway: https://railway.app
- Groq Console: https://console.groq.com
- Streamlit Cloud: https://share.streamlit.io

