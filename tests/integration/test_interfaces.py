"""Tests that each module seam exposes its abstract interface."""

import inspect

import pytest

from rs_isaac_uav_sim.physics import PhysicsEngine
from rs_isaac_uav_sim.scheduler import Scheduler
from rs_isaac_uav_sim.sensors import SensorModel
from rs_isaac_uav_sim.sitl import SitlBridge


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
            SitlBridge,
            {"start", "stop", "send_sensors", "recv_actuators"},
            {
                "start": (True, ()),
                "stop": (True, ()),
                "send_sensors": (True, ("sensor_state", "sim_time")),
                "recv_actuators": (True, ()),
            },
        ),
        (
            Scheduler,
            {"start", "tick", "overrun", "sim_time", "speed_factor", "time_scale"},
            {
                "start": (False, ()),
                "tick": (False, ()),
                "overrun": (False, ()),
                "sim_time": (False, ()),
                "speed_factor": (False, ()),
                "time_scale": (False, ()),
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
    (``self`` excluded). Async-ness is pinned so the SitlBridge coroutine
    methods cannot silently become synchronous (or vice versa).

    Abstract properties (e.g. ``Scheduler.speed_factor``) are asserted to
    be non-async properties with an abstract getter; parameter checks do
    not apply to them.
    """
    raw = inspect.getattr_static(interface, method_name)
    if isinstance(raw, property):
        assert not is_async
        assert raw.fget is not None
        assert not inspect.iscoroutinefunction(raw.fget)
        return
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
