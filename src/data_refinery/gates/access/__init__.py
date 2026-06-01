"""
ACCESS layer: File-system and OS-level validation gates.

These gates ensure the file is readable, accessible, and in the right format
before any parsing is attempted.
"""

from .extension import check_extension
from .size import check_size
from .read import check_read_access
from .is_file import check_is_file

__all__ = [
    "check_extension",
    "check_size",
    "check_read_access",
    "check_is_file",
]