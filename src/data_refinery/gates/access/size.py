from pathlib import Path
from core import FileState, GateFunction

def check_size(min_bytes: int = 1) -> GateFunction:
    """
        A gate factory that configures a runtime file size validation check.
        
        Args:
            min_bytes: The minimum acceptable file size in bytes. Defaults to 1 
                    to catch completely empty, zero-byte exports.
                    
        Returns:
            GateFunction: A configured closure ready to be executed by the Pipeline.
        """
    # This is the actual gate function that the Pipeline runner will execute
    def gate(state: FileState) -> FileState:
        try:
            # os.path.getsize works perfectly on Path objects
            file_size = state.filepath.stat().st_size
            
            if file_size < min_bytes:
                state.is_valid = False
                state.rejection_stage = "check_minimum_size"
                state.rejection_reason = (
                    f"File size ({file_size} bytes) is below the minimum "
                    f"threshold of {min_bytes} bytes."
                )
                
        except FileNotFoundError:
            # Defensive programming: catch if the file disappeared mid-run
            state.is_valid = False
            state.rejection_stage = "check_minimum_size"
            state.rejection_reason = "File not found during size validation."
            
        except Exception as e:
            # Catch unexpected OS/permission errors during stat call
            state.is_valid = False
            state.rejection_stage = "check_minimum_size"
            state.rejection_reason = f"OS error reading file stats: {str(e)}"
            
        return state

    return gate