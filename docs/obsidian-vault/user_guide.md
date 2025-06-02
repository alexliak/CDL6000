# Οδηγός Χρήσης CDL6000

## 1. Εισαγωγή

Το CDL6000 είναι ένα σύστημα ανάλυσης και ταξινόμησης νομικών εγγράφων που χρησιμοποιεί τεχνικές μηχανικής μάθησης και επεξεργασίας φυσικής γλώσσας. Αυτός ο οδηγός παρουσιάζει τη βασική χρήση του συστήματος και καλύπτει όλες τις κύριες λειτουργίες του.

## 2. Εγκατάσταση

### 2.1 Προαπαιτούμενα

- Python 3.8 ή νεότερη έκδοση
- pip (Python package manager)
- Προαιρετικά: NVIDIA GPU με CUDA για επιτάχυνση

### 2.2 Βήματα Εγκατάστασης

1. Κλωνοποίηση του αποθετηρίου:
   ```bash
   git clone https://github.com/yourusername/CDL6000.git
   cd CDL6000
   ```

2. Δημιουργία εικονικού περιβάλλοντος:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ή
   .\venv\Scripts\activate   # Windows
   ```

3. Εγκατάσταση εξαρτήσεων:
   ```bash
   pip install -r requirements.txt
   ```

4. Έλεγχος εγκατάστασης:
   ```bash
   python src/main.py --version
   ```

## 3. Βασική Χρήση

### 3.1 Έλεγχος Διαθεσιμότητας GPU

Για να ελέγξετε αν το σύστημα μπορεί να χρησιμοποιήσει GPU:

```bash
python src/main.py --gpu-check
```

Έξοδος σε περίπτωση που υπάρχει διαθέσιμη GPU:
```
INFO: CUDA available: True
INFO: CUDA device: NVIDIA GeForce RTX 3080
INFO: GPU memory allocated: 0.0 MB
INFO: GPU memory cached: 0.0 MB
```

### 3.2 Εκτέλεση Επίδειξης

Για να εκτελέσετε μια επίδειξη της λειτουργικότητας του συστήματος με δείγματα δεδομένων:

```bash
python src/main.py --demo
```

Αυτή η εντολή θα εκτελέσει:
1. Προεπεξεργασία δειγμάτων νομικών εγγράφων
2. Εξαγωγή νομικών όρων και παραπομπών
3. Εκπαίδευση και δοκιμή ενός μοντέλου ταξινόμησης

## 4. Χρήση ως Βιβλιοθήκη

Μπορείτε επίσης να χρησιμοποιήσετε το CDL6000 ως βιβλιοθήκη στα δικά σας Python scripts.

### 4.1 Προεπεξεργασία Νομικών Εγγράφων

```python
from src.core.preprocessor import LegalDocumentPreprocessor

# Δημιουργία του preprocessor
preprocessor = LegalDocumentPreprocessor(batch_size=16)

# Επεξεργασία ενός εγγράφου
legal_text = """
[2015] EWHC 123 (Ch)
In the matter of Smith v. Jones Corporation Ltd.
This case concerns a breach of Article 5 of the Commercial Agreement Act of 2010.
"""
features = preprocessor.process_document(legal_text)

# Εμφάνιση των χαρακτηριστικών
print(features)
```

### 4.2 Εξαγωγή Νομικών Όρων

```python
from src.ml.legal_extractor import LegalTermExtractor

# Δημιουργία του extractor
extractor = LegalTermExtractor()

# Εξαγωγή νομικών όρων
legal_text = """
The Court finds that section 15, paragraph 3 of the contract was violated by the defendant.
Prior cases include Brown v. Wilson [2012] UKSC 45 and Roberts v. Thompson [2008] EWCA Civ 23.
"""
legal_terms = extractor.extract_legal_terms(legal_text)

# Εμφάνιση των νομικών όρων
print(legal_terms)

# Πλήρης ανάλυση του εγγράφου
analysis = extractor.analyze_document(legal_text)
print(analysis)
```

### 4.3 Ταξινόμηση Νομικών Εγγράφων

```python
from src.core.classifier import LegalDocumentClassifier

# Δημιουργία και εκπαίδευση ταξινομητή
classifier = LegalDocumentClassifier(algorithm='svm', use_gpu=True)

