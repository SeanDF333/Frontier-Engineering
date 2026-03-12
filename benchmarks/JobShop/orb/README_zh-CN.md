# ORB（Applegate & Cook，1991） 基准家族

## 背景
规模统一的 10x10 家族，便于做可复现实验与横向比较。

## 家族概览

- 前缀：`orb`
- 实例范围：orb01-orb10
- 规模范围：10x10
- 元数据里 `optimum` 未知的实例数：0

## 环境依赖

- Python：`>=3.10`
- 在仓库根目录安装统一依赖配置：
  - `pip install -r JobShop/requirements.txt`
- `baseline/init.py`：仅依赖 Python 标准库。
- `verification/reference.py` 与 `verification/evaluate.py`：
  使用仓库内本地 `job_shop_lib` 源码，并依赖 `JobShop/requirements.txt` 中的 OR-Tools（`ortools`）。

## 当前目录结构

```
.
├── README.md
├── README_zh-CN.md
├── Task.md
├── Task_zh-CN.md
├── baseline/
│   └── init.py
└── verification/
    ├── reference.py
    └── evaluate.py
```

## `evaluate.py` 参数说明

- `--instances`：可选，显式指定实例名列表。
  不传时评测该家族全部实例。
- `--max-instances`：可选，限制评测实例数量。
  在可选 `--instances` 过滤后，取前 N 个。
- `--reference-time-limit`：参考求解器每个实例的时间上限（秒）。
  默认值：`10.0`。

## 快速开始

```bash
python JobShop/orb/baseline/init.py --max-instances 2
python JobShop/orb/verification/evaluate.py --max-instances 2 --reference-time-limit 5
```
