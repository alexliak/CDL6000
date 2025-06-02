import pandas as pd
import numpy as np
from pathlib import Path
import logging
from scripts.utils.preprocessing_logger import setup_logger

# Setup logger
logger = setup_logger('preprocessing')

class LegalDataPreprocessor:
    def __init__(self, db_connection):
        self.db = db_connection
        self.logger = logging.getLogger('preprocessing')
        
    def analyze_missing_values(self):
        """Ανάλυση ελλιπών τιμών"""
        self.logger.info("Ξεκινάει η ανάλυση ελλιπών τιμών...")
        
        # Έλεγχος για NULL τιμές στα βασικά πεδία
        query = """
        SELECT 
            SUM(CASE WHEN case_id IS NULL THEN 1 ELSE 0 END) as null_case_ids,
            SUM(CASE WHEN case_outcome IS NULL THEN 1 ELSE 0 END) as null_outcomes,
            SUM(CASE WHEN text_length IS NULL THEN 1 ELSE 0 END) as null_lengths,
            COUNT(*) as total_rows
        FROM legal_cases;
        """
        result = pd.read_sql(query, self.db)
        
        for column in result.columns:
            self.logger.info(f"{column}: {result[column].iloc[0]}")
            
        return result
        
    def detect_outliers(self):
        """Εντοπισμός ακραίων τιμών με IQR"""
        self.logger.info("Ξεκινάει ο εντοπισμός ακραίων τιμών...")
        
        query = """
        WITH stats AS (
            SELECT 
                percentile_cont(0.25) WITHIN GROUP (ORDER BY text_length) as q1,
                percentile_cont(0.75) WITHIN GROUP (ORDER BY text_length) as q3,
                percentile_cont(0.75) WITHIN GROUP (ORDER BY text_length) - 
                percentile_cont(0.25) WITHIN GROUP (ORDER BY text_length) as iqr
            FROM legal_cases
        )
        SELECT 
            COUNT(*) as outlier_count,
            ROUND(AVG(text_length), 2) as avg_outlier_length
        FROM legal_cases, stats
        WHERE text_length < q1 - 1.5 * iqr 
           OR text_length > q3 + 1.5 * iqr;
        """
        
        result = pd.read_sql(query, self.db)
        self.logger.info(f"Βρέθηκαν {result['outlier_count'].iloc[0]} ακραίες τιμές")
        self.logger.info(f"Μέσο μήκος ακραίων τιμών: {result['avg_outlier_length'].iloc[0]}")
        
        return result
        
    def analyze_categorical_distributions(self):
        """Ανάλυση κατανομής κατηγορικών μεταβλητών"""
        self.logger.info("Ανάλυση κατανομής για case_outcome...")
        
        query = """
        SELECT 
            case_outcome,
            COUNT(*) as count,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
        FROM legal_cases
        GROUP BY case_outcome
        ORDER BY count DESC;
        """
        
        result = pd.read_sql(query, self.db)
        for _, row in result.iterrows():
            self.logger.info(f"{row['case_outcome']}: {row['count']} ({row['percentage']}%)")
            
        return result
        
    def calculate_scaling_parameters(self):
        """Υπολογισμός παραμέτρων για κανονικοποίηση"""
        self.logger.info("Υπολογισμός στατιστικών για κανονικοποίηση...")
        
        query = """
        SELECT 
            AVG(text_length) as mean_length,
            STDDEV(text_length) as std_length,
            MIN(text_length) as min_length,
            MAX(text_length) as max_length
        FROM legal_cases;
        """
        
        result = pd.read_sql(query, self.db)
        self.logger.info(f"Στατιστικά μεγέθους κειμένου:")
        self.logger.info(f"Μέσος όρος: {result['mean_length'].iloc[0]:.2f}")
        self.logger.info(f"Τυπική απόκλιση: {result['std_length'].iloc[0]:.2f}")
        
        return result

    def create_train_validation_split(self, train_size=0.8):
        """Δημιουργία διαχωρισμού train/validation"""
        self.logger.info("Δημιουργία διαχωρισμού δεδομένων...")
        
        # Δημιουργία temporary table για το split
        split_query = """
        CREATE TABLE IF NOT EXISTS data_split AS
        SELECT 
            case_id,
            CASE 
                WHEN RANDOM() < ? THEN 'train'
                WHEN RANDOM() < 0.5 THEN 'validation'
                ELSE 'test'
            END as split
        FROM legal_cases;
        """
        
        self.db.execute(split_query, (train_size,))
        
        # Έλεγχος κατανομής
        distribution_query = """
        SELECT split, COUNT(*) as count
        FROM data_split
        GROUP BY split;
        """
        
        result = pd.read_sql(distribution_query, self.db)
        for _, row in result.iterrows():
            self.logger.info(f"Split {row['split']}: {row['count']} cases")
            
        return result