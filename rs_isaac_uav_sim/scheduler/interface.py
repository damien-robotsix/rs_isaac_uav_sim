"""Interface for the simulation-clock scheduler."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Scheduler(ABC):
    """Owns the simulation clock and step cadence.

    The scheduler is the single source of truth for simulation time. It
    advances a monotonic ``sim_time`` by a fixed ``dt`` each step and paces
    the loop according to a configurable *speed factor*:

    * ``speed_factor == 0`` (unlimited) runs as fast as compute allows --
      wall-clock time is observability only, never a pacing constraint;
    * a positive ``speed_factor`` caps the step rate to that multiple of
      real time (``1.0`` == real time, ``5.0`` == five times real time).

    Choosing a value the attached autopilots can sustain is the user's
    responsibility. Implementations report the *measured* achieved
    time-scale and whether the loop is keeping up with the requested
    factor, so callers can log or warn instead of silently corrupting the
    time base.
    """

    @abstractmethod
    def start(self) -> None:
        """Begin scheduling at the configured speed factor."""
        raise NotImplementedError

    @abstractmethod
    def tick(self) -> None:
        """Advance ``sim_time`` by one step, pacing to the speed factor.

        Under an unlimited speed factor this returns as soon as the step's
        work is accounted for; under a capped factor it blocks until the
        next step boundary in wall time.
        """
        raise NotImplementedError

    @abstractmethod
    def sim_time(self) -> float:
        """Return the current monotonic simulation time, in seconds.

        This is the single source of truth for simulation time and the
        value stamped onto sensor messages sent to PX4.
        """
        raise NotImplementedError

    @abstractmethod
    def time_scale(self) -> float:
        """Return the *measured* achieved sim-time / wall-time ratio.

        Observability only: ``1.0`` means real time, ``> 1`` faster than
        real time, ``< 1`` slower. Compare against the requested speed
        factor to detect a compute-bound or PX4-bound bottleneck.
        """
        raise NotImplementedError

    @abstractmethod
    def is_keeping_up(self) -> bool:
        """Return whether the last step met the requested speed factor.

        ``True`` when the achieved rate is at or above the requested factor
        (always ``True`` under an unlimited factor); ``False`` when the
        loop fell behind, signalling the caller to log/warn.
        """
        raise NotImplementedError
