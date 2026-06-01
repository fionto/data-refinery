from pathlib import Path
from ...core import FileState, GateFunction

def check_is_file() -> GateFunction:
    """
    A gate factory that configures a runtime file-type validation check.
    
    Args:
        None (This specific factory only verifies path type).
                
    Returns:
        GateFunction: A configured closure ready to be executed by the Pipeline.
    """
    def gate(state: FileState) -> FileState:
        if not state.is_valid:
            return state

        try:
            # Verify the path exists and is a regular file (not a directory or symlink loop)
            if not state.filepath.is_file():
                state.is_valid = False
                state.rejection_stage = "check_is_file"
                state.rejection_reason = "Path does not point to a regular file or does not exist."

        except PermissionError:
            state.is_valid = False
            state.rejection_stage = "check_is_file"
            state.rejection_reason = "Permission denied while checking file type."

        return state

    return gate