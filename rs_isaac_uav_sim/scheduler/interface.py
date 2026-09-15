"""Interface for the explicit real-time scheduler."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Scheduler(ABC):
    """Owns the simulation clock and step cadence against a speed factor.

    The scheduler is the single source of truth for sim time. A
    configurable ``speed_factor`` paces the loop (0 = unlimited, 1.0 =
    real-time, N = N-times real time); ``time_scale()`` reports the
    measured achieved multiple. The implementation must warn when any
    attached PX4 instance's achieved scale falls below the requested
    factor, so an operator can tell a PX4-bound bottleneck from a
    compute-bound one.
    """

    @abstractmethod
    def start(self) -> None:
        """Begin scheduling at the configured cadence."""
        raise NotImplementedError

    @abstractmethod
    def tick(self) -> None:
        """Block until the next scheduled step boundary."""
        raise NotImplementedError

    @abstractmethod
    def overrun(self) -> bool:
        """Return whether the most recent step exceeded its budget."""
        raise NotImplementedError

    @abstractmethod
    def sim_time(self) -> float:
        """Return the current monotonic sim time in seconds."""
        raise NotImplementedError

    @property
    @abstractmethod
    def speed_factor(self) -> float:
        """Return the configured speed factor (0 = unlimited)."""
        raise NotImplementedError

    @speed_factor.setter
    @abstractmethod
    def speed_factor(self, value: float) -> None:
        """Set the speed factor; 0 = unlimited, 1.0 = real-time."""
        raise NotImplementedError

    @abstractmethod
    def time_scale(self) -> float:
        """Return the measured achieved time scale (multiple of real time)."""
        raise NotImplementedError
