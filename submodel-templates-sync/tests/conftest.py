"""Put the service directory on sys.path.

pytest only prepends the tests/ directory itself, but the modules under test
are flat top-level scripts (app.py, events.py, …) in the service root.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
