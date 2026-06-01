"""
Gates subpackage: Pluggable validation checks organized by validation layer.
 
The pipeline validates files through three sequential layers:
 
1. ACCESS: File-level checks—can the pipeline physically read this file?
   - Does it exist and have correct permissions?
   - Is it the right format (extension)?
   - Can it be opened at the OS level?
   - Is it non-empty?

2. STRUCTURE: Format validation—is this a well-formed data table?
   - Does it have a valid name (if lab metadata is encoded in filename)?
   - Does it have a header row?
   - Does the header match expected schema?
   - Does it have content beyond the header?
   - Does it have the expected number of columns?
   - Can it be parsed as tabular data (e.g., converted to pandas)?

3. CONTENT: Data sufficiency—is there enough meaningful data for analysis?
   - Do I have sufficient samples for statistical fitting?
   - Do I have all required columns populated?
   - Do the values fall within acceptable ranges?
   - Is data completeness adequate (e.g., missing value tolerance)?

Users import gates directly from this module without knowing which layer or file
implements each check. This decouples the public API from internal organization.
 
Example usage:
    from data_refinery.gates import check_extension, check_dataframe_schema
    
    gate_sequence = [
        check_extension,
        check_size,
        check_dataframe_schema,
    ]
   """

# ============================================================================
# ACCESS LAYER: File-system and OS-level validation gates
# ============================================================================

from data_refinery.gates.access import (
    check_extension,
    check_size,
    check_permissions,
    check_integrity,
)

# ============================================================================
# PUBLIC API
# ============================================================================

__all__ = [
    "check_extension",
    "check_size",
    "check_permissions",
    "check_integrity",
]