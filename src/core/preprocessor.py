import pandas as pd
import numpy as np
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
from memory_profiler import profile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LegalDocumentPreprocessor:
    """
    Legal document preprocessing pipeline with performance monitoring.

    Features:
        - Citation extraction
        - Text cleaning
        - Year extraction
        - Performance tracking

    Performance Targets:
        - Processing time: <2s per document
        - Memory usage: <4.5GB
        - GPU utilization: <80%
    """

    def __init__(self, batch_size: int = 32):
        self.batch_size = batch_size
        self.citation_pattern = r"\[\d{4}\]\s+[A-Z]+\s+\d+"
        self.year_pattern = r"\[(\d{4})\]"
        self.performance_metrics: Dict[str, Any] = {}

    @profile
    def process_document(self, text: str) -> Dict[str, Any]:
        """
        Process a single legal document with performance tracking.

        Args:
            text: Raw legal document text

        Returns:
            Dictionary containing processed features

        Raises:
            ValueError: If text is invalid
        """
        if pd.isna(text) or not isinstance(text, str):
            raise ValueError("Invalid text input")

        start_time = datetime.now()

        # Extract features
        citations = self._extract_citations(text)
        years = self._extract_years(text)
        clean_text = self._clean_text(text)

        # Calculate metrics
        features = {
            "text_length": len(clean_text),
            "citation_count": len(citations),
            "years_mentioned": years,
            "year_range": max(years) - min(years) if years else 0,
            "processing_time": (datetime.now() - start_time).total_seconds(),
        }

        return features

    def _extract_citations(self, text: str) -> List[str]:
        """Extract legal citations from text."""
        return re.findall(self.citation_pattern, text)

    def _extract_years(self, text: str) -> List[int]:
        """Extract years from legal citations."""
        years = re.findall(self.year_pattern, text)
        return [int(year) for year in years if 1900 <= int(year) <= 2024]

    def _clean_text(self, text: str) -> str:
        """Clean and normalize legal text."""
        # Basic cleaning
        text = re.sub(r"\s+", " ", text)  # Normalize whitespace
        text = text.strip()
        return text

    @profile
    def batch_process(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Process a batch of documents with memory optimization.

        Args:
            texts: List of legal document texts

        Returns:
            List of feature dictionaries
        """
        start_time = datetime.now()
        results = []

        # Process in batches
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            batch_results = []

            for text in batch:
                try:
                    features = self.process_document(text)
                    batch_results.append(features)
                except ValueError as e:
                    logger.warning(f"Skipping invalid document: {str(e)}")
                    continue

            results.extend(batch_results)

        # Update performance metrics
        self.performance_metrics.update(
            {
                "total_documents": len(texts),
                "processed_documents": len(results),
                "total_time": (datetime.now() - start_time).total_seconds(),
                "avg_time_per_doc": (datetime.now() - start_time).total_seconds()
                / len(texts),
            }
        )

        return results

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Return current performance metrics."""
        return self.performance_metrics
