# scripts/utils/db_utils.py

import sqlite3
import pandas as pd
from pathlib import Path
import csv
from datetime import datetime
import logging

class DatabaseUtils:
    def __init__(self, db_path: str = "data/legal_text.db"):
        """Initialize database utilities with project paths and logging."""
        self.project_root = Path("D:/Projects/LegalTextAnalysis")
        self.db_path = self.project_root / db_path
        
        # Set up logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Create a file handler
        log_path = self.project_root / 'logs' / f'db_utils_{datetime.now():%Y%m%d}.log'
        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.INFO)
        
        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        
        # Add the handler to the logger
        self.logger.addHandler(fh)
        
    def get_connection(self):
        """Create and return a database connection with Row factory and error handling."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            self.logger.info("Database connection established successfully")
            return conn
        except Exception as e:
            self.logger.error(f"Database connection failed: {str(e)}")
            raise

    def query_database(self, query: str, params: tuple = None) -> list:
        """Execute a query with parameters and return results as list of dictionaries."""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(query, params or ())
                results = [dict(row) for row in cursor.fetchall()]
                self.logger.info(f"Query executed successfully, returned {len(results)} results")
                return results
        except Exception as e:
            self.logger.error(f"Query execution failed: {str(e)}\nQuery: {query}")
            raise

    def analyze_null_values(self, table_name: str = 'legal_cases'):
        """Perform comprehensive null value analysis on specified table."""
        query = f"""
        WITH total_rows AS (
            SELECT COUNT(*) as total FROM {table_name}
        )
        SELECT 
            column_name,
            COUNT(*) as null_count,
            ROUND(COUNT(*) * 100.0 / tr.total, 2) as null_percentage,
            tr.total as total_records
        FROM (
            SELECT 'text_length' as column_name, case_text 
            FROM {table_name}
            WHERE case_text IS NULL OR LENGTH(TRIM(case_text)) = 0
            
            UNION ALL
            
            SELECT 'citation_count', CAST(citation_count AS TEXT)
            FROM {table_name}
            WHERE citation_count IS NULL
        ) nulls
        CROSS JOIN total_rows tr
        GROUP BY column_name
        ORDER BY null_count DESC;
        """
        
        try:
            with self.get_connection() as conn:
                df = pd.read_sql_query(query, conn)
                self.logger.info(f"Null value analysis completed for {table_name}")
                return df
        except Exception as e:
            self.logger.error(f"Null analysis failed: {str(e)}")
            raise

    def export_to_csv(self, query: str, output_file: str) -> str:
        """Export query results to CSV with error handling and logging."""
        try:
            results = self.query_database(query)
            if not results:
                self.logger.warning("No results to export")
                return None
                
            output_path = self.project_root / 'data' / output_file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
                
            self.logger.info(f"Successfully exported data to {output_path}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"CSV export failed: {str(e)}")
            raise
        
    def get_case_metrics(self, case_id: str = None) -> dict:
        """Retrieve detailed metrics for specific case or summary statistics."""
        try:
            if case_id:
                query = """
                    SELECT 
                        lc.case_id,
                        lc.case_outcome,
                        tm.*,
                        LENGTH(lc.case_text) as text_length,
                        (SELECT COUNT(*) FROM legal_cases) as total_cases
                    FROM legal_cases lc
                    LEFT JOIN text_metrics tm ON lc.case_id = tm.case_id
                    WHERE lc.case_id = ?
                """
                results = self.query_database(query, (case_id,))
                return results[0] if results else None
                
            else:
                query = """
                    SELECT 
                        COUNT(*) as total_cases,
                        AVG(tm.citation_density) as avg_citation_density,
                        AVG(tm.sentence_complexity) as avg_sentence_complexity,
                        COUNT(DISTINCT lc.case_outcome) as unique_outcomes,
                        MIN(LENGTH(lc.case_text)) as min_length,
                        MAX(LENGTH(lc.case_text)) as max_length,
                        AVG(LENGTH(lc.case_text)) as avg_length
                    FROM legal_cases lc
                    LEFT JOIN text_metrics tm ON lc.case_id = tm.case_id
                """
                return self.query_database(query)[0]
                
        except Exception as e:
            self.logger.error(f"Failed to retrieve case metrics: {str(e)}")
            raise

    def save_features(self, features_df: pd.DataFrame, table_name: str = 'text_metrics'):
        """Save processed features to database with validation."""
        try:
            with self.get_connection() as conn:
                # Verify DataFrame isn't empty
                if features_df.empty:
                    raise ValueError("Features DataFrame is empty")
                    
                # Save to database
                features_df.to_sql(table_name, conn, if_exists='replace', index=False)
                self.logger.info(f"Successfully saved {len(features_df)} records to {table_name}")
                
                # Verify the save
                count_query = f"SELECT COUNT(*) as count FROM {table_name}"
                saved_count = pd.read_sql_query(count_query, conn)['count'].iloc[0]
                
                if saved_count != len(features_df):
                    raise ValueError(f"Save verification failed: {saved_count} rows saved, expected {len(features_df)}")
                    
        except Exception as e:
            self.logger.error(f"Failed to save features: {str(e)}")
            raise