#!/usr/bin/env python3
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
	init_pair(9, COLOR_RED, COLOR_RED);

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
		nr = "%02d" % vmc;
	else:
		nr = vmc;

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
        a = bar = 22; total = 34;
        curstep = bar + sp;

        if (curstep > total): curstep = total;
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
		time.sleep(.003);
	while (ystart != yfinal):
		move_panel (panel, xstart, ystart);
		update_panels();
		doupdate();
		ystart -= 1;
		time.sleep(.003);

def vm_animation(panel, nasp, xfinal, yfinal, flag, ts):
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
		time.sleep(ts);
	while (xstart != xfinal):
		move_panel (panel, xstart, ystart);
		update_panels();
		doupdate();
		if (flag):
			xstart -= 1;
		else:
			xstart += 1;
		time.sleep(ts);

def draw_prompt_corners(window):
	draw_line(window, 0, 122, 1, ACS_URCORNER);
	draw_line(window, 0, 123, 1, ACS_ULCORNER);
	draw_line(window, 1, 122, 2, ACS_VLINE);
	draw_line(window, 2, 122, 1, ACS_LRCORNER);
	draw_line(window, 2, 123, 1, ACS_LLCORNER);

def draw_line(window, a, b, c, char):
	wmove(window, a, b); whline(window, char, c);

def draw_line_color(window, a, b, char, cor):
	wmove(window, a, b); waddstr(window, char, color_pair(cor) + A_BOLD);

def draw_gauge(window, used, limit):
	if (used > 0):
		a = used / limit;
		b = a * 100;
	else:
		b = 0;

	if ( b < 30):
		draw_line_color(window, 3, 1, "    ", 5);
	elif (b < 60):
		draw_line_color(window, 3, 1, "    ", 2);
		draw_line_color(window, 2, 1, "    ", 2);
	else:
		draw_line_color(window, 3, 1, "    ", 9);
		draw_line_color(window, 2, 1, "    ", 9);
		draw_line_color(window, 1, 1, "    ", 9);

def get_continent_dc(dc):
	if (dc == "brazilsouth"):
		return 'southamerica';
	if (dc == "southcentralus" or dc == "eastus" or dc == "eastus2" or dc == "northcentralus" or dc == "centralus" or dc == "westus"):
		return 'northandcentralamerica';
	if (dc == "northeurope" or dc == "westeurope" or dc == "eastasia" or dc == "southeastasia" or dc == "japaneast" or dc == "japanwest" or dc == "centralindia" or dc == "westindia" or dc == "southindia" or dc == "chinaeast" or dc == "chinanorth"):
		return 'europeandasia';

def resize_terminal():
	#errnr = call(["resize", "-s 55 235 >/dev/null"]);
	errnr = 1;
	return errnr;

def create_forms(window_info, window_sys, window_status, windowvm):

	#Let's handle the status wwindow here...
	wmove(window_status, 1, 22); wclrtoeol(window_status);
	box(window_status);
	wmove(window_status, 0, 13); waddstr(window_status, " STATUS ", color_pair(3));

	#Window VM...
	a = 4;
	while (a < 12):
		wmove(windowvm, a, 17); wclrtoeol(windowvm);
		a += 1;
	a = 15;
	while (a < 18):
		wmove(windowvm, a, 12); wclrtoeol(windowvm);
		a += 1;
	box(windowvm);
	wmove(windowvm, 0, 5); waddstr(windowvm, " VM ", color_pair(3));

	#Info and Sys Windows...
	a = 2;
	while (a < 5):
		#Clean up lines...
		wmove(window_info, a, 1); wclrtoeol(window_info);
		wmove(window_sys, a, 1); wclrtoeol(window_sys);
		a += 1;

	#Redraw the box...
	box(window_info); box(window_sys);

	#Create Info form...
	wmove(window_info, 0, 5); waddstr(window_info, " GENERAL INFO ", color_pair(3));
	wmove(window_info, 2, 2); waddstr(window_info, "RG Name...: ", color_pair(4) + A_BOLD);
	wmove(window_info, 2, 37); waddstr(window_info, "VMSS Name: ", color_pair(4) + A_BOLD);
	wmove(window_info, 2, 68); waddstr(window_info, "Tier..: ", color_pair(4) + A_BOLD);
	wmove(window_info, 3, 2); waddstr(window_info, "IP Address: ", color_pair(4) + A_BOLD);
	wmove(window_info, 3, 29); waddstr(window_info, "Region: ", color_pair(4) + A_BOLD);
	wmove(window_info, 3, 68); waddstr(window_info, "SKU...: ", color_pair(4) + A_BOLD);
	wmove(window_info, 4, 68); waddstr(window_info, "Capacity.: ", color_pair(4) + A_BOLD);
	wmove(window_info, 4, 2); waddstr(window_info, "DNS Name..: ", color_pair(4) + A_BOLD);

	#Create Sys form...
	wmove(window_sys, 0, 5); waddstr(window_sys, " SYSTEM INFO ", color_pair(3));
	wmove(window_sys, 1, 2); waddstr(window_sys, "Operating System..: ", color_pair(4) + A_BOLD);
	wmove(window_sys, 2, 2); waddstr(window_sys, "Version...........: ", color_pair(4) + A_BOLD);
	wmove(window_sys, 3, 2); waddstr(window_sys, "Total VMs.........: ", color_pair(4) + A_BOLD);
	wmove(window_sys, 4, 2); waddstr(window_sys, "Provisioning State: ", color_pair(4) + A_BOLD);
