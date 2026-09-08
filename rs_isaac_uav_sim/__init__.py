"""rs_isaac_uav_sim — clean-slate UAV simulation package.

This package provides the module seams for the from-scratch rebuild
described in ADR-0001 (docs/adr/0001-clean-slate-rebuild.md). At this
stage the seams are typed interfaces only: they import cleanly in a
plain CPU Python environment and pull in no Isaac Sim, GPU or torch
dependencies at import time.
"""

__version__ = "0.0.1"

__all__ = ["__version__"]
