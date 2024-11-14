# src/__init__.py
"""
CDL6000 - Legal Document Classification System
"""
__version__ = "0.1.0"

# src/core/__init__.py
"""
Core functionality for legal document processing
"""
from .enhanced_preprocessor import EnhancedLegalTextPreprocessor

__all__ = ["EnhancedLegalTextPreprocessor"]
