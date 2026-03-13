# Task 03: Discrete Rebalance with Lot Constraints (MIP)

This benchmark models execution-ready rebalancing: target portfolio weights must be converted
into integer lots under budget, turnover, and fee constraints.

## Why this task matters

Optimization outputs continuous weights, but trading systems place integer orders.
This gap creates a hard combinatorial optimization problem, especially with turnover limits
and transaction fees.

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
