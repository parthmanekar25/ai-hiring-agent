# Documentation Index

Quick reference for all documentation files.

## 📖 Essential Documentation (5 files)

### 1. **[README.md](README.md)** - Start here!
   - **What:** Project overview and quick start
   - **Read this if:** First time using the tool
   - **Time:** 5 minutes
   - **Contains:** Features, quick start, quick reference

### 2. **[SETUP.md](SETUP.md)** - Installation guide
   - **What:** Detailed setup and configuration
   - **Read this if:** Having installation issues
   - **Time:** 10 minutes
   - **Contains:** Prerequisites, step-by-step setup, troubleshooting

### 3. **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design
   - **What:** How the system works internally
   - **Read this if:** Want to understand the design
   - **Time:** 15 minutes
   - **Contains:** Three-agent pipeline, data flow, components

### 4. **[API.md](API.md)** - Technical API reference
   - **What:** Complete API documentation
   - **Read this if:** Integrating or building on top
   - **Time:** 20 minutes
   - **Contains:** Endpoints, request/response formats, examples

### 5. **[DECISIONS.md](DECISIONS.md)** - Design decisions & assumptions
   - **What:** Why we made specific choices
   - **Read this if:** Curious about design rationale
   - **Time:** 20 minutes
   - **Contains:** Decision explanations, assumptions, trade-offs

---

## 🎯 Quick Paths

### "I just want to use it"
1. Read: [README.md](README.md) (5 min)
2. Follow: [SETUP.md](SETUP.md) (10 min)
3. Start using! 🚀

### "I want to understand how it works"
1. Read: [README.md](README.md) (5 min)
2. Read: [ARCHITECTURE.md](ARCHITECTURE.md) (15 min)
3. Done! You now understand the system 🧠

### "I'm integrating this into my system"
1. Read: [API.md](API.md) (20 min)
2. Check examples at end of API.md
3. Implement integration 🔌

### "I'm concerned about bias/fairness"
1. Read: [DECISIONS.md](DECISIONS.md) (20 min)
2. Focus on: "Assumption 6: User Intentions"
3. Note: Always use with human judgment ⚖️

### "I want to customize the prompts"
1. Read: [ARCHITECTURE.md](ARCHITECTURE.md) - "Prompt Manager" section (5 min)
2. Read: [DECISIONS.md](DECISIONS.md) - "Advanced Prompt Engineering" (5 min)
3. Edit: `backend/prompts/prompt_manager.py`
4. Test your changes ✏️

### "Performance is too slow"
1. Read: [DECISIONS.md](DECISIONS.md) - "Speed vs Quality" (3 min)
2. Try: Upload fewer resumes (~5 max)
3. Check: Groq API status
4. If still slow: See [SETUP.md](SETUP.md) troubleshooting

---

## 📋 File Descriptions

| File | Purpose | Size | Read Time |
|------|---------|------|-----------|
| README.md | Quick start + overview | 3KB | 5 min |
| SETUP.md | Installation guide | 8KB | 10 min |
| ARCHITECTURE.md | System design | 12KB | 15 min |
| API.md | API documentation | 15KB | 20 min |
| DECISIONS.md | Design decisions | 18KB | 20 min |
| **Total** | **Complete docs** | **56KB** | **70 min** |

---

## 🔍 Find What You Need

### By Topic

