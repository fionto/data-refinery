"""
ACCESS layer: File-system and OS-level validation gates.

These gates ensure the file is readable, accessible, and in the right format
before any parsing is attempted.
"""

from data_refinery.gates.access.extension import check_extension
from data_refinery.gates.access.size import check_size
from data_refinery.gates.access.permissions import check_permissions
from data_refinery.gates.access.integrity import check_integrity

__all__ = [
    "check_extension",
    "check_size",
    "check_permissions",
    "check_integrity",
]