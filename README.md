# Launch-on-workspace
Launch applications on a specified workspace in Linux.

The script `launcher.py` implements several useful functions that can launch (in a scriptable manner) applications on designated workspaces on X in Linux. Relies on [wmctrl](http://tripie.sweb.cz/utils/wmctrl/) to manipulate windows on workspaces.

The scripts `displays.py` then moves windows to displays in similar manner. Right now it relies on [xrandr](https://www.x.org/wiki/Projects/XRandR/) to get mapping of displays to workspace coordinates. You can use it even without `xrandr` by supplying the right coordinates for `wmctrl` by yourself.

## Requirements
* Python 3.6+
* [wmctrl](http://tripie.sweb.cz/utils/wmctrl/)
* [xrandr](https://www.x.org/wiki/Projects/XRandR/)
* and compatible window manager 

tested with Gnome 3.34.1 on Ubuntu 19.10

## Examples
The following command launches a new window of Firefox that opens YouTube on workspace 2 (in wmctrl) which is a workspace 3 in Gnome. It is then moved to display connected to DisplayPort#1 (name "DP-1" in `xrandr`) and switched to fullscreen mode.

```python
wid = launcher.firefox(2, "youtube.com")
displays.move_win_to_display(wid, "DP-1", "full")
```

The following command opens a gedit on workspce 4 in Gnome
```python
launch_and_move(['gedit'], 3)
```
