# src/core/classifier.py
"""
Ταξινομητής νομικών εγγράφων με βελτιστοποίηση GPU και παρακολούθηση απόδοσης.
"""

import logging
import numpy as np
import pandas as pd
import torch
import time
from typing import Dict, List, Tuple, Any, Optional, Union
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, f1_score
from sklearn.model_selection import train_test_split

from src.core.gpu_monitor import GPUMonitor, PerformanceMonitor

# Ρύθμιση logging
logger = logging.getLogger(__name__)


class LegalDocumentClassifier:
    """
    Ταξινομητής νομικών εγγράφων με υποστήριξη πολλαπλών αλγορίθμων και βελτιστοποίηση GPU.
    """
    
    def __init__(self, algorithm: str = 'svm', use_gpu: bool = True):
        """
        Αρχικοποίηση ταξινομητή.
        
        Args:
            algorithm: Ο αλγόριθμος ταξινόμησης ('svm', 'naive_bayes', 'random_forest')
            use_gpu: Αν θα χρησιμοποιηθεί GPU (όπου είναι διαθέσιμο)
        """
        self.algorithm = algorithm
        self.class_names = None
        self.vectorizer = None
        self.model = None
        self.performance_monitor = PerformanceMonitor(logger)
        self.gpu_monitor = GPUMonitor(logger)
        
        # Έλεγχος διαθεσιμότητας GPU
        self.device = torch.device('cuda' if torch.cuda.is_available() and use_gpu else 'cpu')
        logger.info(f"Using device: {self.device}")
        
    def _initialize_model(self):
        """
        Αρχικοποίηση του κατάλληλου μοντέλου με βάση τον επιλεγμένο αλγόριθμο.
        """
        if self.algorithm == 'svm':
            self.model = LinearSVC(C=1.0, class_weight='balanced', max_iter=1000)
        elif self.algorithm == 'naive_bayes':
            self.model = MultinomialNB(alpha=0.1)
        elif self.algorithm == 'random_forest':
            self.model = RandomForestClassifier(n_estimators=100, class_weight='balanced')
        else:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")
    
    def preprocess_and_extract_features(self, texts: List[str], max_features: int = 10000) -> np.ndarray:
        """
        Προεπεξεργασία κειμένων και εξαγωγή χαρακτηριστικών.
        
        Args:
            texts: Λίστα κειμένων
            max_features: Μέγιστος αριθμός χαρακτηριστικών για TF-IDF
            
        Returns:
            Πίνακας χαρακτηριστικών
        """
        if self.vectorizer is None:
            logger.info(f"Initializing TF-IDF vectorizer with max_features={max_features}")
            self.vectorizer = TfidfVectorizer(
                max_features=max_features,
                min_df=2,
                max_df=0.85
            )
            features = self.vectorizer.fit_transform(texts)
        else:
            features = self.vectorizer.transform(texts)
            
        logger.info(f"Extracted {features.shape[1]} features from {len(texts)} documents")
        return features
    
    def train(self, texts: List[str], labels: List[Union[str, int]], 
              max_features: int = 10000, test_size: float = 0.2):
        """
        Εκπαίδευση του ταξινομητή.
        
        Args:
            texts: Λίστα κειμένων εκπαίδευσης
            labels: Λίστα ετικετών (κατηγοριών)
            max_features: Μέγιστος αριθμός χαρακτηριστικών
            test_size: Ποσοστό δεδομένων για έλεγχο
            
        Returns:
            Dictionary με μετρικές απόδοσης
        """
        self.performance_monitor.start_monitoring()
        
        # Κωδικοποίηση των ετικετών σε αριθμούς αν είναι strings
        if isinstance(labels[0], str):
            unique_labels = sorted(set(labels))
            self.class_names = unique_labels
            label_map = {label: i for i, label in enumerate(unique_labels)}
            y = np.array([label_map[label] for label in labels])
        else:
            y = np.array(labels)
            self.class_names = sorted(set(y))
            
        # Διαχωρισμός σε train/test
        X_train_texts, X_test_texts, y_train, y_test = train_test_split(
            texts, y, test_size=test_size, stratify=y, random_state=42
        )
        
        # Εξαγωγή χαρακτηριστικών
        logger.info("Extracting features from training data...")
        X_train = self.preprocess_and_extract_features(X_train_texts, max_features)
        X_test = self.vectorizer.transform(X_test_texts)
        
        # Αρχικοποίηση μοντέλου
        self._initialize_model()
        
        # Εκπαίδευση
        logger.info(f"Training {self.algorithm} model...")
        start_time = time.time()
        self.model.fit(X_train, y_train)
        training_time = time.time() - start_time
        
        # Αξιολόγηση
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        logger.info(f"Model training completed in {training_time:.2f} seconds")
        logger.info(f"Test accuracy: {accuracy:.4f}, F1 score: {f1:.4f}")
        
        # Καταγραφή μετρικών απόδοσης
        metrics = self.performance_monitor.get_metrics()
        
        return {
            'accuracy': accuracy,
            'f1_score': f1,
            'training_time': training_time,
            'performance_metrics': metrics
        }
    
    def predict(self, texts: List[str]) -> List[Union[str, int]]:
        """
        Πρόβλεψη κατηγοριών για νέα κείμενα.
        
        Args:
            texts: Λίστα κειμένων για πρόβλεψη
            
        Returns:
            Λίστα με τις προβλέψεις
        """
        if self.vectorizer is None:
            raise ValueError("Classifier is not trained yet. Call train() first.")
        
        # Εξαγωγή χαρακτηριστικών
        X = self.vectorizer.transform(texts)
        
        # Πρόβλεψη
        predictions = self.model.predict(X)
        
        # Μετατροπή αριθμητικών ετικετών σε ονόματα κλάσεων αν υπάρχουν
        if self.class_names is not None and isinstance(self.class_names[0], str):
            return [self.class_names[pred] for pred in predictions]
        
        return predictions.tolist()
    
    def save_model(self, path: str):
        """
        Αποθήκευση του μοντέλου και του vectorizer.
        
        Args:
            path: Διαδρομή για αποθήκευση
        """
        import joblib
        
        model_info = {
            'algorithm': self.algorithm,
            'vectorizer': self.vectorizer,
            'class_names': self.class_names,
            'model': self.model
        }
            
        joblib.dump(model_info, path)
        logger.info(f"Model saved to {path}")
    
    def load_model(self, path: str):
        """
        Φόρτωση μοντέλου και vectorizer.
        
        Args:
            path: Διαδρομή του αποθηκευμένου μοντέλου
        """
        import joblib
        
        model_info = joblib.load(path)
        
        self.algorithm = model_info['algorithm']
        self.vectorizer = model_info['vectorizer']
        self.class_names = model_info['class_names']
        self.model = model_info['model']
            
        logger.info(f"Model loaded from {path}")
