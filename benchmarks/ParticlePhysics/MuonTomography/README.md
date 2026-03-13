# Particle Physics: Muon Tomography Detector Placement Optimization

English | [简体中文](./README_zh-CN.md)

## 1. Task Overview

This task (Muon Tomography Optimization) is a core optimization problem in the **Particle Physics and Nuclear Engineering** domain within the `Frontier-Eng` benchmark.

Muon tomography utilizes the transmission attenuation characteristics of cosmic ray muons to probe the internal structure of large objects (e.g., pyramids, volcanoes, nuclear reactors). This task challenges the AI Agent to find an optimal spatial layout for a detector array, considering real physical constraints (such as the $\cos^2(\theta_z)$ attenuation of muon flux with the zenith angle) and strict economic constraints (detector manufacturing costs and underground excavation costs).

> **Core Challenge**: The Agent cannot simply stack detectors as close to the target as possible. Instead, it must perform precise spatial geometric calculations to find the optimal Pareto solution between "maximizing effective signal reception" and "minimizing engineering costs."

For detailed physical and mathematical models, objective functions, and I/O formats designed for the Agent, please refer to the core task document: [Task.md](./Task.md).