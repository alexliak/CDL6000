# 🔧 Development-Operations Style (DOS-001)
*Version: 1.0.0 | Type: Guide Template | Status: Reference*

## 🎯 Template Purpose
This template is designed for operational documentation, guides, and process documentation requiring clear instructions with visual aids.

## 📋 Front Matter Structure
```yaml
---
type: dev-ops
category: [guide|tutorial|process|log]
status: [active|draft|archived]
last-updated: {{date}}
tags: [tag1, tag2]
---
```

## 🚀 Document Structure
```markdown
# 🔧 [Operation/Component Name]

## 🎯 Quick Reference
> Essential information for quick access

### ⚡ Quick Commands
```bash
command-1 --flag value  # Description
command-2 --flag value  # Description
```

## 📋 Main Content
### 1️⃣ Section One
- Key point
  - Sub-point
  - Example

### 2️⃣ Section Two
1. Step one
   ```bash
   command --flag value
   ```
2. Step two
   - Sub-step A
   - Sub-step B

## ⚠️ Troubleshooting
| Issue | Solution | Priority |
|-------|----------|----------|
| Error 1 | Fix 1 | High |
| Error 2 | Fix 2 | Medium |

## 📊 Status & Metrics
### Key Metrics
- Metric 1: `value`
- Metric 2: `value`

## 📝 Notes & References
- [[link-1|Reference 1]]
- [[link-2|Reference 2]]
```

## 🎨 Style Guidelines

### 1️⃣ Emoji Usage
| Section | Emoji | Usage |
|---------|-------|-------|
| Titles | 🔧 | Main title |
| Quick Reference | 🎯 | Important info |
| Commands | ⚡ | Terminal commands |
| Guides | 📋 | Instructions |
| Warnings | ⚠️ | Important alerts |
| Metrics | 📊 | Data & statistics |
| Notes | 📝 | Additional info |

### 2️⃣ Command Formatting
```markdown
```bash
command --flag value  # Clear description
```   # Indented for sub-steps
```

### 3️⃣ Checklist Format
```markdown
- [ ] Task 1
  - [ ] Sub-task A
  - [ ] Sub-task B
- [ ] Task 2
```

### 4️⃣ Link Structure
```markdown
[[document-name|Display Text]]
[[folder/document|Text]]
```