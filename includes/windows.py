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
		write_str_color(window, 1, 1, nr, 6, 1);
	elif (ps.upper() == "CREATING"):	
		write_str_color(window, 1, 1, nr, 7, 1);
	elif (ps.upper() == "DELETING"):	
		write_str(window, 1, 1, nr);
	#Any other state we do not know about?
	else:
		write_str_color(window, 1, 1, nr, 1, 1);

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
                write_str_color(window, 1, a, " ", 5, 1);
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
	box(window);
	draw_line(window, 0, 122, 1, ACS_URCORNER);
	draw_line(window, 0, 123, 1, ACS_ULCORNER);
	draw_line(window, 1, 122, 2, ACS_VLINE);
	draw_line(window, 2, 122, 1, ACS_LRCORNER);
	draw_line(window, 2, 123, 1, ACS_LLCORNER);
	write_str_color(window, 0, 5, " PROMPT ", 3, 1);
	draw_line(window, 1, 122, 2, ACS_VLINE);
	draw_line(window, 1, 127, 1, ACS_VLINE);
	wrefresh(window);

def draw_line(window, a, b, c, char):
	wmove(window, a, b); whline(window, char, c);

def write_str(window, a, b, char):
	wmove(window, a, b); waddstr(window, char);

def write_str_color(window, a, b, char, cor, flag):
	if (flag):
		wmove(window, a, b); waddstr(window, char, color_pair(cor) + A_BOLD);
	else:
		wmove(window, a, b); waddstr(window, char, color_pair(cor));

def draw_gauge(window, used, limit):
	if (used > 0):
		a = used / limit;
		b = a * 100;
	else:
		b = 0;

	if ( b < 30):
		write_str_color(window, 3, 1, "    ", 5, 1);
	elif (b < 60):
		write_str_color(window, 3, 1, "    ", 2, 1);
		write_str_color(window, 2, 1, "    ", 2, 1);
	else:
		write_str_color(window, 3, 1, "    ", 9, 1);
		write_str_color(window, 2, 1, "    ", 9, 1);
		write_str_color(window, 1, 1, "    ", 9, 1);

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
	write_str_color(window_status, 0, 5, " STATUS ", 3, 1);

	#Window VM...
	a = 2;
	while (a < 10):
		wmove(windowvm, a, 17); wclrtoeol(windowvm);
		a += 1;
	a = 11;
	while (a < 15):
		wmove(windowvm, a, 12); wclrtoeol(windowvm);
		a += 1;
	a = 16;
	while (a < 19):
		wmove(windowvm, a, 12); wclrtoeol(windowvm);
		a += 1;
	box(windowvm);
	write_str_color(windowvm, 0, 5, " VM ", 3, 1);

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
	write_str_color(window_info, 0, 5, " GENERAL INFO ", 3, 1);
	write_str_color(window_info, 2, 2, "RG Name...: ", 4, 1);
	write_str_color(window_info, 2, 37, "VMSS Name: ", 4 , 1);
	write_str_color(window_info, 2, 68, "Tier..: ", 4 , 1);
	write_str_color(window_info, 3, 2, "IP Address: ", 4 , 1);
	write_str_color(window_info, 3, 29, "Region: ", 4 , 1);
	write_str_color(window_info, 3, 68, "SKU...: ", 4 , 1);
	write_str_color(window_info, 4, 68, "Capacity.: ", 4 , 1);
	write_str_color(window_info, 4, 2, "DNS Name..: ", 4 , 1);

	#Create Sys form...
	write_str_color(window_sys, 0, 5, " SYSTEM INFO ", 3, 1);
	write_str_color(window_sys, 1, 2, "Operating System..: ", 4 , 1);
	write_str_color(window_sys, 2, 2, "Version...........: ", 4 , 1);
	write_str_color(window_sys, 3, 2, "Total VMs.........: ", 4 , 1);
	write_str_color(window_sys, 4, 2, "Provisioning State: ", 4 , 1);