# Δείγματα για εκπαίδευση
train_texts = [
    "The court finds that the defendant violated section 15 of the contract.",
    "Pursuant to Article 10 of Regulation EC 2015/123, the claim is dismissed.",
    "The plaintiff filed a motion for summary judgment under Rule 56."
]
train_labels = ["Contract", "Regulatory", "Procedural"]

# Εκπαίδευση
metrics = classifier.train(train_texts, train_labels, max_features=1000)
print(f"Accuracy: {metrics['accuracy']:.4f}")

# Πρόβλεψη
new_text = "The appellant contests the decision on grounds of procedural error."
prediction = classifier.predict([new_text])
print(f"Prediction: {prediction[0]}")

# Αποθήκευση μοντέλου
classifier.save_model("models/legal_classifier.joblib")

# Φόρτωση μοντέλου
loaded_classifier = LegalDocumentClassifier()
loaded_classifier.load_model("models/legal_classifier.joblib")
```

### 4.4 Παρακολούθηση Απόδοσης

```python
from src.core.metrics import PerformanceTracker, ClassificationMetrics

# Δημιουργία του performance tracker
tracker = PerformanceTracker()

# Έναρξη παρακολούθησης
tracker.start()

# Εκτέλεση εργασιών...
# ...

# Καταγραφή επεξεργασίας εγγράφου
metrics = tracker.record_document_processed(len(text))
print(f"Processing time: {metrics['processing_time']:.3f}s")
print(f"Memory usage: {metrics['memory_usage_mb']:.2f} MB")

# Εμφάνιση συγκεντρωτικών μετρικών
summary = tracker.get_summary()
print(summary)

# Αποθήκευση μετρικών σε αρχείο
tracker.save_to_file("logs/performance_metrics.json")

# Οπτικοποίηση μετρικών
tracker.plot_metrics("docs/images/performance_plot.png")
```

## 5. Χρήση του Jupyter Notebook

Το CDL6000 περιλαμβάνει ένα Jupyter notebook που επιδεικνύει όλες τις λειτουργίες του συστήματος:

1. Ενεργοποίηση του εικονικού περιβάλλοντος:
   ```bash
   source venv/bin/activate  # Linux/Mac
   # ή
   .\venv\Scripts\activate   # Windows
   ```

2. Εκκίνηση του Jupyter notebook:
   ```bash
   jupyter notebook
   ```

3. Άνοιγμα του notebook `notebooks/legal_document_processing_pipeline.ipynb`

## 6. Προηγμένες Λειτουργίες

### 6.1 Χρήση Εξειδικευμένου Vectorizer

```python
from src.ml.vectorizer import LegalVectorizer

# Δημιουργία του legal vectorizer
vectorizer = LegalVectorizer(max_features=1000, include_legal_features=True)

# Μετατροπή κειμένων σε διανύσματα
texts = [
    "The court finds that the defendant violated section 15 of the contract.",
    "The plaintiff filed a motion for summary judgment under Rule 56."
]
X = vectorizer.fit_transform(texts)

# Εμφάνιση διαστάσεων
print(f"Dimensions: {X.shape}")

# Προβολή των χαρακτηριστικών
feature_names = vectorizer.get_feature_names()
print(f"Feature names: {feature_names}")
```

### 6.2 Σύγκριση Αλγορίθμων Ταξινόμησης

```python
from src.core.classifier import LegalDocumentClassifier
from src.core.metrics import ClassificationMetrics

# Δείγματα για εκπαίδευση και δοκιμή
train_texts = [...]  # Τα δείγματα εκπαίδευσης
train_labels = [...]  # Οι ετικέτες εκπαίδευσης
test_texts = [...]   # Τα δείγματα δοκιμής
test_labels = [...]  # Οι ετικέτες δοκιμής

# Λίστα αλγορίθμων
algorithms = ['svm', 'naive_bayes', 'random_forest']
results = []

# Δημιουργία του metrics calculator
metrics_calc = ClassificationMetrics()

