# scripts/preprocessing/enhanced_preprocessor.py

import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import StandardScaler
import logging
from pathlib import Path
from ..utils.db_utils import DatabaseUtils

class EnhancedTextPreprocessor:
    def __init__(self, db_utils=None):
        """Initialize the enhanced preprocessor."""
        self.scaler = StandardScaler()
        self.db_utils = db_utils or DatabaseUtils()
        self.logger = logging.getLogger(__name__)
        
    def analyze_text_features(self):
        """Analyze text features and store results."""
        try:
            # First check for nulls
            null_analysis = self.db_utils.analyze_null_values()
            self.logger.info("Completed null value analysis")
            
            # Get all cases
            with self.db_utils.get_connection() as conn:
                cases_df = pd.read_sql("SELECT * FROM legal_cases", conn)
            
            # Calculate features
            features = []
            for _, row in cases_df.iterrows():
                text_features = self.calculate_text_features(row['case_text'])
                if text_features:
                    features.append({
                        'case_id': row['case_id'],
                        **text_features
                    })
            
            features_df = pd.DataFrame(features)
            normalized_features = self.normalize_features(features_df)
            
            # Save to database
            self.db_utils.save_features(normalized_features, 'enhanced_text_metrics')
            
            return normalized_features
            
        except Exception as e:
            self.logger.error(f"Feature analysis failed: {str(e)}")
            raise
    
    def calculate_text_features(self, text):
        """Calculate enhanced text features."""
        if pd.isna(text) or not text:
            return None
            
        features = {
            'char_count': len(text),
            'word_count': len(text.split()),
            'sentence_count': len(re.findall(r'[.!?]+', text)),
            'avg_word_length': np.mean([len(word) for word in text.split()]),
            'citation_count': len(re.findall(r'\[\d{4}\]|\(\d{4}\)', text)),
            'unique_words': len(set(text.lower().split()))
        }
        
        # Add more complex features
        if features['sentence_count'] > 0:
            features['avg_sentence_length'] = features['word_count'] / features['sentence_count']
            features['sentence_complexity'] = features['unique_words'] / features['sentence_count']
        
        if features['char_count'] > 0:
            features['citation_density'] = features['citation_count'] / features['char_count']
            
        return features
    
    def normalize_features(self, features_df):
        """Normalize numerical features."""
        numeric_cols = features_df.select_dtypes(include=['float64', 'int64']).columns
        features_df[numeric_cols] = self.scaler.fit_transform(features_df[numeric_cols])
        return features_df