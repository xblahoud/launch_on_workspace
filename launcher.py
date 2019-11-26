#!/usr/bin/python3
PID_INDEX = 2
TITLE_INDEX = 4

import subprocess
import sys
import time

def get_windows():
    """Return the output of `wmctrl -l -p` as list of lines.

    This is basicaly the list of windows currently opened.
    See man wmctrl for more info.
    """
    pr = subprocess.run(["wmctrl","-l","-p"], text=True, stdout=subprocess.PIPE)
    out = pr.stdout
    return out.split("\n")[:-1]

def get_wids():
    """Return the set of ids (wid) of currently opened windows.
    """
    return {line.split()[0] for line in get_windows()}

def get_window_args(wid):
    """wmctrl arguments that choose `wid` for further processing.
    """
    return ["wmctrl","-i","-r",wid]

def rename_window(wid, new_name):
    """Change the title of the window given by `wid`.

    This is essential when using detection of windows id by
    titles. If you don't change the title, the next time you
    launch the same application, the get_wid_by_title will
    return the first match.
    """
    subprocess.run(get_window_args(wid) + ["-T",new_name])

def move_win_to_ws(wid, workspace):
    """Move windows specified by `wid` to `workspace`.

    `workspace` : id of workspace in wmctrl where to move the window

    The workspaces are indexed from 0 in wmctlr while they are
    indexed from 1 in Gnome!
    """
    subprocess.run(get_window_args(wid) + ["-t",str(workspace)])

def get_new_wid(old_wins, pattern, f_index=PID_INDEX, repeat=False):
    """Get wid of a newly opened window which `value` contains `pattern`.

    The `value` is specified by the `f_index` which is a index of column
    if interest from the output of `wmctrl -l -p`.

    Interesting indices:
     * 2: PID
     * 4: first word of title
    """
    found = False
    c = 0
    while not found and c < 1000:
        c += 1
        wins = get_windows()
        for win in wins:
            f = win.split()
            wid = f[0]
            field = f[f_index]

            if wid in old_wins: 
                continue

            if pattern in field:
                found = True
                break

            time.sleep(0.05)
    if repeat:
        return get_new_wid(get_wids(), pattern, f_index, False)
    return wid

def get_wid_by_pid(old_wids, pid, double=False):
    """Return `wid` of window of process with `pid`.

    It only searches for windows not included in `old_wins`.

    `old_wids` : set of ints - window ids to skip in search.
    `pid`      : int - pid of the process of intrest
    `double`   : Bool (default False) - if True, return the
                 second window that is opened by the process.
                 This is needed for some applications that
                 use a launching window before opening the
                 main window.

    Limitations: some applications do not launch a new process
                 for a new window (Firefox, gnome-terminal)

    Known applications that need `double`:
     * TeXStudio
    """
    return get_new_wid(old_wids, str(pid), PID_INDEX, double)

def get_wid_by_title(old_wids, pattern):
    """Get wid based on the first word of title.

    You should always rename your window if you plan to launch
    an application with the same title pattern as `wmctrl` always
    matches the first one.
    """
    return get_new_wid(old_wids, pattern, TITLE_INDEX)

def launch_and_get_wid(prog_array, get_wid):
    """Launch an application and return the window id for the
    window it creates.

    `prog_array` : list forwarded to subprocess.Popen. This should
                   include the command used to lauch the application
                   and its options. See the subprocess module for
                   more info.

    `get_wid` : Function that returns the window id, takes 2 args:
      * old: iterable with windows opened before our program
      * pid: pid of the new process (not necessarly to be used)
    """
    old  = get_wids()
    proc = subprocess.Popen(prog_array)
    print("Launching process", proc.pid, file=sys.stderr)
    return get_wid(old, proc.pid)

def launch_and_move(prog_array, workspace,
                    get_wid=get_wid_by_pid, new_name=None):
    """Launch application and move the created window to `workspace`.

    Returns the window id as used by wmcrtl.

    `prog_array` : list forwarded to subprocess.Popen. This should
                   include the command used to lauch the application
                   and its options. See the subprocess module for
                   more info.

    `workspace`  : id of workspace in wmctrl where to move the window.
    The workspaces are indexed from 0 in wmctlr while they are
    indexed from 1 in Gnome!

    `get_wid`    : Function that returns the window id, takes 2 args:
      * old: iterable with windows opened before our program
      * pid: pid of the new process (not necessarly to be used)
                   Default get_wid_by_pid

    `new_name`   : string (default None). If specified, title of the
                   created window will be changed to `new_name`.
    Renaming windows is essential when using detection of windows
    id by titles. If you don't change the title, the next time you
    launch the same application, the get_wid_by_title will
    return the first match.
    """
    wid = launch_and_get_wid(prog_array, get_wid)

    if new_name is not None:
        rename_window(wid, new_name)
    move_win_to_ws(wid, workspace)
    return wid
