# test_cuda.py
"""
Έλεγχος CUDA και καθαρισμός GPU cache
"""

import torch
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_cuda():
    """
    Έλεγχος CUDA διαθεσιμότητας και πληροφοριών GPU
    """
    try:
        # Καθαρισμός GPU cache
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            logger.info("🧹 Cleared GPU cache")

        # Έλεγχος CUDA
        logger.info(f"🔍 CUDA available: {torch.cuda.is_available()}")

        if torch.cuda.is_available():
            logger.info(f"📊 CUDA device: {torch.cuda.get_device_name(0)}")
            logger.info(
                f"💾 GPU memory allocated: {torch.cuda.memory_allocated(0)/1024**2:.1f} MB"
            )
            logger.info(
                f"💾 GPU memory cached: {torch.cuda.memory_reserved(0)/1024**2:.1f} MB"
            )

    except Exception as e:
        logger.error(f"❌ Error during CUDA test: {e}")
        raise


if __name__ == "__main__":
    test_cuda()
