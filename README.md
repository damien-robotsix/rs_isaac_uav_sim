# rs_isaac_uav_sim

Isaac Sim-based UAV simulation with ROS 2 autonomy.

This repository is undergoing a from-scratch rebuild. The current code is a
minimal skeleton: typed module seams that import cleanly in a CPU Python
environment, with no GPU or Isaac Sim dependencies at import time.

This repository follows the
[robotsix-standards](https://damien-robotsix.github.io/robotsix-standards/)
conventions, including the
[repo-baseline](https://damien-robotsix.github.io/robotsix-standards/repo-baseline/)
file set.

## Motivation

We evaluated [PegasusSimulator](https://github.com/PegasusSimulator/PegasusSimulator),
the reference Isaac Sim UAV simulator. It is mature and BSD-3 licensed, but this
repository pursues a different goal: **simulate many drones as fast as the
hardware allows**, with PX4 running on simulation time — not a simulator paced
by the wall clock.

1. **As-fast-as-possible, GPU-scale simulation.** Pegasus runs its force and
   sensor models in Python on top of Isaac's rigid-body engine and exposes no
   GPU dynamics path, which caps drone count. We want a tensorized, on-GPU
   dynamics loop where the simulation owns its own clock and advances as fast
   as compute allows — real time is just the special case of speed factor 1.

2. **PX4 on simulation time.** PX4 attaches through its SITL lockstep
   interface: sensor messages carry simulation timestamps, and PX4 slaves its
   clock to them — PX4 waits for the simulation, never the reverse. A
   **speed-factor setting** controls the target rate — unbounded ("as fast as
   compute allows") or capped to a chosen multiple of real time — and it is the
   user's responsibility to pick a value the attached PX4 instances can
   sustain. Because the link is plain MAVLink over TCP, PX4 instances can run
   on other machines. Two limits are accepted by design: the number of
   full-PX4 drones is bounded by how many PX4 SITL instances you deploy, and
   the achievable speed factor is bounded by PX4's own compute rate — the
   simulator **logs/warns** when a PX4 instance cannot keep the requested rate
   rather than silently corrupting its time base.

3. **Dependency lag.** Pegasus (5.1.0) targets Isaac Sim 5.1.0 and PX4 1.14.3,
   while Isaac Sim 6.0.1 and PX4 1.17 are current. Each Pegasus release is
   pinned to a single Isaac version, so keeping up means waiting on — or
   forking — Pegasus.

4. **Seam-separated modules.** Physics, autopilot bridge, and sensors sit
   behind their own interfaces, so a dependency version bump touches one
   module instead of the whole simulator.

If you need standard multirotor PX4/ArduPilot research simulation today, use
Pegasus. If you need GPU-scale, faster-than-real-time, many-drone simulation
with PX4 slaved to simulation time, that's what this repository is for.

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

**PX4 autopilot bridge (SITL lockstep over MAVLink).**

- Interface: `HilBridge` (ABC)
- Methods: `start()`, `stop()`, `send_sensors(sensor_state)`, `recv_actuators()`
- Responsibility: Exchange MAVLink messages with PX4 over the SITL lockstep
  interface — sensor messages carry the simulation timestamp so PX4 slaves its
  clock to simulation time; actuator commands are returned per step. PX4 waits
  for the simulation, never the reverse.
- Import-time cost: None (no MAVLink transport imports at module load).

### `rs_isaac_uav_sim.scheduler`

**Simulation-clock scheduler with a user speed factor.**

- Interface: `Scheduler` (ABC)
- Methods: `start()`, `tick()`, `overrun()`
- Responsibility: Own the simulation clock (`sim_time`) and step cadence. A
  configurable speed factor governs pacing — `0` runs as fast as compute
  allows, a positive value caps the step rate to that multiple of real time —
  and it measures the achieved rate against the requested one.
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
