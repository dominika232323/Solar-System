# Solar-System

This project presents an interactive simulation of planetary motion in the Solar System, where trajectories are calculated numerically based on gravitational interactions. The program provides visualization, adjustable simulation parameters, and a choice of numerical integration methods.

## How to run

### Install the required libraries:

```bash
pip install -r requirements.txt
```

### Run the project using one of the available integration methods:

```bash
python main.py --method euler
python main.py --method verlet
python main.py --method rk4
```