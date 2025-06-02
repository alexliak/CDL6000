# /scripts/utils/db_manager.py
import sqlite3
from contextlib import contextmanager
from typing import Optional

class MCPDatabaseManager:
    """MCP-integrated database operations manager"""
    
    def __init__(self, db_path: str, logger: CentralLogger):
        self.db_path = db_path
        self.logger = logger
        
    @contextmanager
    def get_connection(self):
        """Create MCP-compatible database connection"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            yield conn
            conn.commit()
        except Exception as e:
            self.logger.error(f"Database error: {str(e)}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()