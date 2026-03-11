# EVOLVE-BLOCK-START
"""Baseline for UAVInspectionCoverageWithWind.

Strategy:
- Nearest uncovered inspection-point guidance.
- Wind compensation and acceleration clipping.
- Soft repulsion from no-fly zones and bounds.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np


def _wind_velocity(scene: dict[str, Any], t: float) -> np.ndarray:
    wind = scene["wind"]
    base = np.array(wind["base"], dtype=float)
    amp = np.array(wind["amplitude"], dtype=float)
    freq = np.array(wind["frequency"], dtype=float)
    phase = np.array(wind["phase"], dtype=float)
    return base + amp * np.sin(freq * t + phase)


def _repel_from_bounds(pos: np.ndarray, bounds: list[float], gain: float = 2.2, margin: float = 1.2) -> np.ndarray:
    xmin, xmax, ymin, ymax, zmin, zmax = map(float, bounds)
    repel = np.zeros(3, dtype=float)

    if pos[0] < xmin + margin:
        repel[0] += gain * (xmin + margin - pos[0])
    if pos[0] > xmax - margin:
        repel[0] -= gain * (pos[0] - (xmax - margin))
    if pos[1] < ymin + margin:
        repel[1] += gain * (ymin + margin - pos[1])
    if pos[1] > ymax - margin:
        repel[1] -= gain * (pos[1] - (ymax - margin))
    if pos[2] < zmin + margin * 0.6:
        repel[2] += gain * (zmin + margin * 0.6 - pos[2])
    if pos[2] > zmax - margin * 0.6:
        repel[2] -= gain * (pos[2] - (zmax - margin * 0.6))
    return repel


def _repel_from_no_fly(pos: np.ndarray, zones: list[dict[str, Any]], gain: float = 2.2, influence: float = 1.0) -> np.ndarray:
    repel = np.zeros(3, dtype=float)
    for zone in zones:
        if zone.get("type") != "box":
            continue
        pmin = np.array(zone["min"], dtype=float)
        pmax = np.array(zone["max"], dtype=float)
        closest = np.clip(pos, pmin, pmax)
        delta = pos - closest
        dist = float(np.linalg.norm(delta))
        if dist < influence:
            if dist < 1e-8:
                center = 0.5 * (pmin + pmax)
                d = pos - center
                n = float(np.linalg.norm(d))
                if n < 1e-8:
                    d = np.array([1.0, 0.0, 0.0], dtype=float)
                    n = 1.0
                delta = d / n
                dist = 0.0
            else:
                delta = delta / dist
            repel += gain * (influence - dist) * delta
    return repel


def _dynamic_obstacle_position(obstacle: dict[str, Any], t: float) -> np.ndarray:
    traj = obstacle.get("trajectory", [])
    if not isinstance(traj, list) or len(traj) == 0:
        return np.array([1e9, 1e9, 1e9], dtype=float)

    t_nodes = np.array([float(node["t"]) for node in traj], dtype=float)
    p_nodes = np.array([node["pos"] for node in traj], dtype=float)
    if t <= float(t_nodes[0]):
        return p_nodes[0]
    if t >= float(t_nodes[-1]):
        return p_nodes[-1]

    idx = int(np.searchsorted(t_nodes, t, side="right") - 1)
    idx = max(0, min(idx, len(t_nodes) - 2))
    t0, t1 = float(t_nodes[idx]), float(t_nodes[idx + 1])
    p0, p1 = p_nodes[idx], p_nodes[idx + 1]
    alpha = 0.0 if t1 <= t0 else float((t - t0) / (t1 - t0))
    return p0 + alpha * (p1 - p0)


def _repel_from_dynamic_obstacles(
    pos: np.ndarray,
    dynamic_obstacles: list[dict[str, Any]],
    t: float,
    gain: float = 3.0,
    influence_margin: float = 1.1,
) -> np.ndarray:
    repel = np.zeros(3, dtype=float)
    for obs in dynamic_obstacles:
        radius = float(obs.get("radius", 0.0))
        if radius <= 0.0:
            continue
        center = _dynamic_obstacle_position(obs, t)
        delta = pos - center
        dist = float(np.linalg.norm(delta))
        influence = radius + influence_margin
        if dist < influence:
            if dist < 1e-8:
                delta = np.array([1.0, 0.0, 0.0], dtype=float)
                dist = 0.0
            else:
                delta = delta / dist
            repel += gain * (influence - dist) * delta
    return repel


def _clip_norm(vec: np.ndarray, max_norm: float) -> np.ndarray:
    n = float(np.linalg.norm(vec))
    if n <= max_norm or n < 1e-12:
        return vec
    return vec * (max_norm / n)


def build_submission_for_scene(scene: dict[str, Any], dt: float, coverage_radius: float) -> dict[str, Any]:
    t_max = float(scene["T_max"])
    v_max = float(scene["uav"]["v_max"])
    a_max = float(scene["uav"]["a_max"])
    points = np.array(scene["inspection_points"], dtype=float)
    visited = np.zeros(len(points), dtype=bool)

    state = np.array(scene["start"], dtype=float)
    pos = state[:3].copy()
    vel = state[3:].copy()

    timestamps: list[float] = [0.0]
    controls: list[list[float]] = [[0.0, 0.0, 0.0]]

    t = 0.0
    while t + dt <= t_max + 1e-12:
        dists = np.linalg.norm(points - pos, axis=1)
        visited |= dists <= coverage_radius

        unvisited = np.where(~visited)[0]
        if len(unvisited) > 0:
            nearest_idx = int(unvisited[np.argmin(dists[unvisited])])
            target = points[nearest_idx]
        else:
            target = points[int(np.argmin(dists))]

        wind_v = _wind_velocity(scene, t)
        to_target = target - pos
        desired_vel = _clip_norm(1.2 * to_target, 0.8 * v_max)
        xmin, xmax, ymin, ymax, zmin, zmax = map(float, scene["bounds"])
        edge = 1.0
        if pos[0] > xmax - edge:
            desired_vel[0] = min(desired_vel[0], -0.8)
        if pos[0] < xmin + edge:
            desired_vel[0] = max(desired_vel[0], 0.8)
        if pos[1] > ymax - edge:
            desired_vel[1] = min(desired_vel[1], -0.8)
        if pos[1] < ymin + edge:
            desired_vel[1] = max(desired_vel[1], 0.8)
        if pos[2] > zmax - edge * 0.6:
            desired_vel[2] = min(desired_vel[2], -0.4)
        if pos[2] < zmin + edge * 0.6:
            desired_vel[2] = max(desired_vel[2], 0.4)

        a_cmd = 1.4 * (desired_vel - vel) - 0.75 * wind_v
        a_cmd += _repel_from_bounds(pos, scene["bounds"])
        a_cmd += _repel_from_no_fly(pos, scene["no_fly_zones"])
        a_cmd += _repel_from_dynamic_obstacles(
            pos=pos,
            dynamic_obstacles=scene.get("dynamic_obstacles", []),
            t=t,
        )
        a_cmd = _clip_norm(a_cmd, 0.9 * a_max)

        vel = vel + a_cmd * dt
        vel = _clip_norm(vel, 0.95 * v_max)
        pos = pos + (vel + wind_v) * dt
        t = round(t + dt, 10)

        timestamps.append(float(t))
        controls.append([float(a_cmd[0]), float(a_cmd[1]), float(a_cmd[2])])

    return {"id": scene["id"], "timestamps": timestamps, "controls": controls}


def main() -> None:
    task_root = Path(__file__).resolve().parents[1]
    scenarios_path = task_root / "references" / "scenarios.json"

    with scenarios_path.open("r", encoding="utf-8-sig") as f:
        cfg = json.load(f)

    dt = float(cfg.get("dt", 0.1))
    coverage_radius = float(cfg.get("coverage_radius", 0.45))
    scenario_entries = [
        build_submission_for_scene(scene, dt=dt, coverage_radius=coverage_radius)
        for scene in cfg["scenarios"]
    ]

    submission = {"scenarios": scenario_entries}
    with open("submission.json", "w", encoding="utf-8") as f:
        json.dump(submission, f, indent=2)

    print("Baseline submission written to submission.json")


if __name__ == "__main__":
    main()
# EVOLVE-BLOCK-END
