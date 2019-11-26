import shlex
import time

from .launcher import get_wid_by_pid, get_wid_by_title, launch_and_move, get_wids

def terminal(workspace, directory=None,
             command=None, options=[],
             new_win_name="launched term",
             profile="default"):
    """Launch new gnome-terminal window and move it to `workspace`.

    `workspace`  : id of workspace in wmctrl where to move the window.
    The workspaces are indexed from 0 in wmctlr while they are
    indexed from 1 in Gnome!

    `directory`  : string (default None)
                   working directory of the terminal
    `command`    : command to run in the new terminal
    `options`    : list of strings (default [])
                   additional options for gnome-terminal
    `new_win_name` : string (default "launched term")
                   title for the new window
    `profile`    : string (default "default")
                   a name of profile to be used for the new terminal window
    """
    prog_array = ["gnome-terminal",f'--window-with-profile={profile}']
    if directory is not None:
        prog_array.append(f'--working-directory={directory}')
    prog_array.extend(options)

    if command is not None:
        prog_array.append('--')
        prog_array.extend(shlex.split(command))

    get_wid = lambda old, pid: get_wid_by_title(old, "Terminal")

    if "Terminal" in new_win_name.split()[0]:
        raise ValueError("The new name for terminal can't start with anything containing Terminal")

    return launch_and_move(prog_array, workspace, get_wid, new_win_name)

def firefox(workspace, url=None, new_win_name="Firefox"):
    """Launch new window of firefox and moves it to `workspace`

    `workspace`  : id of workspace in wmctrl where to move the window.
    The workspaces are indexed from 0 in wmctlr while they are
    indexed from 1 in Gnome!

    `url` : url to be opened in the new window.
    
    `new_win_name` : string (default "Firefox")
                     title for the new window
    The window id detection is based on lookup for "mozilla",
    so Firefox is safe even for future invocations.
    """
    old = get_wids()
    prog_array = (["firefox",'-new-window'])
    if url is not None:
        prog_array.append(url)
    get_wid = lambda old, pid: get_wid_by_title(old, "Mozilla")
    return launch_and_move(prog_array, workspace, get_wid, new_win_name)
    
def jupyter_lab(workspace, directory, win_names_pref, port=8890):
    """Open Jupyter server terminal and Jupyter lab in a new firefox
    window and move both windows to `workspace`.

    Return wid of firefox window.

    `workspace` : id of workspace in wmctrl where to move the window.
    The workspaces are indexed from 0 in wmctlr while they are
    indexed from 1 in Gnome!

    `directory` : working directory where Jupyter opens.
    `win_names_pref` : string - the windows titles will be prefixed
                       with this (and add `-JL` for terminal and .
                       `-JL-Firefox` for the browser).
    `port`      : int (default 8890) port where JL will run
    """
    terminal_win_name = f"{win_names_pref}-JL"
    terminal_cmd  = f"jupyter lab --port={port} --no-browser"

    url = f"localhost:{port}/lab"
    firefox_win_name  = f"{win_names_pref}-JL-Firefox"

    # Run the Jupyter server
    term_wid = terminal(workspace, directory, terminal_cmd,
             new_win_name=terminal_win_name, profile="Jupyter")

    # Let's give Jupyter some time to start
    time.sleep(0.2)

    # run firefox
    firefox_wid = firefox(workspace, url, firefox_win_name)
    return (firefox_wid, term_wid)

def texstudio(workspace, file=None):
    """Open new instance of TeXStudio and move the window to
    `workspace`.

    `workspace` : id of workspace in wmctrl where to move the window.
    The workspaces are indexed from 0 in wmctlr while they are
    indexed from 1 in Gnome!

    `file`      : filename to open by texstudio
    """
    get_wid = lambda old, pid:  get_wid_by_pid(old, pid, double=True)
    prog_array = ["texstudio","--start-always"]
    if file is not None:
        prog_array.append(file)
    return launch_and_move(prog_array, workspace, get_wid)

#texstudio(4)
