"""Tests for the rs_isaac_uav_sim package skeleton."""

from importlib import metadata

import pytest

import rs_isaac_uav_sim


def test_version_is_non_empty_string():
    assert isinstance(rs_isaac_uav_sim.__version__, str)
    assert rs_isaac_uav_sim.__version__


def test_installed_metadata_version_matches_dunder_version():
    try:
        installed = metadata.version("rs_isaac_uav_sim")
    except metadata.PackageNotFoundError:
        pytest.skip("rs_isaac_uav_sim is not installed as a distribution")
    assert installed == rs_isaac_uav_sim.__version__
