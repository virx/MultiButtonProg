#!/usr/bin/python
# -*- coding: utf-8 -*-
""" File: mbp.py
Copyright (C) 2011  Virgo Pihlapuu

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from Tkinter import *
import os

print """MultiButtonProg  Copyright (C) 2011  Virgo Pihlapuu

This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it.
"""
# ... under certain conditions; type `show c' for details ...

# read log file of specific tab
def read_log(n):
	fn = "log/"+ tabs[n][0].strip() +".txt"
	with open(fn, 'r') as f:
		fs = f.read()
	return fs
	
# read config.txt file	
def read_conf():
	fs = ''
	with open('config.txt', 'r') as f:
		fs = f.read()
	return fs

# clean string from lines with hashes
def clean_hash_lines(bad_s):
	clean_s = ''
	txt_arr = bad_s.splitlines()
	for line in txt_arr:
		if len(line) > 0:
			if line.strip()[0] != '#':
				clean_s += (line + "\n")
	return clean_s

# parse tabs and buttons from config.txt file into array
def parse_conf():
	fs_arr = clean_hash_lines(read_conf()).split('|')
	fs_i = 0
	tabs_new = []
	coms_new = []
	for part in fs_arr:
		if part.strip() == 'tab':
			tabs_new.append([fs_arr[fs_i+1], fs_arr[fs_i+2].splitlines()])
		elif part == 'command':
			coms_new.append([fs_arr[fs_i+1], fs_arr[fs_i+2], fs_arr[fs_i+3]])
		fs_i += 1
	return tabs_new, coms_new

# execute terminal command sequence
def call_com_term(t_i):
	for line in coms[t_i][2].split('\n'):
		print 'Button with terminal command called: %r' % line
		if os.name in ['nt', 'dos', 'os2'] :
		   # dos
		   pipe = os.popen(line)
		else :
		   # unix
		   pipe = os.popen(line)
		text = pipe.read()
		sts = pipe.close()
		if sts is None: sts = ''
		t.insert(END, sts)
		t.insert(END, text)

# execute python script
def call_com_py(c_i):
	#print 'Button with python command called: %r' % c_i
	#print 'I will execute this: %r' % coms[c_i][2]
	exec(coms[c_i][2])

# Edit configure file
def sel_conf():
	t.delete(0.0, END)
	fs = read_conf()
	t.insert(END, fs)

# Arrange the buttons related to window size
def relocate_buttons(tt, xxx):
	x_sum = 0
	btx = 0
	cl = 0
	rw = 0
	for ttt in tt.grid_slaves():
		btx = ttt.winfo_width()
		if x_sum > xxx - int(btx*0.75):
			cl = 0
			rw += 1
			x_sum = 0
			#print "relocate_buttons: increased rw to %r, column is %r, x_sum is %r, wx is %r" % (rw, cl, x_sum, xxx)
		ttt.grid_configure(row=rw, column=cl)
		x_sum += btx
		cl += 1
		
def reset_panes(yy):
	m1.sash_place(0, 0, 50)
	m1.sash_place(1, 0, (yy - 50))
	
def change_window(event):
	reset_widget_sizes(event.width, event.height)

# make new size and location for widgets to fit better with window
def reset_widget_sizes(xx,yy):
	#print "window size is %r x %r" % (xx,yy)
	for tab_i in range(0,len(tabs)):
		exec("relocate_buttons(f_bot_%r, xx)" % tab_i)
	reset_panes(yy)

# do things when tab button is clicked
def sel_tab(tbn):
	t.delete(0.0, END)
	fs = read_log(tbn)
	t.insert(END, fs)
	cur_tab = tbn
	# change background colors of tab buttons
	# change order of command button frames
	for tbi in range(0,len(tabs)):
		if tbi == cur_tab:
			exec("tbb_%r.configure(bg='#cfc')" % tbi)
			exec("f_bot_%r.grid(sticky=N+S+E+W)" % tbi)
		else:
			exec("tbb_%r.configure(bg=%r)" % (tbi, com_tab_colors[tbi]))
			exec("f_bot_%r.grid_forget()" % tbi)
	for tbi in range(0,len(tabs)):
		if tbi != cur_tab:
			exec("f_bot_%r.grid(sticky=N+S+E+W)" % tbi)
	#print "changed tab to %r" % cur_tab
	
# return list with color values
def make_colors(n):
	colors = []
	c_list = "fdb979bdfeca8acefdb979bdfeca8acefdb979bdfeca8acefdb979bdfeca8"
	for i in range(0,n):
		colors.append("#"+ c_list[i] + c_list[i+1] + c_list[i+2])
	return colors

# make folder and files for tab logs
def files_folders():
	try:
		os.makedirs('log')
	except OSError:
		pass
	ti = 0
	for tab in tabs:
		fn = "log/"+ tabs[ti][0].strip() +".txt"
		with open(fn, 'w') as f:
			pass
		f.close()	
		ti += 1

# root frame
wx = 600
wy = 500
scl = 100 # scale widget sizes from 1 to 100 (scale thing not working) <FIX ME>
top_min = 50
cent_min = 50
bot_min = 50
top_sash_loc = 50
bot_sash_loc = (wy - 50)
root = Tk()
root.geometry('%rx%r+300+200' % (wx, wy))
root.title("MultiButtonProg")

m1 = PanedWindow(root, orient=VERTICAL, bg='#fb8')
m1.bind("<Configure>", change_window)
m1.pack(side=TOP, fill=BOTH, expand=1)

top = LabelFrame(m1, bg='#dbb', text="Tabs")
m1.add(top)

center = LabelFrame(m1, bg='#bdb', text="Text / Log")
m1.add(center)

bottom = LabelFrame(m1, bg='#bbd', text="Command buttons")
m1.add(bottom)

m1.paneconfigure(top, minsize=top_min)
m1.paneconfigure(center, minsize=cent_min)
m1.paneconfigure(bottom, minsize=bot_min)

# top widgets
f_top = Frame(top)
f_top.grid(row=0, column=0, sticky=E+W)

# center widgets
t_sb_y = Scrollbar(center)
t_sb_y.grid(row=0, column=1, sticky=N+E+S)

t_sb_x = Scrollbar(center, orient=HORIZONTAL)
t_sb_x.grid(row=1, column=0, sticky=W+S+E)

t = Text(center, wrap=NONE, xscrollcommand=t_sb_x.set, yscrollcommand=t_sb_y.set)
t.grid(row=0, column=0, sticky=N+E+S+W)

t_sb_y.config(command=t.yview)
t_sb_x.config(command=t.xview)

center.columnconfigure( 0, weight=1000 )
center.rowconfigure( 0, weight=1000 )

# bottom widgets
f_bottom = Frame(bottom)
f_bottom.grid(row=0, column=0, sticky=E+W)

cur_tab = 0
# arrays for tab and command buttons
tabs, coms = parse_conf()

com_tab_colors = make_colors(len(tabs))
files_folders()

# init tab buttons and command button frames
tn = 0
for tab in tabs:
	exec("tbb_%r=Button(f_top, text=%r, bg=%r, command=lambda t_%r=%r: sel_tab(t_%r))" % (tn, tabs[tn][0], com_tab_colors[tn], tn, tn, tn))
	exec("tbb_%r.grid(row=0, column=%r, sticky=W)" % (tn, tn))	
	exec("f_bot_%r=Frame(f_bottom, bg=%r)" % (tn, com_tab_colors[tn]))
	exec("f_bot_%r.grid(sticky=E+W)" % (tn))
	# init command buttons
	ci = 0
	b_row = 0
	b_col = 0
	for cm in coms:
		for n in range(0,(len(tabs[tn][1]))):
			if cm[1].strip() == tabs[tn][1][n].strip('\n'):
				if b_col > 5:
					b_col = 0
					b_row += 1
				if cm[0] == 'python':
					exec("cmb_%r_%r=Button(f_bot_%r, text=%r, bg=%r, command=lambda c_%r=%r: call_com_py(c_%r))" % (tn, n, tn, cm[1], com_tab_colors[tn], ci, ci, ci))
					exec("cmb_%r_%r.grid(row=%r, column=%r, sticky=W+E)" % (tn, n, b_row, b_col))
					b_col += 1
				else:
					exec("cmb_%r_%r=Button(f_bot_%r, text=%r, bg=%r, command=lambda c_%r=%r: call_com_term(c_%r))" % (tn, n, tn, cm[1], com_tab_colors[tn], ci, ci, ci))
					exec("cmb_%r_%r.grid(row=%r, column=%r, sticky=W+E)" % (tn, n, b_row, b_col))
					b_col += 1
		ci += 1
	tn += 1

# select first tab

root.mainloop()


