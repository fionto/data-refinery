from pathlib import Path
from core import FileState, GateFunction

def check_extension(extensions: tuple[str, ...] = ('.txt', '.csv')) -> GateFunction:
    """
    A gate factory that configures a runtime file extension validation check.
    
    This factory pre-normalizes allowed extensions to lowercase to ensure 
    case-insensitive validation when files stream through the pipeline runner.
    
    Args:
        extensions (tuple[str, ...]): A tuple of allowed file extensions, including 
            the leading dot (e.g., ('.csv', '.raman', '.txt')). Defaults to ('.txt', '.csv').
                    
    Returns:
        GateFunction: A configured closure ready to be executed by the Pipeline.
    """

    # Performance Optimization: Normalize extensions once at factory creation time 
    # so we don't repeat loop iterations inside the pipeline stream.
    normalized_exts = tuple(ext.lower() for ext in extensions)

    def gate(state: FileState) -> FileState:
        if not state.is_valid:
            return state
        
        # Extract suffix safely via pathlib and normalize to lowercase
        suffix = state.filepath.suffix.lower()

        if suffix not in normalized_exts:
            state.is_valid = False
            state.rejection_stage = "check_extension"
            state.rejection_reason = (
                f"Invalid file extension '{suffix}'. "
                f"Allowed extensions: {', '.join(normalized_exts)}"
            )
        
        return state
    
    return gate