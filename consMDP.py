#!/usr/bin/python3

from launcher import *

port = 8899
workspace = 3
homedir = "/home/fblahoudek/tools/consumption-MDP"

ws = workspace - 1

terminal(ws, homedir, command="bash -c 'git pull; bash'", new_win_name="consMDP: git")
jupyter_lab(ws, homedir, "consMDP", port)

tex_dir = "/home/fblahoudek/research/consumption-mdp-ltl/"
tex_file = f"{tex_dir}/notes.tex"
workspace = 6
ws = workspace -1
texstudio(ws, tex_file)
terminal(ws, tex_dir, command="bash -c 'git pull; pdflatex notes.tex; pdflatex notes.tex; bash'")

launch_and_move(['evince',f'{tex_file[:-3]}pdf'], ws)