# Δοκιμή κάθε αλγορίθμου
for algorithm in algorithms:
    # Δημιουργία και εκπαίδευση του ταξινομητή
    clf = LegalDocumentClassifier(algorithm=algorithm)
    _ = clf.train(train_texts, train_labels)
    
    # Πρόβλεψη
    predictions = clf.predict(test_texts)
    
    # Υπολογισμός μετρικών
    metrics = metrics_calc.calculate(test_labels, predictions)
    results.append((algorithm, metrics))
    
    print(f"{algorithm} - Accuracy: {metrics['accuracy']:.4f}, F1: {metrics['f1_score']:.4f}")

# Σύγκριση των αλγορίθμων
metrics_calc.compare_models(results, "docs/images/algorithm_comparison.png")
```

## 7. Αντιμετώπιση Προβλημάτων

### 7.1 Συνήθη Προβλήματα

| Πρόβλημα | Πιθανή Αιτία | Λύση |
|----------|--------------|------|
| `ImportError: No module named 'src'` | Το τρέχον directory δεν είναι το root του project | Εκτελέστε την εντολή από το root directory του project |
| `RuntimeError: CUDA error: no CUDA-capable device is detected` | Δεν υπάρχει διαθέσιμη GPU ή δεν έχει εγκατασταθεί το CUDA | Βεβαιωθείτε ότι έχετε GPU και έχετε εγκαταστήσει το CUDA |
| `MemoryError` | Ανεπαρκής μνήμη για την επεξεργασία των δεδομένων | Μειώστε το `batch_size` ή το `max_features` |

### 7.2 Logging και Debugging

Το CDL6000 χρησιμοποιεί το πρότυπο Python logging module. Για να αυξήσετε το επίπεδο λεπτομέρειας:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Τα αρχεία καταγραφής αποθηκεύονται στον φάκελο `logs/`:
- `logs/CDL6000_YYYYMMDD.log`: Γενικά αρχεία καταγραφής
- `logs/performance/`: Μετρικές απόδοσης
- `logs/classification/`: Μετρικές ταξινόμησης

## 8. Παραμετροποίηση

### 8.1 Παράμετροι Προεπεξεργασίας

| Παράμετρος | Περιγραφή | Προεπιλογή |
|------------|-----------|------------|
| `batch_size` | Μέγεθος batch για επεξεργασία | 32 |
| `citation_pattern` | Κανονική έκφραση για παραπομπές | `r"\[\d{4}\]\s+[A-Z]+\s+\d+"` |
| `year_pattern` | Κανονική έκφραση για χρονολογίες | `r"\[(\d{4})\]"` |

### 8.2 Παράμετροι Ταξινόμησης

| Παράμετρος | Περιγραφή | Προεπιλογή |
|------------|-----------|------------|
| `algorithm` | Αλγόριθμος ταξινόμησης | `'svm'` |
| `use_gpu` | Χρήση GPU για επιτάχυνση | `True` |
| `max_features` | Μέγιστος αριθμός χαρακτηριστικών | 10000 |
| `test_size` | Ποσοστό δεδομένων για δοκιμή | 0.2 |

## 9. Πηγές και Αναφορές

- [Scikit-learn Documentation](https://scikit-learn.org/stable/documentation.html)
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)
- [NLTK Documentation](https://www.nltk.org/)
- [Spacy Documentation](https://spacy.io/api/doc)
- [Memory Profiler Documentation](https://pypi.org/project/memory-profiler/)

## 10. Συμβουλές Απόδοσης

1. **Χρήση GPU**: Ενεργοποιήστε τη χρήση GPU για σημαντική επιτάχυνση στην εκπαίδευση των μοντέλων.
2. **Batch Processing**: Χρησιμοποιήστε το batch processing για επεξεργασία μεγάλων συνόλων δεδομένων.
3. **Μείωση Διαστάσεων**: Χρησιμοποιήστε τη μείωση διαστάσεων στον vectorizer για καλύτερη απόδοση.
4. **Caching**: Αποθηκεύστε τα εξαγόμενα χαρακτηριστικά για επαναχρησιμοποίηση.
5. **Προφίλ Μνήμης**: Χρησιμοποιήστε το memory profiling για εντοπισμό διαρροών μνήμης.

## 11. Επικοινωνία και Υποστήριξη

- **GitHub Issues**: [https://github.com/yourusername/CDL6000/issues](https://github.com/yourusername/CDL6000/issues)
- **Email**: support@cdl6000.example.com
- **Documentation**: [https://cdl6000.readthedocs.io/](https://cdl6000.readthedocs.io/)
