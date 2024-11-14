# Development Notes Guide

## Template
```markdown
---
type: dev-note
date: {{date}}
feature: [feature-name]
status: [planning|implementing|testing]
---

# Development Note: {{feature}}

## Overview
Brief description

## Technical Details
```python
# Code example
```

## Testing Notes
- [ ] Test case 1
- [ ] Test case 2

## Questions/Issues
- Question 1
- Issue 1
```

## Example: Feature Development
```markdown
---
type: dev-note
date: 2024-11-14
feature: citation-analyzer
status: implementing
---

# Development Note: Citation Pattern Matching

## Overview
Implementing regex-based legal citation extraction

## Technical Details
```python
citation_pattern = r'\[\d{4}\]\s+[A-Z]+\s+\d+'
matches = re.findall(citation_pattern, text)
```

## Testing Notes
- [x] Basic pattern matching
- [ ] Edge case handling
- [ ] Performance testing

## Questions/Issues
- Handle multi-line citations?
- Optimize regex pattern
```