# CDL6000 Git and Obsidian Setup Guide

## Part 1: Git Initialization

### 1. Navigate to Project Directory
```bash
cd D:/CDL6000-project
```

### 2. Initialize Git Repository
```bash
git init
```

### 3. Configure Git (if not already done)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 4. Add Files to Git
```bash
# Add all files
git add .

# Verify files to be committed
git status
```

### 5. Create Initial Commit
```bash
git commit -m "Initial project setup"
```

## Part 2: GitHub Connection

### 1. Create GitHub Repository
1. Go to GitHub.com and log in
2. Click "New repository"
3. Fill in repository details:
   - Repository name: `CDL6000`
   - Description: "Legal Document Classification System"
   - Visibility: Choose as needed
   - Do NOT initialize with README (we already have one)
   - Do NOT add .gitignore (we already have one)
   - Do NOT add a license file (we already have one)

### 2. Connect Local to Remote
```bash
# Add remote repository
git remote add origin https://github.com/yourusername/CDL6000.git

# Verify remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

### 3. Verify Branch Protection
1. Go to repository settings on GitHub
2. Navigate to Branches
3. Add branch protection rule for `main`:
   - Require pull request reviews
   - Require status checks to pass
   - Include administrators

## Part 3: Obsidian Setup

### 1. Locate Vault Directory
The Obsidian vault is located at:
```
D:/CDL6000-project/docs/obsidian-vault
```

### 2. Open Obsidian
1. Launch Obsidian application
2. Click "Open another vault"
3. Click "Open folder as vault"
4. Navigate to: `D:/CDL6000-project/docs/obsidian-vault`
5. Click "Open"

### 3. Configure Obsidian Settings
1. Open Settings (gear icon)
2. Enable core plugins:
   - File explorer
   - Search
   - Tags pane
   - Page preview
   - Templates

3. Configure Templates:
   - Go to Templates in Settings
   - Set template folder location: `templates`
   - Ensure template folder exists at: `D:/CDL6000-project/docs/obsidian-vault/templates`

### 4. Verify Vault Structure
Your vault should have these directories:
```
obsidian-vault/
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
```

### 5. Test Templates
1. Create a new note
2. Press Ctrl/Cmd + P to open command palette
3. Type "Template" and select "Insert template"
4. Choose a template:
   - meeting-note.md
   - specification.md
   - design-doc.md
   - daily-note.md

## Troubleshooting

### Git Issues
```bash
# If push fails with authentication error
git remote set-url origin https://yourusername@github.com/yourusername/CDL6000.git

# If branch name needs updating
git branch -M main

# If remote URL needs verification
git remote -v
```

### Obsidian Issues
1. If vault doesn't load:
   - Verify path has no special characters
   - Use forward slashes in paths
   - Ensure folder permissions are correct

2. If templates don't appear:
   - Verify template folder name is exactly "templates"
   - Check template folder location in settings
   - Ensure template files end with .md

3. If changes don't sync:
   - Verify .obsidian folder exists in vault
   - Check file permissions
   - Restart Obsidian

## Validation Checklist

### Git Setup ✓
- [ ] Git initialized
- [ ] Files added and committed
- [ ] Remote repository connected
- [ ] Initial push successful
- [ ] Branch protection configured

### Obsidian Setup ✓
- [ ] Vault opened successfully
- [ ] Core plugins enabled
- [ ] Templates configured
- [ ] Directory structure verified
- [ ] Test note created with template
