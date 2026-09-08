# ADR-0001: Clean-slate rebuild for a sim-time, many-drone UAV simulator

- Status: Accepted (amended 2026-09-08: timing model and PX4 integration path)
- Date: 2026-09-07
- Deciders: Robotsix

## Context

`rs_isaac_uav_sim` is a proof-of-concept NVIDIA Isaac Sim UAV simulator. It
spawns quadrotors in Isaac Sim and bridges to PX4 via MAVLink
hardware-in-the-loop (HIL). The PoC works as a demo but never reached reliable
real-time performance — and the ultimate goal has since been sharpened: the
simulator must run **as fast as the hardware allows** for many drones, with
real time as a special case rather than the target.

The root causes of the PoC's failure are structural, not incidental:

- **GPU→CPU synchronization on every physics step.** Each step stalls waiting
  for data to come back to the host, destroying throughput.
- **Per-drone Python/scipy work in the hot loop.** Dynamics are computed
  per-vehicle on the CPU, so cost scales linearly with the number of drones and
  cannot exploit the GPU.
- **No coherent time base.** The PoC paced itself off the wall clock and the
  MAVLink round-trip implicitly, with no owned simulation clock — so it could
  neither hold real time nor run faster than it.

PX4 offers two integration paths with opposite timestamp semantics (verified
in PX4 source, `main`):

- **HITL** (`mavlink_receiver.cpp`): incoming `HIL_SENSOR` data is stamped
  with PX4's local `hrt_absolute_time()`; the message's `time_usec` is
  ignored. This path only works in real time.
- **SITL lockstep** (`SimulatorMavlink.cpp`): PX4 rebases its monotonic clock
  onto `HIL_SENSOR.time_usec` (`px4_clock_settime`). Simulation time drives
  PX4, so faster- and slower-than-real-time are coherent.

Only the SITL lockstep path is compatible with the goal.

## Decision

Rebuild the simulator from a clean slate around a **simulation-owned clock**:

- **On-GPU, tensorized physics** across all drones — no per-vehicle CPU work in
  the hot loop, no per-step GPU→CPU sync.
- **Sim-clock scheduler with a user speed factor.** The scheduler owns a
  monotonic `sim_time`, advanced by `dt` per step. A configurable
  **speed factor** governs pacing: `0`/`unlimited` runs as fast as compute
  allows; a positive value (e.g. `1.0` real time, `5.0` five-times real time)
  caps the step rate to that multiple of wall time. Choosing a sustainable
  value is the user's responsibility.
- **PX4 via SITL lockstep, slaved to sim time.** Sensor messages carry
  `time_usec = sim_time`; each PX4 instance rebases its clock onto them and
  returns `HIL_ACTUATOR_CONTROLS`. **PX4 waits for the simulation, never the
  reverse.** A PX4 instance that cannot keep pace at the requested speed factor
  is **detected and logged/warned** (per-instance achieved-vs-requested rate);
  the simulation does not stall for it, and the operator decides whether to
  lower the factor. This surfaces the limit instead of hiding it as silent
  estimator corruption.
- **Deportable autopilots.** The PX4 link is plain MAVLink over TCP (one
  simulator port per instance), so PX4 instances can run on other hosts. The
  number of full-PX4 drones is bounded by deployed PX4 instances, not by the
  physics engine.
- **HITL is a non-goal** for the core loop. Real-hardware validation is
  inherently real-time-only and, if needed later, becomes a separate harness —
  it must never constrain the sim's timing model.
- **Clean, independently testable module seams** — spawn, dynamics, autopilot
  bridge, sensors, and scheduling are separable and unit-testable.

The rebuild proceeds as small, tested, independently reviewable deliverables:

1. Architecture-decision doc + minimal skeleton (this ADR).
2. GPU-spawn + profiling harness that measures step throughput and the
   achieved time-scale factor.
3. Tensorized dynamics.
4. SITL-lockstep PX4 bridge (sim as TCP server and time master).
5. Sensors.
6. Full parity with the current sim.

## Consequences

**Positive**

- Physics cost scales with GPU capacity, enabling many-drone scenarios.
- Faster-than-real-time batch runs are first-class, with PX4 time-coherent.
- Sim time as the single source of truth makes runs reproducible and PX4's
  estimator immune to wall-clock skew.
- Autopilot capacity scales horizontally by deporting PX4 instances.

**Negative / risks**

- The achievable speed factor is capped by the slowest attached PX4 instance's
  compute; full-PX4 drone count is capped by instance count. Both accepted.
- Two distinct "cannot keep up" signals must be distinguished so the warning is
  actionable: **compute-bound** (the GPU physics cannot hit the requested
  factor — a property of the sim/hardware) versus **PX4-bound** (physics could
  go faster but a lockstep PX4 instance is the bottleneck — a property of that
  autopilot). Same symptom (achieved < requested), different remedy (smaller
  scene vs. lower factor / fewer PX4 drones).
- PX4's lockstep path is normally driven in strict alternation (sim waits for
  the actuator reply). Free-running the sim against it — publishing sensor
  messages faster than PX4 consumes them — deviates from that pattern and must
  be validated early (step 4 spike): message queuing behaviour, clock-jump
  tolerance, and estimator health under skipped frames. A bounded look-ahead
  (sim at most K steps ahead per instance) is the fallback if uncapped
  free-running proves unstable.
- Tensorized on-GPU dynamics require careful validation against the current
  scipy-based model to avoid silent behavioural drift.
- Effort is front-loaded: steps 1–2 deliver infrastructure and proof, not new
  user-visible capability.

## Notes

This ADR supersedes the original PoC's implicit architecture, and its
2026-09-08 amendment replaces the earlier "real-time budget" framing: the
budget is now step *throughput*, with real time as speed factor 1.

Entrypoint implications: PX4 attaches through the SITL binary's simulator
channel (TCP 4560 + instance offset, `PX4_SIM_HOSTNAME` for remote hosts),
not the HITL firmware path. Exact launch invocation and port conventions are
to be pinned against the PX4 documentation at the start of step 4.

Interface implications (follow-up change): `Scheduler` gains `sim_time()`, a
configurable `speed_factor` (0 = unlimited), and a measured `time_scale()`,
and emits a warning when the achieved rate for any attached PX4 instance falls
below the requested factor; `HilBridge.send_sensors` carries the sim-time
stamp. `PhysicsEngine` and `SensorModel` are unchanged — the time base lives
in the scheduler.
