# Obsidian Academic Integration Guide
Version: 1.0.1 | Updated: 2024-11-27

## 1. Vault Creation

### 1.1 Initial Setup
1. **Vault Name**: `CLD6000-ANALYSIS`
2. **Location**: `D:\Development\uob-msc-2024\cld6000-analysis`
3. Επιλέξτε "Create"

### 1.2 Υπάρχουσα Δομή Αρχείων
```plaintext
.obsidian/
├── plugins/
│   ├── dataview/         # Δυναμική προβολή δεδομένων
│   ├── graph-analysis/   # Κβαντικό γράφημα
│   └── templater/        # Templates για σημειώσεις
└── research-flow/
    ├── assessment-proposal/
    │   ├── foundation/
    │   │   ├── initial_data_exploration.md
    │   │   └── revised-focus.md
    │   ├── implementation/
    │   │   ├── CLD6000_Legal_Text_Analysis_*.md
    │   │   ├── cld6000-feature-engineering-plan-2024H1.md
    │   │   ├── cld6000-nlp-preprocessing-specs-2024H1.md
    │   │   └── cld6000-technical-foundation-2024H1.md
    │   └── methodology/
    │       ├── markdown-research-guide.md
    │       └── Configuration_Docker_Desktop_with_WSL2.md
    └── documentation/
```

## 2. Σύνδεση Σημειώσεων

### 2.1 Παράδειγμα Σύνδεσης
```markdown
---
title: Initial Data Exploration
date: 2024-11-27
type: foundation
links:
  - [[cld6000-feature-engineering-plan-2024H1]]
  - [[revised-focus]]
---

# Initial Data Exploration

## Related Documents
- Implementation: [[cld6000-feature-engineering-plan-2024H1]]
- Focus Updates: [[revised-focus]]
```

### 2.2 Graph View Setup
1. Άνοιγμα Graph View (Ctrl+G)
2. Filters:
   - Path: `research-flow/assessment-proposal`
   - Tags: `#foundation`, `#implementation`, `#methodology`

## 3. Ανανέωση & Συγχρονισμός

### 3.1 Git Integration
```bash
# Μετά από αλλαγές στο Obsidian
git add .obsidian/
git add "research-flow/"
git commit -m "docs(obsidian): update note connections"
git push origin master
```

### 3.2 Διατήρηση Δομής
- Keep `.gitkeep` στους άδειους φακέλους
- Διατήρηση του παράλληλου `/docs/notes`

## 4. Σημαντικές Σημειώσεις
1. Το vault είναι συγχρονισμένο με το WSL path
2. Οι συνδέσεις διατηρούνται στο Git
3. Παράλληλη δομή με `/docs` για συνέπεια
4. Χρήση plugins για καλύτερη οργάνωση
