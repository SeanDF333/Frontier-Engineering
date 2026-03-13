# 任务 02：CVaR 压力控制配置

该基准聚焦于“情景收益下的尾部风险优化”：
在收益门槛与暴露约束下，最小化组合 CVaR。

## 这个任务为什么重要

实盘组合常受回撤与压力测试指标约束。
在重尾市场中，仅用方差不足以描述风险，因此情景化 CVaR 优化在机构风控中很常见。

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
