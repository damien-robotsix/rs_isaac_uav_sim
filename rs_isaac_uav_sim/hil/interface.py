"""Interface for the PX4 SITL-lockstep HIL (MAVLink) bridge."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class HilBridge(ABC):
    """Hardware-in-the-loop bridge to PX4 over MAVLink (SITL lockstep).

    PX4 attaches through its SITL lockstep interface: each sensor message
    carries the simulation timestamp, and PX4 rebases its monotonic clock
    onto it. PX4 therefore waits for the simulation, never the reverse --
    the simulation is the time master. Because the link is plain MAVLink
    over TCP (one simulator channel per instance), PX4 instances may run
    on other hosts.
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
    async def send_sensors(self, sensor_state: Any, sim_time_us: int) -> None:
        """Publish simulated sensor state to PX4, stamped with sim time.

        ``sim_time_us`` is the scheduler's ``sim_time`` in microseconds;
        PX4 rebases its clock onto this stamp (SITL lockstep), so it must
        be the simulation clock, never wall-clock time.
        """
        raise NotImplementedError

    @abstractmethod
    async def recv_actuators(self) -> Any:
        """Return the most recent actuator command received from PX4."""
        raise NotImplementedError
