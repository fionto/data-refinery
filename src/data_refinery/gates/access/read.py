from pathlib import Path
from data_refinery.core import FileState, GateFunction

def check_read_access() -> GateFunction:
    """
    A gate factory that configures a runtime readability validation check.
    
    Args:
        None (This specific factory only verifies general read access).
                
    Returns:
        GateFunction: A configured closure ready to be executed by the Pipeline.
    """
    def gate(state: FileState) -> FileState:
        if not state.is_valid:
            return state

        try:
            # Attempt a minimal read block to verify actual OS-level read rights
            with open(state.filepath, "rb"):
                pass
        
        except PermissionError:
            state.is_valid = False
            state.rejection_stage = "check_read_access"  # Updated for uniformity
            state.rejection_reason = "Permission denied reading file."
        
        except FileNotFoundError:
            state.is_valid = False
            state.rejection_stage = "check_read_access"  # Updated for uniformity
            state.rejection_reason = "File not found during permission validation."

        return state

    return gate