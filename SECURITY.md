# Security Guidelines

## Before Pushing to GitHub

### ✅ Security Checklist

- [x] `.env` file is in `.gitignore`
- [x] No API keys hardcoded in source code
- [x] `.env.example` contains only placeholders
- [x] No sensitive data in documentation
- [x] Logs directory in `.gitignore`
- [x] Python cache files in `.gitignore`

### 🔒 Protected Files

These files are **excluded from Git** via `.gitignore`:

```
.env                    # Contains your actual API key
logs/                   # May contain sensitive runtime data
__pycache__/           # Python cache
*.pyc                  # Compiled Python
.vscode/               # IDE settings
.idea/                 # IDE settings
```

### 📝 Safe to Commit

These files are **safe to push** to GitHub:

```
.env.example           # Template with placeholders only
.gitignore            # Git ignore rules
*.py                  # Source code (no hardcoded secrets)
*.md                  # Documentation
requirements.txt      # Dependencies
```

## API Key Security

### ⚠️ NEVER Commit

```bash
# ❌ WRONG - Contains real API key
DEEPSEEK_API_KEY_CHAT=sk-abc123def456ghi789jkl012mno345pqr
```

### ✅ Always Use Placeholders

```bash
# ✅ CORRECT - Placeholder only
DEEPSEEK_API_KEY_CHAT=your_deepseek_api_key_here
```

## Setting Up the Repository

### 1. First Time Setup

```bash
cd /Users/chouheisei/Repos/winwin

# Initialize git (if not already done)
git init

# Verify .env is ignored
git status
# Should NOT show .env in the list

# Add all safe files
git add -A

# Verify what will be committed
git status
# Make sure .env is NOT listed

# Create first commit
git commit -m "Initial commit: Japanese Hedging Translator"
```

### 2. Connect to GitHub

```bash
# Create repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

### 3. Verify Security

After pushing, check GitHub repository:
- [ ] `.env` is **NOT** visible in the repository
- [ ] `.env.example` contains only placeholders
- [ ] No API keys in any file

## What to Do If You Accidentally Commit Secrets

### 🚨 If API Key Was Committed

**IMMEDIATELY:**

1. **Revoke the exposed API key** at https://platform.deepseek.com/api_keys
2. **Generate a new API key**
3. **Update your local `.env` file** with the new key
4. **Remove from Git history:**

```bash
# Remove file from history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (use with caution)
git push origin --force --all
```

5. **Better approach - Use BFG Repo Cleaner:**

```bash
# Install BFG
brew install bfg  # macOS

# Remove secrets
bfg --replace-text <(echo 'sk-your-exposed-key-here==>REMOVED')

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

## Best Practices

### Environment Variables

1. **Never commit `.env` files**
2. **Always provide `.env.example` with placeholders**
3. **Document required environment variables** in README
4. **Use different keys for development and production**

### API Keys

1. **Rotate keys regularly**
2. **Use separate keys for each project**
3. **Set appropriate permissions/scopes**
4. **Monitor usage for anomalies**

### Code Reviews

Before every commit:

```bash
# Check what will be committed
git diff --cached

# Look for common secret patterns
git diff --cached | grep -i "api_key\|password\|secret\|token"

# Verify .env is not staged
git status | grep ".env"
```

## Development Workflow

### Local Development

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/REPO_NAME.git
cd REPO_NAME

# 2. Copy environment template
cp .env.example .env

# 3. Edit .env with your actual API key
nano .env
# Add: DEEPSEEK_API_KEY_CHAT=sk-your-actual-key

# 4. Never commit .env
git status  # Should NOT show .env
```

### Sharing with Team

**Share via secure channels:**
- 1Password / LastPass shared vaults
- Encrypted messaging
- Environment variable management services

**DO NOT share via:**
- Email
- Slack/Discord
- Git commits
- Code comments

## Additional Security Measures

### 1. Pre-commit Hooks

Install a pre-commit hook to prevent accidental commits:

```bash
# Create .git/hooks/pre-commit
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
if git diff --cached --name-only | grep -q "^.env$"; then
    echo "ERROR: Attempting to commit .env file!"
    echo "This file contains secrets and should not be committed."
    exit 1
fi

# Check for potential secrets in staged files
if git diff --cached | grep -i "api_key.*sk-"; then
    echo "WARNING: Potential API key found in commit!"
    echo "Please review your changes."
    exit 1
fi
EOF

chmod +x .git/hooks/pre-commit
```

### 2. GitHub Repository Settings

After creating the repository:

1. Go to Settings > Security
2. Enable "Dependency alerts"
3. Enable "Dependabot alerts"
4. Consider enabling "Secret scanning" (if available)

### 3. .gitattributes

Create `.gitattributes` for better Git handling:

```
# Ensure .env is never committed even if accidentally added
.env export-ignore
*.log export-ignore
```

## Incident Response

### If Secrets Are Exposed

1. **Immediate Actions:**
   - [ ] Revoke exposed credentials
   - [ ] Generate new credentials
   - [ ] Update local configuration
   - [ ] Notify team members

2. **Investigation:**
   - [ ] Check API usage logs for unauthorized access
   - [ ] Review access patterns
   - [ ] Identify scope of exposure

3. **Remediation:**
   - [ ] Remove secrets from Git history
   - [ ] Force push cleaned history
   - [ ] Document incident
   - [ ] Update security procedures

4. **Prevention:**
   - [ ] Implement pre-commit hooks
   - [ ] Add secret scanning tools
   - [ ] Team security training
   - [ ] Regular security audits

## Contact

For security concerns or to report vulnerabilities, please:
1. Do NOT open a public GitHub issue
2. Contact the repository owner directly
3. Provide detailed information about the vulnerability
4. Allow time for remediation before public disclosure

## Resources

- [GitHub: Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)
- [git-secrets](https://github.com/awslabs/git-secrets)
- [DeepSeek API Key Management](https://platform.deepseek.com/api_keys)

---

**Remember**: Once a secret is committed to Git history, assume it has been compromised. Always revoke and regenerate exposed credentials immediately.
