"""Interface for sensor models."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class SensorModel(ABC):
    """Derives sensor readings from tensorized vehicle state.

    Implementations map the physics state of all vehicles to simulated
    sensor outputs (e.g. IMU, GPS) that feed the HIL bridge.
    """

    @abstractmethod
    def reset(self, num_drones: int) -> None:
        """Initialize sensor state for ``num_drones`` vehicles."""
        raise NotImplementedError

    @abstractmethod
    def sample(self, state: Any, dt: float) -> Any:
        """Return sensor readings for ``state`` advanced by ``dt`` seconds."""
        raise NotImplementedError
