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
        (Scheduler, {"start", "tick", "sim_time", "time_scale", "is_keeping_up"}),
        (SensorModel, {"reset", "sample"}),
    ],
)
def test_interface_declares_abstract_methods(interface, expected_methods):
    # The interface is abstract and cannot be instantiated directly.
    assert inspect.isabstract(interface)
    assert expected_methods <= interface.__abstractmethods__


@pytest.mark.parametrize("interface", [Scheduler, HilBridge])
def test_interface_docstrings_reflect_sim_clock_model(interface):
    # The sim-clock rework retired the old "real-time budget" framing;
    # guard against it silently creeping back into the seam docstrings.
    doc = (interface.__doc__ or "").lower()
    assert "real-time budget" not in doc
