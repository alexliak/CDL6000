import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import torch
from ..utils.logger import setup_logger


class ExperimentTracker:
    """Tracks experiments and performance metrics."""

    def __init__(self, experiment_name: str, log_dir: Optional[Path] = None):
        """Initialize experiment tracker.

        Args:
            experiment_name: Name of the experiment
            log_dir: Optional directory for logs
        """
        self.experiment_name = experiment_name
        self.log_dir = log_dir or Path("logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Setup logger
        log_file = (
            self.log_dir
            / f"{experiment_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        self.logger = setup_logger(experiment_name, log_file)

        self.start_time = None
        self.metrics = {}

    def start_iteration(self):
        """Start timing an iteration."""
        self.start_time = datetime.now()
        self.logger.info(f"Starting iteration of {self.experiment_name}")

    def end_iteration(
        self,
        batch_size: int,
        accuracy_metrics: Dict[str, float],
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """End iteration and log metrics.

        Args:
            batch_size: Size of processed batch
            accuracy_metrics: Dictionary of accuracy metrics
            metadata: Optional additional metadata
        """
        duration = datetime.now() - self.start_time

        # Log metrics
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": duration.total_seconds(),
            "batch_size": batch_size,
            **accuracy_metrics,
        }

        if metadata:
            metrics["metadata"] = metadata

        self.metrics = metrics

        # Log to file
        metrics_file = self.log_dir / f"{self.experiment_name}_metrics.json"
        with open(metrics_file, "a") as f:
            json.dump(metrics, f)
            f.write("\n")

        self.logger.info(f"Completed iteration: {metrics}")

    def get_metrics(self) -> Dict[str, Any]:
        """Return current metrics."""
        return self.metrics
