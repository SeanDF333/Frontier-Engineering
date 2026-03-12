# JobShop Benchmark Workspace

This folder organizes 7 classic JSSP benchmark families into a uniform training/evaluation layout.

## Shared traits

- All families are **classical JSSP** instances: each job has a fixed operation order and each operation uses one machine.
- Objective is to minimize **makespan** (time when all jobs are completed).
- Each family provides benchmark metadata: `optimum` (if known), `lower_bound`, `upper_bound`, and literature `reference`.
- Each family folder has the same files:
  - `README.md`, `README_zh-CN.md`
  - `Task.md`, `Task_zh-CN.md`
  - `baseline/init.py` (simple greedy solver; pure Python, stdlib only)
  - `verification/reference.py` (OR-Tools CP-SAT reference)
  - `verification/evaluate.py` (runs baseline + reference and scores both)

## Key differences

| Family | Count | Typical sizes (jobs x machines) | Difficulty trend |
|---|---:|---|---|
| FT | 3 | 6x6, 10x10, 20x5 | Introductory / teaching-friendly |
| LA | 40 | 10x5 to 30x10 | Standard mid-scale benchmark |
| ABZ | 5 | 10x10, 20x15 | Medium to hard |
| ORB | 10 | 10x10 | Medium; often used for controlled comparisons |
| SWV | 20 | 20x10, 20x15, 50x10 | Larger and harder |
| YN | 4 | 20x20 | Hard and dense |
| TA | 80 | 15x15 to 100x20 | Large-scale stress-test set |

## Scoring conventions used here

- **Best-known score**: `score_best = min(100, 100 * target / makespan)`
  - `target = optimum` if known, otherwise `upper_bound`
- **Theoretical-limit score**: `score_lb = min(100, 100 * lower_bound / makespan)`
  - `100` is the theoretical ceiling under this formula.
- Higher score is better.

## Environment

- Python: `>=3.10`
- Install shared dependencies from repository root:
  - `pip install -r JobShop/requirements.txt`
- Baseline (`baseline/init.py`): Python standard library only.
- Reference + evaluation scripts use local `job_shop_lib` source code in this repository
  and OR-Tools (`ortools`) from `JobShop/requirements.txt`.

## `evaluate.py` arguments

- `--instances`: optional explicit instance names.
  If omitted, all instances in the selected family are evaluated.
- `--max-instances`: optional cap on selected instances.
  The evaluator keeps the first N instances after optional `--instances` filtering.
- `--reference-time-limit`: time limit (seconds) per instance for reference solver.
  Default: `10.0`.

## Run examples

```bash
python JobShop/ft/verification/evaluate.py --max-instances 3 --reference-time-limit 5
python JobShop/ta/verification/evaluate.py --max-instances 2 --reference-time-limit 5
```
