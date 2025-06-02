# Obsidian Reorganization Plan

## Current Structure
```
CLD6000Contemporary_Problem_Analysis_Fall24/
├── 2024/
│   └── FALL/
│       └── CLD6000/
│           └── .obsidian/
├── COURSE_MATERIAL/
├── DATASETS/
├── DELIVERABLES/
├── FOLDERS_MEDIA/
├── MANAGEMENT/
└── RESEARCH_MATERIAL/
```

## Recommended Structure
```
CLD6000Contemporary_Problem_Analysis_Fall24/
└── 2024/
    └── FALL/
        └── CLD6000/           # This becomes your Obsidian vault root
            ├── .obsidian/     # Obsidian config
            ├── course/        # Move from COURSE_MATERIAL
            ├── data/          # Move from DATASETS
            ├── deliverables/  # Move from DELIVERABLES
            ├── media/         # Move from FOLDERS_MEDIA
            ├── management/    # Move from MANAGEMENT
            └── research/      # Move from RESEARCH_MATERIAL
```

## Steps to Reorganize

1. In File Explorer:
```
1. Navigate to CLD6000Contemporary_Problem_Analysis_Fall24/2024/FALL/CLD6000
2. Move all folders from root into this directory:
   - COURSE_MATERIAL → course/
   - DATASETS → data/
   - DELIVERABLES → deliverables/
   - FOLDERS_MEDIA → media/
   - MANAGEMENT → management/
   - RESEARCH_MATERIAL → research/
```

2. In Obsidian:
```
1. Open Obsidian
2. Select "Open folder as vault"
3. Navigate to: .../2024/FALL/CLD6000
4. Select this folder as your vault
```

3. Verify Structure:
```
1. Check all files are accessible in Obsidian
2. Verify all links still work
3. Update any broken paths
```

## New Obsidian Configuration

1. Core Settings:
```markdown
- Files & Links:
  ✓ Default location for attachments: In subfolder under current folder
  ✓ Subfolder name: _attachments
  ✓ Show file extensions: enabled
```

2. Create Index Files:
```markdown
Create an index.md in each main folder:
- course/index.md
- data/index.md
- deliverables/index.md
- media/index.md
- management/index.md
- research/index.md
```

3. Root README:
```markdown
Create a README.md in CLD6000 folder:
- Project overview
- Folder structure explanation
- Quick links to main sections
```