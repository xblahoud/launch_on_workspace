from launcher import *

port = 8899
workspace = 3
homedir = "/home/fblahoudek/tools/consumption-MDP"

ws = workspace - 1

jupyter_lab(ws, homedir, "consMDP", port)
terminal(ws, homedir, new_win_name="consMDP: git")
