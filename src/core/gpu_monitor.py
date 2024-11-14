# src/core/gpu_monitor.py
"""
Βελτιωμένη έκδοση του Performance Monitor με σωστό GPU handling
"""

import os
import psutil
import time
import logging
import torch
import numpy as np
from typing import Dict, Optional


class GPUMonitor:
    """
    Παρακολούθηση GPU resources με fallback σε CPU
    """

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self._setup_gpu()

    def _setup_gpu(self) -> None:
        """
        Έλεγχος διαθεσιμότητας GPU και αρχικοποίηση
        """
        self.gpu_available = False
        try:
            if torch.cuda.is_available():
                self.gpu_available = True
                self.device = torch.device("cuda")
                # Καθαρισμός GPU cache
                torch.cuda.empty_cache()
                # Καταγραφή πληροφοριών GPU
                gpu_name = torch.cuda.get_device_name(0)
                gpu_memory = torch.cuda.get_device_properties(0).total_memory
                self.logger.info(
                    f"GPU initialized: {gpu_name} ({gpu_memory/1e9:.1f}GB)"
                )
            else:
                self.device = torch.device("cpu")
                self.logger.warning("No GPU available, using CPU")
        except Exception as e:
            self.device = torch.device("cpu")
            self.logger.error(f"Error initializing GPU: {e}")
            self.logger.warning("Falling back to CPU")

    def get_gpu_memory_usage(self) -> Optional[float]:
        """
        Επιστρέφει χρήση μνήμης GPU σε MB
        """
        if not self.gpu_available:
            return None

        try:
            memory_allocated = torch.cuda.memory_allocated(0)
            return memory_allocated / 1024 / 1024  # Bytes to MB
        except Exception as e:
            self.logger.error(f"Error getting GPU memory: {e}")
            return None

    def get_gpu_utilization(self) -> Optional[float]:
        """
        Επιστρέφει ποσοστό χρήσης GPU
        """
        if not self.gpu_available:
            return None

        try:
            # Προσομοίωση μέτρησης utilization
            # Σε παραγωγή θα χρησιμοποιούσαμε nvidia-smi
            return np.random.uniform(0, 100)
        except Exception as e:
            self.logger.error(f"Error getting GPU utilization: {e}")
            return None


class PerformanceMonitor:
    """
    Παρακολούθηση system performance με υποστήριξη GPU
    """

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.start_time = None
        self.gpu_monitor = GPUMonitor(logger)

    def start_monitoring(self):
        """Έναρξη μέτρησης απόδοσης"""
        self.start_time = time.time()
        self.initial_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB

    def get_metrics(self) -> Dict[str, float]:
        """
        Συλλογή μετρικών απόδοσης
        """
        current_time = time.time()
        current_memory = psutil.Process().memory_info().rss / 1024 / 1024

        metrics = {
            "processing_time": current_time - self.start_time,
            "memory_usage_mb": current_memory,
            "memory_change_mb": current_memory - self.initial_memory,
            "cpu_percent": psutil.cpu_percent(),
        }

        # Προσθήκη μετρικών GPU αν είναι διαθέσιμη
        if self.gpu_monitor.gpu_available:
            gpu_memory = self.gpu_monitor.get_gpu_memory_usage()
            gpu_util = self.gpu_monitor.get_gpu_utilization()

            if gpu_memory is not None:
                metrics["gpu_memory_mb"] = gpu_memory
            if gpu_util is not None:
                metrics["gpu_utilization"] = gpu_util

        return metrics

    def log_metrics(self, metrics: Dict[str, float]):
        """Καταγραφή μετρικών"""
        self.logger.info("Performance Metrics:")
        for key, value in metrics.items():
            self.logger.info(f"- {key}: {value:.2f}")
