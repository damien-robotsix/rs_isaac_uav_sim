"""Decoupled async hardware-in-the-loop (HIL) bridge seam.

Defines the interface for the MAVLink/PX4 hardware-in-the-loop bridge.
The bridge runs as an independent async component so the simulation no
longer paces itself off the MAVLink round-trip. This module declares the
interface only; no MAVLink transport is imported at import time.
"""

from .interface import HilBridge

__all__ = ["HilBridge"]
