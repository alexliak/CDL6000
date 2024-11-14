# Python Environment Setup Guide for CDL6000
Version: 1.0.0
Last Updated: 2024-11-14

## Initial Setup Steps

1. **Create Virtual Environment**
```powershell
# Navigate to project directory
cd D:\CDL6000-project

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate
```

2. **Configure VS Code Python Interpreter**
- Press Ctrl + Shift + P
- Type "Python: Select Interpreter"
- Choose "Python 3.12.7 ('env': venv) from `..\venv\Scripts\python.exe`"
- This is the RECOMMENDED option as it's project-specific

3. **Update Workspace Settings**
Create `.vscode/settings.json` with:
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}\\venv\\Scripts\\python.exe",
    "python.formatting.provider": "black",
    "python.formatting.blackPath": "${workspaceFolder}\\venv\\Scripts\\black.exe",
    "editor.formatOnSave": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.pylintPath": "${workspaceFolder}\\venv\\Scripts\\pylint.exe",
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false,
    "jupyter.notebookFileRoot": "${workspaceFolder}",
    "[python]": {
        "editor.rulers": [88],
        "editor.tabSize": 4,
        "editor.insertSpaces": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    }
}
```

4. **Install Required Packages**
```powershell
# Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# Install core requirements
pip install black pylint pytest jupyter
pip install -r requirements.txt

# Install Jupyter kernel
python -m ipykernel install --user --name CDL6000 --display-name "Python (CDL6000)"
```

## Verification Steps

1. **Verify Python Installation**
```powershell
python --version  # Should show Python 3.12.7
where python     # Should show venv path first
```

2. **Verify Virtual Environment**
```powershell
# Should show (venv) in prompt
.\venv\Scripts\activate
```

3. **Verify VS Code Integration**
- Open a Python file
- Check status bar shows "Python 3.12.7 ('env': venv)"
- Try formatting (Shift + Alt + F)
- Try running a Python file

## Common Issues & Solutions

1. **Invalid Interpreter Selected**
- Make sure virtual environment is activated
- Use full path to Python in venv
- Reload VS Code if needed

2. **Package Installation Issues**
```powershell
# If packages fail to install
python -m pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
```

3. **Path Issues**
- Use Windows-style paths (backslashes)
- Use ${workspaceFolder} for relative paths
- Verify venv is in project directory

## Environment Variables

No need to modify system environment variables. The virtual environment will handle Python path isolation.

## Next Steps

1. Verify installation:
```powershell
python -c "import sys; print(sys.executable)"
# Should point to venv Python
```

2. Test Jupyter integration:
```powershell
jupyter kernelspec list
# Should show CDL6000 kernel
```

3. Test VS Code features:
- IntelliSense
- Code formatting
- Linting
- Debugging