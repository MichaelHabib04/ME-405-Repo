import os
import sys
# sys.path.insert(0, os.path.abspath(".."))

# Add the on_board folder so modules like boot, main, etc. can be imported
sys.path.insert(0, os.path.abspath("../Final Term Project/on_board"))

# --- RTD / CPython compatibility shims --------------------------------------
# Make MicroPython-style functions available so imports don't fail on RTD.

import time as _time

# Fallback implementation of ticks_us (microsecond ticks)
if not hasattr(_time, "ticks_us"):
    # simple monotonic microsecond counter based on perf_counter
    import time as _t
    _start = _t.perf_counter()

    def ticks_us():
        """Rough replacement for MicroPython's time.ticks_us().

        Returns:
            int: Microseconds since an arbitrary start point.
        """
        return int((_t.perf_counter() - _start) * 1_000_000)

    _time.ticks_us = ticks_us

# Fallback implementation of ticks_ms (millisecond ticks)
if not hasattr(_time, "ticks_ms"):
    import time as _t
    _start_ms = _t.perf_counter()

    def ticks_ms():
        """Rough replacement for MicroPython's time.ticks_ms().

        Returns:
            int: Milliseconds since an arbitrary start point.
        """
        return int((_t.perf_counter() - _start_ms) * 1000)

    _time.ticks_ms = ticks_ms

# Fallback implementation of ticks_diff
if not hasattr(_time, "ticks_diff"):
    def ticks_diff(end, start):
        """Fallback implementation of MicroPython's time.ticks_diff()."""
        return end - start

    _time.ticks_diff = ticks_diff

# Ensure our patched module is what gets imported as 'time'
sys.modules["time"] = _time


# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ME 405 Final Project'
copyright = '2025, Katherine Meezan, Michael Habib, Zachery Boyer'
author = 'Katherine Meezan, Michael Habib, Zachery Boyer'
release = '1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "special-members": "__init__",
}


templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

autodoc_mock_imports = ["utime", "machine", "pyb", "micropython", "cqueue"]



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
