# 📚 Implementation Guide: Legal Document Analysis
*Οδηγός Υλοποίησης: Ανάλυση Νομικών Εγγράφων*

## 🎯 Βασικά Στάδια Υλοποίησης

### 1️⃣ Προετοιμασία & Εξερεύνηση Δεδομένων
```python
# notebook: 01_data_exploration.ipynb

# 1. Βασικές βιβλιοθήκες
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# 2. Φόρτωση δεδομένων
df = pd.read_csv("data/raw/legal_cases.csv")

# 3. Βασική ανάλυση
def analyze_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Ανάλυση βασικών χαρακτηριστικών του dataset
    
    Μετρικές:
    - Κατανομή κατηγοριών
    - Στατιστικά μήκους κειμένου
    - Έλεγχος ελλιπών τιμών
    """
    analysis = {
        'total_cases': len(df),
        'missing_values': df.isnull().sum(),
        'text_length_stats': df['case_text'].str.len().describe(),
        'outcome_distribution': df['case_outcome'].value_counts()
    }
    return analysis

# 4. Οπτικοποίηση
def plot_distributions(df: pd.DataFrame) -> None:
    """
    Οπτικοποίηση βασικών κατανομών
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Κατανομή μήκους κειμένου
    df['text_length'].hist(bins=50, ax=ax1)
    ax1.set_title('Κατανομή Μήκους Κειμένου')
    
    # Κατανομή κατηγοριών
    df['case_outcome'].value_counts().plot(kind='bar', ax=ax2)
    ax2.set_title('Κατανομή Κατηγοριών')
```

### 2️⃣ Εξαγωγή Νομικών Χαρακτηριστικών
```python
# notebook: 02_feature_extraction.ipynb

# 1. Εξαγωγή αναφορών (citations)
def extract_legal_features(text: str) -> Dict[str, Any]:
    """
    Εξαγωγή νομικών χαρακτηριστικών από κείμενο
    
    Χαρακτηριστικά:
    - Αναφορές σε νόμους
    - Δικαστικές αποφάσεις
    - Νομικοί όροι
    """
    features = {
        'citations': extract_citations(text),
        'legal_terms': extract_legal_terms(text),
        'case_references': extract_case_refs(text)
    }
    return features

# 2. Υπολογισμός στατιστικών
def calculate_legal_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Υπολογισμός νομικών μετρικών
    
    Μετρικές:
    - Πλήθος αναφορών
    - Συχνότητα νομικών όρων
    - Σχέσεις μεταξύ υποθέσεων
    """
    metrics = pd.DataFrame()
    metrics['citation_count'] = df['case_text'].apply(
        lambda x: len(extract_citations(x))
    )
    return metrics
```

### 3️⃣ Προετοιμασία για Μοντελοποίηση
```python
# notebook: 03_model_preparation.ipynb

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

def prepare_for_modeling(df: pd.DataFrame) -> Tuple[np.array, np.array]:
    """
    Προετοιμασία δεδομένων για εκπαίδευση
    
    Διαδικασία:
    1. Καθαρισμός κειμένου
    2. Vectorization
    3. Train-test split
    """
    # Vectorization
    vectorizer = TfidfVectorizer(
        max_features=5000,
        stop_words='english'
    )
    
    X = vectorizer.fit_transform(df['case_text'])
    y = df['case_outcome']
    
    return train_test_split(X, y, test_size=0.15, random_state=42)
```

### 4️⃣ Εκπαίδευση & Αξιολόγηση
```python
# notebook: 04_model_training.ipynb

from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report

def train_evaluate_model(X_train, X_test, y_train, y_test):
    """
    Εκπαίδευση και αξιολόγηση μοντέλου
    
    Στόχοι:
    - Ακρίβεια > 75%
    - F1 Score > 0.74
    - Χρόνος εκπαίδευσης < 10 λεπτά
    """
    model = LinearSVC(random_state=42)
    
    # Καταγραφή χρόνου εκπαίδευσης
    start_time = time.time()
    model.fit(X_train, y_train)
    train_time = time.time() - start_time
    
    # Αξιολόγηση
    y_pred = model.predict(X_test)
    performance = classification_report(y_test, y_pred, output_dict=True)
    
    return {
        'model': model,
        'training_time': train_time,
        'performance': performance
    }
```

## 📊 Αναμενόμενα Αποτελέσματα

### 1. Κατανομή Δεδομένων
```yaml
Dataset Stats:
  Total Cases: ~25,000
  Categories: 10
  Avg Text Length: ~2,500 words
  Missing Values: <1%

Expected Patterns:
  - Ανισορροπία κατηγοριών (60-20-20)
  - Μεγάλη διακύμανση μήκους κειμένου
  - Συσχέτιση μεταξύ μήκους και κατηγορίας
```

### 2. Νομικά Χαρακτηριστικά
```yaml
Citation Patterns:
  - ~5-15 citations per document
  - Χρονική κατανομή αναφορών
  - Συσχέτιση με case outcome

Legal Terms:
  - Συχνότητα εμφάνισης
  - Κατηγοριοποίηση όρων
  - Σημασιολογική ανάλυση
```

### 3. Απόδοση Μοντέλου
```yaml
Performance Targets:
  Accuracy: >75%
  F1 Score: >0.74
  Processing: <2s/document
  
Resource Usage:
  Memory: <4.5GB
  GPU: <80%
  Training Time: <10min
```

## 🔧 Τεχνικές Προδιαγραφές

### Jupyter Notebook Setup
```python
# Στην αρχή κάθε notebook
%matplotlib inline
%load_ext memory_profiler
%config InlineBackend.figure_format = 'retina'

# Καταγραφή χρόνου και μνήμης
from memory_profiler import profile

@profile
def process_function():
    pass
```

### Data Processing Pipeline
```python
# Τυπική ροή επεξεργασίας
def process_legal_document(text: str) -> Dict[str, Any]:
    """
    Πλήρης επεξεργασία νομικού κειμένου
    
    Βήματα:
    1. Καθαρισμός & προεπεξεργασία
    2. Εξαγωγή χαρακτηριστικών
    3. Ανάλυση & μετρικές
    """
    clean_text = preprocess_text(text)
    features = extract_features(clean_text)
    metrics = calculate_metrics(features)
    
    return {
        'features': features,
        'metrics': metrics
    }
```

## 📈 Παρακολούθηση Προόδου

### Μετρικές Απόδοσης
```python
def track_performance(func):
    """
    Decorator για παρακολούθηση απόδοσης
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        
        print(f"Execution time: {execution_time:.2f} seconds")
        print(f"Memory usage: {get_memory_usage():.2f} MB")
        
        return result
    return wrapper
```

### Αναφορά Προόδου
```markdown
# Progress Report [Date]

## Μετρικές
- Ακρίβεια: X%
- F1 Score: X
- Χρόνος επεξεργασίας: Xs/document

## Επόμενα Βήματα
1. [Επόμενη εργασία]
2. [Προτεραιότητες]
```