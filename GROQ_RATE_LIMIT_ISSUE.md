# 🚨 Groq API Rate Limit Exceeded

## The Issue

Your backend is returning **0 candidates evaluated** because the **Groq API free tier rate limit has been exceeded**.

### What Happened

```
❌ Error: Rate limit reached for model `llama-3.3-70b-versatile`
   Limit: 100,000 tokens per day (free tier)
   Used: 99,583 tokens
   Requested: 895 more tokens
   Wait time: 6-7 minutes
```

## Why This Happens

The AI Hiring Agent uses **Groq's LLM API** (llama-3.3-70b model) for:
1. **Resume Analysis** - Parsing and understanding resumes (~200-400 tokens per resume)
2. **Candidate Scoring** - Evaluating against job description (~300-500 tokens)
3. **Question Generation** - Creating interview questions (~100-200 tokens)

**Total per candidate**: ~600-1100 tokens

**Free tier quota**: 100,000 tokens/day
**Capacity**: ~90-160 candidates per day (depending on resume length)

## Solutions

### Option 1: Wait for Daily Reset ⏱️ (Quick Fix - FREE)

The rate limit **resets daily at midnight UTC**. If you tested multiple times today, just wait:

```
⏳ Wait ~6-7 minutes (or until midnight UTC)
✅ Try again in a few minutes
```

### Option 2: Upgrade to Groq Dev Tier 💳 (Best Option)

Upgrade your Groq account to get more tokens:

1. Go to: https://console.groq.com/settings/billing
2. Click **"Upgrade to Dev Tier"**
3. Choose your plan:
   - **Dev Tier**: 40 requests/minute, 14,000 tokens/minute
   - **Pro Tier**: Higher limits

Cost is based on token usage (very affordable, typically $0-1/month for testing).

### Option 3: Use Different LLM Provider 🔄 (Alternative)

You can switch to other LLM providers by modifying the backend:

**Options:**
- **OpenAI API** (GPT-4, GPT-3.5)
- **Anthropic Claude** (API)
- **Azure OpenAI**
- **Local LLM** (Ollama, LM Studio)

Would require code changes in:
- `backend/agents/resume_analyzer.py`
- `backend/agents/scorer.py`
- `backend/agents/question_generator.py`

## How to Check Current Status

Run this command to see the actual error:

```bash
# Check backend logs
tail -50 /Users/parth/Projects/ai-hiring-agent/backend.log | grep -i "rate\|Error"
```

## Prevention for Future Use

### Track Token Usage
- Monitor daily at: https://console.groq.com/usage
- Set reminders for daily limits

### Optimize Token Usage
- **Shorter resumes**: Use concise job descriptions (~200 chars)
- **Batch processing**: Evaluate multiple candidates in one session
- **Cache results**: Keep evaluation results to avoid re-processing

### Best Practices
1. ✅ Upgrade to Dev Tier (recommended for production use)
2. ✅ Monitor token usage daily
3. ✅ Batch evaluate candidates to spread token usage
4. ✅ Use caching for repeated job descriptions

## Status Check

Run the test script to verify when you can resume:

```bash
cd /Users/parth/Projects/ai-hiring-agent
source .venv/bin/activate
python test_backend.py
```

You'll see one of:
- ✅ **"Evaluation endpoint is working!"** - You're good to go!
- ⚠️ **"Groq API rate limit exceeded"** - Wait longer
- ❌ **Other error** - Check backend logs

## Troubleshooting

### If you don't have a Groq account:
1. Sign up (free) at: https://console.groq.com
2. Get your API key from: https://console.groq.com/keys
3. Add to `.env` file: `GROQ_API_KEY=your_key_here`
4. Restart backend

### If upgrade button doesn't work:
- Contact Groq support: support@groq.com
- Check: https://console.groq.com/settings/billing

### If you still get rate limit errors:
- May need to wait for daily reset (midnight UTC)
- Contact Groq support for immediate increase
- Consider switching to different LLM provider

---

**Estimated Wait Time**: 6-7 minutes (or until midnight UTC)

**Recommended Action**: Upgrade to Dev Tier for unlimited testing

Once resolved, you'll be able to evaluate candidates normally! 🎉
