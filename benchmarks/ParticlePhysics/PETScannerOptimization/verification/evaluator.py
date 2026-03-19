import json
import sys
import math
from pathlib import Path

def evaluate(solution_path: Path) -> dict:
    if not solution_path.exists():
        return {"status": "failed", "message": f"Solution file not found: {solution_path}"}
        
    try:
        with open(solution_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return {"status": "failed", "message": f"Failed to parse JSON: {e}"}

    try:
        R = float(data.get("ring_radius", 400.0))
        L = float(data.get("axial_length", 200.0))
        H = float(data.get("crystal_thickness", 20.0))
        W = float(data.get("crystal_width", 3.0))
    except ValueError:
        return {"status": "failed", "message": "Invalid variable types. Must be floats."}

    
    out_of_bounds_penalty = 0.0
    if not (300 <= R <= 500): out_of_bounds_penalty += 5000
    if not (150 <= L <= 300): out_of_bounds_penalty += 5000
    if not (10 <= H <= 30): out_of_bounds_penalty += 5000
    if not (2 <= W <= 6): out_of_bounds_penalty += 5000

    
    volume = math.pi * ((R + H)**2 - R**2) * L
    
    # 灵敏度 (Sensitivity)
    # 衰减系数 mu = 0.087 mm^-1 for 511 keV in LYSO
    solid_angle_factor = L / math.sqrt(R**2 + (L/2)**2)
    stopping_power = (1.0 - math.exp(-0.087 * H))**2
    sensitivity = solid_angle_factor * stopping_power
    
    # 视差误差与分辨率展宽 (Parallax Error / DOI)
    gamma = math.sqrt(W**2 + (200.0 * H / R)**2)


    MAX_VOLUME = 15000000.0
    
    cost_penalty = 0.0
    if volume > MAX_VOLUME:
        cost_penalty = (volume - MAX_VOLUME) * 0.002
        

    sensitivity_score = sensitivity * 20000.0
    resolution_penalty = gamma * 500.0
    
    total_score = sensitivity_score - resolution_penalty - cost_penalty - out_of_bounds_penalty

    return {
        "status": "success",
        "score": total_score,
        "metrics": {
            "volume_mm3": volume,
            "sensitivity_factor": sensitivity,
            "resolution_gamma": gamma,
            "cost_penalty": cost_penalty
        }
    }

if __name__ == "__main__":
    target_file = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("solution.json")
    
    result = evaluate(target_file)
    print(json.dumps(result))