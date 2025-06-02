#!/usr/bin/env python3
"""
Ανάλυση της Legal Text Database και προετοιμασία για το CDL6000 pipeline
"""

import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_database():
    """Αναλυτική εξερεύνηση της database"""

    # Σύνδεση με τη database
    db_path = Path("data/processed/legal_text.db")
    conn = sqlite3.connect(db_path)

    print("📊 CDL6000 Database Analysis")
    print("=" * 50)

    # 1. Φόρτωση των κύριων δεδομένων
    print("\n1️⃣ Φόρτωση δεδομένων...")
    legal_cases = pd.read_sql_query("SELECT * FROM legal_cases", conn)
    text_metrics = pd.read_sql_query("SELECT * FROM text_metrics", conn)
    data_splits = pd.read_sql_query("SELECT * FROM data_splits", conn)

    print(f"✓ Legal cases: {len(legal_cases):,} εγγραφές")
    print(f"✓ Text metrics: {len(text_metrics):,} εγγραφές")

    # 2. Ανάλυση κατανομής outcomes
    print("\n2️⃣ Κατανομή Case Outcomes:")
    outcome_dist = legal_cases['case_outcome'].value_counts()
    for outcome, count in outcome_dist.items():
        percentage = (count / len(legal_cases)) * 100
        print(f"  - {outcome}: {count:,} ({percentage:.1f}%)")

    # 3. Στατιστικά κειμένου
    print("\n3️⃣ Στατιστικά Κειμένου:")
    print(f"  - Μέσο μήκος: {legal_cases['text_length'].mean():.0f} χαρακτήρες")
    print(f"  - Μέσες λέξεις: {legal_cases['word_count'].mean():.0f}")
    print(f"  - Μέσες παραπομπές: {legal_cases['citation_count'].mean():.1f}")
    print(f"  - Max παραπομπές: {legal_cases['citation_count'].max()}")

    # 4. Ανάλυση splits
    print("\n4️⃣ Data Splits:")
    split_dist = data_splits['split_type'].value_counts()
    for split, count in split_dist.items():
        percentage = (count / len(data_splits)) * 100
        print(f"  - {split}: {count:,} ({percentage:.1f}%)")

    # 5. Έλεγχος για missing values
    print("\n5️⃣ Missing Values Check:")
    missing = legal_cases.isnull().sum()
    for col, count in missing.items():
        if count > 0:
            print(f"  - {col}: {count} missing")
    if missing.sum() == 0:
        print("  ✓ Δεν υπάρχουν missing values!")

    # 6. Δημιουργία visualizations
    print("\n6️⃣ Δημιουργία Visualizations...")
    create_visualizations(legal_cases, text_metrics)

    # 7. Προετοιμασία για ML pipeline
    print("\n7️⃣ Προετοιμασία δεδομένων για ML Pipeline...")
    prepare_ml_data(legal_cases, data_splits, conn)

    conn.close()
    print("\n✅ Ανάλυση ολοκληρώθηκε!")

def create_visualizations(legal_cases, text_metrics):
    """Δημιουργία γραφημάτων"""

    # Δημιουργία φακέλου για visualizations
    viz_dir = Path("data/visualizations")
    viz_dir.mkdir(exist_ok=True, parents=True)

    # 1. Text length distribution
    plt.figure(figsize=(10, 6))
    plt.hist(legal_cases['text_length'], bins=50, edgecolor='black', alpha=0.7)
    plt.xlabel('Text Length (characters)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Legal Text Lengths')
    plt.savefig(viz_dir / 'text_length_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Citation count distribution
    plt.figure(figsize=(10, 6))
    citation_data = legal_cases[legal_cases['citation_count'] <= 50]  # Για καλύτερη οπτικοποίηση
    plt.hist(citation_data['citation_count'], bins=30, edgecolor='black', alpha=0.7)
    plt.xlabel('Citation Count')
    plt.ylabel('Frequency')
    plt.title('Distribution of Citation Counts (≤50)')
    plt.savefig(viz_dir / 'citation_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 3. Outcome distribution pie chart
    plt.figure(figsize=(8, 8))
    outcome_counts = legal_cases['case_outcome'].value_counts()
    plt.pie(outcome_counts.values, labels=outcome_counts.index, autopct='%1.1f%%')
    plt.title('Distribution of Case Outcomes')
    plt.savefig(viz_dir / 'outcome_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"  ✓ Αποθηκεύτηκαν 3 visualizations στο {viz_dir}")

def prepare_ml_data(legal_cases, data_splits, conn):
    """Προετοιμασία δεδομένων για το ML pipeline"""

    # Merge με splits
    ml_data = legal_cases.merge(data_splits, on='case_id')

    # Δημιουργία train/test/val sets
    train_data = ml_data[ml_data['split_type'] == 'train']
    test_data = ml_data[ml_data['split_type'] == 'test']
    val_data = ml_data[ml_data['split_type'] == 'validation']

    print(f"  ✓ Train set: {len(train_data):,} samples")
    print(f"  ✓ Test set: {len(test_data):,} samples")
    print(f"  ✓ Validation set: {len(val_data):,} samples")

    # Αποθήκευση σε CSV για εύκολη πρόσβαση
    output_dir = Path("data/ml_ready")
    output_dir.mkdir(exist_ok=True, parents=True)

    train_data.to_csv(output_dir / 'train.csv', index=False)
    test_data.to_csv(output_dir / 'test.csv', index=False)
    val_data.to_csv(output_dir / 'val.csv', index=False)

    print(f"  ✓ Αποθηκεύτηκαν τα datasets στο {output_dir}")

    # Δημιουργία sample για γρήγορο testing
    sample_data = train_data.sample(n=min(100, len(train_data)), random_state=42)
    sample_data.to_csv(output_dir / 'sample_train.csv', index=False)
    print(f"  ✓ Δημιουργήθηκε sample dataset με 100 εγγραφές")

def check_existing_models():
    """Έλεγχος για υπάρχοντα models"""
    model_dir = Path("models")
    if model_dir.exists():
        models = list(model_dir.glob("*.pkl")) + list(model_dir.glob("*.pt"))
        if models:
            print("\n📦 Βρέθηκαν saved models:")
            for model in models:
                print(f"  - {model.name}")
        else:
            print("\n📦 Δεν βρέθηκαν saved models")

if __name__ == "__main__":
    analyze_database()
    check_existing_models()

    print("\n🚀 Επόμενα Βήματα:")
    print("1. Έλεγξε τα visualizations στο data/visualizations/")
    print("2. Τα ML-ready datasets είναι στο data/ml_ready/")
    print("3. Τρέξε: python src/main.py για να ξεκινήσεις το training")
    print("4. Ή τρέξε το notebook: jupyter notebook notebooks/legal_document_processing_pipeline.ipynb")