# Launch-on-workspace
Launch applications on a specified workspace in Linux.

The script `launcher.py` implements several useful functions that can launch (in a scriptable manner) applications on designated workspaces on X in Linux. Relies on [wmctrl](http://tripie.sweb.cz/utils/wmctrl/) to manipulate windows on workspaces.

## Requirements
* Python 3.6+
* [wmctrl](http://tripie.sweb.cz/utils/wmctrl/)
* and compatible window manager 

tested with Gnome 3.34.1 on Ubuntu 19.10

## Examples
The following command launches a new window of Firefox that opens YouTube on workspace 2 (in wmctrl) which is a workspace 3 in Gnome.

```python
firefox(2, "youtube.com")
```

The following command opens a gedit on workspce 4 in Gnome
```python
launch_and_move(['gedit'], 3)
```
