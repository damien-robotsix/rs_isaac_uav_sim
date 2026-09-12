"""Tests that each module seam exposes its abstract interface."""

import inspect

import pytest

from rs_isaac_uav_sim.hil import HilBridge
from rs_isaac_uav_sim.physics import PhysicsEngine
from rs_isaac_uav_sim.scheduler import Scheduler
from rs_isaac_uav_sim.sensors import SensorModel


@pytest.mark.parametrize(
    ("interface", "expected_methods", "expected_signatures"),
    [
        (
            PhysicsEngine,
            {"reset", "step", "state"},
            {
                "reset": (False, ("num_drones",)),
                "step": (False, ("controls", "dt")),
                "state": (False, ()),
            },
        ),
        (
            HilBridge,
            {"start", "stop", "send_sensors", "recv_actuators"},
            {
                "start": (True, ()),
                "stop": (True, ()),
                "send_sensors": (True, ("sensor_state",)),
                "recv_actuators": (True, ()),
            },
        ),
        (
            Scheduler,
            {"start", "tick", "overrun"},
            {
                "start": (False, ()),
                "tick": (False, ()),
                "overrun": (False, ()),
            },
        ),
        (
            SensorModel,
            {"reset", "sample"},
            {
                "reset": (False, ("num_drones",)),
                "sample": (False, ("state", "dt")),
            },
        ),
    ],
)
def test_interface_declares_abstract_methods(
    interface, expected_methods, expected_signatures
):
    # The interface is abstract and cannot be instantiated directly.
    assert inspect.isabstract(interface)
    # Exact-set equality, not a subset check: a seam gaining or losing an
    # abstract method (e.g. the Scheduler sim_time()/speed_factor additions)
    # fails here until this contract test and README.md are updated.
    assert interface.__abstractmethods__ == expected_methods
    # Every expected method must have a signature entry and vice versa.
    assert set(expected_signatures) == expected_methods
    for method_name, (is_async, expected_params) in expected_signatures.items():
        _assert_abstract_signature(interface, method_name, is_async, expected_params)


def _assert_abstract_signature(interface, method_name, is_async, expected_params):
    """Assert an abstract method's async-ness and parameter names/kinds.

    ``expected_params`` lists the positional-or-keyword parameters
    (``self`` excluded). Async-ness is pinned so the HilBridge coroutine
    methods cannot silently become synchronous (or vice versa).
    """
    func = getattr(interface, method_name)
    assert inspect.iscoroutinefunction(func) == is_async
    signature = inspect.signature(func)
    actual_params = [
        (name, parameter.kind)
        for name, parameter in signature.parameters.items()
        if name != "self"
    ]
    assert actual_params == [
        (name, inspect.Parameter.POSITIONAL_OR_KEYWORD) for name in expected_params
    ]
