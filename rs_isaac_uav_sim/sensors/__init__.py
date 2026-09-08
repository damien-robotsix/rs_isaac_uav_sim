"""Sensor model seam.

Defines the interface for sensor models that derive sensor readings
from the tensorized vehicle state. This module declares the interface
only; no Isaac Sim or GPU imports happen at import time.
"""

from .interface import SensorModel

__all__ = ["SensorModel"]
