# GitHub Workflow Guide for Academic Projects
## MSc Computer Science - University of Bolton 2024

---

### 1. Project Structure Overview

#### Base Directory Structure
```bash
D:\Development\
├── uob-msc-2024\           # Main project repository
├── uob-cld6000-analysis\   # CLD6000 submodule
├── uob-cld6001-research\   # CLD6001 submodule
└── uob-swe6002-enterprise\ # SWE6002 submodule
```

#### WSL Path Mapping
```bash
/mnt/d/Development/         # WSL base path
```

---

### 2. Daily Git Commands

#### Basic Operations
```bash
# Status check
git status

# Add changes
git add .
git add specific_file.md

# Commit
git commit -m "type(scope): descriptive message"

# Push changes
git push origin main

# Pull updates
git pull origin main
```

#### Branch Operations
```bash
# Create new branch
git branch feature-name
git checkout -b feature-name

# Switch branches
git checkout main

# List branches
git branch -a
```

---

### 3. Project-Specific Paths & Commands

#### Main Repository
```bash
# Clone main repository
git clone https://github.com/liakopal/uob-msc-2024.git
cd uob-msc-2024

# Update all submodules
git submodule update --init --recursive
```

#### Module-Specific Operations
```bash
# CLD6000 Module
cd /mnt/d/Development/uob-cld6000-analysis
git status

# CLD6001 Research
cd /mnt/d/Development/uob-cld6001-research
git status

# SWE6002 Enterprise
cd /mnt/d/Development/uob-swe6002-enterprise
git status
```

---

### 4. Troubleshooting Commands

#### Fix Line Endings
```bash
# Windows
git config --global core.autocrlf true

# WSL/Linux
git config --global core.autocrlf input
```

#### Reset Local Changes
```bash
# Discard local changes
git checkout -- .

# Hard reset to remote
git fetch origin
git reset --hard origin/main
```

#### Fix Submodule Issues
```bash
# Reset submodules
git submodule deinit -f .
git submodule update --init

# Fix specific submodule
git submodule deinit -f path/to/submodule
git submodule update --init path/to/submodule
```

---

### 5. WSL Integration Commands

#### WSL Management
```bash
# List WSL distributions
wsl --list --verbose

# Shutdown WSL
wsl --shutdown

# Start specific distro
wsl -d Ubuntu

# Set default user
/etc/wsl.conf content:
[user]
default=alexa
```

---

### 6. Advanced Git Operations

#### Stash Management
```bash
# Save changes temporarily
git stash

# List stashes
git stash list

# Apply stashed changes
git stash pop

# Apply specific stash
git stash apply stash@{0}
```

#### History and Logs
```bash
# View commit history
git log --oneline

# View detailed changes
git log -p

# View file history
git log --follow -p -- filename
```

---

### 7. Configuration Settings

#### Git Configuration
```bash
# User settings
git config --global user.name "liakopal"
git config --global user.email "liakopoulosalex@gmail.com"

# Editor settings
git config --global core.editor "code --wait"
```

#### .gitignore Settings
```bash
# Standard ignores
.DS_Store
.vscode/
__pycache__/
*.pyc
.env
.obsidian/workspace.json
```

---

### 8. Repository Management

#### Submodule Management
```bash
# Add submodule
git submodule add https://github.com/liakopal/uob-cld6000-analysis.git cld6000-analysis

# Update submodules
git submodule update --remote

# Remove submodule
git submodule deinit -f path/to/submodule
rm -rf .git/modules/path/to/submodule
git rm -f path/to/submodule
```

---

### 9. Common Issues & Solutions

#### Permission Issues
```bash
# Fix permission denied
sudo chown -R alexa:alexa .git/

# Fix executable bit issues
git config core.fileMode false
```

#### Authentication Issues
```bash
# Set credential helper
git config --global credential.helper store

# Clear credentials
git credential reject
protocol=https
host=github.com
```

---

### 10. Best Practices

#### Commit Standards
```bash
# Commit message format
type(scope): subject

# Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Adding tests
- chore: Maintenance
```

#### Branch Management
```bash
# Create feature branch
git checkout -b feature/description

# Create research branch
git checkout -b research/topic-name

# Create documentation branch
git checkout -b docs/update-readme
```

---

### 11. Emergency Recovery

#### Lost Changes
```bash
# Find lost commits
git reflog

# Recover deleted branch
git checkout -b recovered-branch commit-hash

# Undo last commit
git reset --soft HEAD~1
```

#### Conflict Resolution
```bash
# Show conflict markers
git diff

# Abort merge
git merge --abort

# Use visual tool
git mergetool
```