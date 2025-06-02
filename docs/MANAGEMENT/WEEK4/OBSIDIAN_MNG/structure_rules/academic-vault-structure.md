# Academic Year 2024-2025 Vault Structure

## Root Structure
```
2024/
└── FALL/
    ├── 00-academic-hub/          # Central dashboard and navigation
    ├── CLD6000/                  # Contemporary Problem Analysis
    ├── CLD6001/                  # Undergraduate Research Project
    ├── SWE6002/                  # Enterprise Systems Development
    └── _resources/               # Shared resources across courses

## Per Course Structure (Example for CLD6000)
CLD6000/
├── 00-course-hub/               # Course overview & tracking
│   ├── _index.md               # Quick links & overview
│   ├── grade-requirements.md   # Assessment criteria tracking
│   └── timeline.md            # Key dates & milestones
│
├── 01-research/                # Research materials
│   ├── literature/            # Literature review
│   ├── papers/               # Key papers and sources
│   └── notes/                # Research notes
│
├── 02-development/            # Implementation work
│   ├── code/                 # Source code
│   ├── notebooks/            # Jupyter notebooks
│   └── experiments/          # Test results
│
├── 03-documentation/          # Project documentation
│   ├── api/                  # API documentation
│   ├── system-design/        # Design documents
│   └── user-guides/          # Usage documentation
│
├── 04-deliverables/          # Assessment submissions
│   ├── assessment-001/       # Per assessment folder
│   ├── presentations/        # Presentation materials
│   └── final-report/        # Final report drafts
│
├── 05-weekly-logs/           # Progress tracking
│   ├── week-01.md           # Weekly progress
│   └── weekly-template.md   # Log template
│
└── 06-meetings/              # Meeting notes
    ├── supervisor/          # Supervisor meetings
    └── team/               # Team meetings

## Dissertation Structure (CLD6001)
CLD6001/
├── 00-thesis-hub/
│   ├── _index.md
│   ├── timeline.md
│   └── objectives.md
│
├── 01-proposal/              # Assessment 1
│   ├── drafts/
│   ├── research/
│   └── presentation/
│
├── 02-research/              # Main research
│   ├── literature-review/
│   ├── methodology/
│   └── data-collection/
│
├── 03-implementation/        # Assessment 2
│   ├── code/
│   ├── experiments/
│   └── results/
│
├── 04-thesis/               # Assessment 3
│   ├── chapters/
│   ├── figures/
│   └── references/
│
└── 05-defense/              # Final presentation
    ├── slides/
    └── notes/
```

## Key Files & Templates

1. Weekly Log Template (`weekly-template.md`):
```markdown
# Week X (YYYY-MM-DD to YYYY-MM-DD)

## Objectives
- [ ] Objective 1
- [ ] Objective 2

## Progress
### Research
- 

### Implementation
- 

### Documentation
- 

## Challenges & Solutions
| Challenge | Solution | Status |
|-----------|----------|---------|
|           |          |         |

## Time Tracking
- Research: Xh
- Development: Yh
- Documentation: Zh

## Next Steps
1. 
2. 
3. 

## Resources
- [[Related Documents]]
- [[Code References]]
```

2. Assessment Tracking (`grade-requirements.md`):
```markdown
# Assessment Grade Tracking

## Assessment 001 (XX%)
### Requirements
- [ ] Requirement 1
- [ ] Requirement 2

### Grading Criteria
- [ ] Relevance (15%)
- [ ] Knowledge (20%)
- [ ] Analysis (20%)
- [ ] Structure (10%)
- [ ] Presentation (15%)
- [ ] Written English (10%)
- [ ] Research/Referencing (10%)

### References
- [ ] 3+ refereed academic journals
- [ ] 5+ academic books
- [ ] 15-20 total sources
```

3. Research Note Template (`research-template.md`):
```markdown
# Paper Title

## Citation
[Harvard format citation]

## Key Points
- 

## Relevance to Project
- 

## Methodology Used
- 

## Results
- 

## Quotes
> Important quote

## Notes
- 

## Links to Other Research
- [[Related Paper 1]]
- [[Related Paper 2]]
```