#!/usr/bin/env python3
# scripts/performance_benchmark.py
"""
Benchmark επιδόσεων για το CDL6000 project.

Χρήση:
    python performance_benchmark.py --batch-size 32 --documents 100 --algorithm svm
    
Αυτό το script εκτελεί:
1. Παραγωγή δοκιμαστικών δεδομένων συγκεκριμένου μεγέθους
2. Μέτρηση χρόνου επεξεργασίας ανά έγγραφο
3. Παρακολούθηση χρήσης μνήμης (CPU και GPU)
4. Εξαγωγή αναφοράς επιδόσεων σε μορφή JSON/CSV
"""

import os
import sys
import argparse
import time
import json
import csv
import psutil
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
import logging
import tracemalloc
import gc

# Προσθήκη του project root στο path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Εισαγωγή των modules του project
from src.core.preprocessor import LegalDocumentPreprocessor
from src.core.classifier import LegalDocumentClassifier
from src.ml.legal_extractor import LegalTermExtractor
from src.core.test_cuda import test_cuda
from src.core.gpu_monitor import GPUMonitor

# Ρύθμιση logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def generate_test_documents(num_documents, length_range=(500, 2000)):
    """
    Παραγωγή δοκιμαστικών νομικών εγγράφων για benchmark.
    
    Args:
        num_documents: Αριθμός εγγράφων
        length_range: Εύρος μήκους κειμένου (min, max χαρακτήρες)
        
    Returns:
        List με δοκιμαστικά νομικά κείμενα
    """
    logger.info(f"Generating {num_documents} test documents...")
    
    # Νομική ορολογία για δοκιμαστικά έγγραφα
    legal_terms = {
        'courts': ['Supreme Court', 'High Court', 'Court of Appeal', 'District Court', 
                 'Circuit Court', 'Tribunal', 'Magistrates Court'],
        'citations': ['[2020] UKSC 45', '[2019] EWCA Civ 1234', '[2018] EWHC 567 (Ch)', 
                     '[2021] UKUT 123', '[2017] 2 Lloyd\'s Rep 1'],
        'acts': ['Data Protection Act 2018', 'Companies Act 2006', 'Human Rights Act 1998',
               'Criminal Justice Act 2003', 'Employment Rights Act 1996'],
        'legal_phrases': ['breach of contract', 'reasonable doubt', 'beyond reasonable doubt',
                        'balance of probabilities', 'burden of proof', 'duty of care',
                        'judicial review', 'summary judgment', 'force majeure']
    }
    
    # Πρότυπες προτάσεις νομικών εγγράφων
    templates = [
        "The {court} in the case of {citation} ruled that {legal_phrase}.",
        "According to section 15 of the {act}, the defendant must prove {legal_phrase}.",
        "The claimant argued that under {citation}, the principle of {legal_phrase} applies.",
        "In {citation}, the {court} established the test for {legal_phrase}.",
        "The {court} rejected the application of {legal_phrase} in the context of {act}.",
        "The judge referred to {citation} where the {court} discussed {legal_phrase}.",
        "Under {act}, there is a statutory obligation to consider {legal_phrase}.",
        "The {court} in {citation} overturned the previous decision regarding {legal_phrase}."
    ]
    
    documents = []
    categories = ['Contract', 'Tort', 'Criminal', 'Family', 'Property', 
                 'Employment', 'Tax', 'Administrative', 'Competition', 'Intellectual Property']
    
    for i in range(num_documents):
        category = categories[i % len(categories)]
        length = np.random.randint(length_range[0], length_range[1])
        
        # Δημιουργία εγγράφου από πρότυπες προτάσεις
        doc_lines = []
        current_length = 0
        
        # Προσθήκη τίτλου και κατηγορίας
        doc_lines.append(f"LEGAL DOCUMENT {i+1}")
        doc_lines.append(f"Category: {category}")
        doc_lines.append("")
        
        # Προσθήκη περιεχομένου
        while current_length < length:
            template = np.random.choice(templates)
            court = np.random.choice(legal_terms['courts'])
            citation = np.random.choice(legal_terms['citations'])
            act = np.random.choice(legal_terms['acts'])
            legal_phrase = np.random.choice(legal_terms['legal_phrases'])
            
            sentence = template.format(
                court=court, citation=citation, 
                act=act, legal_phrase=legal_phrase
            )
            
            doc_lines.append(sentence)
            current_length += len(sentence)
        
        document = "\n".join(doc_lines)
        documents.append(document)
    
    return documents, categories

