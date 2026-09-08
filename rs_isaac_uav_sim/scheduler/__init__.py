"""Explicit real-time scheduler seam.

Defines the interface for the scheduler that owns the simulation step
cadence and measures it against a stated real-time budget. This module
declares the interface only.
"""

from .interface import Scheduler

__all__ = ["Scheduler"]
