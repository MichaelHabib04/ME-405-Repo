"""
Stub cqueue module for documentation builds.

This file is used only by Sphinx/ReadTheDocs so that imports like
`import cqueue` in main.py do not execute the real MicroPython test code
or cause circular-import errors.
"""

class IntQueue:
    """Minimal placeholder for cqueue.IntQueue used in docs."""
    def __init__(self, size):
        self.size = size

    def put(self, value):
        pass

    def get(self):
        return None

