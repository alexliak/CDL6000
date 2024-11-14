# Corrected Git Commands for Your Structure

## Step 1: Check Current Structure
```bash
# First, let's verify where we are
cd D:\CDL6000-project
dir

# Check if we're in the correct location that has the docs/obsidian-vault folder
dir docs\obsidian-vault
```

## Step 2: Stage Files (Corrected Paths)

### Documentation Files
```bash
# Stage files from docs/obsidian-vault directory
git add "docs/obsidian-vault/00-overview/daily/2024-11-13/documentation-structure.md"
git add "docs/obsidian-vault/00-overview/daily/2024-11-13/exploration-setup.md"
git add "docs/obsidian-vault/00-overview/daily/2024-11-13/implementations-steps.md"
git add "docs/obsidian-vault/00-overview/daily/2024-11-13/obsidian-appearance.md"
git add "docs/obsidian-vault/00-overview/daily/2024-11-13/verification-requirements.md"
git add "docs/obsidian-vault/00-overview/daily/2024-11-13/virtual-environment-setup.md"

# Stage 2024-11-14 files
git add "docs/obsidian-vault/00-overview/daily/2024-11-14/legal-analysis.md"
git add "docs/obsidian-vault/00-overview/daily/2024-11-14/legal-citation-pattern-analysis.md"
git add "docs/obsidian-vault/00-overview/daily/2024-11-14/python-environment-extended.md"
git add "docs/obsidian-vault/00-overview/daily/2024-11-14/vs-code-setup-guide.md"
```

### Project Files
```bash
# Stage index files
git add "docs/obsidian-vault/01-specs/index.md"
git add "docs/obsidian-vault/02-design/index.md"
git add "docs/obsidian-vault/03-impl/index.md"
git add "docs/obsidian-vault/04-test/index.md"
git add "docs/obsidian-vault/05-deploy/index.md"
git add "docs/obsidian-vault/06-maintain/index.md"

# Stage other project files
git add "docs/obsidian-vault/01-specs/project-specs.md"
git add "docs/obsidian-vault/02-design/design-doc.md"
git add "docs/obsidian-vault/02-design/proposal.md"
```

### Configuration Files
```bash
# Stage setup and configuration files
git add .gitignore
git add requirements.txt
git add setup_env.ps1
git add setup_env.sh

# Stage VS Code configuration if present
git add .vscode/settings.json
```

## Step 3: Alternative Staging Method
```bash
# If you want to stage all files in the vault (easier method)
git add "docs/obsidian-vault/**/*.md"

# Or stage everything except what's in .gitignore
git add .
```

## Step 4: Create Initial Commit
```bash
git commit -m "feat(initial): setup CDL6000 project structure

- Add Obsidian vault structure with documentation
- Configure development environment
- Setup project specifications and design docs
- Initialize implementation structure

Documentation includes:
- Legal analysis documentation
- Development environment setup
- Project configuration files"
```

## Step 5: Connect to GitHub
```bash
git remote add origin https://github.com/alexliak/CDL6000.git
git branch -M main
git push -u origin main
```

## Daily Workflow (Corrected Paths)
```bash
# Stage daily changes
git add "docs/obsidian-vault/00-overview/daily/$(date +%Y-%m-%d)/*.md"

# Stage specific changes
git add "docs/obsidian-vault/**/*.md"

# Create feature branch
git checkout -b feature/legal-analysis
```

## Verification Commands
```bash
# Check status
git status

# View staged files
git diff --cached --name-only

# Check remote connection
git remote -v
```