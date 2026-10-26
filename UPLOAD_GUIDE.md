# 📤 GitHub Upload Guide - Day by Day

Complete guide to upload your AI learning projects to GitHub, one day at a time.

## 🎯 Quick Start

### Method 1: Using Helper Script (Recommended)

```powershell
# Upload a specific day
.\upload-day.ps1 -Week "week1" -Day "day1"

# With custom message
.\upload-day.ps1 -Week "week1" -Day "day1" -Message "Add Day 1: Hello LLM with explanations"
```

### Method 2: Manual Git Commands

```powershell
# Upload Day 1
git add week1/day1
git commit -m "Add week1/day1: Hello LLM implementation"
git push origin main
```

---

## 📅 Day-by-Day Upload Schedule

### Week 1: LLM Fundamentals

#### Day 1 - Hello LLM
```powershell
.\upload-day.ps1 -Week "week1" -Day "day1" -Message "Add Day 1: First LLM API call with Groq"
```

Files included:
- ✓ `hello_llm.py` - Basic API call
- ✓ `main.py` - Main implementation
- ✓ `EXPLANATION.md` - Comprehensive docs (900+ lines)
- ✓ `pyproject.toml` - Dependencies
- ✓ `README.md` - Quick overview
- ✗ `.env` (excluded by .gitignore)
- ✗ `.venv/` (excluded by .gitignore)

#### Day 2 - System Prompts
```powershell
.\upload-day.ps1 -Week "week1" -Day "day2" -Message "Add Day 2: System prompts and temperature control"
```

Files included:
- ✓ `system_temp.py`
- ✓ `main.py`
- ✓ `EXPLANATION.md` (850+ lines)
- ✓ `pyproject.toml`

#### Day 3 - Tokens
```powershell
.\upload-day.ps1 -Week "week1" -Day "day3" -Message "Add Day 3: Tokenization and token counting"
```

Files included:
- ✓ `tokens.py`
- ✓ `main.py`
- ✓ `EXPLANATION.md` (1000+ lines)

#### Day 4 - JSON & Pydantic
```powershell
.\upload-day.ps1 -Week "week1" -Day "day4" -Message "Add Day 4: Structured outputs with JSON and Pydantic"
```

Files included:
- ✓ `json_pydantic.py`
- ✓ `main.py`
- ✓ `EXPLANATION.md` (1100+ lines)

#### Day 5 - Resume Parser
```powershell
.\upload-day.ps1 -Week "week1" -Day "day5" -Message "Add Day 5: Resume parser with Pydantic validation"
```

Files included:
- ✓ `project1.py`
- ✓ `main.py`
- ✓ `resumes/` folder with sample PDFs
- ✓ `EXPLANATION.md` (900+ lines)

---

### Week 2: Prompt Engineering & Chains

#### Day 6 - Prompt Engineering
```powershell
.\upload-day.ps1 -Week "week2" -Day "day6" -Message "Add Day 6: Advanced prompt engineering techniques"
```

#### Day 7 - ReAct Agents
```powershell
.\upload-day.ps1 -Week "week2" -Day "day7" -Message "Add Day 7: ReAct agent with reasoning and acting"
```

Files included:
- ✓ `react_chain.py`
- ✓ `EXPLANATION.md` (1000+ lines)

#### Day 8 - LLM Chains
```powershell
.\upload-day.ps1 -Week "week2" -Day "day8" -Message "Add Day 8: Sequential LLM chains"
```

Files included:
- ✓ `chain.py`
- ✓ `EXPLANATION.md` (900+ lines)

#### Day 9 - Streaming
```powershell
.\upload-day.ps1 -Week "week2" -Day "day9" -Message "Add Day 9: Real-time streaming responses"
```

Files included:
- ✓ `EXPLANATION.md` (700+ lines)

---

### Week 3: RAG Systems

#### Day 11 - Basic RAG
```powershell
.\upload-day.ps1 -Week "week3" -Day "day11" -Message "Add Day 11: Basic RAG implementation"
```

