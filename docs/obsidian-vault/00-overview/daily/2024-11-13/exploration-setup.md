# Initial Data Exploration Setup

## 1. Create Jupyter Environment
```bash
# In D:\CDL6000-project
python -m venv env
.\env\Scripts\activate
pip install jupyter pandas numpy scikit-learn matplotlib seaborn spacy
python -m ipykernel install --user --name cdl6000 --display-name "CDL6000 Legal"
```

## 2. Setup First Notebook
Create `notebooks/01_initial_exploration.ipynb`

## 3. Document in Obsidian
Create in `docs/obsidian-vault/daily/2024-11-14-exploration.md`:
```markdown
---
type: exploration
date: 2024-11-14
tags: #data #exploration #initial-analysis
---

# Data Exploration Log

## Setup Completed
- [ ] Jupyter environment
- [ ] Initial notebook
- [ ] Data loading verification

## Next Steps
- [ ] Basic statistics
- [ ] Data quality checks
- [ ] Visualization of key metrics
```