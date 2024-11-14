# Cell 1: Imports & Setup
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
```

# Cell 2: Load Data
```python
# Φόρτωση του πλήρους dataset
df = pd.read_csv("data/raw/legal_text_classification.csv")
print(f"Loaded {len(df)} documents")
print("\nColumns:", df.columns.tolist())
print("\nSample sizes:\n", df['case_outcome'].value_counts())
```

# Cell 3: Initial Text Stats
```python
# Βασικά στατιστικά κειμένου
df['text_length'] = df['case_text'].str.len()
df['word_count'] = df['case_text'].str.split().str.len()

print("Text Statistics:")
print(df[['text_length', 'word_count']].describe())
```

# Cell 4: Load Preprocessor
```python
# Import our enhanced preprocessor
from src.core.enhanced_preprocessor import EnhancedLegalTextPreprocessor

# Initialize preprocessor
processor = EnhancedLegalTextPreprocessor()
```

# Cell 5: Process Sample
```python
# Δοκιμή με ένα κείμενο
sample_text = df['case_text'].iloc[0]
result = processor.process_text(sample_text)

print("Sample Processing Results:")
print("\nText Stats:", result['text_stats'])
print("\nCitations Found:", len(result['citations']))
print("\nTemporal Info:", result['temporal_info'])
```

# Cell 6: Batch Processing Test
```python
# Δοκιμή batch processing
test_batch = df['case_text'].head(32).tolist()
batch_results = processor.process_batch(test_batch)

print("Batch Processing Metrics:")
print(batch_results[0]['performance'])
```

# Cell 7: Citation Analysis
```python
# Ανάλυση αναφορών
def analyze_citations(batch_results):
    citation_years = []
    courts = []
    
    for result in batch_results:
        for citation in result['citations']:
            citation_years.append(citation['year'])
            courts.append(citation['court'])
    
    print("Citation Years Range:", min(citation_years), "-", max(citation_years))
    print("\nCourts Found:", pd.Series(courts).value_counts())

analyze_citations(batch_results)
```

# Cell 8: Performance Visualization
```python
# Visualization των μετρικών απόδοσης
processing_times = [r['performance']['processing_time_seconds'] for r in batch_results]

plt.figure(figsize=(10, 5))
plt.hist(processing_times, bins=20)
plt.title('Processing Time Distribution')
plt.xlabel('Seconds')
plt.ylabel('Frequency')
plt.show()
```

# Cell 9: Memory Usage Analysis
```python
# Ανάλυση χρήσης μνήμης
memory_usage = [r['performance']['memory_usage_mb'] for r in batch_results]

print("Memory Usage Statistics:")
print(pd.Series(memory_usage).describe())
```

# Cell 10: Save Results
```python
# Αποθήκευση αποτελεσμάτων
results_df = pd.DataFrame(batch_results)
results_df.to_csv('data/processed/preprocessing_results.csv', index=False)
print("Results saved to preprocessing_results.csv")
```