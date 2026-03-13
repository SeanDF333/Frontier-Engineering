# 任务 03：带手数约束的离散再平衡（MIP）

该基准描述“可交易化”再平衡：
目标权重必须转换成整数手数，并同时满足预算、换手和交易费约束。

## 这个任务为什么重要

优化器通常输出连续权重，但交易系统下单是整数数量。
在换手上限和交易费存在时，这会变成组合优化中的离散难题。

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
