# 任务 01：鲁棒均值方差再平衡

该基准聚焦于一个贴近实盘的单期组合再平衡问题：
在行业暴露、因子暴露、仓位边界、换手率上限等约束下，最大化风险调整收益，同时考虑交易惩罚。

## 这个任务为什么重要

经典 Markowitz 结果通常不能直接下单，工程落地时必须处理：
- 暴露控制（行业约束）；
- 风险风格控制（因子暴露约束）；
- 实施摩擦（换手约束与交易惩罚）；
- 从当前持仓 `w_prev` 平滑过渡到新持仓 `w`。

这个基准把这些约束统一到一个优化问题里。

## 环境配置

请按统一依赖配置安装环境：

```bash
pip install -r benchmarks/PyPortfolioOpt/requirements.txt
```

如果你在当前子目录执行命令，可使用：

```bash
pip install -r ../requirements.txt
```

## 目录结构

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
