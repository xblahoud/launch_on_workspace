__all__ = [
    "launcher",
    "displays",
    "custom_launchers",
]

__version__ = "1.0.0"

import launch_on_workspace.launcher
import launch_on_workspace.displays
from launch_on_workspace.launcher import launch_and_move
from launch_on_workspace.displays import move_win_to_display
from launch_on_workspace.custom_launchers import firefox as firefox
from launch_on_workspace.custom_launchers import terminal as terminal
from launch_on_workspace.custom_launchers import texstudio as texstudio
from launch_on_workspace.custom_launchers import jupyter_lab as jupyter_lab