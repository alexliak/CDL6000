# Changelog Management

## Template
```markdown
---
type: changelog
version: {{version}}
date: {{date}}
category: [feature|fix|update]
---

# Changelog Entry

## Added
- New feature 1
- New feature 2

## Changed
- Update 1
- Update 2

## Fixed
- Bug fix 1
- Bug fix 2

## Dependencies
- Package update 1
- Package update 2
```

## Example: Feature Update
```markdown
---
type: changelog
version: 1.2.0
date: 2024-11-14
category: feature
---

# Changelog Entry

## Added
- Citation pattern matching
- Performance monitoring

## Changed
- Optimized memory usage
- Updated logging format

## Fixed
- Memory leak in analysis
- Regex pattern timeout

## Dependencies
- Updated spaCy to 3.1.0
- Added pandas 1.3.0
```