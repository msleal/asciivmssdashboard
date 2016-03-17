#!/usr/bin/env python
# All uniCurses routines to ASCii Effects representation on the terminal are here (or should be)...

"""
Copyright (c) 2016, Marcelo Leal
Description: The power is in the terminal...
License: MIT (see LICENSE.txt file for details)
"""

import time
from subprocess import call
from unicurses import *

#Colors...
def set_colors():
	init_pair(1, COLOR_BLUE, COLOR_BLUE);
	init_pair(2, COLOR_YELLOW, COLOR_YELLOW);
	init_pair(3, COLOR_BLACK, COLOR_WHITE);
	init_pair(4, COLOR_WHITE, COLOR_BLACK);
	init_pair(5, COLOR_GREEN, COLOR_GREEN);
	init_pair(6, COLOR_GREEN, COLOR_BLACK);
	init_pair(7, COLOR_YELLOW, COLOR_BLACK);
	init_pair(8, COLOR_RED, COLOR_BLACK);

#Create Windows...
def create_window(x, y, w, z):
        #window = newwin(lines, colunms, startline, startcolunm);
	window = newwin(x, y, w, z);
	#DEBUG
        #box(window);
	return window;

#Draw VM...
def draw_vm(vmc, window, ps, flag):
	if (vmc < 10):
		nr = "%02d" % vmc
	if (ps.upper() == "SUCCEEDED"):
		wmove(window, 1, 1); waddstr(window, nr, color_pair(6) + A_BOLD);
	elif (ps.upper() == "CREATING"):	
		wmove(window, 1, 1); waddstr(window, nr, color_pair(7) + A_BOLD);
	elif (ps.upper() == "DELETING"):	
		wmove(window, 1, 1); waddstr(window, nr);
	#Any other state we do not know about?
	else:
		wmove(window, 1, 1); waddstr(window, nr, color_pair(1) + A_BOLD);

	#Mark VM Selected by the user...
	if (flag):
		wmove(window, 2, 1); whline(window, "<" , 1);
		wmove(window, 2, 2); whline(window, ">" , 1);
	else:
		box(window);

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
		time.sleep(.002);
	while (ystart != yfinal):
		move_panel (panel, xstart, ystart);
		update_panels();
		doupdate();
		ystart -= 1;
		time.sleep(.002);

def vm_animation(panel, nasp, xfinal, yfinal, flag):
	xstart = nasp[0];
	ystart = nasp[1];

	while (ystart != yfinal):
		move_panel (panel, xstart, ystart);
		update_panels();
		doupdate();
		if (flag):
			ystart += 1;
		else:
			ystart -= 1;
		time.sleep(.02);
	while (xstart != xfinal):
		move_panel (panel, xstart, ystart);
		update_panels();
		doupdate();
		if (flag):
			xstart -= 1;
		else:
			xstart += 1;
		time.sleep(.02);

def draw_prompt_corners(window):
	draw_line(window, 0, 62, 1, ACS_URCORNER);
	draw_line(window, 0, 63, 1, ACS_ULCORNER);
	draw_line(window, 1, 62, 2, ACS_VLINE);
	draw_line(window, 2, 62, 1, ACS_LRCORNER);
	draw_line(window, 2, 63, 1, ACS_LLCORNER);

def draw_line(window, a, b, c, char):
	wmove(window, a, b); whline(window, char, c);

def get_continent_dc(dc):
	if (dc == "brazilsouth"):
		return 'southamerica';
	if (dc == "southcentralus" or dc == "eastus" or dc == "eastus2" or dc == "northcentralus" or dc == "centralus" or dc == "westus"):
		return 'northandcentralamerica';
	if (dc == "northeurope" or dc == "westeurope" or dc == "eastasia" or dc == "southeastasia" or dc == "japaneast" or dc == "japanwest" or dc == "centralindia" or dc == "westindia" or dc == "southindia" or dc == "chinaeast" or dc == "chinanorth"):
		return 'europeandasia';

def resize_terminal():
	#errnr = call(["resize", "-s 50 200 >/dev/null"]);
	errnr = 1;
	return errnr;
