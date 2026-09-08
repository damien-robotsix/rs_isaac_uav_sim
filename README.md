# rs_isaac_uav_sim

Isaac Sim-based UAV simulation with ROS 2 autonomy.

This repository is undergoing a from-scratch rebuild following the clean-slate architecture defined in [ADR-0001](docs/adr/0001-clean-slate-rebuild.md). This document describes the current skeleton: typed module seams that import cleanly in a CPU Python environment, with no GPU or Isaac Sim dependencies at import time.

This repository follows the
[robotsix-standards](https://damien-robotsix.github.io/robotsix-standards/)
conventions, including the
[repo-baseline](https://damien-robotsix.github.io/robotsix-standards/repo-baseline/)
file set.

## Installation

```bash
# Install the package and development dependencies
pip install -e ".[dev]"
```

This installs the package in editable mode with the `dev` extra group, which includes `pytest` and `ruff`.

## Package Structure

The `rs_isaac_uav_sim` package defines four typed module seams that serve as the architectural boundaries for the clean-slate rebuild. Each seam declares an abstract interface (typed methods, docstrings, no heavy implementation) and imports cleanly in a plain CPU Python environment:

### `rs_isaac_uav_sim.physics`

**Tensorized on-GPU dynamics engine.**

- Interface: `PhysicsEngine` (ABC)
- Methods: `reset(num_drones)`, `step(controls, dt)`, `state()`
- Responsibility: Compute dynamics for all drones in a single tensorized step on GPU.
- Import-time cost: None (no GPU or torch imports at module load).

### `rs_isaac_uav_sim.hil`

**Decoupled async hardware-in-the-loop (MAVLink/PX4) bridge.**

- Interface: `HilBridge` (ABC)
- Methods: `start()`, `stop()`, `send_sensors(sensor_state)`, `recv_actuators()`
- Responsibility: Exchange MAVLink messages with PX4 asynchronously, decoupled from the simulation step cadence.
- Import-time cost: None (no MAVLink transport imports at module load).

### `rs_isaac_uav_sim.scheduler`

**Explicit real-time scheduler.**

- Interface: `Scheduler` (ABC)
- Methods: `start()`, `tick()`, `overrun()`
- Responsibility: Own the simulation step cadence and measure it against a stated real-time budget.
- Import-time cost: None.

### `rs_isaac_uav_sim.sensors`

**Sensor model derivation from tensorized state.**

- Interface: `SensorModel` (ABC)
- Methods: `reset(num_drones)`, `sample(state, dt)`
- Responsibility: Map vehicle physics state to simulated sensor outputs (IMU, GPS, etc.).
- Import-time cost: None (no Isaac Sim imports at module load).

## Development & Testing

### Run all CPU-compatible tests (standard CI)

```bash
pytest -m "not gpu and not isaac"
```

This runs the default test suite on a standard GitHub-hosted runner with only CPU resources.

### Run all tests (including GPU and Isaac tests)

```bash
pytest
```

This runs the full test suite, including tests marked with `@pytest.mark.gpu` and `@pytest.mark.isaac`. These tests are deselected by default on standard CI runners because they require:
- **`gpu`**: NVIDIA GPU and CUDA/cuDNN.
- **`isaac`**: Isaac Sim (currently requires a self-hosted runner or manual setup).

### Lint the code

```bash
ruff check .
```

## For More Details

See [ADR-0001](docs/adr/0001-clean-slate-rebuild.md) for the complete architecture rationale and roadmap for the clean-slate rebuild.