**Getting Started:**
- Installation → [SETUP.md](SETUP.md)
- First run → [README.md](README.md)
- How to use → [README.md](README.md#-how-to-use)

**Understanding the System:**
- Architecture overview → [ARCHITECTURE.md](ARCHITECTURE.md#system-overview)
- Three agents explained → [ARCHITECTURE.md](ARCHITECTURE.md#three-agent-pipeline)
- Data flow → [ARCHITECTURE.md](ARCHITECTURE.md#data-flow)

**Using the API:**
- Endpoint reference → [API.md](API.md#endpoints)
- Request/response format → [API.md](API.md#endpoint-post-apievaluate)
- Code examples → [API.md](API.md#practical-examples)

**Troubleshooting:**
- Setup issues → [SETUP.md](SETUP.md#common-setup-issues)
- API errors → [API.md](API.md#error-responses)
- Performance → [DECISIONS.md](DECISIONS.md#speed-vs-quality)

**Design & Customization:**
- Why these choices? → [DECISIONS.md](DECISIONS.md)
- Assumptions made → [DECISIONS.md](DECISIONS.md#assumptions)
- Future improvements → [DECISIONS.md](DECISIONS.md#future-considerations)
- Adding custom logic → [ARCHITECTURE.md](ARCHITECTURE.md#extensibility)

### By Question

**Q: How do I install this?**
→ [SETUP.md](SETUP.md)

**Q: How does it work?**
→ [ARCHITECTURE.md](ARCHITECTURE.md)

**Q: What's the API?**
→ [API.md](API.md)

**Q: Why was this designed this way?**
→ [DECISIONS.md](DECISIONS.md)

**Q: How do I use it?**
→ [README.md](README.md#-how-to-use)

**Q: Something isn't working**
→ [SETUP.md](SETUP.md#common-setup-issues)

**Q: Can I customize it?**
→ [ARCHITECTURE.md](ARCHITECTURE.md#extensibility)

**Q: Will this be biased?**
→ [DECISIONS.md](DECISIONS.md#assumption-6-user-intentions)

**Q: How fast is it?**
→ [DECISIONS.md](DECISIONS.md#speed-vs-quality)

---

## 📚 Reading Order (Complete)

1. **Start:** README.md (5 min)
   - Understand what this does

2. **Setup:** SETUP.md (10 min)
   - Install and run it

3. **Design:** ARCHITECTURE.md (15 min)
   - Learn how it works internally

4. **Reference:** API.md (20 min)
   - Understand the technical API

5. **Rationale:** DECISIONS.md (20 min)
   - Understand why things are designed this way

**Total time:** ~70 minutes for complete understanding

---

## 🚀 Pro Tips

- **Bookmarks:** Save these URLs to your browser
  - http://localhost:8501 (UI)
  - http://localhost:8000/docs (API docs)
  - http://localhost:8000/health (health check)

- **Search:** Use browser search (Ctrl/Cmd + F) within docs

- **Offline:** Save all .md files and open in any editor

- **Printing:** Pages are formatted for printing (include both markdown view and code)

- **Links:** All documentation links are relative - works offline too

---

## ✅ Documentation Checklist

- ✅ README.md - Quick start and overview
- ✅ SETUP.md - Installation and troubleshooting
- ✅ ARCHITECTURE.md - System design and components
- ✅ API.md - Complete API reference
- ✅ DECISIONS.md - Design choices and assumptions
- ✅ DOCS_INDEX.md - This file (quick navigation)

---

## 🎓 Learning Path

### Beginner (Just want to use it)
1. README.md
2. SETUP.md
3. Start using!

### Intermediate (Want to understand how it works)
1. README.md
2. SETUP.md
3. ARCHITECTURE.md
4. API.md

### Advanced (Want to customize or contribute)
1. All of above
2. DECISIONS.md
3. Review source code in `backend/` and `frontend/`

### Expert (Want to improve the system)
1. All documentation
2. Study each agent implementation
3. Review prompt engineering choices
4. Experiment with prompt versions
5. Test custom modifications

---

## 📞 Need Help?

Check these in order:
1. **Installation issues** → [SETUP.md](SETUP.md#common-setup-issues)
2. **How to use** → [README.md](README.md#-how-to-use)
3. **API questions** → [API.md](API.md)
4. **System design** → [ARCHITECTURE.md](ARCHITECTURE.md)
5. **Everything else** → [DECISIONS.md](DECISIONS.md)

---

**Last Updated:** 2024

**Documentation Version:** 5 files, ~2,600 lines, ~56KB

**Status:** ✅ Complete and up-to-date
