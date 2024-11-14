# System Logging Guide

## Template
```markdown
---
type: system-log
date: {{date}}
component: [service-name]
severity: [critical|warning|info]
---

# System Log Entry

## Event Details
- Time: {{time}}
- Component: {{component}}
- Status: [active|resolved]

## Description
[Brief description of the event]

## Impact
- Service Impact:
- User Impact:

## Resolution
- [ ] Steps taken
- [ ] Verification

## Follow-up
- [ ] Required actions
```

## Example: Error Log
```markdown
---
type: system-log
date: 2024-11-14
component: citation-analyzer
severity: warning
---

# System Log Entry

## Event Details
- Time: 14:30 UTC
- Component: Citation Analysis Service
- Status: resolved

## Description
Memory usage spike during large document processing

## Impact
- Service Impact: 30sec processing delay
- User Impact: 3 user requests queued

## Resolution
- [x] Increased memory allocation
- [x] Verified service recovery

## Follow-up
- [ ] Implement memory optimization
- [ ] Add monitoring alert
```