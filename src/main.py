import os
from pathlib import Path
import sys
import logging
from datetime import datetime

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(project_root / 'logs' / f'CDL6000_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    logger.info("Starting CDL6000 - Legal Document Classification System")
    try:
        logger.info("System initialized successfully")
    except Exception as e:
        logger.error(f"Error during initialization: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()