# ADR-0001: Clean-slate rebuild for real-time UAV simulation

- Status: Accepted
- Date: 2026-09-07
- Deciders: Robotsix

## Context

`rs_isaac_uav_sim` is a proof-of-concept NVIDIA Isaac Sim UAV simulator. It
spawns quadrotors in Isaac Sim and bridges to PX4 via MAVLink
hardware-in-the-loop (HIL). The PoC works as a demo but never reached reliable
real-time performance.

The root causes are structural, not incidental:

- **GPU→CPU synchronization on every physics step.** Each step stalls waiting
  for data to come back to the host, destroying throughput.
- **Per-drone Python/scipy work in the hot loop.** Dynamics are computed
  per-vehicle on the CPU, so cost scales linearly with the number of drones and
  cannot exploit the GPU.
- **Tight lockstep coupling to PX4.** The simulation paces itself off the
  MAVLink round-trip, so its real-time budget is hostage to network latency.

Because these problems are baked into the core loop, incremental patching of the
existing code cannot get us to a stable real-time budget. The cost of
re-architecting in place is comparable to a clean rebuild, without the clarity a
fresh start provides.

## Decision

Rebuild the simulator from a clean slate, targeting reliable real-time
performance from the ground up. The target architecture is:

- **On-GPU, tensorized physics** across all drones — no per-vehicle CPU work in
  the hot loop, no per-step GPU→CPU sync.
- **Decoupled async HIL bridge** — the MAVLink/PX4 link runs as an independent
  async component so the sim no longer paces off the network round-trip.
- **Explicit real-time scheduler** — the step cadence is owned by the sim and
  measured against a stated real-time budget.
- **Clean, independently testable module seams** — spawn, dynamics, HIL bridge,
  sensors, and scheduling are separable and unit-testable.

The rebuild proceeds as small, tested, independently reviewable deliverables:

1. Architecture-decision doc + minimal skeleton (this ADR).
2. GPU-spawn + profiling harness that proves the real-time budget.
3. Tensorized dynamics.
4. Async HIL bridge.
5. Sensors.
6. Full parity with the current sim.

## Consequences

**Positive**

- A stated, measurable real-time budget with a profiling harness (step 2) that
  proves it before feature work continues.
- Physics cost scales with GPU capacity, not with per-drone CPU work, enabling
  many-drone scenarios.
- The HIL bridge and PX4 coupling no longer gate the sim's step rate.
- Clean module seams make each layer independently testable and reviewable.

**Negative / risks**

- Full feature parity with the existing PoC is deferred until step 6; the new
  code is not a drop-in replacement until then.
- Tensorized on-GPU dynamics require careful validation against the current
  scipy-based model to avoid silent behavioural drift.
- Effort is front-loaded: steps 1–2 deliver infrastructure and proof, not
  new user-visible capability.

## Notes

This ADR supersedes the original PoC's implicit architecture. Subsequent ADRs
will record decisions made within each step (e.g. the dynamics tensor layout,
the async bridge's transport, and the scheduler's timing model).
