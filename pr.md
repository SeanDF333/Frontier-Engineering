## 任务概述
本 PR 新增并整理了 6 个工程优化 benchmark，覆盖机器人群飞控制、增材制造可微仿真、电动车智能充电、数据库工作负载优化、结构拓扑优化与飞行器概念设计。

所有任务均按 Frontier-Engineering 统一范式提供：
- 可演化候选程序（`scripts/init.py` 或等价入口）
- 独立评测器（`verification/evaluator.py`）
- unified 接入元数据（`benchmarks/<Domain>/<Task>/frontier_eval/*`）

作者：`@DocZbs`

## 领域与任务名称
| 领域 | 任务名称 | 对应 benchmark 路径 | 来源/参考 |
|---|---|---|---|
| Robotics | `CoFlyersVasarhelyiTuning` | `Robotics/CoFlyersVasarhelyiTuning` | https://github.com/micros-uav/CoFlyers |
| AdditiveManufacturing | `DiffSimThermalControl` | `AdditiveManufacturing/DiffSimThermalControl` | https://github.com/mojtabamozaffar/differentiable-simulation-am |
| PowerSystems | `EV2GymSmartCharging` | `PowerSystems/EV2GymSmartCharging` | https://github.com/StavrosOrf/EV2Gym |
| ComputerSystems | `DuckDBWorkloadOptimization` | `ComputerSystems/DuckDBWorkloadOptimization` | SQL workload tuning task design (index/MV + rewrite) |
| StructuralOptimization | `PyMOTOSIMPCompliance` | `StructuralOptimization/PyMOTOSIMPCompliance` | https://github.com/aatmdelissen/pyMOTO |
| Aerodynamics | `DawnAircraftDesignOptimization` | `Aerodynamics/DawnAircraftDesignOptimization` | https://github.com/peterdsharpe/DawnDesignTool |

## 背景与来源
1. `CoFlyersVasarhelyiTuning`：多无人机队形收敛与避碰控制，目标兼顾收敛时间、碰撞惩罚与控制平滑性。
2. `DiffSimThermalControl`：增材制造中热过程参数优化，目标是在仿真调用预算下最小化缺陷/应力 proxy loss。
3. `EV2GymSmartCharging`：多 EV + 小型配网调度，优化电费、过载惩罚与电压偏差代理指标。
4. `DuckDBWorkloadOptimization`：联合索引/物化视图选择与查询改写，目标是工作负载总时延优化并保证语义一致。
5. `PyMOTOSIMPCompliance`：体积分数约束下的柔度最小化拓扑优化，采用 SIMP 风格基线与可演化更新策略。
6. `DawnAircraftDesignOptimization`：在巡航/续航/载荷约束下联合优化机翼、机身、动力参数，最小化总质量。

## 解决方案方法
- 每个任务都提供可行 baseline（可执行、可评测）。
- 评测器负责：约束检查、指标计算、`valid/combined_score` 汇总。
- unified 元数据中提供：
  - `initial_program.txt`
  - `eval_command.txt`
  - `constraints.txt`
  - 可选 `readonly_files.txt` / `agent_files.txt`
- 支持 `python -m frontier_eval ... algorithm.iterations=0` 快速接入自检。

## 如何运行验证
### 基本功能测试（在任务目录内）
```bash
python verification/evaluator.py scripts/init.py
```

### 框架集成测试（统一）
```bash
python -m frontier_eval task=unified task.benchmark=<Domain>/<Task> task.runtime.use_conda_run=false algorithm.iterations=0
```

### 已配置快捷 task（可直接跑）
```bash
python -m frontier_eval task=coflyers_vasarhelyi_tuning algorithm.iterations=0
python -m frontier_eval task=diffsim_thermal_control algorithm.iterations=0
python -m frontier_eval task=ev2gym_smart_charging algorithm.iterations=0
python -m frontier_eval task=duckdb_workload_optimization algorithm.iterations=0
python -m frontier_eval task=pymoto_simp_compliance algorithm.iterations=0
python -m frontier_eval task=dawn_aircraft_design_optimization algorithm.iterations=0
```

## 测试证据
测试日期：2026-03-19

### 1) 基本功能测试（`python verification/evaluator.py scripts/init.py`）
- `Aerodynamics/DawnAircraftDesignOptimization`
  - 退出码：`0`
  - 输出：`{"score": 0.7414962858845127, "valid": 1.0, "total_mass_kg": 139.44976881826167, "cruise_power_kw": 1.9376303112971096}`
- `Robotics/CoFlyersVasarhelyiTuning`
  - 退出码：`0`
  - 输出（节选）：`{"combined_score": 45.62863404341821, "valid": 1.0, ...}`
- `AdditiveManufacturing/DiffSimThermalControl`
  - 退出码：`0`
  - 输出（节选）：`{"combined_score": 0.4607170813812293, "valid": 1.0, ...}`
- `PowerSystems/EV2GymSmartCharging`
  - 退出码：`0`
  - 输出：`{"combined_score": 99.96840069399254, "score": 99.96840069399254, "valid": 1.0, "runtime_s": 7.776015758514404, "mean_total_reward": -368768.90256949054, "mean_total_profits": -110.56453684223534, "mean_energy_user_satisfaction": 100.0}`
- `ComputerSystems/DuckDBWorkloadOptimization`
  - 退出码：`0`
  - 指标：`combined_score=1.0129468412794114, valid=1.0`
- `StructuralOptimization/PyMOTOSIMPCompliance`
  - 退出码：`0`
  - 输出：`{"combined_score": 4.834812682789783, "valid": 1.0, "runtime_s": 2.7229208946228027, "timeout": 0.0, "candidate_returncode": 0.0, "compliance": 218.2753434164417, "volume_fraction": 0.4999927628746863, "feasible": 1.0, "baseline_uniform_compliance": 1055.3203986901078, "score_ratio": 4.834812682789783}`

### 2) 框架集成测试（`python -m frontier_eval ... algorithm.iterations=0`）
- `Aerodynamics/DawnAircraftDesignOptimization`：`exit=0`, `Best score=0.7414962858845127`, `valid=1.0000`
- `Robotics/CoFlyersVasarhelyiTuning`：`exit=0`, `Best score=45.62863404341821`, `valid=1.0000`
- `AdditiveManufacturing/DiffSimThermalControl`：`exit=0`, `Best score=0.4607170813812293`, `valid=1.0000`
- `PowerSystems/EV2GymSmartCharging`：`exit=0`, `Best score=99.96840069399254`, `valid=1.0000`
- `ComputerSystems/DuckDBWorkloadOptimization`：`exit=0`, `Best score=0.9971130125681027`, `valid=1.0000`
- `StructuralOptimization/PyMOTOSIMPCompliance`：`exit=0`, `Best score=4.834812682789783`, `valid=1.0000`


## 备注
- 本 PR 的主要交付是 benchmark 任务与评测接入本身。
- 对于依赖驱动的任务（EV2Gym），建议在 CI 或指定环境中补跑“基础功能测试”以确保依赖与评分一致。
- `PyMOTOSIMPCompliance` 已采用轻依赖（NumPy-only）实现，规避了本地 SciPy ABI 差异导致的失效问题。
