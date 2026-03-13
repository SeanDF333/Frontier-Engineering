# Task 01: Robust Mean-Variance Rebalancing

This benchmark focuses on a realistic single-period portfolio rebalancing problem:
maximize risk-adjusted return under practical constraints (sector exposure, factor exposure,
weight bounds, and turnover limit), while paying transaction penalties.

## Why this task matters

A pure Markowitz optimizer is rarely deployable as-is. Real production systems must handle:
- exposure controls (sector constraints),
- style/risk controls (factor exposure constraints),
- implementation frictions (turnover and transaction costs),
- stable transitions from current holdings (`w_prev`) to new holdings (`w`).

This benchmark forces all of these constraints into one optimization problem.

## Environment Setup

Please install dependencies using the unified Task configuration:

```bash
pip install -r benchmarks/PyPortfolioOpt/requirements.txt
```

If you are running commands from this subfolder, use:

```bash
pip install -r ../requirements.txt
```

## Directory Structure

```text
.
├── README.md
├── README_zh-CN.md
├── Task.md
├── Task_zh-CN.md
├── baseline
│   └── init.py
└── verification
    ├── reference.py
    └── evaluate.py
```
