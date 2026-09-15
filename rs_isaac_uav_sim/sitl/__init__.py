"""Decoupled async software-in-the-loop (SITL) bridge seam.

Defines the interface for the MAVLink/PX4 SITL-lockstep bridge. The
simulation acts as the MAVLink TCP server and time master; sensor
messages carry the sim-time stamp so PX4 slaves its clock to simulation
time. This module declares the interface only; no MAVLink transport is
imported at import time.
"""

from .interface import SitlBridge

__all__ = ["SitlBridge"]