def benchmark_preprocessing(documents, batch_size=32):
    """
    Benchmark επιδόσεων προεπεξεργασίας εγγράφων.
    
    Args:
        documents: Λίστα με νομικά κείμενα
        batch_size: Μέγεθος batch για επεξεργασία
        
    Returns:
        Dictionary με μετρήσεις επιδόσεων
    """
    logger.info("Benchmarking document preprocessing...")
    
    # Έναρξη παρακολούθησης μνήμης
    tracemalloc.start()
    initial_mem = tracemalloc.get_traced_memory()[0] / (1024 * 1024)  # MB
    
    # Αρχικοποίηση preprocessor
    preprocessor = LegalDocumentPreprocessor(batch_size=batch_size)
    
    # Μέτρηση χρόνου επεξεργασίας
    start_time = time.time()
    results = preprocessor.batch_process(documents)
    total_time = time.time() - start_time
    
    # Μέτρηση χρήσης μνήμης
    peak_mem = tracemalloc.get_traced_memory()[1] / (1024 * 1024)  # MB
    mem_diff = peak_mem - initial_mem
    tracemalloc.stop()
    
    # Συλλογή μετρήσεων
    metrics = {
        'total_documents': len(documents),
        'batch_size': batch_size,
        'total_time_seconds': total_time,
        'avg_time_per_doc_ms': (total_time / len(documents)) * 1000,
        'initial_memory_mb': initial_mem,
        'peak_memory_mb': peak_mem,
        'memory_increase_mb': mem_diff,
        'preprocessor_metrics': preprocessor.get_performance_metrics()
    }
    
    logger.info(f"Preprocessing completed in {total_time:.2f} seconds")
    logger.info(f"Average time per document: {metrics['avg_time_per_doc_ms']:.2f} ms")
    logger.info(f"Memory usage: {mem_diff:.2f} MB")
    
    return metrics

def benchmark_classification(documents, categories, algorithm='svm', train_test_ratio=0.7):
    """
    Benchmark επιδόσεων ταξινόμησης νομικών εγγράφων.
    
    Args:
        documents: Λίστα με νομικά κείμενα
        categories: Λίστα με κατηγορίες των εγγράφων
        algorithm: Αλγόριθμος ταξινόμησης
        train_test_ratio: Αναλογία δεδομένων εκπαίδευσης/αξιολόγησης
        
    Returns:
        Dictionary με μετρήσεις επιδόσεων
    """
    logger.info(f"Benchmarking document classification using {algorithm}...")
    
    # Διαχωρισμός σε train/test
    n_train = int(len(documents) * train_test_ratio)
    
    train_docs = documents[:n_train]
    train_cats = categories[:n_train]
    test_docs = documents[n_train:]
    test_cats = categories[n_train:]
    
    logger.info(f"Training on {len(train_docs)} documents, testing on {len(test_docs)} documents")
    
    # Έναρξη παρακολούθησης μνήμης
    tracemalloc.start()
    initial_mem = tracemalloc.get_traced_memory()[0] / (1024 * 1024)  # MB
    
    # Αρχικοποίηση ταξινομητή
    classifier = LegalDocumentClassifier(algorithm=algorithm)
    
    # Εκπαίδευση και αξιολόγηση
    start_time = time.time()
    train_metrics = classifier.train(train_docs, train_cats)
    training_time = time.time() - start_time
    
    # Πρόβλεψη στα test data
    start_time = time.time()
    predictions = classifier.predict(test_docs)
    prediction_time = time.time() - start_time
    
    # Υπολογισμός ακρίβειας
    correct = sum(1 for pred, true in zip(predictions, test_cats) if pred == true)
    accuracy = correct / len(test_docs) if test_docs else 0
    
    # Μέτρηση χρήσης μνήμης
    peak_mem = tracemalloc.get_traced_memory()[1] / (1024 * 1024)  # MB
    mem_diff = peak_mem - initial_mem
    tracemalloc.stop()
    
    # Συλλογή μετρήσεων
    metrics = {
        'algorithm': algorithm,
        'training_samples': len(train_docs),
        'test_samples': len(test_docs),
        'training_time_seconds': training_time,
        'prediction_time_seconds': prediction_time,
        'avg_prediction_time_ms': (prediction_time / len(test_docs)) * 1000 if test_docs else 0,
        'accuracy': accuracy,
        'initial_memory_mb': initial_mem,
        'peak_memory_mb': peak_mem,
        'memory_increase_mb': mem_diff,
        'training_metrics': train_metrics
    }
    
    logger.info(f"Classification completed: training in {training_time:.2f}s, prediction in {prediction_time:.2f}s")
    logger.info(f"Accuracy: {accuracy:.4f}")
    logger.info(f"Memory usage: {mem_diff:.2f} MB")
    
    return metrics

