# 🛡️ Real-to-Sim Safety Verification Pipeline

![Isaac Sim](https://img.shields.io/badge/Isaac%20Sim-4.0.0-green.svg)
![IsaacLab](https://img.shields.io/badge/IsaacLab-latest-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10-yellow.svg)

> **A scalable, physics-based evaluation pipeline for robotic motion policies in dynamically reconstructed real-world environments.**

This project is developed as a technical evaluation for the Embodied AI research program. It bridges the gap between real-world visual reconstruction and physics-based motion safety validation using **IsaacLab** and **cuRobo**.

## 🎥 Project Demo
*(Coming Soon: A 60-second video demonstrating the Franka FR3 avoiding dynamic obstacles in a reconstructed room)*

## ✨ Core Features
1. **Real-to-Sim Asset Ingestion:** Import `.glb/.usd` 3D meshes from real-world scans (via Polycam/Gaussian Splatting) with high-fidelity collision physics.
2. **Dynamic Scene Generation:** Programmatically spawn and animate dynamic obstacles within the free space of the reconstructed environment.
3. **Motion Safety Verification:** Integrate Franka FR3 URDF and utilize `cuRobo` for collision-free trajectory generation and real-time contact listening.

## 🛠️ Tech Stack
* **Simulation Engine:** NVIDIA Isaac Sim 4.0.0 & IsaacLab
* **Motion Planning:** NVIDIA cuRobo
* **Robot Asset:** Franka Emika FR3 (URDF)
* **Hardware:** NVIDIA RTX 4090D

## 🚀 Quick Start
*(Detailed reproduction steps will be updated here...)*

---
*Developed by [你的名字/ID] | 2026*