Files included:
- ✓ `EXPLANATION.md` (800+ lines)

#### Day 12 - Embeddings
```powershell
.\upload-day.ps1 -Week "week3" -Day "day12" -Message "Add Day 12: Text embeddings and similarity"
```

Files included:
- ✓ `EXPLANATION.md` (900+ lines)

#### Day 13 - Full RAG
```powershell
.\upload-day.ps1 -Week "week3" -Day "day13" -Message "Add Day 13: Complete RAG pipeline"
```

Files included:
- ✓ `EXPLANATION.md` (1000+ lines)

#### Day 14 - Qdrant
```powershell
.\upload-day.ps1 -Week "week3" -Day "day14" -Message "Add Day 14: Qdrant vector database integration"
```

Files included:
- ✓ `EXPLANATION.md` (1100+ lines)

#### Day 15 - Advanced Qdrant
```powershell
.\upload-day.ps1 -Week "week3" -Day "day15" -Message "Add Day 15: Advanced Qdrant with filtering"
```

Files included:
- ✓ `qdrantfull.py`
- ✓ `knowledge.json`
- ✓ `EXPLANATION.md` (1100+ lines)

---

### Week 4: Production & Advanced

#### Day 16 - Chunking
```powershell
.\upload-day.ps1 -Week "week4" -Day "day16" -Message "Add Day 16: Text chunking strategies for RAG"
```

Files included:
- ✓ `chunking.py`
- ✓ `EXPLANATION.md` (800+ lines)

#### Day 18 - Tool-Calling Agent
```powershell
.\upload-day.ps1 -Week "week4" -Day "day18" -Message "Add Day 18: Tool-calling agent with web search"
```

Files included:
- ✓ `myagent.py`
- ✓ `EXPLANATION.md` (1000+ lines)

---

## 🔍 Before Each Upload - Checklist

- [ ] Check if `.env` file is excluded (should NOT be uploaded)
- [ ] Verify `.venv` folder is excluded
- [ ] Ensure `EXPLANATION.md` is present
- [ ] Test run the code once
- [ ] Check for any hardcoded API keys (replace with env variables)

---

## 🛠️ Manual Upload Process (Step by Step)

If you prefer manual control:

### 1. Navigate to Repository
```powershell
cd c:\Users\vaibh\padho-ai-engineer
```

### 2. Check Current Status
```powershell
git status
```

### 3. Add Specific Day
```powershell
# Example: Add day1
git add week1/day1

# Verify what will be committed
git status
```

### 4. Commit with Message
```powershell
git commit -m "Add week1/day1: Hello LLM implementation with comprehensive docs"
```

### 5. Push to GitHub
```powershell
git push origin main
```

### 6. Verify Upload
Check: https://github.com/Vaibhu79/Learning_Ai

---

## 🚨 Common Issues & Solutions

### Issue 1: ".env file should not be uploaded"
**Solution:** It's already in `.gitignore`, so it won't be uploaded. But double-check:
```powershell
git status
# Should NOT show .env files
```

### Issue 2: "Permission denied (publickey)"
**Solution:** Set up GitHub authentication:
```powershell
# Option 1: Use GitHub CLI
gh auth login

# Option 2: Use Personal Access Token
# Generate token at: https://github.com/settings/tokens
# Use token as password when prompted
```

### Issue 3: "Large files rejected"
**Solution:** GitHub has 100MB file limit. Check file sizes:
```powershell
# Find large files
Get-ChildItem -Recurse | Where-Object {$_.Length -gt 50MB} | Select-Object FullName, @{Name="Size(MB)";Expression={[math]::Round($_.Length/1MB,2)}}
```

### Issue 4: "Conflicts with remote"
**Solution:**
```powershell
# Pull latest changes first
git pull origin main

# If conflicts, resolve manually then:
git add .
git commit -m "Resolve conflicts"
git push origin main
```

---

