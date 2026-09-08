"""Interface for the explicit real-time scheduler."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Scheduler(ABC):
    """Owns the simulation step cadence against a real-time budget.

    Implementations pace the simulation loop explicitly and report
    whether each step met the stated real-time budget, rather than
    letting the cadence drift with external latency.
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
