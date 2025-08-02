# Roster-Incident-Risk-Modelling
A simulation-based framework for illustrating co-occurrence patterns in shift-weighted healthcare rosters.

A configurable Monte Carlo simulation tool for analyzing incident exposure patterns in healthcare workforce scheduling, employing realistic nurse scheduling patterns and simulating how incidents distribute among staff members over time.

## Overview
This tool addresses a perceived gap in healthcare risk assessment and legal analysis: understanding whether observed incident patterns reflect systematic scheduling factors or indicate individual performance issues. By simulating realistic staffing patterns, the model establishes baseline expectations for incident exposure distribution.

## Key Features
Realistic Workforce Modeling: Simulates five-tier nursing workforce with varying hour commitments (9-36 hours/week, with an option for a high-impact tier)
Sophisticated Scheduling: Uses swap-based binary matrix sampling to generate feasible roster assignments
Statistical Analysis: Monte Carlo simulation with configurable parameters for robust statistical inference
Visualization: Generates histograms showing distribution of maximum incident exposure per nurse

## Use Cases
Healthcare Administration
Legal Proceedings
Academic Research

## The "Bad Penny" Fallacy
Traditional analysis might calculate incident co-occurrence probability as 0.5^n, yielding astronomically small probabilities (e.g., 0.5^25 ≈ 3×10^-8). However, this approach does not take sufficient cognisance of the structural impact of  incidents in the context of roster schedules. This model demonstrates that patterns appearing "impossibly coincidental" under naive probability assumptions can occur with reasonable frequency when systematic factors are taken into account.

## Installation
To clone the repository
git clone https://github.com/Elevation9184/Roster-Incident-Risk-Modelling.git
cd Roster-Incident-Risk-Modelling

## Install dependencies
pip install -r requirements.txt

## Requirements
```
Python 3.7+
NumPy
Matplotlib
Numba (for performance optimization)
```
## Configuration Options
### Staff tier ... adjust as required
```
TIER_SPECS = {
    'A': {'hrs_m': 36, 'hrs_sd': 3, 'count': 15},   # 3     shifts per week
    'B': {'hrs_m': 24, 'hrs_sd': 4, 'count': 10},   # 2     shifts per week
    'C': {'hrs_m': 18, 'hrs_sd': 3, 'count':  9},   # 1     shift  per week
    'D': {'hrs_m':  9, 'hrs_sd': 2, 'count':  3},   # 0.75  shifts per week
    'E': {'hrs_m': 48, 'hrs_sd': 2, 'count':  1},   # 4     shifts per week - potential exceptional performer
}
```
### Shift coverage based on CEH/16 estimates:
```
Day: rng.normal(8.78, 2.39) 
Night: rng.normal(5.63, 0.81)
```
### Configurable run parameters
run(seed=2025, incident_count=50, n_runs=1000, n_swaps=20_000)

## License
MIT License - See LICENSE file for details

## Citation
If using this code in academic or legal work, please cite:
```
Roster-Incident-Risk-Modelling: Monte Carlo Simulation of Healthcare Incident Exposure Patterns
GitHub Repository: https://github.com/Elevation9184/Roster-Incident-Risk-Modelling
```
## Disclaimer
This tool is intended for educational and analytical purposes. Results should be interpreted by qualified statisticians and domain experts. The model makes simplifying assumptions about healthcare operations and should be validated against specific institutional data before use in high-stakes decisions.

