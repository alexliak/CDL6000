# Στο legal_extractor.py
from src.core.preprocessor import LegalDocumentPreprocessor
import re
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class LegalTermExtractor:
    """
    Εξαγωγή νομικών όρων και οντοτήτων από νομικά έγγραφα.
    Χρησιμοποιεί τον LegalDocumentPreprocessor για αρχική προεπεξεργασία.
    
    Χαρακτηριστικά:
        - Εξαγωγή νομικών όρων
        - Αναγνώριση νομικών οντοτήτων
        - Ανάλυση παραπομπών
    """
    def __init__(self):
        self.preprocessor = LegalDocumentPreprocessor()
        self.legal_terms_patterns = {
            'court': r'\b(?:Supreme|High|District|Circuit|Appeal|Federal|International)\s+Court\b',
            'act': r'\b(?:Act|Law|Regulation|Directive|Treaty)\s+(?:of|on)\s+\d{4}\b',
            'case': r'\b(?:case|matter|suit)\s+(?:of|between)\b',
            'clause': r'\b(?:clause|section|article|paragraph)\s+\d+\b'
        }
    
    def extract_legal_terms(self, text: str) -> Dict[str, List[str]]:
        """
        Εξαγωγή νομικών όρων από κείμενο με βάση προκαθορισμένα patterns.
        
        Args:
            text: Το κείμενο προς ανάλυση
            
        Returns:
            Λεξικό με κατηγορίες νομικών όρων και τις αντίστοιχες λίστες τους
        """
        results = {}
        
        for term_type, pattern in self.legal_terms_patterns.items():
            matches = re.findall(pattern, text)
            results[term_type] = matches
            
        logger.info(f"Extracted {sum(len(terms) for terms in results.values())} legal terms")
        return results
    
    def analyze_document(self, text: str) -> Dict[str, Any]:
        """
        Πλήρης ανάλυση νομικού εγγράφου.
        
        Args:
            text: Το κείμενο του νομικού εγγράφου
            
        Returns:
            Λεξικό με αποτελέσματα ανάλυσης
        """
        # Χρήση του preprocessor για βασική προεπεξεργασία
        features = self.preprocessor.process_document(text)
        
        # Εξαγωγή νομικών όρων
        legal_terms = self.extract_legal_terms(text)
        
        # Συνδυασμός αποτελεσμάτων
        results = {
            **features,
            "legal_terms": legal_terms,
            "total_legal_terms": sum(len(terms) for terms in legal_terms.values())
        }
        
        return results
