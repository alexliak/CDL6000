# 🔄 Git Workflow Guide
*Last Updated: 2024-11-14*

## 📋 Daily Git Workflow

### 1️⃣ Initialize Repository (First Time Only)
```bash
# Initialize Git in project directory
git init

# Configure Git (if not already done)
git config --global user.name "your-username"
git config --global credential.helper manager
git config --global credential.helper store
```

### 2️⃣ Stage Changes

#### Method 1: Stage All Changes
```bash
# Stage everything (easiest method)
git add .
```

#### Method 2: Stage by Categories
```bash
# Stage documentation changes
git add "docs/obsidian-vault/**/*.md"

# Stage Python files
git add "src/**/*.py"

# Stage configuration files
git add "*.json"
git add "*.txt"
```

### 3️⃣ Commit Changes
```bash
# Create a semantic commit
git commit -m "type(scope): description

- Detail point 1
- Detail point 2
- Detail point 3"
```

#### 📝 Commit Types
| Type | Usage |
|------|--------|
| `feat` | New features |
| `fix` | Bug fixes |
| `docs` | Documentation |
| `style` | Formatting |
| `refactor` | Code restructuring |
| `test` | Adding tests |
| `chore` | Maintenance |

### 4️⃣ Remote Operations
```bash
# Add remote (first time)
git remote add origin https://github.com/username/repo.git

# Set main branch
git branch -M main

# Push changes
git push -u origin main
```

## 🔍 Common Checks

### Status Check
```bash
# View current status
git status

# View branch information
git branch -v

# View remote information
git remote -v
```

### Common Issues & Solutions

#### 🚫 CRLF Warnings
```plaintext
warning: LF will be replaced by CRLF...
```
➡️ *This is normal on Windows, files will work correctly*

#### 🔄 Remote Already Exists
```bash
# Remove old remote and add new
git remote remove origin
git remote add origin https://github.com/username/repo.git
```

## 📌 Best Practices

### Commit Messages
```bash
# Good Examples
feat(docs): add legal analysis documentation
fix(env): resolve virtual environment path issues
docs(guide): update development workflow
```

### Branch Management
```bash
# Create feature branch
git checkout -b feature/name

# Create documentation branch
git checkout -b docs/section-name

# Switch branches
git checkout main
```

## 🎯 Quick Reference

### Daily Commands
```bash
# Morning Update
git pull origin main

# Check Status
git status

# Stage & Commit
git add .
git commit -m "type(scope): message"

# Push Changes
git push
```

### File Management
```bash
# Stage specific types
git add "**/*.md"    # All markdown
git add "**/*.py"    # All Python
git add "**/*.json"  # All JSON

# Unstage file
git restore --staged <file>
```

## ⚠️ Common Warnings

1. **File not found**
   - Check path spelling
   - Verify file exists
   - Use correct slashes (/)

2. **Ignored Files**
   - Check .gitignore
   - Use -f to force if needed
   - Verify path is correct

3. **Remote Issues**
   - Verify credentials
   - Check remote URL
   - Ensure branch exists

---

*💡 Tip: Keep this guide open in a split pane while working for quick reference*