## 📊 Upload Progress Tracker

Track your progress:

### Week 1
- [ ] Day 1 - Hello LLM
- [ ] Day 2 - System Prompts
- [ ] Day 3 - Tokens
- [ ] Day 4 - JSON & Pydantic
- [ ] Day 5 - Resume Parser

### Week 2
- [ ] Day 6 - Prompt Engineering
- [ ] Day 7 - ReAct Agents
- [ ] Day 8 - LLM Chains
- [ ] Day 9 - Streaming

### Week 3
- [ ] Day 11 - Basic RAG
- [ ] Day 12 - Embeddings
- [ ] Day 13 - Full RAG
- [ ] Day 14 - Qdrant
- [ ] Day 15 - Advanced Qdrant

### Week 4
- [ ] Day 16 - Chunking
- [ ] Day 18 - Tool-Calling Agent

---

## 💡 Pro Tips

1. **Upload in order:** Start with day1, then day2, etc. for logical progression

2. **Write good commit messages:**
   ```
   ✓ Good: "Add Day 1: First LLM API call with error handling"
   ✗ Bad: "day1"
   ```

3. **One day at a time:** Don't rush, upload one day properly

4. **Test locally first:** Always run code before uploading

5. **Check GitHub after upload:** Verify files are visible

6. **Add descriptions:** Use GitHub's web interface to add day-specific READMEs

---

## 🎯 Example: Complete Upload of Day 1

```powershell
# Step 1: Navigate
cd c:\Users\vaibh\padho-ai-engineer

# Step 2: Check status
git status

# Step 3: Add day1
git add week1/day1

# Step 4: Verify (should show week1/day1 files)
git status

# Step 5: Commit
git commit -m "Add Day 1: Hello LLM - First API call with Groq, includes comprehensive documentation"

# Step 6: Push
git push origin main

# Step 7: Verify on GitHub
# Visit: https://github.com/Vaibhu79/Learning_Ai/tree/main/week1/day1
```

---

## 📱 Quick Commands Reference

```powershell
# Status check
git status

# Add specific day
git add week1/day1

# Add multiple days at once (not recommended)
git add week1/day1 week1/day2

# Commit
git commit -m "Your message here"

# Push
git push origin main

# Undo last commit (before push)
git reset --soft HEAD~1

# See what will be uploaded
git diff --staged

# Remove file from staging
git reset HEAD week1/day1/somefile.py
```

---

## 🎉 Recommended Upload Schedule

### Day 1: Upload Week 1, Days 1-2
```powershell
.\upload-day.ps1 -Week "week1" -Day "day1"
.\upload-day.ps1 -Week "week1" -Day "day2"
```

### Day 2: Upload Week 1, Days 3-5
```powershell
.\upload-day.ps1 -Week "week1" -Day "day3"
.\upload-day.ps1 -Week "week1" -Day "day4"
.\upload-day.ps1 -Week "week1" -Day "day5"
```

### Day 3: Upload Week 2
```powershell
.\upload-day.ps1 -Week "week2" -Day "day6"
.\upload-day.ps1 -Week "week2" -Day "day7"
.\upload-day.ps1 -Week "week2" -Day "day8"
.\upload-day.ps1 -Week "week2" -Day "day9"
```

### Day 4: Upload Week 3
```powershell
.\upload-day.ps1 -Week "week3" -Day "day11"
.\upload-day.ps1 -Week "week3" -Day "day12"
.\upload-day.ps1 -Week "week3" -Day "day13"
.\upload-day.ps1 -Week "week3" -Day "day14"
.\upload-day.ps1 -Week "week3" -Day "day15"
```

### Day 5: Upload Week 4
```powershell
.\upload-day.ps1 -Week "week4" -Day "day16"
.\upload-day.ps1 -Week "week4" -Day "day18"
```

---

**Happy Uploading! 🚀**

For issues: Check [GitHub Issues](https://github.com/Vaibhu79/Learning_Ai/issues)
