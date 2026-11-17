"""Start without a command prompt window (Windows pythonw association)."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('chess_coach_live.py')), run_name='__main__')
