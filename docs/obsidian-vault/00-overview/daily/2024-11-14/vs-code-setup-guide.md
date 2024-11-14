# VS Code Setup Guide for CDL6000
Version: 1.0.0
Last Updated: 2024-11-14

## 1. VS Code Extensions Setup

### Required Extensions
```json
{
    "recommendations": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-toolsai.jupyter",
        "ms-python.black-formatter",
        "njpwerner.autodocstring",
        "streetsidesoftware.code-spell-checker",
        "eamodio.gitlens",
        "yzhang.markdown-all-in-one"
    ]
}
```

### VS Code Settings (settings.json)
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.formatting.provider": "black",
    "python.formatting.blackPath": "${workspaceFolder}/venv/bin/black",
    "editor.formatOnSave": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.pylintPath": "${workspaceFolder}/venv/bin/pylint",
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

## 2. Environment Setup Scripts

### 2.1 Windows Setup Script (setup_env.ps1)
```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate

# Upgrade pip and install core dependencies
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Install development tools
pip install black pylint pytest jupyter

# Install and register Jupyter kernel
python -m ipykernel install --user --name CDL6000 --display-name "Python (CDL6000)"

# Create VS Code workspace file
@"
{
    "folders": [
        {
            "path": "."
        }
    ],
    "settings": {
        "python.defaultInterpreterPath": "`${workspaceFolder}/venv/Scripts/python.exe"
    }
}
"@ | Out-File -FilePath "CDL6000.code-workspace" -Encoding UTF8
```

### 2.2 Unix Setup Script (setup_env.sh)
```bash
#!/bin/bash

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Upgrade pip and install core dependencies
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Install development tools
pip install black pylint pytest jupyter

# Install and register Jupyter kernel
python -m ipykernel install --user --name CDL6000 --display-name "Python (CDL6000)"

# Create VS Code workspace file
cat > CDL6000.code-workspace << EOL
{
    "folders": [
        {
            "path": "."
        }
    ],
    "settings": {
        "python.defaultInterpreterPath": "\${workspaceFolder}/venv/bin/python"
    }
}
EOL
```

## 3. Project Requirements (requirements.txt)
```txt
# Core ML Dependencies
numpy>=1.21.0
pandas>=1.3.0
scikit-learn>=0.24.2
torch>=1.9.0
transformers>=4.10.0

# NLP Tools
nltk>=3.6.2
spacy>=3.1.0

# Data Processing
tqdm>=4.62.0
python-dotenv>=0.19.0
pyyaml>=5.4.1

# Development Tools
black>=21.7b0
pylint>=2.10.2
pytest>=6.2.5
jupyter>=1.0.0

# Documentation
sphinx>=4.0.2
sphinx-rtd-theme>=0.5.2
```

## 4. Launch Configuration (.vscode/launch.json)
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true,
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        },
        {
            "name": "Python: Legal Classification Pipeline",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/src/main.py",
            "console": "integratedTerminal",
            "justMyCode": true,
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
```

## 5. Testing Configuration (.vscode/settings.json)
```json
{
    "python.testing.pytestArgs": [
        "tests"
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false,
    "python.testing.pytestEnabled": true,
    "python.testing.autoTestDiscoverOnSaveEnabled": true
}
```

## 6. Initial Validation Script (validate_setup.py)
```python
import sys
import pkg_resources
import subprocess
from pathlib import Path

def validate_environment():
    """Validate the development environment setup."""
    checks = {
        "Python Version": check_python_version,
        "Required Packages": check_required_packages,
        "Jupyter Kernel": check_jupyter_kernel,
        "Project Structure": check_project_structure,
        "GPU Availability": check_gpu_availability
    }
    
    results = []
    for check_name, check_func in checks.items():
        try:
            check_func()
            results.append(f"✅ {check_name}: OK")
        except Exception as e:
            results.append(f"❌ {check_name}: Failed - {str(e)}")
    
    return results

def check_python_version():
    required_version = (3, 8)
    current_version = sys.version_info[:2]
    if current_version < required_version:
        raise ValueError(
            f"Python {required_version[0]}.{required_version[1]} or higher required"
        )

def check_required_packages():
    with open("requirements.txt") as f:
        required = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    
    installed = [pkg.key for pkg in pkg_resources.working_set]
    missing = [pkg for pkg in required if pkg.split("==")[0] not in installed]
    
    if missing:
        raise ValueError(f"Missing packages: {', '.join(missing)}")

def check_jupyter_kernel():
    result = subprocess.run(
        ["jupyter", "kernelspec", "list"], 
        capture_output=True, 
        text=True
    )
    if "CDL6000" not in result.stdout:
        raise ValueError("CDL6000 Jupyter kernel not found")

def check_project_structure():
    required_dirs = ["src", "tests", "data", "notebooks", "docs"]
    missing_dirs = [
        dir_name for dir_name in required_dirs 
        if not Path(dir_name).exists()
    ]
    if missing_dirs:
        raise ValueError(f"Missing directories: {', '.join(missing_dirs)}")

def check_gpu_availability():
    try:
        import torch
        if not torch.cuda.is_available():
            raise ValueError("CUDA not available")
        gpu_count = torch.cuda.device_count()
        gpu_name = torch.cuda.get_device_name(0)
        print(f"Found {gpu_count} GPU(s): {gpu_name}")
    except ImportError:
        raise ValueError("PyTorch not installed")

if __name__ == "__main__":
    print("Validating development environment...")
    results = validate_environment()
    for result in results:
        print(result)
```

## 7. Usage Instructions

1. **Initial Setup**:
   ```bash
   # Windows
   .\setup_env.ps1

   # Unix
   chmod +x setup_env.sh
   ./setup_env.sh
   ```

2. **Validate Setup**:
   ```bash
   python validate_setup.py
   ```

3. **VS Code Integration**:
   - Open VS Code
   - File -> Open Workspace from File
   - Select CDL6000.code-workspace

4. **Verify Jupyter Integration**:
   - Open any .ipynb file
   - Select "Python (CDL6000)" kernel
   - Run test cell:
   ```python
   import sys
   print(f"Python {sys.version}")
   ```

## 8. Common Issues & Solutions

1. **Virtual Environment Not Recognized**
   ```bash
   # Windows
   .\venv\Scripts\Activate
   
   # Unix
   source venv/bin/activate
   ```

2. **Jupyter Kernel Not Found**
   ```bash
   python -m ipykernel install --user --name CDL6000 --display-name "Python (CDL6000)"
   ```

3. **PYTHONPATH Issues**
   ```bash
   # Add to .env file
   PYTHONPATH=${workspaceFolder}
   ```

4. **Git Integration**
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```