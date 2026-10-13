# N-Body Benchmark

A small benchmark comparing implementations of the same five-body gravitational simulation:

- C++: `src/python_nbody/cpp_nbody.cpp`
- Pure Python: `src/python_nbody/python_pure.py`
- Python with NumPy arrays: `src/python_nbody/python_numpy.py`
- Python with NumPy and Numba: `src/python_nbody/python_numba.py`

Each simulation starts with the Sun and four outer planets, adjusts the Sun's velocity to balance the system momentum, advances the system in fixed time steps, and reports its energy before and after the run.

## Requirements

- Python 3.14 or newer
- Dependencies listed in `pyproject.toml`
- A C++20 compiler for the C++ implementation

Install the Python dependencies with [uv](https://docs.astral.sh/uv/):

```bash
uv sync
uv run python src/python_nbody/python_pure.py
uv run python src/python_nbody/python_numpy.py
uv run python src/python_nbody/python_numba.py
```

Compiling and running the C++ version

```bash

g++ -O3 -std=c++20 src/python_nbody/cpp_nbody.cpp -o nbody_run
./nbody_run 50000000

```

## Benchmarks

The following values are sample benchmark results from the project and are intended for comparison only.

| Implementation | Time (s) | Factor |
| --- | ---: | ---: |
| C++ | 1.15 | 1.00x |
| Pure Python | 105.08 | 90x |
| Python + NumPy | 660 | 574x |
| Python + NumPy + Numba | 2.013 | 1.74x |
| Python + NumPy + Numba (Fast Math) | 1.95 | 1.70x |

## System Details

- OS: MacOS Tahoe 26.5.2
- Python: 3.14
- CPU: Apple M5
- RAM: 16 GB