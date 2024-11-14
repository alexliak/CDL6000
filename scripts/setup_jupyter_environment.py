# scripts/setup_jupyter_environment.py

import subprocess
import sys
import os
import json
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def run_command(command: str) -> bool:
    """Εκτέλεση εντολής και καταγραφή αποτελέσματος"""
    try:
        subprocess.run(command.split(), check=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing {command}: {str(e)}")
        return False


def setup_jupyter_environment():
    """Εγκατάσταση και ρύθμιση Jupyter περιβάλλοντος"""

    logger.info("Starting Jupyter environment setup...")

    # 1. Εγκατάσταση απαραίτητων packages
    packages = [
        "jupyter",
        "notebook",
        "ipykernel",
        "jupyterlab",
        "numpy",
        "pandas",
        "matplotlib",
        "seaborn",
    ]

    logger.info("Installing required packages...")
    for package in packages:
        if not run_command(f"pip install --upgrade {package}"):
            logger.error(f"Failed to install {package}")
            return False

    # 2. Δημιουργία Jupyter kernel για το project
    logger.info("Creating Jupyter kernel...")
    kernel_commands = [
        "python -m ipykernel install --user --name CDL6000 --display-name 'Python (CDL6000)'",
        "jupyter notebook --generate-config",
        "jupyter notebook clean",
    ]

    for cmd in kernel_commands:
        if not run_command(cmd):
            logger.error(f"Failed to execute: {cmd}")
            return False

    # 3. Ρύθμιση VS Code settings
    logger.info("Configuring VS Code settings...")
    vscode_settings = {
        "jupyter.widgetScriptSources": ["jsdelivr.com", "unpkg.com"],
        "jupyter.experiments.enabled": False,
        "jupyter.themeMatplotlibPlots": True,
        "jupyter.askForKernelRestart": False,
        "python.defaultInterpreterPath": str(Path(sys.executable)),
        "jupyter.notebookFileRoot": "${workspaceFolder}",
    }

    # Δημιουργία .vscode directory αν δεν υπάρχει
    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)

    # Ενημέρωση settings.json
    settings_file = vscode_dir / "settings.json"
    if settings_file.exists():
        try:
            with open(settings_file) as f:
                current_settings = json.load(f)
            current_settings.update(vscode_settings)
        except json.JSONDecodeError:
            current_settings = vscode_settings
    else:
        current_settings = vscode_settings

    with open(settings_file, "w") as f:
        json.dump(current_settings, f, indent=4)

    logger.info("Setup completed successfully!")
    logger.info("\nΕπόμενα βήματα:")
    logger.info("1. Κλείστε και ανοίξτε ξανά το VS Code")
    logger.info("2. Επιβεβαιώστε ότι το extension Jupyter είναι εγκατεστημένο")
    logger.info("3. Δοκιμάστε να ανοίξετε ένα notebook")

    return True


if __name__ == "__main__":
    setup_jupyter_environment()
