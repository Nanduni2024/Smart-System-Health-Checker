"""
Basic sanity tests for Smart System Health Checker.
These tests avoid importing app.py directly, since app.py runs
an infinite Streamlit loop at import time.
"""

import psutil
import py_compile
import os


def test_app_py_compiles():
    """Check that app.py has valid Python syntax (no import/execution)."""
    app_path = os.path.join(os.path.dirname(__file__), "..", "app.py")
    py_compile.compile(app_path, doraise=True)


def test_cpu_percent_returns_valid_range():
    cpu = psutil.cpu_percent(interval=0.1)
    assert 0 <= cpu <= 100


def test_ram_percent_returns_valid_range():
    ram = psutil.virtual_memory().percent
    assert 0 <= ram <= 100


def test_disk_percent_returns_valid_range():
    disk = psutil.disk_usage("/").percent
    assert 0 <= disk <= 100