#!/bin/bash
# Script για setup του Python environment

echo "🔧 Setting up CDL6000 Python Environment..."

# Έλεγχος αν υπάρχει το venv
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating..."
    python3 -m venv venv
fi

# Ενεργοποίηση venv
echo "🚀 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Εγκατάσταση requirements
echo "📥 Installing requirements..."
pip install numpy>=1.21.0
pip install pandas>=1.3.0
pip install scikit-learn>=0.24.2

# PyTorch με CUDA support (αν έχεις GPU)
echo "🎮 Installing PyTorch..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# NLP packages
echo "📚 Installing NLP packages..."
pip install spacy>=3.1.0
pip install nltk>=3.6.2

# Download spacy model
python -m spacy download en_core_web_sm

# Visualization
echo "📊 Installing visualization packages..."
pip install matplotlib>=3.4.0
pip install seaborn>=0.11.0

# Jupyter
echo "📓 Installing Jupyter..."
pip install jupyter>=1.0.0
pip install ipykernel>=6.0.0

# Development tools
echo "🛠️ Installing development tools..."
pip install black>=21.7b0
pip install flake8>=3.9.2
pip install pytest>=6.2.5
pip install pytest-cov>=2.12.0

# Utilities
echo "🔧 Installing utilities..."
pip install python-dotenv>=0.19.0
pip install pyyaml>=5.4.1
pip install tqdm>=4.62.0

# Documentation (optional)
echo "📚 Installing documentation tools..."
pip install sphinx>=4.0.0
pip install sphinx-rtd-theme>=0.5.2

echo "✅ Environment setup complete!"
echo ""
echo "🔍 Checking installation..."
python -c "import pandas; print(f'✓ Pandas: {pandas.__version__}')"
python -c "import sklearn; print(f'✓ Scikit-learn: {sklearn.__version__}')"
python -c "import torch; print(f'✓ PyTorch: {torch.__version__}')"
python -c "import torch; print(f'✓ CUDA available: {torch.cuda.is_available()}')"

echo ""
echo "📌 To activate this environment in the future, run:"
echo "   source venv/bin/activate"
