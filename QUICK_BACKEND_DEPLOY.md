# 🚀 Quick Backend Deployment - 5 Minutes

## The Problem
✅ Frontend (Streamlit) is deployed  
❌ Backend (FastAPI) is not running

## The Solution

### **Step 1: Deploy Backend to Render (FREE)**

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect GitHub repo: `parthmanekar25/ai-hiring-agent`

### **Step 2: Configure**

```
Name: ai-hiring-agent-backend
Environment: Python 3
Region: (Choose closest to you)
Build Command: pip install -r requirements.txt
Start Command: uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### **Step 3: Add Environment Variable**

```
GROQ_API_KEY = your-actual-key-from-console.groq.com
```

### **Step 4: Deploy & Get URL**

- Click "Create Web Service"
- Wait 2-5 minutes
- Copy the URL (e.g., `https://ai-hiring-agent-backend-xxx.onrender.com`)

### **Step 5: Update Streamlit Secrets**

Go to your Streamlit app:
1. Click ⚙️ (settings)
2. Click "Secrets"
3. Update:
   ```
   BACKEND_URL = "https://ai-hiring-agent-backend-xxx.onrender.com"
   ```
4. Save

### **Step 6: Verify**

Your Streamlit app should now show: ✅ Backend Connected

---

## **Testing Locally First (Optional)**

```bash
# Terminal 1 - Start Backend
cd /Users/parth/Projects/ai-hiring-agent
source .venv/bin/activate
python backend/main.py

# Terminal 2 - Test it's running
curl http://localhost:8000/health
# Should return: {"status": "healthy"}

# Terminal 3 - Start Frontend (if testing locally)
streamlit run frontend/app.py
```

---

## **Common Issues**

| Issue | Fix |
|-------|-----|
| "502 Bad Gateway" | Wait for deployment to finish |
| Backend not responding | Check GROQ_API_KEY in Render env vars |
| "Connection refused" | Verify BACKEND_URL in Streamlit secrets |
| Still shows "❌ Backend Offline" | Clear Streamlit cache and refresh |

---

## **Next Steps**

1. ✅ Deploy backend to Render
2. ✅ Get the backend URL
3. ✅ Update Streamlit secrets with BACKEND_URL
4. ✅ Refresh Streamlit app
5. ✅ You're done! 🎉

---

**Need detailed help?** See `BACKEND_DEPLOYMENT.md` for complete instructions.

