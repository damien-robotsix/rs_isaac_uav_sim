# Core

Documentation for the `core` module
(`rs_isaac_uav_sim`): the top-level package initialiser.

It holds the package `__version__` (the single source of truth for
the installed package version, which pyproject builds dynamically
from this file), the package docstring, and the public surface
declared in `__all__`. The package import/version contract is
exercised in `tests/core/test_package.py`.

Module-specific documentation will be added here as the package
initialiser expands. Cross-module architecture decisions live in
[`docs/adr/`](../adr/).