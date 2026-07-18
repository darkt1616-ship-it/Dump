"""
Breach Research - Cybersecurity Research Package
"""

from .generator import genera_dataset, genera_batch
from .analyzer import BreachAnalyzer
from .security_tester import SecuritySystemTester
from .utils import (
    setup_logging,
    get_memory_usage,
    format_bytes,
    timer,
    validate_file,
    generate_hash,
    calculate_speed,
    human_readable_time,
    ProgressBar,
    MemoryOptimizer,
)

__version__ = "1.0.0"
__author__ = "[Il Tuo Nome]"

__all__ = [
    "genera_dataset",
    "genera_batch",
    "BreachAnalyzer",
    "SecuritySystemTester",
    "setup_logging",
    "get_memory_usage",
    "format_bytes",
    "timer",
    "validate_file",
    "generate_hash",
    "calculate_speed",
    "human_readable_time",
    "ProgressBar",
    "MemoryOptimizer",
]