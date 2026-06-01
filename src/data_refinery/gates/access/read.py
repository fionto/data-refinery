from pathlib import Path
from core import FileState, GateFunction

def check_read_access() -> GateFunction:
    """
    A gate factory that configures a runtime readibility validation check.
    
    Args:
        None (This specific factory only verifies general read access).
                
    Returns:
        GateFunction: A configured closure ready to be executed by the Pipeline.
    """
    def gate(state: FileState) -> FileState:
        
        if not state.is_valid:
            return state

        try:
            with open(state.filepath, "rb"):
                pass
        
        except PermissionError:
            state.is_valid = False
            state.rejection_stage = "check_permission"
            state.rejection_reason = "Permission denied reading file."
        
        except FileNotFoundError:
            # Defensive programming: catch if the file disappeared mid-run
            state.is_valid = False
            state.rejection_stage = "check_permission"
            state.rejection_reason = "File not found during permission validation."

        return state

    return gate