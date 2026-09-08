"""Tests that each module seam exposes its abstract interface."""

import inspect

import pytest

from rs_isaac_uav_sim.hil import HilBridge
from rs_isaac_uav_sim.physics import PhysicsEngine
from rs_isaac_uav_sim.scheduler import Scheduler
from rs_isaac_uav_sim.sensors import SensorModel


@pytest.mark.parametrize(
    ("interface", "expected_methods"),
    [
        (PhysicsEngine, {"reset", "step", "state"}),
        (HilBridge, {"start", "stop", "send_sensors", "recv_actuators"}),
        (Scheduler, {"start", "tick", "overrun"}),
        (SensorModel, {"reset", "sample"}),
    ],
)
def test_interface_declares_abstract_methods(interface, expected_methods):
    # The interface is abstract and cannot be instantiated directly.
    assert inspect.isabstract(interface)
    assert expected_methods <= interface.__abstractmethods__
