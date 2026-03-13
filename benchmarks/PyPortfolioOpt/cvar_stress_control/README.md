# Task 02: CVaR Stress-Controlled Allocation

This benchmark focuses on tail-risk-aware optimization under scenario returns.
The optimizer must satisfy return and exposure constraints while minimizing CVaR.

## Why this task matters

Production portfolios are often constrained by drawdown and stress mandates.
Variance alone is not enough for heavy-tailed markets, so scenario-based CVaR
optimization is widely used in risk committees.

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
