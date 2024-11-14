# Sprint Backlog Management

## Template
```markdown
---
type: sprint-backlog
sprint: {{number}}
dates: {{start}}-{{end}}
status: [planning|active|review]
---

# Sprint {{number}} Backlog

## Goals
1. [Primary goal]
2. [Secondary goal]

## User Stories
| ID | Story | Priority | Points |
|----|-------|----------|---------|
| US-01 | Story 1 | High | 5 |
| US-02 | Story 2 | Medium | 3 |

## Technical Tasks
- [ ] Task 1
- [ ] Task 2

## Blockers
- Issue 1
- Issue 2
```

## Example: Sprint Planning
```markdown
---
type: sprint-backlog
sprint: 3
dates: 2024-11-14 - 2024-11-28
status: active
---

# Sprint 3 Backlog

## Goals
1. Implement citation pattern matching
2. Improve performance metrics

## User Stories
| ID | Story | Priority | Points |
|----|-------|----------|---------|
| US-11 | Citation pattern extraction | High | 5 |
| US-12 | Performance monitoring | Medium | 3 |

## Technical Tasks
- [x] Setup regex patterns
- [ ] Implement counters
- [ ] Add monitoring

## Blockers
- Awaiting legal pattern validation
- Performance baseline needed
```