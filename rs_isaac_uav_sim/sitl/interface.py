"""Interface for the decoupled async SITL (MAVLink/PX4) bridge."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class SitlBridge(ABC):
    """Async software-in-the-loop (SITL) bridge to PX4 over MAVLink.

    The simulation acts as the MAVLink TCP server and time master:
    sensor messages carry the sim-time stamp so PX4 rebases its clock
    onto simulation time and waits for the sim, never the reverse.
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
    async def send_sensors(self, sensor_state: Any, sim_time: float) -> None:
        """Publish ``sensor_state`` to PX4 stamped with ``time_usec = sim_time``."""
        raise NotImplementedError

    @abstractmethod
    async def recv_actuators(self) -> Any:
        """Return the most recent ``HIL_ACTUATOR_CONTROLS`` from PX4."""
        raise NotImplementedError
