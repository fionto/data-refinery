import sys
from pathlib import Path

# Force Python to find our local 'src' directory without needing a pip install
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from data_refinery.core import Pipeline, FileStateCollection, FileState
from data_refinery.gates.access import (
    check_extension,
    check_is_file,
    check_size,
    check_read_access,
)

def build_mock_environment(base_dir: Path) -> list[Path]:
    """Sets up physical files representing diverse real-world lab anomalies."""
    base_dir.mkdir(exist_ok=True, parents=True)
    
    files = {
        "valid_spectrum.csv": "Wave,Intensity\n200,10500\n201,10600",
        "empty_corrupted.csv": "",
        "wrong_format.json": '{"laser": "532nm"}',
        "missing_file.csv": "__TRIGGER_DELETE__"  # We will delete this to trigger a mid-run FileNotFoundError
    }
    
    paths = []
    for name, content in files.items():
        p = base_dir / name
        if content != "__TRIGGER_DELETE__":
            p.write_text(content)
        paths.append(p)
        
    return paths

def run_comprehensive_test():
    # 1. Setup workspace environment
    mock_dir = Path(__file__).parent / "test_lab_data"
    file_paths = build_mock_environment(mock_dir)
    
    # 2. Instantiate our Access Layer Pipeline using the structural factories
    access_pipeline = Pipeline(
        stage_name="access_layer_validation",
        gates=[
            check_extension(extensions=('.csv', '.txt')),
            check_is_file(),
            check_size(min_bytes=1),
            check_read_access()
        ]
    )
    
    # 3. Create our collection to aggregate batch diagnostics
    results = FileStateCollection()
    
    print("🔬 Starting 'data-refinery' End-to-End Test Stream...")
    print("=" * 80)
    
    # Simulate a file disappearing mid-pipeline run right before processing
    # (Triggers your defensive FileNotFoundError catch blocks)
    ghost_file = mock_dir / "missing_file.csv"
    if ghost_file.exists():
        ghost_file.unlink()

    # 4. Stream files using the engine's 'run_new' entry point
    for path in file_paths:
        # Convert path to string as specified by run_new(filepath: str)
        state = access_pipeline.run_new(str(path))
        results.files.append(state)

    # 5. Visual Summary Report using your Collection Class structures
    print(f"📊 BATCH DIAGNOSTICS SUMMARY:")
    print(f"   Total Files Screened: {len(results.files)}")
    print(f"   Passed Gates:        {len(results.passed())}")
    print(f"   Rejected Gates:      {len(results.rejected())}")
    print("-" * 80)

    # Print breakdown of passes
    for item in results.passed():
        print(f"🟩 PASSED | Stage: {item.pipeline_stage} | File: {item.filepath.name}")
        
    # Print breakdown of rejections
    for item in results.rejected():
        print(f"🟥 REJECTED")
        print(f"   ├── File:   {item.filepath.name}")
        print(f"   ├── Stage:  {item.pipeline_stage} ({item.rejection_stage})")
        print(f"   └── Reason: {item.rejection_reason}")
    
    print("=" * 80)
    
    # 6. Test 'run_existing' (Simulating a secondary pipeline down the road)
    print("🔄 Testing Pipeline Chaining via 'run_existing'...")
    downstream_pipeline = Pipeline(stage_name="advanced_math_parsing", gates=[])
    
    # Take a survivor from stage 1 and try to pass it to stage 2
    if results.passed():
        survivor = results.passed()[0]
        next_stage_state = downstream_pipeline.run_existing(survivor)
        print(f"   🚀 Success! File transitioned to: '{next_stage_state.pipeline_stage}'")
    
    # Environment cleanup
    for p in mock_dir.iterdir():
        p.unlink()
    mock_dir.rmdir()
    print("\n🧹 Temporary test files cleared cleanly.")

if __name__ == "__main__":
    run_comprehensive_test()