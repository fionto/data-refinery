"""
Core pipeline machinery: state tracking and validation orchestration.
"""

from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
from typing import Optional, Callable

@dataclass
class FileState:
    """
    Tracks validation lifecycle for a single file moving through the pipeline.
    
    Attributes:
        filepath: The file being validated.
        pipeline_stage: Current Pipeline stage
        is_valid: Current validation status; remains True until a gate rejects it.
        rejection_reason: Human-readable explanation of why validation failed.
        rejection_stage: The specific gate that rejected the file (e.g., "extension_check").
        timestamp_created: When this file entered the pipeline (useful for batch diagnostics).
    """
    filepath : Path
    pipeline_stage : Optional[str] = None
    is_valid : bool = True
    rejection_reason : Optional[str] = None
    rejection_stage : Optional[str] = None
    # Automatically captures the native datetime object upon instantiation
    timestamp_created : datetime = field(default_factory=datetime.now)


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
   
    def rejected_at_stage(self, stage: str) -> list[FileState]:
        """Return files that were rejected at a specific pipeline stage."""
        return [f for f in self.files if not f.is_valid and f.pipeline_stage == stage]
    
    def summary(self):
        """Provide quick stats for logging or UI display."""
        pass


# Defining what a gate function signature looks like
GateFunction = Callable[[FileState], FileState]


class Pipeline:
    """
    The validation engine: orchestrates files through a sequence of gates.
    """
    
    def __init__(self, gates: list[GateFunction], stage_name: str) -> None:
        """
        Initialize the pipeline with a sequence of validation gates.
        
        Args:
            gates: List of callable gate functions (or gate objects), 
            each transforming FileState
            stage_name: Name of this pipeline stage (e.g., "validation")
        """
        self.gates = gates
        self.stage_name = stage_name

    def _run_gates(self, state: FileState) -> FileState:
        """
        Internal helper: execute the fail-fast gate sequence.
        """
        for gate in self.gates:
            if not state.is_valid:
                break  # Fail-fast: stop on first rejection
            state = gate(state)
        
        return state   
    
    def add_gate(self, gate: GateFunction) -> "Pipeline":
        """
        Register a new gate to the pipeline chain.
        
        Returns self to enable method chaining (e.g., pipeline.add_gate(g1).add_gate(g2)).
        """
        self.gates.append(gate)
        return self
    
    def run_new(self, filepath:str) -> FileState:
        """
        Create a fresh FileState and stream it through all gates.
        Use this when starting a workflow on a new file.
        
        Args:
            filepath: Path to the file to validate.
        
        Returns:
            FileState: The validation result.
        """
        state = FileState(filepath=Path(filepath), pipeline_stage=self.stage_name)
        return self._run_gates(state)

    def run_existing(self, state: FileState) -> FileState:
        """
        Run an existing FileState through all gates.

        Updates pipeline_stage to this pipeline's stage_name, overwriting the previous stage.
        Use this when passing a file through a subsequent pipeline stage.
        
        Args:
            state: An existing FileState (likely from a prior pipeline stage).
        
        Returns:
            FileState: The modified state after validation.
        """
        # Guard clause: If it's already dead, don't let a subsequent pipeline claim it
        if not state.is_valid:
            return state
        
        # Update the stage tracker before running gates
        state.pipeline_stage = self.stage_name
        return self._run_gates(state)