"""Tensorized on-GPU dynamics seam.

Defines the interface for the physics engine that computes drone
dynamics across all vehicles in a single tensorized step, with no
per-vehicle CPU work and no per-step GPU->CPU synchronization (see
ADR-0001). This module declares the interface only; no GPU or torch
imports happen at import time.
"""

from .interface import PhysicsEngine

__all__ = ["PhysicsEngine"]
