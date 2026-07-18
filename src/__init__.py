"""
Breach Research - Cybersecurity Research Package
"""

from .generator import genera_dataset, genera_batch
from .analyzer import BreachAnalyzer
from .security_tester import SecuritySystemTester

__version__ = "1.0.0"
__author__ = "[Il Tuo Nome]"

__all__ = [
    "genera_dataset",
    "genera_batch",
    "BreachAnalyzer",
    "SecuritySystemTester",
]
