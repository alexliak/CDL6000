# CDL6000 Complete Setup Guide

## Part 1: Git Initialization

### 1. Project Setup
```bash
# Navigate to project directory
cd D:/CDL6000-project

# Initialize Git
git init

# Configure Git globally
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Setup Git Credential Manager
git config --global credential.helper manager
git config --global credential.helper store
git config --global credential.https://github.com.username your_github_username
```

### 2. Git Configuration Files
```bash
# Create .gitattributes
echo ".env filter=git-crypt" > .gitattributes
echo ".gitattributes !filter !diff" >> .gitattributes

# Verify .gitattributes
cat .gitattributes
```

### 3. Verify Git Setup
```bash
# Check repository and branch
git remote -v
git branch

# Verify path case
pwd

# Check configurations
git config --list
```

## Part 2: GitHub Connection

### 1. Repository Setup
1. Create repository on GitHub:
   - Name: `CDL6000` (exact case)
   - Description: "Legal Document Classification System"
   - Private repository
   - Skip README/license/gitignore creation

### 2. Connect and Push
```bash
# Add remote
git remote add origin https://github.com/yourusername/CDL6000.git

# Verify remote URL format
git remote -v

# Push to main branch
git branch -M main
git push -u origin main
```

## Part 3: Obsidian Setup

### 1. Verify Vault Structure
```bash
# Check vault directory structure
dir "D:/CDL6000-project/docs/obsidian-vault"

# Expected structure:
obsidian-vault/
├── .obsidian/
├── 00-overview/
├── 01-specs/
├── 02-design/
├── 03-impl/
├── 04-test/
├── 05-deploy/
├── 06-maintain/
├── templates/
├── assets/
└── meetings/

# Verify templates
dir "D:/CDL6000-project/docs/obsidian-vault/templates"

# Check index files
dir "D:/CDL6000-project/docs/obsidian-vault/**/index.md"
```

### 2. Obsidian Configuration
1. Open Obsidian
2. Select "Open another vault"
3. Navigate to `D:/CDL6000-project/docs/obsidian-vault`
4. Configure settings:
   - Enable Core plugins:
     - File explorer
     - Search
     - Tags pane
     - Page preview
     - Templates
   - Set template location to `templates`
   - Install Community Plugins:
     - Obsidian Git
     - Dataview
     - Calendar

## Validation Checklist

### Git/GitHub ✓
- [ ] Git initialized and configured
- [ ] .gitattributes created correctly
- [ ] Remote repository connected
- [ ] Branch name is 'main'
- [ ] Credential manager configured

### Paths and Names ✓
- [ ] Repository: CDL6000 (exact case)
- [ ] Root: D:/CDL6000-project
- [ ] Vault: D:/CDL6000-project/docs/obsidian-vault
- [ ] All folders use correct case
- [ ] No spaces in paths

### Obsidian ✓
- [ ] Vault loads correctly
- [ ] Templates folder is lowercase
- [ ] Core plugins enabled
- [ ] Git plugin installed
- [ ] Template location set

## Verification Commands
```bash
# Git Status
git status
git branch
git remote -v

# Structure Check
dir "D:/CDL6000-project"
dir "D:/CDL6000-project/docs/obsidian-vault"

# Configuration Check
git config --list
```

## Troubleshooting

### Git Issues
- Authentication errors: Use Git Credential Manager
- Push failures: Verify remote URL format
- Branch issues: Ensure on 'main' branch

### Obsidian Issues
- Vault not loading: Check path case
- Templates missing: Verify templates folder name
- Plugin issues: Restart Obsidian
