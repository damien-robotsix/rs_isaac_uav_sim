# Agent Guide

Guidance for AI coding agents and contributors working in this repository.
This project follows the
[robotsix-standards](https://damien-robotsix.github.io/robotsix-standards/)
conventions.

## Project overview

`rs_isaac_uav_sim` provides an Isaac Sim-based UAV simulation with ROS 2
autonomy. It is a Python project.

## Conventions

- Keep changes minimal and focused on the task at hand.
- Follow the existing code style; lint with `ruff` before committing.
- Use [Conventional Commits](https://www.conventionalcommits.org/) for
  commit subjects and pull request titles
  (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`, `ci:`).
- Add or update tests alongside behavioural changes.

## Development

- CI runs on every push and pull request (see
  `.github/workflows/ci.yml`): it sets up Python, installs dependencies,
  lints, and runs the test suite.
- Dependencies are kept up to date via Dependabot
  (see `.github/dependabot.yml`).

## Security

See [SECURITY.md](SECURITY.md) for how to report vulnerabilities.
