from pathlib import Path
from data_refinery.core import FileState, GateFunction

def check_size(min_bytes: int = 1) -> GateFunction:
    """
    A gate factory that configures a runtime file size validation check.
    
    Args:
        min_bytes (int): The minimum acceptable file size in bytes. Defaults to 1 
                         to catch empty/zero-byte files.
                    
    Returns:
        GateFunction: A configured closure ready to be executed by the Pipeline.
    """
    def gate(state: FileState) -> FileState:
        
        if not state.is_valid:
            return state
       
        try:
            # Clean and direct—leveraging the Path object attributes smoothly
            file_size = state.filepath.stat().st_size
            
            if file_size < min_bytes:
                state.is_valid = False
                state.rejection_stage = "check_size"
                
                # Provide a descriptive error message depending on configuration
                if min_bytes == 1:
                    state.rejection_reason = "File size is zero bytes."
                else:
                    state.rejection_reason = (
                        f"File size ({file_size} bytes) is below minimum threshold "
                        f"of {min_bytes} bytes."
                    )
                
        except FileNotFoundError:
            state.is_valid = False
            state.rejection_stage = "check_size"
            state.rejection_reason = "File not found during size validation."
            
        return state

    return gate