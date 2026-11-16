# Agent Guide

Guidance for AI coding agents and contributors working in this repository.
This project follows the
[robotsix-standards](https://damien-robotsix.github.io/robotsix-standards/)
conventions.

## Project overview

`rs_isaac_uav_sim` provides an Isaac Sim-based UAV simulation with ROS 2
autonomy. It is a Python project undergoing a from-scratch rebuild. The
current code is a minimal skeleton defining four typed module seams —
`physics` (tensorized on-GPU dynamics), `sitl` (SITL-lockstep MAVLink/PX4
bridge), `scheduler` (explicit real-time scheduler), and `sensors` (sensor
model derivation) — each importing cleanly in a plain CPU Python environment
with no GPU or Isaac Sim dependencies at import time.

## Conventions

- Keep changes minimal and focused on the task at hand.
- Follow the existing code style; lint with `ruff` before committing.
- Use [Conventional Commits](https://www.conventionalcommits.org/) for
  commit subjects and pull request titles
  (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`, `ci:`).
- Add or update tests alongside behavioural changes.
- Do not reference the design document from code, docstrings, or the README.
  The architecture record in `docs/adr/` is point-in-time and will be
  superseded or removed as the rebuild lands; state the rationale inline so
  comments never dangle on a document that no longer exists.

## Project layout

- Every new top-level file or directory, including dot-directories such as
  `.github/`, must be listed under an owning module in `docs/modules.yaml`
  in the same change that adds it.

## Development

- CI runs on every push and pull request (see
  `.github/workflows/ci.yml`): it sets up Python, installs dependencies,
  lints, and runs the test suite.
- Dependencies are kept up to date via Dependabot
  (see `.github/dependabot.yml`).

## Python version exception

- The project pins Python 3.11 (`requires-python = ">=3.11"` and mypy
  `python_version = "3.11"` in `pyproject.toml`, and the `3.11` test matrix
  and `python-security` job in `.github/workflows/ci.yml`). The reason is
  that Isaac Sim 5.x bundles a Python 3.11 interpreter, and the simulation
  code must run inside that interpreter.
- The robotsix-standards
  [Python `requires-python` rule](https://damien-robotsix.github.io/robotsix-standards/python/#requires-python)
  sets a `>= 3.14` fleet baseline. It allows a lower floor only when a real
  consumer runs an older runtime, and Isaac Sim is that consumer here. The
  3.11 pin is that documented exception, not drift.
- The `modules-drift` CI job runs on Python 3.14 on purpose, because
  robotsix-modules requires Python >= 3.14. Only that job uses 3.14.
- Do not bump the pin to match the fleet baseline. Raise it only when Isaac
  Sim's bundled Python version changes, and update every location listed
  above in the same change.

## Security

See [SECURITY.md](SECURITY.md) for how to report vulnerabilities.
