# Launch-on-workspace
Launch applications on a specified workspace in Linux.

The module [launcher](launcher.py) implements several useful functions that can launch (in a scriptable manner) applications on designated workspaces on X in Linux. Relies on [wmctrl](http://tripie.sweb.cz/utils/wmctrl/) to manipulate windows on workspaces.

The module [displays](displays.py) moves windows to displays in similar manner. Right now it relies on [xrandr](https://www.x.org/wiki/Projects/XRandR/) to get mapping of displays to workspace coordinates. You can use it even without `xrandr` by supplying the right coordinates for `wmctrl` by yourself.

The module [custom_launchers](custom_launchers.py) uses the functionality of [launcher](launcher.py) to provide functions that launch specific programs. They serve as an easy abstraction from some implementation details for non-standard situations. The motivation for these is threefold:
 1. Some programs need carefull treatment as they (a) use some temporary window at startup and we actually want to move the second one (`texstudio`), or (b) you usually have some other instances running in the system and no new process is created (`firefox`,`Pycharm`)
 2. It simplifies supplying arguments (`terminal`)
 3. Some applications need 2 or more windows to be moved (`jupyter-lab`)
Currently, we have functions for launching:
 * `gnome-terminal`
 * `firefox`
 * `jupyter_lab`
 * `texstudio`
 * `pycharm`

All these functions return the IDs of windows they create so they can be further positioned on monitors using the functions from [displays](displays.py).

## Installation

### Requirements
* Python 3.6+
* [wmctrl](http://tripie.sweb.cz/utils/wmctrl/)
* [xrandr](https://www.x.org/wiki/Projects/XRandR/)
* and compatible window manager 

tested with Gnome 3.34.1 on Ubuntu 19.10

```
python3 -m pip install launch_on_workspace
```

## Usage examples
The following command launches a new window of Firefox that opens YouTube on workspace 2 (in wmctrl) which is a workspace 3 in Gnome. It is then moved to display connected to DisplayPort#1 (name "DP-1" in `xrandr`) and switched to fullscreen mode.

```python
import launch_on_workspace as low

wid = low.firefox(2, "youtube.com")
low.move_win_to_display(wid, "DP-1", "full")
```

The following command opens a gedit on workspace 4 in Gnome
```python
low.launch_and_move(['gedit'], 3)
```
