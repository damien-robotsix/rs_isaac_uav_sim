"""Interface for the decoupled async HIL (MAVLink/PX4) bridge."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class HilBridge(ABC):
    """Async hardware-in-the-loop bridge to PX4 over MAVLink.

    Implementations exchange sensor and actuator messages with PX4
    asynchronously, decoupled from the simulation step cadence so the
    sim's real-time budget is not hostage to network latency.
    """

    @abstractmethod
    async def start(self) -> None:
        """Open the MAVLink link and begin servicing it asynchronously."""
        raise NotImplementedError

    @abstractmethod
    async def stop(self) -> None:
        """Close the MAVLink link and release resources."""
        raise NotImplementedError

    @abstractmethod
    async def send_sensors(self, sensor_state: Any) -> None:
        """Publish the latest simulated sensor state to PX4."""
        raise NotImplementedError

    @abstractmethod
    async def recv_actuators(self) -> Any:
        """Return the most recent actuator command received from PX4."""
        raise NotImplementedError
