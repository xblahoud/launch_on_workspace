import subprocess
import sys

### My personal monitor names ###
LAP  = "eDP-1"
SIDE = "DP-1"
BIG  = "DP-3"
#################################

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

def get_window_args(win_id):
    return ["wmctrl","-i","-r",win_id]

def add_fullscreen(win_id):
    args = get_window_args(win_id) + ["-b","add,fullscreen"]
    subprocess.run(args)
    
def remove_fullscreen(win_id):
    args = get_window_args(win_id) + ["-b","remove,fullscreen"]
    subprocess.run(args)
    args = get_window_args(win_id) + ["-b","remove,maximized_vert,maximized_horz"]
    subprocess.run(args)

def move_win_to_display(win_id, display_name, position="full"):
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
        add_fullscreen(win_id)
    else:
        remove_fullscreen(win_id)
        
    displays = get_displays()
    if display_name not in displays:
        print(f"Display {display_name} not found.",
              "Moving to the primary display",
              file=sys.stderr)
        display_name = get_primary()
    
    xrandr_pos = get_displays()[display_name]
    mvargs = get_mvarg(xrandr_pos, position)
    print(mvargs)
    args = get_window_args(win_id) + ["-e", mvargs]
    subprocess.run(args)
        
    
# disp = get_displays()
# print(get_primary())
#print(disp[BIG])
#print(get_mvarg(disp[get_primary()]))
#print(get_mvarg(disp[LAP]))
#print(get_mvarg(disp[SIDE],"full"))
#print(get_mvarg(disp[LAP],"left"))
#print(get_mvarg(disp[SIDE],"right"))