"""
Core pipeline machinery: state tracking and validation orchestration.
"""

from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Callable

@dataclass
class FileState:
    """
    Tracks validation lifecycle for a single file moving through the pipeline.
    
    Attributes:
        path: The file being validated.
        valid: Current validation status; remains True until a gate rejects it.
        rejection_reason: Human-readable explanation of why validation failed.
        rejection_stage: The specific gate that rejected the file (e.g., "extension_check").
        timestamp_created: When this file entered the pipeline (useful for batch diagnostics).
    """
    filepath: Path
    is_valid: bool = True
    # Optional[str] signals to users that these fields may be None during early pipeline stages
    rejection_reason: Optional[str] = None
    rejection_stage: Optional[str] = None
    # Automatically captures the native datetime object upon instantiation
    timestamp_created: datetime = field(default_factory=datetime.now)


@dataclass
class FileStateCollection:
    """
    Aggregates validation results across multiple files.
    Enables batch-level reporting and filtering.
    """
    files: list[FileState] = field(default_factory=list)
    
    def passed(self) -> list[FileState]:
        """Return only files that passed all gates."""
        return [f for f in self.files if f.is_valid]
    
    def rejected(self) -> list[FileState]:
        """Return only files that were rejected."""
        return [f for f in self.files if not f.is_valid]
    
    def summary(self):
        """Provide quick stats for logging or UI display."""
        pass


# Defining what a gate function signature looks like
GateFunction = Callable[[FileState], FileState]


class Pipeline:
    """
    The validation engine: orchestrates files through a sequence of gates.
    """
    
    def __init__(self, gates: List[GateFunction]) -> None:
        """
        Initialize the pipeline with a sequence of validation gates.
        
        Args:
            gates: List of callable gate functions (or gate objects), 
            each transforming FileState
        """
        self.gates = gates

    def add_gate(self, gate: GateFunction) -> None:
        """Register a new gate."""
        self.gates.append(gate)
    
    def validate(self, filepath: str) -> FileState:
        """
        Stream a file through all gates, stopping at first failure.
        
        Args:
            filepath: Path to the file to validate.
        
        Returns:
            FileState: The validation result.
        """
        state = FileState(filepath=Path(filepath))
        
        for gate in self.gates:
            if not state.is_valid:
                break  # Fail-fast: stop on first rejection
            state = gate(state)
        
        return state