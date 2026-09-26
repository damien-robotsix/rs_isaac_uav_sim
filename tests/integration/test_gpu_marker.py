"""Example GPU-marked test.

This test is decorated with ``@pytest.mark.gpu`` so it is deselected by
the default CPU-only selection ``pytest -m "not gpu and not isaac"``. It
demonstrates the marker mechanism without requiring real GPU/Isaac
hardware.
"""

import pytest


@pytest.mark.gpu
def test_gpu_placeholder():
    # Would exercise on-GPU dynamics; skipped on standard CI.
    raise AssertionError("GPU tests must not run on standard CPU-only CI.")
