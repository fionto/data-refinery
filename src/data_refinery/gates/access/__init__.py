"""
ACCESS layer: File-system and OS-level validation gates.

These gates ensure the file is readable, accessible, and in the right format
before any parsing is attempted.
"""

from .extension import check_extension
from .size import check_size
from .permissions import check_permissions
from .integrity import check_integrity

__all__ = [
    "check_extension",
    "check_size",
    "check_permissions",
    "check_integrity",
]