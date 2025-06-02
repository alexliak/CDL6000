# /scripts/utils/central_logger.py
from pathlib import Path
import logging
from datetime import datetime

class CentralLogger:
    """Unified logging system for Legal Text Analysis"""
    
    def __init__(self, name: str, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create component-specific logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Add handlers
        file_handler = logging.FileHandler(
            self.log_dir / f"{name}_{datetime.now():%Y%m%d}.log"
        )
        console_handler = logging.StreamHandler()
        
        # Configure format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)