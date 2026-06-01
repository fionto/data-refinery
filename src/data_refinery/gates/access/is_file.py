from pathlib import Path
from core import FileState, GateFunction

def check_is_file():
    """
    Gate that ensures the provided path points to a regular file.
    
    Args:
        None (This specific factory only verifies ...).
                
    Returns:
        GateFunction: A configured closure ready to be executed by the Pipeline.
    """
    def gate(state: FileState) -> FileState:

        if not state.is_valid:
            return state

        try:
            if not state.filepath.is_file():
                state.is_valid = False
                state.rejection_stage = "check_is_file"
                state.rejection_reason = "Path is not a file or does not exist."

        except PermissionError:
            state.is_valid = False
            state.rejection_stage = "check_is_file"
            state.rejection_reason = "Permission denied while checking file type."

        return state

    return gate