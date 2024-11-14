# Daily Development & Maintenance Guide
Version: 1.0.0
Last Updated: 2024-11-14

## 🔄 Daily Workflow Checklist

### 1. Start of Day Checklist
#### Git & GitHub
- [ ] Pull latest changes
```bash
git checkout develop
git pull origin develop
```
- [ ] Check branch status
```bash
git status
git branch -v
```
- [ ] Review open PRs on GitHub
- [ ] Check issue tracker

#### Environment
- [ ] Activate virtual environment
```bash
# Windows
.\venv\Scripts\activate

# Unix
source venv/bin/activate
```
- [ ] Verify Python path
```bash
where python  # Windows
which python  # Unix
```

### 2. Development Standards Checklist
#### Code Quality
- [ ] Follow PEP 8 standards
- [ ] Use type hints
```python
def process_legal_case(case_text: str) -> dict[str, Any]:
    pass
```
- [ ] Write docstrings (Google style)
```python
def analyze_citations(text: str) -> list[str]:
    """Analyzes legal citations in text.

    Args:
        text: The legal text to analyze.

    Returns:
        A list of extracted citations.

    Raises:
        ValueError: If text is empty or invalid.
    """
```

#### Testing Standards
- [ ] Run tests before commits
```bash
pytest tests/
pytest --cov=src tests/
```
- [ ] Update test documentation
- [ ] Verify test coverage

#### Documentation Standards
- [ ] Update daily log in Obsidian
```markdown
---
type: daily-log
date: {{date}}
tags: [development, legal-analysis]
---

## Tasks Completed
- 

## Issues Encountered
- 

## Next Actions
- 
```
- [ ] Link related documents
- [ ] Add code examples

### 3. Version Control Workflow
#### Local Changes
```bash
# Create feature branch
git checkout -b feature/name develop

# Stage changes
git add docs/obsidian-vault/00-overview/daily/$(date +%Y-%m-%d)/*.md
git add src/**/*.py

# Commit
git commit -m "feat(scope): description

- Detail 1
- Detail 2"
```

#### Commit Message Standards
- [ ] Use semantic commit types:
  - `feat`: New feature
  - `fix`: Bug fix
  - `docs`: Documentation
  - `style`: Formatting
  - `refactor`: Code restructuring
  - `test`: Adding tests
  - `chore`: Maintenance

#### GitHub Integration
- [ ] Push changes
```bash
git push -u origin feature/name
```
- [ ] Create pull request
  - Title: Clear description
  - Description: Link to issues
  - Reviewers: Assign team members
  - Labels: Add appropriate labels

### 4. Code Review Checklist
- [ ] Code follows style guide
- [ ] Tests included
- [ ] Documentation updated
- [ ] No sensitive data
- [ ] Error handling present
- [ ] Type hints used
- [ ] Comments clear

### 5. Daily Backup Checklist
- [ ] Commit all documentation changes
- [ ] Push to remote
- [ ] Verify Obsidian Git plugin sync
- [ ] Check backup status

## 🔧 Common Commands Reference

### Git Operations
```bash
# Branch Management
git branch -v                    # List branches
git checkout -b feature/name     # Create branch
git merge --no-ff feature/name   # Merge branch

# Status & History
git status                      # Check status
git log --oneline              # View history
git diff                       # View changes

# Remote Operations
git fetch origin               # Get updates
git pull origin develop        # Pull changes
git push -u origin feature/name # Push branch
```

### Environment Management
```bash
# Virtual Environment
python -m venv venv            # Create
.\venv\Scripts\activate        # Activate (Windows)
pip install -r requirements.txt # Install packages

# Testing
pytest                        # Run tests
pytest --cov=src tests/      # Coverage
```

### VS Code Commands
```bash
code .                       # Open project
Ctrl + Shift + P            # Command palette
Ctrl + Shift + G            # Git panel
Ctrl + `                    # Terminal
```

## 📝 Daily Log Template
```markdown
# Daily Development Log: {{date}}

## Environment Checks
- [ ] Git status clean
- [ ] Virtual environment active
- [ ] Tests passing

## Development Tasks
### Completed
- 

### In Progress
- 

### Blocked
- 

## Code Review Status
- [ ] PRs reviewed
- [ ] Comments addressed
- [ ] Tests verified

## Documentation Updates
- [ ] Daily log created
- [ ] Code documentation updated
- [ ] Wiki pages updated

## Next Day Planning
### Priority Tasks
1. 
2. 
3. 

### Notes for Tomorrow
- 
```

## 🚨 Common Issues & Solutions

### Git Issues
1. Merge Conflicts
```bash
git fetch origin
git rebase origin/develop
# Fix conflicts in files
git add .
git rebase --continue
```

2. Wrong Branch
```bash
git stash
git checkout correct-branch
git stash pop
```

### Environment Issues
1. Package Conflicts
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

2. Virtual Environment Problems
```bash
deactivate
rm -rf venv
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## 📊 Progress Tracking

### Daily Metrics
- [ ] Lines of code added/modified
- [ ] Tests added/modified
- [ ] Documentation pages updated
- [ ] Issues resolved
- [ ] PRs merged

### Weekly Review
- [ ] Code coverage trends
- [ ] Documentation completeness
- [ ] Test suite health
- [ ] Technical debt assessment

## 🔍 Validation Steps

### Before Committing
1. Run static analysis
```bash
black src/
pylint src/
mypy src/
```

2. Run tests
```bash
pytest
pytest --cov=src tests/
```

3. Check documentation
```bash
sphinx-build -b html docs/source docs/build
```

### Before Pull Request
- [ ] Rebase on latest develop
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Add change notes
- [ ] Self-review changes

## 🔄 Automation Scripts

### Quick Status Check
```python
#!/usr/bin/env python
import subprocess
import sys
from pathlib import Path

def check_status():
    """Checks development environment status."""
    checks = {
        "Git Status": ["git", "status"],
        "Test Status": ["pytest", "-v"],
        "Coverage": ["pytest", "--cov=src", "tests/"],
        "Lint": ["pylint", "src/"],
    }
    
    for name, command in checks.items():
        print(f"\n=== {name} ===")
        subprocess.run(command)

if __name__ == "__main__":
    check_status()
```

Save this guide in `docs/obsidian-vault/06-maintain/development-guide.md` and link it to your daily notes for easy reference.

To link in daily notes:
```markdown
[[06-maintain/development-guide|Development Guide]]
```