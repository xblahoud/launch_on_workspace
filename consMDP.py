#!/usr/bin/python3

### My personal monitor names ###
LAP  = "eDP-1"
SIDE = "DP-1"
BIG  = "DP-3"
#################################

from custom_launchers import terminal, jupyter_lab, texstudio
from launcher import launch_and_move
from displays import move_win_to_display

port = 8899
workspace = 3
homedir = "/home/fblahoudek/tools/consumption-MDP"

ws = workspace - 1

git = terminal(ws, homedir, command="bash -c 'git pull; bash'", new_win_name="consMDP: git")
ff, jl = jupyter_lab(ws, homedir, "consMDP", port)
move_win_to_display(ff, BIG, "full")
move_win_to_display(git, LAP, "left")
move_win_to_display(jl, LAP, "right")


tex_dir = "/home/fblahoudek/research/consumption-mdp-ltl/"
tex_file = f"{tex_dir}/notes.tex"
workspace = 6
ws = workspace -1
ts = texstudio(ws, tex_file)
git = terminal(ws, tex_dir, command="bash -c 'git pull; pdflatex notes.tex; pdflatex notes.tex; bash'")

pdf = launch_and_move(['evince',f'{tex_file[:-3]}pdf'], ws)

move_win_to_display(ts, BIG, "full")
move_win_to_display(git, LAP, "full")
move_win_to_display(pdf, SIDE, "full")
