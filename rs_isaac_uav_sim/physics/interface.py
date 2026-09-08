"""Interface for the tensorized on-GPU dynamics engine."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class PhysicsEngine(ABC):
    """Tensorized dynamics engine for all drones.

    Implementations compute the dynamics of every vehicle in a single
    tensorized step on the GPU. The interface intentionally uses opaque
    ``Any`` state/tensor types so this seam carries no GPU or torch
    import at module load time.
    """

    @abstractmethod
    def reset(self, num_drones: int) -> None:
        """Allocate and initialize state for ``num_drones`` vehicles."""
        raise NotImplementedError

    @abstractmethod
    def step(self, controls: Any, dt: float) -> Any:
        """Advance all drones by ``dt`` seconds given ``controls``.

        Returns the updated tensorized state for every vehicle.
        """
        raise NotImplementedError

    @abstractmethod
    def state(self) -> Any:
        """Return the current tensorized state for all vehicles."""
        raise NotImplementedError
