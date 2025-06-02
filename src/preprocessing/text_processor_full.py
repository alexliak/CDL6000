# scripts/pipeline/text_processor.py

"""
Legal Text Analysis Processing Pipeline
Supports concurrent access with MCP server
"""

import logging
from pathlib import Path
import sqlite3
from datetime import datetime
from typing import Dict, Any, Optional
import time
from contextlib import contextmanager

class TextProcessor:
    def __init__(self, db_path: str = "data/legal_text.db", max_retries: int = 3, timeout: int = 20):
        """Initialize text processor with retry logic.
        
        Args:
            db_path: Path to SQLite database relative to project root
            max_retries: Maximum number of retries for locked database
            timeout: SQLite timeout in seconds
        """
        self.project_root = Path("D:/Projects/LegalTextAnalysis")
        self.db_path = self.project_root / db_path
        self.logs_dir = self.project_root / "scripts" / "pipeline" / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.max_retries = max_retries
        self.timeout = timeout
        
        self.setup_logging()

    def setup_logging(self) -> None:
        """Configure logging using existing project structure."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = self.logs_dir / f"pipeline_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('legal_text_pipeline')

    @contextmanager
    def get_db_connection(self):
        """Create database connection with retry logic for locked database."""
        for attempt in range(self.max_retries):
            try:
                conn = sqlite3.connect(self.db_path, timeout=self.timeout)
                conn.execute("PRAGMA busy_timeout = {}000".format(self.timeout))
                conn.row_factory = sqlite3.Row
                yield conn
                conn.close()
                break
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) and attempt < self.max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    self.logger.warning(f"Database locked, waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                else:
                    raise

    def get_case_stats(self) -> Dict[str, Any]:
        """Get basic statistics about the cases."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.execute("""
                    SELECT COUNT(*) as total_cases,
                           COUNT(DISTINCT case_outcome) as unique_outcomes
                    FROM legal_cases
                """)
                stats = dict(cursor.fetchone())
                self.logger.info(f"Retrieved case stats: {stats}")
                return stats
        except Exception as e:
            self.logger.error(f"Error getting case stats: {str(e)}")
            raise

    def process_batch(self, offset: int, limit: int = 100) -> int:
        """Process a batch of cases with retry logic.
        
        Args:
            offset: Starting position in the database
            limit: Number of cases to process
            
        Returns:
            Number of cases processed
        """
        processed = 0
        try:
            with self.get_db_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT case_id, case_text 
                    FROM legal_cases 
                    LIMIT ? OFFSET ?
                    """, 
                    (limit, offset)
                )
                
                for row in cursor:
                    try:
                        metrics = self.compute_metrics(row['case_text'])
                        self.update_metrics(conn, row['case_id'], metrics)
                        processed += 1
                        
                        if processed % 10 == 0:  # Log progress every 10 cases
                            self.logger.info(f"Processed {processed} cases in current batch")
                            
                    except Exception as e:
                        self.logger.error(f"Error processing case {row['case_id']}: {str(e)}")
                        continue
                        
                return processed
                
        except Exception as e:
            self.logger.error(f"Error in batch processing: {str(e)}")
            raise

    def compute_metrics(self, text: str) -> Dict[str, Any]:
        """Compute text analysis metrics."""
        if not text:
            return {
                'sentence_count': 0,
                'citation_density': 0,
                'sentence_complexity': 0,
                'length_category': 'short'
            }
            
        metrics = {
            'sentence_count': text.count('.'),
            'citation_density': (text.count('[') + text.count('(')) / len(text) if len(text) > 0 else 0,
            'sentence_complexity': len(text.split()) / (text.count('.') or 1),
            'length_category': 'short' if len(text) < 1000 else 'medium' if len(text) < 3000 else 'long'
        }
        
        return metrics

    def update_metrics(self, conn: sqlite3.Connection, case_id: str, metrics: Dict[str, Any]) -> None:
        """Update metrics with retry logic."""
        try:
            conn.execute("""
                INSERT OR REPLACE INTO text_metrics (
                    case_id,
                    sentence_count,
                    citation_density,
                    sentence_complexity,
                    length_category
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                case_id,
                metrics['sentence_count'],
                metrics['citation_density'],
                metrics['sentence_complexity'],
                metrics['length_category']
            ))
            conn.commit()
            
        except Exception as e:
            self.logger.error(f"Error updating metrics for case {case_id}: {str(e)}")
            raise

    def process_all(self, batch_size: int = 50) -> None:
        """Process all cases in small batches with progress tracking."""
        try:
            stats = self.get_case_stats()
            total_cases = stats['total_cases']
            processed_total = 0
            
            self.logger.info(f"Starting processing of {total_cases} cases")
            start_time = time.time()
            
            for offset in range(0, total_cases, batch_size):
                try:
                    processed = self.process_batch(offset, batch_size)
                    processed_total += processed
                    
                    # Calculate progress and estimated time
                    progress = (processed_total / total_cases) * 100
                    elapsed = time.time() - start_time
                    cases_per_second = processed_total / elapsed if elapsed > 0 else 0
                    
                    self.logger.info(
                        f"Progress: {progress:.1f}% ({processed_total}/{total_cases}) "
                        f"Speed: {cases_per_second:.1f} cases/s"
                    )
                    
                except Exception as e:
                    self.logger.error(f"Error in batch starting at offset {offset}: {str(e)}")
                    continue
                    
            self.logger.info(f"Completed processing {processed_total} cases")
            
        except Exception as e:
            self.logger.error(f"Error in overall processing: {str(e)}")
            raise

if __name__ == "__main__":
    processor = TextProcessor(max_retries=5, timeout=30)
    
    try:
        # Get initial stats
        stats = processor.get_case_stats()
        print(f"Total cases: {stats['total_cases']}")
        print(f"Unique outcomes: {stats['unique_outcomes']}")
        
        # Process with smaller batches and retry logic
        processor.process_all(batch_size=50)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Check database file permissions")
        print("2. Verify database integrity")
        print("3. Try decreasing batch size")
        print("4. Check available disk space")