# How to Push to GitHub - Complete Guide

## Step 1: Initialize Git Repository (First Time Only)

```bash
cd /Users/parth/Projects/ai-hiring-agent

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: AI Hiring Agent with context engineering and multi-question support"
```

## Step 2: Create Repository on GitHub

1. Go to https://github.com/new
2. Enter repository name: `ai-hiring-agent`
3. Add description: "AI-powered candidate evaluation tool using Groq LLM"
4. Choose: **Public** (for others to see) or **Private** (only you)
5. **Do NOT** initialize with README, .gitignore, or license (you already have them)
6. Click **Create repository**

## Step 3: Connect Local Repository to GitHub

GitHub will show you commands. Use these:

```bash
cd /Users/parth/Projects/ai-hiring-agent

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/ai-hiring-agent.git

# Verify it worked
git remote -v
```

Expected output:
```
origin  https://github.com/YOUR_USERNAME/ai-hiring-agent.git (fetch)
origin  https://github.com/YOUR_USERNAME/ai-hiring-agent.git (push)
```

## Step 4: Push to GitHub

```bash
# Push main branch to GitHub (creates it if doesn't exist)
git branch -M main
git push -u origin main
```

This will prompt for authentication. You have two options:

### Option A: Personal Access Token (Recommended)
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click **Generate new token (classic)**
3. Name it: `ai-hiring-agent-push`
4. Select scopes: `repo` (full control)
5. Click **Generate token**
6. Copy the token
7. When prompted for password, paste the token

### Option B: SSH Key
1. Generate SSH key: `ssh-keygen -t ed25519 -C "your_email@example.com"`
2. Add to GitHub: Settings → SSH and GPG keys → New SSH key
3. Use SSH URL instead: `git@github.com:YOUR_USERNAME/ai-hiring-agent.git`

## Step 5: Verify Push Succeeded

After pushing, verify on GitHub:
1. Go to https://github.com/YOUR_USERNAME/ai-hiring-agent
2. You should see all your files there
3. Check the commit history

---

## Quick Reference Commands

```bash
# Check git status
git status

# View changes
git diff

# View commit history
git log --oneline

# Add specific file
git add filename.py

# Stage all changes
git add .

# Commit with message
git commit -m "Your message here"

# Push to GitHub
git push

# Pull from GitHub
git pull
```

---

## What Files Will Be Pushed

✅ Included (should push):
- All Python code (`backend/`, `frontend/`)
- Configuration files (`requirements.txt`, `.env.example`)
- Documentation (`README.md`, `SETUP.md`, `ARCHITECTURE.md`, etc.)
- `.gitignore` file

❌ Excluded (won't push):
- `.env` file (contains API key - protected by .gitignore)
- `.venv/` virtual environment
- `__pycache__/` directories
- `.pyc` compiled Python files

---

## First Push Step-by-Step

```bash
# 1. Navigate to project
cd /Users/parth/Projects/ai-hiring-agent

# 2. Initialize git (only first time)
git init

# 3. Add all files
git add .

# 4. Create first commit
git commit -m "Initial commit: AI Hiring Agent - Full Stack Application

- Context engineering with prompt versioning (V1, V2, V3)
- Three-agent pipeline: Resume Analyzer, Scorer, Question Generator
- FastAPI backend + Streamlit frontend
- Advanced JSON parsing with fallbacks
- 5-7 strategic interview questions per candidate
- Token optimization (95% efficiency)
- Complete documentation"

# 5. Add GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/ai-hiring-agent.git

# 6. Rename branch to main
git branch -M main

# 7. Push to GitHub
git push -u origin main

# Success! Check at: https://github.com/YOUR_USERNAME/ai-hiring-agent
```

---

## Troubleshooting

### "fatal: not a git repository"
Solution: Run `git init` first

### "remote origin already exists"
Solution: `git remote set-url origin https://new-url.git`

### "Everything up-to-date"
Solution: You haven't made new commits since last push

### Authentication failed
Solution: Check your personal access token or SSH key

### Large files rejected
Solution: GitHub has 100MB file limit. Use `.gitignore` to exclude large files

---

## Future Pushes (After Initial Push)

Once set up, just use:

```bash
# Make changes
# Edit files...

# Stage changes
git add .

# Commit changes
git commit -m "Descriptive message about changes"

# Push to GitHub
git push
```

---

## Good Commit Messages

✅ Good:
- "Add multi-question support to question generator"
- "Fix JSON parsing for V3 prompt format"
- "Update documentation for setup process"
- "Improve token efficiency to 95%"

❌ Bad:
- "fix"
- "update"
- "wip"
- "asdf"

---

## Need Help?

GitHub official guide: https://docs.github.com/en/get-started/importing-your-project-to-github
