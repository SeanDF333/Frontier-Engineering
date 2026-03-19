import json
from pathlib import Path

# EVOLVE-BLOCK-START
def generate_baseline():
    """
    Generate a heuristic baseline for PET scanner geometry.
    Strategy: A very conservative approach using thin crystals (10mm) to strictly
    avoid the volume/cost budget limit, at the severe expense of sensitivity.
    """
    return {
        "ring_radius": 400.0,
        "axial_length": 200.0,
        "crystal_thickness": 10.0,
        "crystal_width": 4.0
    }
# EVOLVE-BLOCK-END

def _output_path() -> Path:
    # frontier_eval evaluates candidates from a temporary working directory,
    # so the contract is to always write `solution.json` in the current cwd.
    return Path("solution.json")

if __name__ == "__main__":
    design_data = generate_baseline()
    output_path = _output_path()
    
    try:
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(design_data, f, indent=2)
        print(f"Baseline design successfully generated: {output_path.as_posix()}")
    except Exception as e:
        print(f"Failed to generate baseline design: {str(e)}")