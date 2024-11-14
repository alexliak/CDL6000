![[]]# 🔧 Ανάλυση & Επίλυση Προβλήματος

## 1. Το Πρόβλημα
```yaml
Error: ModuleNotFoundError: No module named 'src.core.enhanced_preprocessor'
Root Cause:
  - Λάθος δομή project
  - Python path δεν περιλαμβάνει το project root
  - Λάθος imports
```

![[Screenshot 2024-11-14 123642.png]]
## 2. Project Structure
Το σωστό directory structure πρέπει να είναι:
```
CDL6000-project/
├── src/
│   ├── __init__.py  # 👈 Χρειάζεται αυτό
│   └── core/
│       ├── __init__.py  # 👈 Και αυτό
│       └── enhanced_preprocessor.py
├── notebooks/
│   └── 02_text_preprocessing.ipynb
└── data/
    └── raw/
        └── legal_text_classification.csv
```

## 3. Βήματα Επίλυσης

### 3.1 Create __init__.py files
```bash
# Στο root directory του project
touch src/__init__.py
touch src/core/__init__.py
```

### 3.2 Update PYTHONPATH
```python
# Στην αρχή του notebook
import os
import sys
project_root = os.path.abspath(os.path.join(os.getcwd(), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
```

### 3.3 Σωστό Import Statement
```python
# Αντί για
from src.core.enhanced_preprocessor import EnhancedLegalTextPreprocessor

# Χρησιμοποιούμε
from core.enhanced_preprocessor import EnhancedLegalTextPreprocessor
```

## 4. Pipeline Explanation

### 4.1 Data Flow
```mermaid
graph LR
    A[legal_text_classification.csv] --> B[Preprocessor]
    B --> C[Features]
    C --> D[Analysis]
    
    B -->|GPU Acceleration| C
```

### 4.2 Preprocessor Role
```yaml
Input: 
  - Raw legal texts from CSV
Processing:
  - Text cleaning
  - Citation extraction
  - Feature computation
  - GPU acceleration για batch processing
Output:
  - Structured features
  - Performance metrics
```

### 4.3 GPU Usage
- Batch processing των κειμένων
- PyTorch για GPU acceleration
- Memory management για μεγάλα datasets

## 5. Τελικό Notebook Setup

```python
# 1. Setup Path
import os
import sys
project_root = os.path.abspath(os.path.join(os.getcwd(), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# 2. Imports
import pandas as pd
from core.enhanced_preprocessor import EnhancedLegalTextPreprocessor

# 3. Load Data
df = pd.read_csv("../data/raw/legal_text_classification.csv")

# 4. Initialize Preprocessor
processor = EnhancedLegalTextPreprocessor()
```

## 6. Επόμενα Βήματα
1. Verify GPU detection
2. Test batch processing
3. Monitor performance metrics

## 7. Σημείωση για GPU
```python
# Επιβεβαίωση GPU
import torch
print(f"GPU Available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU Device: {torch.cuda.get_device_name(0)}")
    print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
```