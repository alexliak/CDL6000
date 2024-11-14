# Virtual Environment Setup Log
Date: 2024-11-14
Tags: #setup #python #venv

## Current Issue
- VS Code warning about global Python packages
- Need to properly isolate project dependencies

## Correct Setup Steps

### 1. Clean Environment Setup
```bash
# Remove existing env if present
rm -rf env/  # or on Windows: rmdir /s /q env

# Create fresh environment
python -m venv env

# Activate (Windows)
.\env\Scripts\activate

# Verify clean activation
where python  # Should show env path first
```

### 2. Safe Installation Process
```bash
# Upgrade pip first
python -m pip install --upgrade pip setuptools wheel

# Install requirements
pip install -r requirements.txt
```

### 3. VS Code Configuration
1. Select Python Interpreter:
   - Cmd + Shift + P (or Ctrl + Shift + P)
   - "Python: Select Interpreter"
   - Choose `./env/Scripts/python.exe`

2. Update VS Code settings.json:
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/env/Scripts/python.exe",
    "python.terminal.activateEnvironment": true,
    "jupyter.notebookFileRoot": "${workspaceFolder}"
}
```

## Verification Steps
1. [ ] Check Python path
2. [ ] Verify package isolation
3. [ ] Test imports
4. [ ] Configure Jupyter kernel

## Next Actions
1. Run environment verification:
```python
import sys
import pandas as pd
import numpy as np
import torch
print(f"Python: {sys.executable}")
print(f"Pandas: {pd.__version__}")
print(f"NumPy: {np.__version__}")
print(f"PyTorch: {torch.__version__}")
```

2. Setup Jupyter kernel:
```bash
python -m ipykernel install --user --name CDL6000 --display-name "CDL6000 Legal"
```

Status: IN_PROGRESS
Next Review: End of setup