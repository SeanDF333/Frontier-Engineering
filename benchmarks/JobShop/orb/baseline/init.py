"""Simple greedy baseline for ORB (Applegate & Cook, 1991).

Baseline constraints:
- Pure Python implementation.
- Standard library only.
- No `job_shop_lib` import and no external solver usage.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

FAMILY_PREFIX = "orb"
FAMILY_NAME = "ORB (Applegate & Cook, 1991)"


def _natural_key(name: str) -> list[object]:
    parts = re.split(r"(\d+)", name)
    return [int(p) if p.isdigit() else p for p in parts]


def _benchmark_json_path() -> Path:
    # Preferred local path in this repository (legacy layout).
    benchmark_root = Path(__file__).resolve().parents[3]
    local_path = benchmark_root / "job_shop_lib" / "benchmarking" / "benchmark_instances.json"
    if local_path.is_file():
        return local_path

    # Fallback to installed package data (for environments without in-repo job_shop_lib source).
    for entry in sys.path:
        if not entry:
            continue
        pkg_path = Path(entry) / "job_shop_lib" / "benchmarking" / "benchmark_instances.json"
        if pkg_path.is_file():
            return pkg_path

    raise FileNotFoundError(
        "benchmark_instances.json not found. Tried local path "
        f"{local_path} and installed-package lookup via sys.path."
    )


def load_benchmark_json() -> dict[str, dict[str, Any]]:
    with _benchmark_json_path().open("r", encoding="utf-8") as f:
        return json.load(f)


def load_family_instances() -> list[dict[str, Any]]:
    data = load_benchmark_json()
    selected = [
        value
        for name, value in data.items()
        if name.startswith(FAMILY_PREFIX)
    ]
    return sorted(selected, key=lambda x: _natural_key(x["name"]))


def load_instance_by_name(name: str) -> dict[str, Any]:
    data = load_benchmark_json()
    if name not in data:
        raise KeyError(f"Unknown instance: {name}")
    return data[name]


def solve_instance(instance: dict[str, Any]) -> dict[str, Any]:
    """Greedy EST+SPT scheduler on raw benchmark matrices.

    Input:
        instance dict with keys:
        - name
        - duration_matrix
        - machines_matrix
        - metadata

    Output:
        dict with at least:
        - name
        - makespan
        - machine_schedules
    """
    durations: list[list[int]] = instance["duration_matrix"]
    machines: list[list[int]] = instance["machines_matrix"]

    num_jobs = len(durations)
    total_operations = sum(len(job) for job in durations)
    num_machines = max(max(row) for row in machines) + 1

    next_op = [0] * num_jobs
    job_ready = [0] * num_jobs
    machine_ready = [0] * num_machines

    machine_schedules: list[list[dict[str, int]]] = [
        [] for _ in range(num_machines)
    ]

    scheduled = 0
    while scheduled < total_operations:
        candidates: list[tuple[int, int, int, int, int]] = []
        # (earliest_start, duration, job_id, op_idx, machine_id)
        for job_id in range(num_jobs):
            op_idx = next_op[job_id]
            if op_idx >= len(durations[job_id]):
                continue

            machine_id = machines[job_id][op_idx]
            duration = durations[job_id][op_idx]
            est = max(job_ready[job_id], machine_ready[machine_id])
            candidates.append((est, duration, job_id, op_idx, machine_id))

        if not candidates:
            raise RuntimeError("No schedulable operation found.")

        est, duration, job_id, op_idx, machine_id = min(
            candidates,
            key=lambda x: (x[0], x[1], x[2]),
        )
        end = est + duration

        machine_schedules[machine_id].append(
            {
                "job_id": job_id,
                "operation_index": op_idx,
                "start_time": est,
                "end_time": end,
                "duration": duration,
            }
        )

        next_op[job_id] += 1
        job_ready[job_id] = end
        machine_ready[machine_id] = end
        scheduled += 1

    makespan = max(job_ready) if job_ready else 0
    return {
        "name": instance["name"],
        "makespan": makespan,
        "machine_schedules": machine_schedules,
        "solved_by": "GreedyESTSPTBaseline",
        "family": FAMILY_PREFIX,
    }


def _cli() -> None:
    parser = argparse.ArgumentParser(
        description=f"Run pure-python baseline on {FAMILY_NAME}."
    )
    parser.add_argument(
        "--instance",
        type=str,
        default=None,
        help="Instance name. If omitted, run the first N family instances.",
    )
    parser.add_argument(
        "--max-instances",
        type=int,
        default=3,
        help="How many family instances to run when --instance is omitted.",
    )
    args = parser.parse_args()

    if args.instance:
        instances = [load_instance_by_name(args.instance)]
    else:
        instances = load_family_instances()[: max(args.max_instances, 1)]

    for instance in instances:
        start = time.perf_counter()
        result = solve_instance(instance)
        elapsed = time.perf_counter() - start
        print(
            f"[{FAMILY_PREFIX}] {instance['name']}: "
            f"makespan={result['makespan']} elapsed={elapsed:.4f}s"
        )


if __name__ == "__main__":
    _cli()
