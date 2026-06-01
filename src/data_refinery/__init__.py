"""
data-refinery: A modular, observable data-ingress validation pipeline
for research lab files.
"""

__version__ = "0.1.0"
__author__ = "Matteo"
__description__ = "Fail-fast validation pipeline for research characterization data"

from .core import FileState, FileStateCollection, Pipeline

__all__ = [
    "FileState",
    "FileStateCollection",
    "Pipeline",
]