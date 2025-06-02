import logging
from pathlib import Path

def setup_logger(name):
    """Δημιουργεί και επιστρέφει έναν logger με το συγκεκριμένο όνομα"""
    
    # Δημιουργία του logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Έλεγχος αν ο logger έχει ήδη handlers για να αποφύγουμε διπλά μηνύματα
    if not logger.handlers:
        # Δημιουργία του formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Δημιουργία του file handler
        log_dir = Path("D:/Projects/LegalTextAnalysis/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        fh = logging.FileHandler(log_dir / f"{name}.log")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
        # Προσθήκη console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    
    return logger