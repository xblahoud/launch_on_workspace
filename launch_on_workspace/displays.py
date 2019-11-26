import subprocess
from .launcher import get_window_args
import sys

def parse_displays():
    """Parse the output of `xrandr` and extract info about displays.
    
    Return
    ======
    displays: dict (display-name → size&position)
    primary : name of primary display
    
    xrandr has to be installed in the system
    """
    displays = {}
    primary = ""
    xrandr = subprocess.check_output(["xrandr"],universal_newlines=True)
    for line in xrandr.split("\n"):
        if " connected" in line:
            d = line.split()
            name = d[0]
            if d[2] == "primary":
                pos_and_size = d[3]
                primary = name
            else:
                pos_and_size = d[2]
            displays[name] = pos_and_size
    return displays, primary
    
def get_displays():
    return parse_displays()[0]

def get_primary():
    return parse_displays()[1]

def get_mvarg(size_pos, position="full"):
    """Take xrandrs size&pos and prepare it for wmctrl (MVARG) format
    
    MVARG: <G>,<X>,<Y>,<W>,<H>
      * <G> - gravity, 0 is default
    """
    allowed = ["left", "right", "top", "bottom", "full"]
    if position not in allowed:
        raise ValueError(f"Position has to be one of {allowed}")
    
    size, x, y = size_pos.split("+")
    w, h = size.split("x")
    
    if position == "left":
        w = int(w) // 2
    if position == "right":
        w = int(w) // 2
        x = int(x) + w
    return f"0,{x},{y},{w},{h}"

def add_fullscreen(wid):
    args = get_window_args(wid) + ["-b","add,fullscreen"]
    subprocess.run(args)
    
def remove_fullscreen(wid):
    args = get_window_args(wid) + ["-b","remove,fullscreen"]
    subprocess.run(args)
    args = get_window_args(wid) + ["-b","remove,maximized_vert,maximized_horz"]
    subprocess.run(args)

def move_win_to_display(wid, display_name, position="full"):
    """Move window to given display.
    
    By default, the window is put to fullscreen mode. The placement
    on the display can be controlled by `position`. The allowed values
    are:
    
    ```
    left, right, top, bottom, full  
    ```
    """
    allowed = ["left", "right", "top", "bottom", "full"]
    if position not in allowed:
        raise ValueError(f"Position has to be one of {allowed}")
        
    if position == "full":
        add_fullscreen(wid)
    else:
        remove_fullscreen(wid)
        
    displays = get_displays()
    if display_name not in displays:
        print(f"Display {display_name} not found.",
              "Moving to the primary display",
              file=sys.stderr)
        display_name = get_primary()
    
    xrandr_pos = get_displays()[display_name]
    mvargs = get_mvarg(xrandr_pos, position)
    print(mvargs)
    args = get_window_args(wid) + ["-e", mvargs]
    subprocess.run(args)
