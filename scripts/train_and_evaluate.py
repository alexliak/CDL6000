#!/usr/bin/env python
# scripts/train_and_evaluate.py
"""
Script για εκπαίδευση και αξιολόγηση ταξινομητή νομικών εγγράφων.
Υποστηρίζει διάφορους αλγορίθμους και παραμέτρους μέσω γραμμής εντολών.

Χρήση:
    python train_and_evaluate.py --algorithm svm --data path/to/data.csv --output path/to/model.pkl
"""

import os
import sys
import logging
import argparse
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix

# Προσθήκη του project root στο Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Ρύθμιση logging
logs_dir = project_root / 'logs'
logs_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(logs_dir / f'training_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Εισαγωγή των modules του project
from src.core.preprocessor import LegalDocumentPreprocessor
from src.core.classifier import LegalDocumentClassifier
from src.core.test_cuda import test_cuda
from src.ml.legal_extractor import LegalTermExtractor
from src.ml.vectorizer import LegalVectorizer


def parse_arguments():
    """Ανάλυση παραμέτρων γραμμής εντολών."""
    parser = argparse.ArgumentParser(description='Train and evaluate legal document classifier')
    
    # Βασικές παράμετροι
    parser.add_argument('--algorithm', type=str, default='svm', 
                        choices=['svm', 'naive_bayes', 'random_forest'],
                        help='Classification algorithm to use')
    parser.add_argument('--data', type=str, required=True,
                        help='Path to CSV data file with text and labels')
    parser.add_argument('--text-column', type=str, default='text',
                        help='Name of column containing document text')
    parser.add_argument('--label-column', type=str, default='label',
                        help='Name of column containing document labels')
    
    # Παράμετροι εκπαίδευσης
    parser.add_argument('--test-size', type=float, default=0.2,
                        help='Fraction of data to use for testing')
    parser.add_argument('--max-features', type=int, default=10000,
                        help='Maximum number of features for vectorization')
    parser.add_argument('--use-gpu', action='store_true',
                        help='Use GPU if available')
    parser.add_argument('--use-legal-features', action='store_true',
                        help='Extract specialized legal features')
    parser.add_argument('--output', type=str,
                        help='Path to save trained model')
    parser.add_argument('--cross-validation', type=int, default=0,
                        help='Number of cross-validation folds (0 to disable)')
    
    return parser.parse_args()


def load_and_prepare_data(args):
    """Φόρτωση και προετοιμασία δεδομένων από αρχείο CSV."""
    logger.info(f"Loading data from {args.data}")
    
    try:
        # Φόρτωση δεδομένων
        df = pd.read_csv(args.data)
        logger.info(f"Loaded {len(df)} documents")
        
        # Έλεγχος στηλών
        if args.text_column not in df.columns:
            raise ValueError(f"Text column '{args.text_column}' not found in data")
        if args.label_column not in df.columns:
            raise ValueError(f"Label column '{args.label_column}' not found in data")
        
        # Αφαίρεση κενών τιμών
        df = df.dropna(subset=[args.text_column, args.label_column])
        logger.info(f"After removing missing values: {len(df)} documents")
        
        # Εξαγωγή κειμένων και ετικετών
        texts = df[args.text_column].tolist()
        labels = df[args.label_column].tolist()
        
        # Έλεγχος ισορροπίας κλάσεων
        label_counts = df[args.label_column].value_counts()
        logger.info(f"Class distribution:\n{label_counts}")
        
        return texts, labels
    
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise


def train_model(texts, labels, args):
    """Εκπαίδευση μοντέλου με τα παρεχόμενα δεδομένα."""
    logger.info(f"Training {args.algorithm} model with {len(texts)} documents")
    
    # Δημιουργία classifier
    classifier = LegalDocumentClassifier(
        algorithm=args.algorithm,
        use_gpu=args.use_gpu
    )
    
    # Προεπεξεργασία εγγράφων
    preprocessor = LegalDocumentPreprocessor()
    
    if args.cross_validation > 1:
        # Εκτέλεση cross-validation
        logger.info(f"Performing {args.cross_validation}-fold cross-validation")
        
        # Η cross-validation γίνεται μέσα στη μέθοδο train που επιστρέφει τις μετρικές
        metrics = classifier.train(
            texts, labels, 
            max_features=args.max_features,
            test_size=args.test_size
        )
        
        logger.info(f"Cross-validation results: {metrics}")
    else:
        # Διαχωρισμός σε train/test
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=args.test_size, random_state=42, stratify=labels
        )
        
        logger.info(f"Training on {len(X_train)} documents, testing on {len(X_test)} documents")
        
        # Εκπαίδευση μοντέλου
        metrics = classifier.train(
            X_train, y_train, 
            max_features=args.max_features
        )
        
        # Αξιολόγηση μοντέλου
        predictions = classifier.predict(X_test)
        
        # Εμφάνιση αναφοράς ταξινόμησης
        report = classification_report(y_test, predictions)
        logger.info(f"Classification report:\n{report}")
    
    # Αποθήκευση μοντέλου αν έχει οριστεί path
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(exist_ok=True, parents=True)
        classifier.save_model(args.output)
        logger.info(f"Model saved to {args.output}")
    
    return classifier, metrics


def main():
    """Κύρια λειτουργία του script."""
    try:
        # Ανάλυση παραμέτρων
        args = parse_arguments()
        
        # Έλεγχος GPU αν ζητηθεί
        if args.use_gpu:
            try:
                test_cuda()
            except Exception as e:
                logger.warning(f"GPU check failed: {str(e)}. Continuing with CPU.")
        
        # Φόρτωση και προετοιμασία δεδομένων
        texts, labels = load_and_prepare_data(args)
        
        # Εκπαίδευση μοντέλου
        classifier, metrics = train_model(texts, labels, args)
        
        logger.info("Training and evaluation completed successfully")
        logger.info(f"Final metrics: {metrics}")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
