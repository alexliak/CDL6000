# src/ml/vectorizer.py
"""
Εξειδικευμένες λύσεις μετατροπής νομικών κειμένων σε διανύσματα
με βελτιστοποιήσεις για χρήση GPU.
"""

import numpy as np
import torch
from typing import List, Dict, Any, Union, Optional
import re
import logging
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.preprocessing import normalize
from sklearn.decomposition import TruncatedSVD

logger = logging.getLogger(__name__)


class LegalVectorizer:
    """
    Προσαρμοσμένος vectorizer για νομικά κείμενα με υποστήριξη TF-IDF και εξειδικευμένα 
    χαρακτηριστικά για νομικές οντότητες.
    
    Χαρακτηριστικά:
        - Εξαγωγή νομικών όρων
        - Κανονικοποίηση παραπομπών
        - Διαχείριση μνήμης για μεγάλα corpora
        - Βελτιστοποίηση GPU
    """
    
    def __init__(
        self, 
        max_features: int = 10000, 
        use_gpu: bool = True,
        include_legal_features: bool = True,
        dimensionality_reduction: Optional[int] = None
    ):
        """
        Αρχικοποίηση του νομικού vectorizer.
        
        Args:
            max_features: Μέγιστος αριθμός χαρακτηριστικών για το λεξικό
            use_gpu: Αν θα χρησιμοποιηθεί GPU όπου είναι διαθέσιμο
            include_legal_features: Αν θα εξαχθούν εξειδικευμένα νομικά χαρακτηριστικά
            dimensionality_reduction: Αριθμός διαστάσεων μετά από μείωση (None για καμία μείωση)
        """
        self.max_features = max_features
        self.use_gpu = use_gpu and torch.cuda.is_available()
        self.include_legal_features = include_legal_features
        self.dimensionality_reduction = dimensionality_reduction
        self.device = torch.device('cuda' if self.use_gpu else 'cpu')
        
        # Βασικός TF-IDF vectorizer
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=max_features,
            min_df=2,
            max_df=0.85,
            norm='l2',
            sublinear_tf=True,
            ngram_range=(1, 2)
        )
        
        # Μείωση διαστάσεων
        self.svd = None
        if dimensionality_reduction is not None:
            self.svd = TruncatedSVD(n_components=dimensionality_reduction)
        
        # Patterns για νομικά χαρακτηριστικά
        self.legal_patterns = {
            'citation': r'\[\d{4}\]\s+[A-Z]+\s+\d+',
            'section': r'[Ss]ection\s+\d+',
            'article': r'[Aa]rticle\s+\d+',
            'court': r'[A-Z][a-z]*\s+Court',
            'act': r'Act\s+of\s+\d{4}',
            'regulation': r'Regulation\s+[A-Z0-9]+\/\d+'
        }
        
        # Αρχικοποίηση λεξικών και μητρώων
        self.vocabulary_ = None
        self.legal_feature_names = []
        
        logger.info(f"LegalVectorizer initialized (GPU: {self.use_gpu}, "
                   f"max_features: {max_features}, "
                   f"dimensionality_reduction: {dimensionality_reduction})")
    
    def _extract_legal_features(self, texts: List[str]) -> np.ndarray:
        """
        Εξάγει εξειδικευμένα νομικά χαρακτηριστικά από τα κείμενα.
        
        Args:
            texts: Λίστα νομικών κειμένων
        
        Returns:
            Πίνακας με τα εξειδικευμένα νομικά χαρακτηριστικά
        """
        # Αριθμός κειμένων
        n_samples = len(texts)
        
        # Αριθμός νομικών χαρακτηριστικών
        n_legal_features = len(self.legal_patterns)
        
        # Δημιουργία πίνακα για αποθήκευση των χαρακτηριστικών
        legal_features = np.zeros((n_samples, n_legal_features))
        
        # Αποθήκευση των ονομάτων των χαρακτηριστικών
        self.legal_feature_names = list(self.legal_patterns.keys())
        
        # Εξαγωγή χαρακτηριστικών για κάθε κείμενο
        for i, text in enumerate(texts):
            for j, (feature_name, pattern) in enumerate(self.legal_patterns.items()):
                # Αναζήτηση και μέτρηση των αντιστοιχιών του pattern
                matches = re.findall(pattern, text)
                legal_features[i, j] = len(matches)
        
        # Κανονικοποίηση των χαρακτηριστικών
        if np.sum(legal_features) > 0:
            legal_features = normalize(legal_features, norm='l2', axis=0)
        
        return legal_features
    
    def fit_transform(self, texts: List[str], y=None) -> np.ndarray:
        """
        Προσαρμογή του vectorizer στα δεδομένα και μετατροπή των κειμένων σε διανύσματα.
        
        Args:
            texts: Λίστα νομικών κειμένων
            y: Ετικέτες (δεν χρησιμοποιούνται - για συμβατότητα με sklearn)
        
        Returns:
            Διανύσματα χαρακτηριστικών για τα κείμενα
        """
        logger.info(f"Fitting and transforming {len(texts)} documents")
        
        # Εξαγωγή TF-IDF χαρακτηριστικών
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
        
        # Εξαγωγή εξειδικευμένων νομικών χαρακτηριστικών αν έχει ζητηθεί
        if self.include_legal_features:
            legal_features = self._extract_legal_features(texts)
            
            # Συνδυασμός TF-IDF και νομικών χαρακτηριστικών
            # Μετατροπή του sparse matrix σε πυκνό πίνακα
            if isinstance(tfidf_matrix, np.ndarray):
                X = np.hstack((tfidf_matrix, legal_features))
            else:
                X = np.hstack((tfidf_matrix.toarray(), legal_features))
        else:
            X = tfidf_matrix.toarray() if not isinstance(tfidf_matrix, np.ndarray) else tfidf_matrix
        
        # Μείωση διαστάσεων αν έχει ζητηθεί
        if self.svd is not None:
            logger.info(f"Reducing dimensions from {X.shape[1]} to {self.dimensionality_reduction}")
            X = self.svd.fit_transform(X)
        
        # Μεταφορά στο GPU αν χρησιμοποιείται
        if self.use_gpu:
            X_tensor = torch.FloatTensor(X).to(self.device)
            return X_tensor.cpu().numpy()  # Επιστροφή σε CPU για συμβατότητα
        
        return X
    
    def transform(self, texts: List[str]) -> np.ndarray:
        """
        Μετατροπή νέων κειμένων σε διανύσματα χρησιμοποιώντας τον προσαρμοσμένο vectorizer.
        
        Args:
            texts: Λίστα νομικών κειμένων
        
        Returns:
            Διανύσματα χαρακτηριστικών για τα κείμενα
        """
        logger.info(f"Transforming {len(texts)} documents")
        
        # Εξαγωγή TF-IDF χαρακτηριστικών
        tfidf_matrix = self.tfidf_vectorizer.transform(texts)
        
        # Εξαγωγή εξειδικευμένων νομικών χαρακτηριστικών αν έχει ζητηθεί
        if self.include_legal_features:
            legal_features = self._extract_legal_features(texts)
            
            # Συνδυασμός TF-IDF και νομικών χαρακτηριστικών
            # Μετατροπή του sparse matrix σε πυκνό πίνακα
            if isinstance(tfidf_matrix, np.ndarray):
                X = np.hstack((tfidf_matrix, legal_features))
            else:
                X = np.hstack((tfidf_matrix.toarray(), legal_features))
        else:
            X = tfidf_matrix.toarray() if not isinstance(tfidf_matrix, np.ndarray) else tfidf_matrix
        
        # Μείωση διαστάσεων αν έχει εφαρμοστεί
        if self.svd is not None:
            X = self.svd.transform(X)
        
        # Μεταφορά στο GPU αν χρησιμοποιείται
        if self.use_gpu:
            X_tensor = torch.FloatTensor(X).to(self.device)
            return X_tensor.cpu().numpy()  # Επιστροφή σε CPU για συμβατότητα
        
        return X
    
    def get_feature_names(self) -> List[str]:
        """
        Ανάκτηση των ονομάτων όλων των χαρακτηριστικών.
        
        Returns:
            Λίστα με τα ονόματα των χαρακτηριστικών
        """
        tfidf_features = self.tfidf_vectorizer.get_feature_names_out()
        
        if self.include_legal_features:
            # Συνδυασμός TF-IDF και νομικών χαρακτηριστικών
            all_features = np.concatenate([tfidf_features, self.legal_feature_names])
            return all_features.tolist()
        
        return tfidf_features.tolist()
    
    def save_model(self, path: str):
        """
        Αποθήκευση του vectorizer για μελλοντική χρήση.
        
        Args:
            path: Διαδρομή για αποθήκευση
        """
        import joblib
        
        model_info = {
            'tfidf_vectorizer': self.tfidf_vectorizer,
            'max_features': self.max_features,
            'include_legal_features': self.include_legal_features,
            'dimensionality_reduction': self.dimensionality_reduction,
            'svd': self.svd,
            'legal_patterns': self.legal_patterns,
            'legal_feature_names': self.legal_feature_names
        }
        
        joblib.dump(model_info, path)
        logger.info(f"Vectorizer saved to {path}")
    
    def load_model(self, path: str):
        """
        Φόρτωση του vectorizer από αποθηκευμένο αρχείο.
        
        Args:
            path: Διαδρομή του αποθηκευμένου vectorizer
        """
        import joblib
        
        model_info = joblib.load(path)
        
        self.tfidf_vectorizer = model_info['tfidf_vectorizer']
        self.max_features = model_info['max_features']
        self.include_legal_features = model_info['include_legal_features']
        self.dimensionality_reduction = model_info['dimensionality_reduction']
        self.svd = model_info['svd']
        self.legal_patterns = model_info['legal_patterns']
        self.legal_feature_names = model_info['legal_feature_names']
        
        logger.info(f"Vectorizer loaded from {path}")
