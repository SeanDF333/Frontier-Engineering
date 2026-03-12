# JobShop 基准工作区

这个目录把 7 个经典 JSSP 基准家族统一成同一套训练/评测结构。

## 共同点

- 全部是**经典 JSSP**：每个工件的工序顺序固定，每道工序只在一台机器上加工。
- 目标都是最小化 **makespan（总完工时间）**。
- 每个实例都带有元数据：`optimum`（若已知）、`lower_bound`、`upper_bound`、`reference`。
- 每个家族目录结构一致：
  - `README.md`, `README_zh-CN.md`
  - `Task.md`, `Task_zh-CN.md`
  - `baseline/init.py`（简单贪心基线，纯 Python 标准库实现）
  - `verification/reference.py`（可调用 OR-Tools CP-SAT 的参考实现）
  - `verification/evaluate.py`（同时评测 baseline 和 reference 并打分）

## 主要差异

| 家族 | 实例数 | 典型规模（工件 x 机器） | 难度趋势 |
|---|---:|---|---|
| FT | 3 | 6x6, 10x10, 20x5 | 入门教学友好 |
| LA | 40 | 10x5 到 30x10 | 中等规模，最常用 |
| ABZ | 5 | 10x10, 20x15 | 中到高难 |
| ORB | 10 | 10x10 | 中等，便于横向比较 |
| SWV | 20 | 20x10, 20x15, 50x10 | 规模更大、难度更高 |
| YN | 4 | 20x20 | 高难、约束密集 |
| TA | 80 | 15x15 到 100x20 | 大规模压力测试 |

## 本目录评分规则

- **最佳已知得分**：`score_best = min(100, 100 * target / makespan)`
  - 若 `optimum` 已知，`target = optimum`；否则 `target = upper_bound`
- **理论上限对比得分**：`score_lb = min(100, 100 * lower_bound / makespan)`
  - 在该公式下，理论上限是 `100`。
- 分数越高越好。

## 环境依赖

- Python：`>=3.10`
- 在仓库根目录安装统一依赖配置：
  - `pip install -r JobShop/requirements.txt`
- baseline（`baseline/init.py`）：仅依赖 Python 标准库。
- reference + evaluate 使用仓库内本地 `job_shop_lib` 源码，
  并依赖 `JobShop/requirements.txt` 中的 OR-Tools（`ortools`）。

## `evaluate.py` 参数说明

- `--instances`：可选，显式指定实例名列表。
  不传时评测所选家族全部实例。
- `--max-instances`：可选，限制评测实例数量。
  在可选 `--instances` 过滤后，取前 N 个。
- `--reference-time-limit`：参考求解器每个实例的时间上限（秒）。
  默认值：`10.0`。

## 运行示例

```bash
python JobShop/ft/verification/evaluate.py --max-instances 3 --reference-time-limit 5
python JobShop/ta/verification/evaluate.py --max-instances 2 --reference-time-limit 5
```
