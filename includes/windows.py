#!/usr/bin/env python
# All uniCurses routines to ASCii Effects representation on the terminal are here (or should be)...

"""
Copyright (c) 2016, Marcelo Leal
Description: The power is in the terminal...
License: MIT (see LICENSE.txt file for details)
"""

import time
from unicurses import *
from auxs import *

#Create Windows...
def create_window(x, y, w, z):
        #window = newwin(lines, colunms, startline, startcolunm);
	window = newwin(x, y, w, z);
	#DEBUG
        #box(window);
	return window;

#Draw VM...
def draw_vm(window, ps):
	wmove(window, 2, 2); whline(window, "<" , 1);
	wmove(window, 2, 3); whline(window, ">" , 1);
	if (ps.upper() == "SUCCEEDED"):
		wmove(window, 1, 2); waddstr(window, "VM", color_pair(6) + A_BOLD);
	elif (ps.upper() == "CREATING"):	
		wmove(window, 1, 2); waddstr(window, "VM", color_pair(7) + A_BOLD);
	elif (ps.upper() == "DELETING"):	
		wmove(window, 1, 2); waddstr(window, "VM");
	#Any other state we do not know about?
	else:
		wmove(window, 1, 2); waddstr(window, "VM", color_pair(1) + A_BOLD);

def do_update_bar(window, sp, flag):
        a = bar = 12; total = 22;
        curstep = bar + sp;

        if (curstep > 22): curstep = 22;
        if (flag != 1): total = curstep;

        while (a < total):
                wmove(window, 1, a); waddstr(window, " ", color_pair(5) + A_BOLD);
                a += 1;
        wrefresh(window);
        time.sleep(.2);

def win_animation(panel, nasp, xfinal, yfinal):
	xstart = nasp[0];
	ystart = nasp[1];

	while (xstart != xfinal):
		move_panel (panel, xstart, ystart);
		update_panels();
		doupdate();
		xstart -= 1;
		time.sleep(.0002);
	while (ystart != yfinal):
		move_panel (panel, xstart, ystart);
		update_panels();
		doupdate();
		ystart -= 1;
		time.sleep(.0002);

def vm_animation(panel, nasp, xfinal, yfinal):
	xstart = nasp[0];
	ystart = nasp[1];

	while (ystart != yfinal):
		move_panel (panel, xstart, ystart);
		update_panels();
		doupdate();
		ystart += 1;
		time.sleep(.01);
	while (xstart != xfinal):
		move_panel (panel, xstart, ystart);
		update_panels();
		doupdate();
		xstart -= 1;
		time.sleep(.01);

def vm_deletion(panel, nasp, xfinal, yfinal):
	xstart = nasp[0];
	ystart = nasp[1];

	while (xstart <= xfinal):
		move_panel (panel, xstart, ystart);
		update_panels();
		doupdate();
		xstart += 1;
		time.sleep(.01);
	while (ystart >= yfinal):
		move_panel(panel, xstart, ystart);
		update_panels();
		doupdate();
		ystart -= 1;
		time.sleep(.01);
