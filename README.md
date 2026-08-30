# QACO-VRPTW: Quantum-Inspired Fleet Routing Engine

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.103+-009688.svg)
![Optimization](https://img.shields.io/badge/Algorithm-QACO-purple.svg)
![Status](https://img.shields.io/badge/Status-Benchmark_Ready-success.svg)

A highly scalable backend engine utilizing **Quantum-Inspired Ant Colony Optimization (QACO)** to solve complex Vehicle Routing Problems with Time Windows (VRPTW). 

This framework applies quantum mechanics (superposition and rotation gates) to classical Data Structures and Algorithms (DSA) to dispatch fleets, manage vehicle load capacities, and satisfy strict delivery time constraints with near-optimal efficiency. Designed with a RESTful architecture, this engine is built to easily integrate into full-stack dashboards and decision-support pipelines.

## 🚀 Key Features
* **Quantum Pheromone Matrix:** Utilizes $(N+1) \times (N+1)$ qubit states $[\alpha, \beta]$ to map probabilistic routing paths.
* **Dynamic Fleet Dispatching:** Automatically spins up new vehicles based on strict weight limits and delivery window constraints.
* **Quantum Rotation Gates:** Mathematically shifts probability amplitudes to aggressively learn and reinforce optimal fleet sequences over continuous iterations.
* **REST API Delivery:** Wraps the core optimization engine in a FastAPI layer for seamless client-tier integration.
* **Solomon Benchmark Validation:** Fully compatible with standard Solomon VRPTW Kaggle CSV datasets.

## 🛠️ Tech Stack
* **Core Optimization:** Python, NumPy, SciPy (Spatial Distance Matrices)
* **Data Parsing:** Pandas
* **API Architecture:** FastAPI, Uvicorn, Pydantic

## 📂 Repository Structure
```text
qaco-vrptw-framework/
├── backend/
│   ├── api.py                    # FastAPI application and endpoints
│   └── core/
│       ├── solomon_parser.py     # Ingests and formats Kaggle CSV datasets
│       ├── qaco_vrptw_engine.py  # The primary QACO dispatcher and quantum matrix logic
│       └── classical_vrptw.py    # Clarke-Wright savings baseline algorithm
├── benchmarks/
│   ├── run_solomon_tests.py      # CLI execution script for benchmark testing
│   └── plot_results.py           # Matplotlib visualization generators
├── data/
│   └── solomon_instances/        # Directory for benchmark CSVs (e.g., C101.csv)
├── requirements.txt              # Project dependencies
└── README.md                     # Documentation
