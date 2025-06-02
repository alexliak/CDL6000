import os
from pathlib import Path
import sys
import logging
from datetime import datetime
import argparse
import torch

# Προσθήκη του project root στο Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Δημιουργία του φακέλου logs αν δεν υπάρχει
logs_dir = project_root / 'logs'
logs_dir.mkdir(exist_ok=True)

# Ρύθμιση logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(logs_dir / f'CDL6000_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Εισαγωγή των modules του project
from src.core.preprocessor import LegalDocumentPreprocessor
from src.core.classifier import LegalDocumentClassifier
from src.core.test_cuda import test_cuda
from src.ml.legal_extractor import LegalTermExtractor


def check_gpu():
    """Έλεγχος διαθεσιμότητας GPU και εμφάνιση πληροφοριών."""
    logger.info("Checking GPU availability...")
    try:
        test_cuda()
    except Exception as e:
        logger.warning(f"Error during GPU check: {str(e)}")
        logger.info("Continuing with CPU only")


def process_sample_document():
    """Επεξεργασία ενός δείγματος εγγράφου για επίδειξη του pipeline."""
    logger.info("Processing sample document...")
    
    # Δείγμα νομικού κειμένου
    sample_text = """
    [2015] EWHC 123 (Ch)
    In the matter of Smith v. Jones Corporation Ltd.
    This case concerns a breach of Article 5 of the Commercial Agreement Act of 2010.
    The Court finds that section 15, paragraph 3 of the contract was violated by the defendant.
    Prior cases include Brown v. Wilson [2012] UKSC 45 and Roberts v. Thompson [2008] EWCA Civ 23.
    """
    
    # Χρήση του preprocessor
    preprocessor = LegalDocumentPreprocessor()
    features = preprocessor.process_document(sample_text)
    
    # Χρήση του legal term extractor
    extractor = LegalTermExtractor()
    legal_terms = extractor.extract_legal_terms(sample_text)
    
    # Εμφάνιση αποτελεσμάτων
    logger.info("Document processing results:")
    logger.info(f"Features: {features}")
    logger.info(f"Legal terms: {legal_terms}")
    
    return features, legal_terms


def demo_classification():
    """Επίδειξη της λειτουργίας ταξινόμησης με δείγμα δεδομένων."""
    logger.info("Demonstrating classification functionality...")
    
    # Δείγμα δεδομένων εκπαίδευσης
    texts = [
        "The court finds that the defendant violated section 15 of the contract.",
        "Pursuant to Article 10 of Regulation EC 2015/123, the claim is dismissed.",
        "The plaintiff filed a motion for summary judgment under Rule 56.",
        "The Supreme Court overturned the decision of the Court of Appeal.",
        "The parties have reached a settlement agreement on all claims.",
        "The Court of Appeal upheld the judgment of the lower court.",
        "The claimant seeks damages for breach of contract under common law.",
        "The case was referred to the European Court of Justice.",
        "The tribunal found that the company had violated labor regulations.",
        "The arbitration award was set aside by the High Court."
    ]
    
    # Ετικέτες κατηγοριών για τα δείγματα
    labels = [
        "Contract", "Regulatory", "Procedural", "Appeal", "Settlement",
        "Appeal", "Contract", "Referral", "Employment", "Arbitration"
    ]
    
    # Δημιουργία και εκπαίδευση ταξινομητή
    classifier = LegalDocumentClassifier(algorithm='svm')
    metrics = classifier.train(texts, labels, max_features=1000)
    
    # Εμφάνιση αποτελεσμάτων
    logger.info("Classification results:")
    logger.info(f"Metrics: {metrics}")
    
    # Δοκιμή πρόβλεψης σε νέο κείμενο
    test_text = "The appellant contests the decision on grounds of procedural error."
    prediction = classifier.predict([test_text])
    logger.info(f"Prediction for test text: {prediction[0]}")
    
    return metrics, prediction[0]


def parse_arguments():
    """Ανάλυση παραμέτρων γραμμής εντολών."""
    parser = argparse.ArgumentParser(description='CDL6000 - Legal Document Classification System')
    parser.add_argument('--demo', action='store_true', help='Run demonstration with sample data')
    parser.add_argument('--gpu-check', action='store_true', help='Check GPU availability')
    parser.add_argument('--version', action='version', version='CDL6000 v0.1.0')
    
    return parser.parse_args()


def main():
    """Κύρια λειτουργία του προγράμματος."""
    logger.info("Starting CDL6000 - Legal Document Classification System")
    
    try:
        # Ανάλυση παραμέτρων
        args = parse_arguments()
        
        # Έλεγχος GPU αν ζητηθεί
        if args.gpu_check:
            check_gpu()
        
        # Εκτέλεση demo αν ζητηθεί
        if args.demo:
            logger.info("Running demonstration mode")
            process_sample_document()
            demo_classification()
        else:
            logger.info("No specific action requested. Use --demo or --gpu-check to see functionality.")
        
        logger.info("System initialized successfully")
    
    except Exception as e:
        logger.error(f"Error during initialization: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()