# src/core/metrics.py
"""
Σύστημα παρακολούθησης απόδοσης και μετρικών για το CDL6000.

Παρέχει εργαλεία για:
- Παρακολούθηση χρόνου επεξεργασίας
- Μέτρηση χρήσης μνήμης
- Στατιστικά ακρίβειας ταξινόμησης
- Εξαγωγή μετρικών σε διάφορες μορφές
"""

import time
import json
import logging
import numpy as np
import pandas as pd
import psutil
import torch
import os
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
import matplotlib.pyplot as plt
from pathlib import Path

logger = logging.getLogger(__name__)


class PerformanceTracker:
    """
    Παρακολούθηση απόδοσης του συστήματος CDL6000.
    
    Χαρακτηριστικά:
    - Μέτρηση χρόνου επεξεργασίας ανά έγγραφο
    - Παρακολούθηση χρήσης μνήμης (CPU και GPU)
    - Καταγραφή στατιστικών επεξεργασίας
    - Αποθήκευση και φόρτωση ιστορικών δεδομένων
    """
    
    def __init__(self, log_dir: Optional[str] = None):
        """
        Αρχικοποίηση tracker.
        
        Args:
            log_dir: Προαιρετικός φάκελος για αποθήκευση αρχείων καταγραφής
        """
        self.start_time = None
        self.process = psutil.Process(os.getpid())
        self.use_gpu = torch.cuda.is_available()
        
        # Αρχικοποίηση των μετρήσεων
        self.measurements = {
            'document_times': [],
            'memory_usage': [],
            'document_count': 0,
            'total_time': 0,
            'peak_memory': 0,
            'gpu_memory': [] if self.use_gpu else None,
            'timestamps': []
        }
        
        # Ορισμός του φακέλου καταγραφής
        if log_dir:
            self.log_dir = Path(log_dir)
        else:
            project_root = Path(__file__).parents[2]  # 2 επίπεδα πάνω από το metrics.py
            self.log_dir = project_root / 'logs' / 'performance'
            
        # Δημιουργία του φακέλου αν δεν υπάρχει
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Performance tracker initialized. Log directory: {self.log_dir}")
        logger.info(f"GPU available: {self.use_gpu}")
        
    def start(self) -> None:
        """Έναρξη παρακολούθησης απόδοσης."""
        self.start_time = time.time()
        self.initial_memory = self.process.memory_info().rss / (1024 * 1024)  # MB
        
        # Καταγραφή αρχικής χρήσης GPU αν είναι διαθέσιμο
        if self.use_gpu:
            self.initial_gpu_memory = torch.cuda.memory_allocated() / (1024 * 1024)  # MB
            
        logger.info(f"Performance tracking started. Initial memory: {self.initial_memory:.2f} MB")
        
    def record_document_processed(self, doc_size: int) -> Dict[str, float]:
        """
        Καταγραφή επεξεργασίας ενός εγγράφου.
        
        Args:
            doc_size: Μέγεθος του εγγράφου σε χαρακτήρες
            
        Returns:
            Dictionary με μετρικές για το έγγραφο
        """
        if self.start_time is None:
            self.start()
            
        # Υπολογισμός χρόνου επεξεργασίας
        current_time = time.time()
        processing_time = current_time - self.start_time
        
        # Μέτρηση χρήσης μνήμης
        current_memory = self.process.memory_info().rss / (1024 * 1024)  # MB
        memory_change = current_memory - self.initial_memory
        
        # Μέτρηση χρήσης GPU αν είναι διαθέσιμο
        gpu_memory = None
        if self.use_gpu:
            gpu_memory = torch.cuda.memory_allocated() / (1024 * 1024)  # MB
            gpu_memory_change = gpu_memory - self.initial_gpu_memory
            
        # Ενημέρωση των μετρήσεων
        self.measurements['document_times'].append(processing_time)
        self.measurements['memory_usage'].append(current_memory)
        self.measurements['document_count'] += 1
        self.measurements['total_time'] += processing_time
        self.measurements['peak_memory'] = max(self.measurements['peak_memory'], current_memory)
        self.measurements['timestamps'].append(datetime.now().isoformat())
        
        if self.use_gpu:
            self.measurements['gpu_memory'].append(gpu_memory)
            
        # Καταγραφή σε αρχείο καταγραφής
        self._log_measurement(processing_time, current_memory, doc_size, gpu_memory)
        
        # Επαναφορά του χρόνου έναρξης για το επόμενο έγγραφο
        self.start_time = current_time
        
        # Δημιουργία dictionary με τις μετρικές για το έγγραφο
        metrics = {
            'processing_time': processing_time,
            'memory_usage_mb': current_memory,
            'memory_change_mb': memory_change,
            'doc_size': doc_size,
            'processing_speed': doc_size / processing_time if processing_time > 0 else 0
        }
        
        if self.use_gpu:
            metrics['gpu_memory_mb'] = gpu_memory
            metrics['gpu_memory_change_mb'] = gpu_memory_change
            
        return metrics
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Παραγωγή περίληψης των μετρικών απόδοσης.
        
        Returns:
            Dictionary με συγκεντρωτικές μετρικές
        """
        if not self.measurements['document_count']:
            return {'document_count': 0, 'message': 'No documents processed yet'}
            
        avg_time = np.mean(self.measurements['document_times'])
        std_time = np.std(self.measurements['document_times'])
        avg_memory = np.mean(self.measurements['memory_usage'])
        
        summary = {
            'document_count': self.measurements['document_count'],
            'total_time': self.measurements['total_time'],
            'average_time_per_doc': avg_time,
            'std_time_per_doc': std_time,
            'min_time': min(self.measurements['document_times']),
            'max_time': max(self.measurements['document_times']),
            'average_memory_usage': avg_memory,
            'peak_memory': self.measurements['peak_memory']
        }
        
        if self.use_gpu:
            avg_gpu = np.mean(self.measurements['gpu_memory'])
            peak_gpu = max(self.measurements['gpu_memory'])
            summary['average_gpu_memory'] = avg_gpu
            summary['peak_gpu_memory'] = peak_gpu
            
        return summary
    
    def reset(self) -> None:
        """Επαναφορά όλων των μετρικών."""
        self.start_time = None
        self.measurements = {
            'document_times': [],
            'memory_usage': [],
            'document_count': 0,
            'total_time': 0,
            'peak_memory': 0,
            'gpu_memory': [] if self.use_gpu else None,
            'timestamps': []
        }
        logger.info("Performance tracker reset")
    
    def _log_measurement(self, processing_time: float, memory_usage: float, 
                         doc_size: int, gpu_memory: Optional[float] = None) -> None:
        """
        Καταγραφή μέτρησης σε αρχείο.
        
        Args:
            processing_time: Χρόνος επεξεργασίας σε δευτερόλεπτα
            memory_usage: Χρήση μνήμης σε MB
            doc_size: Μέγεθος εγγράφου σε χαρακτήρες
            gpu_memory: Χρήση μνήμης GPU σε MB (προαιρετικό)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        log_file = self.log_dir / f"performance_log_{datetime.now().strftime('%Y%m%d')}.csv"
        
        # Έλεγχος αν το αρχείο υπάρχει
        file_exists = log_file.exists()
        
        # Προετοιμασία των δεδομένων
        data = {
            'timestamp': timestamp,
            'doc_id': self.measurements['document_count'],
            'processing_time': f"{processing_time:.4f}",
            'memory_usage_mb': f"{memory_usage:.2f}",
            'doc_size': doc_size,
            'chars_per_second': f"{doc_size / processing_time:.2f}" if processing_time > 0 else "0"
        }
        
        if gpu_memory is not None:
            data['gpu_memory_mb'] = f"{gpu_memory:.2f}"
        
        # Εγγραφή στο αρχείο
        with open(log_file, 'a', encoding='utf-8') as f:
            if not file_exists:
                # Προσθήκη επικεφαλίδων αν το αρχείο είναι νέο
                f.write(','.join(data.keys()) + '\n')
            
            # Προσθήκη της νέας γραμμής
            f.write(','.join(str(v) for v in data.values()) + '\n')
    
    def save_to_file(self, filename: Optional[str] = None) -> str:
        """
        Αποθήκευση όλων των μετρικών σε αρχείο JSON.
        
        Args:
            filename: Προαιρετικό όνομα αρχείου
            
        Returns:
            Διαδρομή του αρχείου που δημιουργήθηκε
        """
        if filename is None:
            filename = f"performance_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
        file_path = self.log_dir / filename
        
        # Μετατροπή των numpy arrays σε λίστες για σειριοποίηση JSON
        json_data = {
            'document_count': self.measurements['document_count'],
            'document_times': self.measurements['document_times'],
            'memory_usage': self.measurements['memory_usage'],
            'total_time': self.measurements['total_time'],
            'peak_memory': self.measurements['peak_memory'],
            'timestamps': self.measurements['timestamps'],
            'summary': self.get_summary()
        }
        
        if self.use_gpu and self.measurements['gpu_memory']:
            json_data['gpu_memory'] = self.measurements['gpu_memory']
            
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2)
            
        logger.info(f"Performance metrics saved to {file_path}")
        return str(file_path)
    
    def load_from_file(self, file_path: str) -> Dict[str, Any]:
        """
        Φόρτωση μετρικών από αρχείο JSON.
        
        Args:
            file_path: Διαδρομή του αρχείου JSON
            
        Returns:
            Dictionary με τις φορτωμένες μετρικές
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        self.measurements = {
            'document_times': data.get('document_times', []),
            'memory_usage': data.get('memory_usage', []),
            'document_count': data.get('document_count', 0),
            'total_time': data.get('total_time', 0),
            'peak_memory': data.get('peak_memory', 0),
            'gpu_memory': data.get('gpu_memory', []) if self.use_gpu else None,
            'timestamps': data.get('timestamps', [])
        }
        
        logger.info(f"Performance metrics loaded from {file_path}")
        return data
    
    def plot_metrics(self, save_path: Optional[str] = None) -> None:
        """
        Δημιουργία γραφικών παραστάσεων των μετρικών απόδοσης.
        
        Args:
            save_path: Προαιρετική διαδρομή για αποθήκευση της εικόνας
        """
        if not self.measurements['document_count']:
            logger.warning("No data to plot")
            return
            
        # Δημιουργία του figure με 2 ή 3 subplots
        num_plots = 3 if self.use_gpu else 2
        fig, axes = plt.subplots(num_plots, 1, figsize=(10, 4 * num_plots))
        
        # Δημιουργία x axis
        x = list(range(1, self.measurements['document_count'] + 1))
        
        # Plot 1: Χρόνος επεξεργασίας ανά έγγραφο
        axes[0].plot(x, self.measurements['document_times'])
        axes[0].set_title('Processing Time per Document')
        axes[0].set_xlabel('Document ID')
        axes[0].set_ylabel('Time (seconds)')
        axes[0].grid(True)
        
        # Plot 2: Χρήση μνήμης
        axes[1].plot(x, self.measurements['memory_usage'])
        axes[1].set_title('Memory Usage')
        axes[1].set_xlabel('Document ID')
        axes[1].set_ylabel('Memory (MB)')
        axes[1].grid(True)
        
        # Plot 3: Χρήση GPU (αν είναι διαθέσιμο)
        if self.use_gpu and self.measurements['gpu_memory']:
            axes[2].plot(x, self.measurements['gpu_memory'])
            axes[2].set_title('GPU Memory Usage')
            axes[2].set_xlabel('Document ID')
            axes[2].set_ylabel('GPU Memory (MB)')
            axes[2].grid(True)
            
        plt.tight_layout()
        
        # Αποθήκευση ή εμφάνιση
        if save_path:
            plt.savefig(save_path)
            logger.info(f"Performance plots saved to {save_path}")
        else:
            plt.show()
            

class ClassificationMetrics:
    """
    Υπολογισμός και παρακολούθηση μετρικών απόδοσης για μοντέλα ταξινόμησης.
    
    Χαρακτηριστικά:
    - Υπολογισμός accuracy, precision, recall, F1 score
    - Παραγωγή πίνακα σύγχυσης (confusion matrix)
    - Αναλυτικές αναφορές ανά κατηγορία
    - Αποθήκευση και οπτικοποίηση αποτελεσμάτων
    """
    
    def __init__(self, log_dir: Optional[str] = None):
        """
        Αρχικοποίηση υπολογισμού μετρικών.
        
        Args:
            log_dir: Προαιρετικός φάκελος για αποθήκευση αρχείων καταγραφής
        """
        # Ορισμός του φακέλου καταγραφής
        if log_dir:
            self.log_dir = Path(log_dir)
        else:
            project_root = Path(__file__).parents[2]  # 2 επίπεδα πάνω από το metrics.py
            self.log_dir = project_root / 'logs' / 'classification'
            
        # Δημιουργία του φακέλου αν δεν υπάρχει
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Αρχικοποίηση του ιστορικού μετρικών
        self.history = []
        
        logger.info(f"Classification metrics initialized. Log directory: {self.log_dir}")
        
    def calculate(self, y_true: List, y_pred: List, 
                  class_names: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Υπολογισμός μετρικών απόδοσης ταξινόμησης.
        
        Args:
            y_true: Πραγματικές ετικέτες
            y_pred: Προβλεπόμενες ετικέτες
            class_names: Προαιρετική λίστα με τα ονόματα των κατηγοριών
            
        Returns:
            Dictionary με τις μετρικές
        """
        if len(y_true) != len(y_pred):
            raise ValueError(f"Length mismatch: y_true has {len(y_true)} elements, "
                            f"y_pred has {len(y_pred)} elements")
            
        # Μετατροπή σε numpy arrays για τους υπολογισμούς
        y_true_np = np.array(y_true)
        y_pred_np = np.array(y_pred)
        
        # Βασικές μετρικές
        accuracy = accuracy_score(y_true_np, y_pred_np)
        
        # Ρυθμίσεις για multi-class
        average_method = 'weighted'
        
        # Precision, recall, F1
        precision = precision_score(y_true_np, y_pred_np, average=average_method, zero_division=0)
        recall = recall_score(y_true_np, y_pred_np, average=average_method, zero_division=0)
        f1 = f1_score(y_true_np, y_pred_np, average=average_method, zero_division=0)
        
        # Confusion matrix
        cm = confusion_matrix(y_true_np, y_pred_np)
        
        # Αναλυτική αναφορά ταξινόμησης
        report = classification_report(y_true_np, y_pred_np, 
                                     target_names=class_names, 
                                     output_dict=True)
        
        # Συγκέντρωση των αποτελεσμάτων
        results = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'confusion_matrix': cm.tolist(),
            'classification_report': report,
            'timestamp': datetime.now().isoformat()
        }
        
        # Προσθήκη στο ιστορικό
        self.history.append(results)
        
        return results
    
    def log_results(self, results: Dict[str, Any], model_name: str) -> str:
        """
        Καταγραφή αποτελεσμάτων σε αρχείο.
        
        Args:
            results: Dictionary με τις μετρικές απόδοσης
            model_name: Όνομα του μοντέλου
            
        Returns:
            Διαδρομή του αρχείου καταγραφής
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{model_name}_metrics_{timestamp}.json"
        file_path = self.log_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
            
        logger.info(f"Classification metrics for {model_name} saved to {file_path}")
        
        return str(file_path)
    
    def plot_confusion_matrix(self, results: Dict[str, Any], class_names: List[str], 
                             model_name: str, save_path: Optional[str] = None) -> None:
        """
        Δημιουργία οπτικοποίησης του πίνακα σύγχυσης.
        
        Args:
            results: Dictionary με τις μετρικές απόδοσης
            class_names: Λίστα με τα ονόματα των κατηγοριών
            model_name: Όνομα του μοντέλου
            save_path: Προαιρετική διαδρομή για αποθήκευση της εικόνας
        """
        cm = np.array(results['confusion_matrix'])
        
        # Δημιουργία της εικόνας
        plt.figure(figsize=(10, 8))
        plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title(f'Confusion Matrix - {model_name}')
        plt.colorbar()
        
        # Ρύθμιση των tick marks
        tick_marks = np.arange(len(class_names))
        plt.xticks(tick_marks, class_names, rotation=45)
        plt.yticks(tick_marks, class_names)
        
        # Εμφάνιση των τιμών
        thresh = cm.max() / 2.
        for i, j in np.ndindex(cm.shape):
            plt.text(j, i, format(cm[i, j], 'd'),
                   horizontalalignment="center",
                   color="white" if cm[i, j] > thresh else "black")
            
        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        
        # Αποθήκευση ή εμφάνιση
        if save_path:
            plt.savefig(save_path)
            logger.info(f"Confusion matrix plot saved to {save_path}")
        else:
            plt.show()
    
    def plot_metrics_history(self, save_path: Optional[str] = None) -> None:
        """
        Δημιουργία γραφικών παραστάσεων του ιστορικού μετρικών.
        
        Args:
            save_path: Προαιρετική διαδρομή για αποθήκευση της εικόνας
        """
        if not self.history:
            logger.warning("No metrics history to plot")
            return
            
        # Εξαγωγή των μετρικών από το ιστορικό
        timestamps = [i for i in range(len(self.history))]
        accuracy = [entry['accuracy'] for entry in self.history]
        precision = [entry['precision'] for entry in self.history]
        recall = [entry['recall'] for entry in self.history]
        f1 = [entry['f1_score'] for entry in self.history]
        
        # Δημιουργία του figure
        plt.figure(figsize=(12, 6))
        
        plt.plot(timestamps, accuracy, 'o-', label='Accuracy')
        plt.plot(timestamps, precision, 's-', label='Precision')
        plt.plot(timestamps, recall, '^-', label='Recall')
        plt.plot(timestamps, f1, 'd-', label='F1 Score')
        
        plt.title('Classification Metrics History')
        plt.xlabel('Experiment')
        plt.ylabel('Score')
        plt.grid(True)
        plt.legend()
        
        # Αποθήκευση ή εμφάνιση
        if save_path:
            plt.savefig(save_path)
            logger.info(f"Metrics history plot saved to {save_path}")
        else:
            plt.show()
    
    def compare_models(self, model_results: List[Tuple[str, Dict[str, Any]]], 
                      save_path: Optional[str] = None) -> None:
        """
        Σύγκριση μετρικών απόδοσης διαφόρων μοντέλων.
        
        Args:
            model_results: Λίστα με tuples (model_name, results)
            save_path: Προαιρετική διαδρομή για αποθήκευση της εικόνας
        """
        if not model_results:
            logger.warning("No model results to compare")
            return
            
        # Εξαγωγή των δεδομένων
        model_names = [model[0] for model in model_results]
        accuracy = [model[1]['accuracy'] for model in model_results]
        precision = [model[1]['precision'] for model in model_results]
        recall = [model[1]['recall'] for model in model_results]
        f1 = [model[1]['f1_score'] for model in model_results]
        
        # Δημιουργία του dataframe
        data = {
            'Model': model_names,
            'Accuracy': accuracy,
            'Precision': precision,
            'Recall': recall,
            'F1 Score': f1
        }
        
        df = pd.DataFrame(data)
        
        # Εμφάνιση ως πίνακα
        print("Model Comparison:")
        print(df)
        
        # Δημιουργία του γραφήματος
        metrics = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
        
        plt.figure(figsize=(14, 8))
        
        x = np.arange(len(model_names))
        width = 0.2
        
        for i, metric in enumerate(metrics):
            plt.bar(x + i*width, df[metric], width, label=metric)
            
        plt.xlabel('Models')
        plt.ylabel('Score')
        plt.title('Model Comparison')
        plt.xticks(x + width*1.5, model_names)
        plt.legend(loc='lower right')
        plt.ylim(0, 1.0)
        plt.grid(axis='y')
        
        # Αποθήκευση ή εμφάνιση
        if save_path:
            plt.savefig(save_path)
            logger.info(f"Model comparison plot saved to {save_path}")
        else:
            plt.show()
            
        # Επιστροφή του "καλύτερου" μοντέλου (με βάση το F1 score)
        best_model_idx = np.argmax(f1)
        logger.info(f"Best model (F1 Score): {model_names[best_model_idx]} "
                  f"(F1: {f1[best_model_idx]:.4f})")