def run_full_benchmark(args):
    """
    Εκτέλεση πλήρους benchmark και δημιουργία αναφοράς.
    
    Args:
        args: Παράμετροι γραμμής εντολών
        
    Returns:
        Dictionary με όλες τις μετρήσεις
    """
    # Έλεγχος GPU
    gpu_available = False
    gpu_info = {}
    try:
        import torch
        if torch.cuda.is_available():
            gpu_available = True
            gpu_info = {
                'device_name': torch.cuda.get_device_name(0),
                'memory_allocated_mb': torch.cuda.memory_allocated(0) / (1024 * 1024),
                'memory_reserved_mb': torch.cuda.memory_reserved(0) / (1024 * 1024)
            }
            logger.info(f"GPU available: {gpu_info['device_name']}")
        else:
            logger.info("No GPU available, running on CPU only")
    except Exception as e:
        logger.warning(f"Error checking GPU: {str(e)}")
        
    # Παραγωγή δοκιμαστικών δεδομένων
    documents, categories = generate_test_documents(args.documents)
    
    # Συλλογή πληροφοριών συστήματος
    system_info = {
        'cpu': psutil.cpu_count(logical=True),
        'memory_total_gb': psutil.virtual_memory().total / (1024 * 1024 * 1024),
        'gpu_available': gpu_available,
        'gpu_info': gpu_info,
        'platform': sys.platform,
        'python_version': sys.version
    }
    
    # Benchmark επιδόσεων
    logger.info("Starting full benchmark...")
    
    # Benchmark προεπεξεργασίας με διαφορετικά μεγέθη batch
    preprocessing_metrics = {}
    for batch_size in [8, 16, 32, 64]:
        if batch_size > args.documents:
            continue
        gc.collect()  # Καθαρισμός μνήμης
        preprocessing_metrics[f'batch_{batch_size}'] = benchmark_preprocessing(documents, batch_size)
    
    # Benchmark ταξινόμησης με διαφορετικούς αλγόριθμους
    classification_metrics = {}
    for algorithm in ['svm', 'naive_bayes', 'random_forest']:
        if algorithm != args.algorithm and args.algorithm != 'all':
            continue
        gc.collect()  # Καθαρισμός μνήμης
        classification_metrics[algorithm] = benchmark_classification(documents, categories, algorithm)
    
    # Συγκέντρωση όλων των μετρήσεων
    all_metrics = {
        'timestamp': datetime.now().isoformat(),
        'benchmark_config': vars(args),
        'system_info': system_info,
        'preprocessing': preprocessing_metrics,
        'classification': classification_metrics
    }
    
    # Αποθήκευση αποτελεσμάτων
    output_dir = project_root / 'logs' / 'benchmarks'
    output_dir.mkdir(exist_ok=True, parents=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = output_dir / f"benchmark_{timestamp}.json"
    
    with open(json_path, 'w') as f:
        json.dump(all_metrics, f, indent=2)
    
    logger.info(f"Benchmark results saved to {json_path}")
    
    # Δημιουργία συνοπτικής αναφοράς CSV
    csv_path = output_dir / f"benchmark_summary_{timestamp}.csv"
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Metric', 'Value'])
        writer.writerow(['Timestamp', all_metrics['timestamp']])
        writer.writerow(['Documents', args.documents])
        writer.writerow(['Batch Size', args.batch_size])
        writer.writerow(['Algorithm', args.algorithm])
        writer.writerow(['GPU Available', gpu_available])
        
        # Προσθήκη βασικών μετρικών προεπεξεργασίας
        if f'batch_{args.batch_size}' in preprocessing_metrics:
            prep_metrics = preprocessing_metrics[f'batch_{args.batch_size}']
            writer.writerow(['Preprocessing Time (s)', prep_metrics['total_time_seconds']])
            writer.writerow(['Avg. Doc Processing Time (ms)', prep_metrics['avg_time_per_doc_ms']])
            writer.writerow(['Preprocessing Memory (MB)', prep_metrics['memory_increase_mb']])
        
        # Προσθήκη βασικών μετρικών ταξινόμησης
        if args.algorithm in classification_metrics:
            class_metrics = classification_metrics[args.algorithm]
            writer.writerow(['Training Time (s)', class_metrics['training_time_seconds']])
            writer.writerow(['Prediction Time (s)', class_metrics['prediction_time_seconds']])
            writer.writerow(['Classification Accuracy', class_metrics['accuracy']])
            writer.writerow(['Classification Memory (MB)', class_metrics['memory_increase_mb']])
    
    logger.info(f"Benchmark summary saved to {csv_path}")
    
    return all_metrics

def main():
    parser = argparse.ArgumentParser(description='CDL6000 Performance Benchmark')
    parser.add_argument('--batch-size', type=int, default=32, help='Batch size for document processing')
    parser.add_argument('--documents', type=int, default=100, help='Number of test documents to generate')
    parser.add_argument('--algorithm', type=str, default='svm', choices=['svm', 'naive_bayes', 'random_forest', 'all'],
                        help='Classification algorithm to benchmark')
    parser.add_argument('--output-dir', type=str, default=None, help='Directory to save benchmark results')
    
    args = parser.parse_args()
    
    try:
        run_full_benchmark(args)
        logger.info("Benchmark completed successfully")
    except Exception as e:
        logger.error(f"Error during benchmark: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
