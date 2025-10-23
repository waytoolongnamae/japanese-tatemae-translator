# Pre-Push Security Checklist

## ✅ Complete This Checklist Before Pushing to GitHub

### 1. API Keys & Secrets

- [ ] `.env` file is **NOT** staged for commit
- [ ] No `sk-` pattern found in any Python files
- [ ] No API keys in documentation (only placeholders)
- [ ] `.env.example` contains only placeholder text

**Verify:**
```bash
# Check .env is not staged
git status | grep ".env" && echo "ERROR: .env is staged!" || echo "✓ .env not staged"

# Check for API key patterns
grep -r "sk-" --include="*.py" --include="*.md" . && echo "ERROR: Found API key!" || echo "✓ No API keys found"
```

### 2. Ignored Files

- [ ] `.gitignore` includes `.env`
- [ ] `.gitignore` includes `logs/`
- [ ] `.gitignore` includes `__pycache__/`
- [ ] `.gitignore` includes `.claude/`

**Verify:**
```bash
cat .gitignore | grep -E "\.env|logs/|__pycache__|\.claude" && echo "✓ All critical patterns in .gitignore"
```

### 3. Repository Contents

- [ ] Review all staged files
- [ ] No sensitive data in any file
- [ ] No personal information in comments
- [ ] No internal URLs or system paths

**Verify:**
```bash
# List all files to be committed
git diff --cached --name-only

# Review diff
git diff --cached
```

### 4. Documentation

- [ ] README.md is complete
- [ ] Installation instructions are clear
- [ ] Examples don't contain real API keys
- [ ] License file is present

### 5. Code Quality

- [ ] All tests pass
- [ ] No debug print statements with sensitive data
- [ ] No commented-out code with secrets
- [ ] Requirements.txt is up to date

**Verify:**
```bash
# Run tests
python test_translator.py

# Check requirements
pip freeze | grep -E "openai|langgraph|python-dotenv"
```

### 6. Git Configuration

- [ ] `.gitattributes` created (optional but recommended)
- [ ] Pre-commit hook installed (optional but recommended)
- [ ] Correct remote URL configured

**Verify:**
```bash
git remote -v
```

## Quick Security Scan

Run this comprehensive check:

```bash
#!/bin/bash
echo "=== Security Check ==="

# Check 1: .env not staged
if git diff --cached --name-only | grep -q "^.env$"; then
    echo "❌ ERROR: .env is staged!"
    exit 1
else
    echo "✓ .env not staged"
fi

# Check 2: No API keys in code
if grep -r "sk-" --include="*.py" --include="*.md" . | grep -v ".env.example" | grep -v "SECURITY.md" | grep -v "PUSH_CHECKLIST.md"; then
    echo "❌ ERROR: Found API key pattern in code!"
    exit 1
else
    echo "✓ No API keys in code"
fi

# Check 3: .gitignore has .env
if grep -q "^.env$" .gitignore; then
    echo "✓ .gitignore includes .env"
else
    echo "❌ ERROR: .env not in .gitignore!"
    exit 1
fi

# Check 4: No logs directory staged
if git diff --cached --name-only | grep -q "^logs/"; then
    echo "❌ WARNING: logs directory is staged"
else
    echo "✓ logs directory not staged"
fi

echo ""
echo "=== All Security Checks Passed ==="
echo "Safe to push to GitHub!"
```

Save as `security_check.sh` and run before every push:

```bash
chmod +x security_check.sh
./security_check.sh && git push
```

## After First Push

Verify on GitHub:

1. Go to your repository URL
2. Check that these files **DO NOT** appear:
   - [ ] `.env`
   - [ ] `logs/` directory
   - [ ] `.claude/` directory

3. Check that these files **DO** appear:
   - [ ] `.env.example` (with placeholders only)
   - [ ] `.gitignore`
   - [ ] `README.md`
   - [ ] `LICENSE`
   - [ ] `SECURITY.md`

4. Browse a few files to ensure no secrets are visible

## If You Find Issues After Pushing

See [SECURITY.md](SECURITY.md) for:
- How to remove secrets from Git history
- How to revoke and rotate API keys
- Incident response procedures

## Emergency Contacts

If secrets are exposed:
1. **Immediately revoke** the API key at https://platform.deepseek.com/api_keys
2. Follow cleanup procedures in SECURITY.md
3. Generate new credentials
4. Update local `.env`

---

## Ready to Push?

Once all checkboxes are complete:

```bash
# Stage all safe files
git add -A

# Verify staging
git status

# Create commit
git commit -m "Initial commit: Japanese Hedging Translator (京都風建前)"

# Push to GitHub
git push -u origin main
```

🎉 **Your repository is now secure and ready for the world!**
