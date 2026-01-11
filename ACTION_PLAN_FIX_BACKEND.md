# 📋 ACTION PLAN - Fix "Backend Offline" Issue

## ⏱️ Time Estimate: 10-15 minutes

---

## 🎯 Goal
Make the "✅ Backend Connected" message appear instead of "❌ Backend Offline"

---

## Step-by-Step Action Plan

### **STEP 1: Deploy Backend to Render (5 minutes)**

**What to do:**
1. Open https://render.com in your browser
2. Click "Sign up" → "Continue with GitHub"
3. Authorize access to your GitHub account
4. Click "New +" button (top right)
5. Select "Web Service"
6. Click "Connect a repository"
7. Search for and select: `parthmanekar25/ai-hiring-agent`
8. Click "Connect"

**You should now see a form to fill:**

```
Name:                    ai-hiring-agent-backend
Environment:             Python 3
Region:                  (Select your region)
Branch:                  main
Root Directory:          (leave empty)

Build Command:           pip install -r requirements.txt
Start Command:           uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

9. Scroll down and click "Create Web Service"
10. **Wait for deployment** (2-5 minutes) - you'll see the logs building

**When complete:** You'll get a URL like `https://ai-hiring-agent-backend-xxx.onrender.com`

---

### **STEP 2: Add API Key (2 minutes)**

**Before deployment fully completes:**

1. In Render dashboard, find the "Environment" section
2. Click "Add Environment Variable"
3. Add:
   ```
   Key:   GROQ_API_KEY
   Value: [your-actual-key-from-console.groq.com]
   ```
4. Click "Add"

**Don't have a Groq API key?**
- Go to https://console.groq.com
- Sign up free
- Generate API key
- Copy it

---

### **STEP 3: Get Backend URL (1 minute)**

**After deployment completes:**

1. Look at the top of the Render service page
2. Copy the URL (format: `https://ai-hiring-agent-backend-xxx.onrender.com`)
3. **Keep this copied** - you'll need it next

**Verify it's working:**
```
https://your-backend-url/health
```

Should show: `{"status":"healthy"}`

---

### **STEP 4: Update Streamlit Secrets (2 minutes)**

1. Go to your Streamlit app URL in browser
2. Click the **⚙️ gear icon** in top right
3. Click **"Settings"**
4. Click **"Secrets"** tab
5. You'll see a text area with your current secrets
6. Find or add this line:
   ```
   BACKEND_URL = "https://your-backend-url.onrender.com"
   ```
   (Replace with actual URL from Step 3)
7. Click **"Save"**

**Streamlit will automatically restart your app**

---

### **STEP 5: Verify It Works (2 minutes)**

1. Go back to your Streamlit app
2. Refresh the page
3. Look for the backend status in sidebar
4. Should now show: **✅ Backend Connected**

---

## ✅ Verification Checklist

After completing all steps, check:

- [ ] Render deployment shows "Live"
- [ ] Backend URL is accessible (test `/health`)
- [ ] GROQ_API_KEY is set in Render
- [ ] Streamlit secrets updated with BACKEND_URL
- [ ] Streamlit app refreshed
- [ ] Shows "✅ Backend Connected" in sidebar
- [ ] Can upload resume and evaluate (try sample data)

---

## 🆘 If Something Goes Wrong

### Issue: "Still shows ❌ Backend Offline"

**Try these in order:**

1. **Hard refresh Streamlit**
   - Press `Ctrl+Shift+R` (or `Cmd+Shift+R` on Mac)
   - Or press `⚙️ Settings → Clear cache`

2. **Check Render logs**
   - Go to Render dashboard
   - Click on your service
   - Check "Logs" tab for errors
   - Look for: "ERROR" or "FAILED"

3. **Verify URL format**
   - Should NOT have `/` at the end
   - Example ✅: `https://ai-hiring-agent-backend-xxx.onrender.com`
   - Example ❌: `https://ai-hiring-agent-backend-xxx.onrender.com/`

4. **Check GROQ_API_KEY**
   - Make sure it's set in Render environment
   - Make sure it's a valid key from console.groq.com

5. **Wait a bit longer**
   - First deployment takes 2-5 minutes
   - App might still be booting up
   - Check Render logs for "running on"

### Issue: Render deployment failed

Check the build logs in Render:
- Click your service
- Scroll down to see build output
- Look for red error messages
- Common fix: Make sure `requirements.txt` is correct

### Issue: Can't find GROQ API key

1. Go to https://console.groq.com
2. Sign in (or sign up free)
3. Click your profile → "API Keys"
4. Click "Create API Key"
5. Copy the key
6. Paste into Render environment variables

---

## 📞 Quick Support

| Issue | Resource |
|-------|----------|
| Render problems | https://render.com/docs |
| Groq API questions | https://console.groq.com/docs |
| Streamlit issues | https://docs.streamlit.io |

---

## 🎉 Success Looks Like

After all steps complete, your app will:
1. Show "✅ Backend Connected" in the sidebar
2. Allow you to upload resumes
3. Evaluate candidates
4. Display results with AI-generated explanations
5. Export reports (JSON/Markdown)

---

## 💡 Pro Tips

1. **Test with sample data first**
   - Use files from `samples/` directory in repo
   - Helps verify everything works before using real data

2. **Backend goes to sleep on free Render**
   - After 15 minutes of no requests, it hibernates
   - First request will take 30-120 seconds to wake up
   - This is normal for free tier

3. **Performance improvements**
   - Upgrade Render to "Starter" plan ($7/month) for always-on backend
   - Use Railway instead (similar speed, different pricing)

4. **Monitor logs regularly**
   - Check Render logs if you see errors
   - Helps catch issues early

---

## 🚀 You're This Close!

Just deploy the backend and you're done. The frontend is already live! 

**Estimated time to completion: 10-15 minutes**

Follow the 5 steps above and you'll have a fully functional AI Hiring Agent! 

---

**Questions?** Check the detailed guides in your repo:
- `QUICK_BACKEND_DEPLOY.md` - Quick reference
- `BACKEND_DEPLOYMENT.md` - Detailed instructions
- `DEPLOYMENT_STATUS.md` - Full deployment status
- `STREAMLIT_DEPLOYMENT.md` - Frontend reference

