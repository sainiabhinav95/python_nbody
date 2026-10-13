# N-Body Benchmark

A small benchmark comparing implementations of the same five-body gravitational simulation:

- C++: `src/python_nbody/cpp_nbody.cpp`
- Pure Python: `src/python_nbody/python_pure.py`
- Python with NumPy arrays: `src/python_nbody/python_numpy.py`
- Python with NumPy and Numba: `src/python_nbody/python_numba.py`

Each simulation starts with the Sun and four outer planets, adjusts the Sun's velocity to balance the system momentum, advances the system in fixed time steps, and reports its energy before and after the run.

## Requirements

- Python 3.13 or newer
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
| C++ | 2.04 | 1.00x |
| Pure Python | 152.83 | 69.15x |
| Python + NumPy | 660 | 298.64x |
| Python + NumPy + Numba | 2.828 | 1.28x |
| Python + NumPy + Numba (Fast Math) | 2.446 | 1.11x |

## System Details

- OS: Linux
- Python: 3.13.15
- CPU: Ryzen 5 7500X3D
- RAM: 32 GB DDR5 6000 Mhz
- GPU: AMD RX 9070