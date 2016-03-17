#!/usr/bin/env python
# ASCii VMSS Console - The power is in the terminal...

"""
Copyright (c) 2016, Marcelo Leal
Description: The power is in the terminal...
License: MIT (see LICENSE.txt file for details)
"""

import sys
import time
import platform
from unicurses import *
#Now to load our modules, we need to inform our modules path first...
sys.path.append('./includes/')
from maps import *
from azure import *
from windows import *
from datacenters import *

# app state variables
vmssProperties = [];
vmssVmProperties = [];
vmssVmInstanceView = '';
access_token="";

# Curses...
window_continents = {'northandcentralamerica':0,'southamerica':0,'europeandasia':0,'africa':0,'oceania':0};
panel_continents = {'northandcentralamerica':0,'southamerica':0,'europeandasia':0,'africa':0,'oceania':0};
window_information = {'vmss_info':0,'system':0,'status':0,'virtualmachines':0,'vm':0,'cmd':0,'help':0};
panel_information = {'vmss_info':0,'system':0,'status':0,'virtualmachines':0,'vm':0,'cmd':0,'help':0};

def main(): #{
	#Initialize...
	COLSTART=100;
	ourhome = platform.system();
	stdscr = initscr();

	if (ourhome == "Linux"):
		# Non-block when waiting for getch (cmd prompt).
		# This does not work on Windows, so we will not be able to exit nicely...
		stdscr.nodelay(1);

	termsize = getmaxyx(stdscr);
	if (termsize[0] >= 50 and termsize[1] >= 200):
		SZ = 1;
	else:
		if (ourhome == "Linux"):
			errnr = resize_terminal();
			SZ == errnr;
		else:
			SZ = 0;
	if (SZ == 0):
		print ("You need a terminal at least 50x200...");
		print ("If you are running this application on Linux, you can resize your terminal using: resize -s 50 200.");
		endwin();
		exit(1);

	if (not has_colors()): #{
		print ("You need to have colors")
		return 0;
        #}
	start_color();
	set_colors();
	noecho();
	curs_set(False);
	keypad(stdscr,True);

        #Our main window with margin and out title...
        #newwin(lines, colunms, startline, startcolunm);
	window = newwin(0, 0, 0, 0);
	box(window);
	panel = new_panel(window);
	#Window Headers...
	wmove(window, 0, 5); waddstr(window, "| ASCii VMSS Dashboard - Version: 1.0 |");
	wmove(window, 0, termsize[1] - 28); waddstr(window, " Window Size: ");
	wmove(window, 0, termsize[1] - 14); waddstr(window, str(termsize));

	#Here starts our game...
	#Continents create_window(lines, colunms, startline, startcolunm)
	window_continents['northandcentralamerica'] = create_window(26, 86, 2, 2);
	panel_continents['northandcentralamerica'] = new_panel(window_continents['northandcentralamerica']);
	draw_map(window_continents['northandcentralamerica'], "northandcentralamerica");
	mark_datacenters_map(window_continents['northandcentralamerica'], "northandcentralamerica");
	#win_animation(panel_continents['northandcentralamerica'], termsize, 2, 2);

	window_continents['southamerica'] = create_window(20, 27, 27, 49);
	panel_continents['southamerica'] = new_panel(window_continents['southamerica']);
	draw_map(window_continents['southamerica'], "southamerica");
	mark_datacenters_map(window_continents['southamerica'], "southamerica");
	#win_animation(panel_continents['southamerica'], termsize, 27, 49);

	window_continents['europeandasia'] = create_window(26, 110, 4, 88);
	panel_continents['europeandasia'] = new_panel(window_continents['europeandasia']);
	draw_map(window_continents['europeandasia'], "europeandasia");
	mark_datacenters_map(window_continents['europeandasia'], "europeandasia");
	#win_animation(panel_continents['europeandasia'], termsize, 4, 88);

	window_continents['africa'] = create_window(20, 38, 20, 84);
	panel_continents['africa'] = new_panel(window_continents['africa']);
	draw_map(window_continents['africa'], "africa");
	#win_animation(panel_continents['africa'], termsize, 20, 84);

	window_continents['oceania'] = create_window(15, 48, 29, 143);
	panel_continents['oceania'] = new_panel(window_continents['oceania']);
	draw_map(window_continents['oceania'], "oceania");
	mark_datacenters_map(window_continents['oceania'], "oceania");
	#win_animation(panel_continents['oceania'], termsize, 29, 143);

	#Create all information windows...
	window_information['vmss_info'] = create_window(6, 90, 43, 70); 
	panel_information['vmss_info'] = new_panel(window_information['vmss_info']);
	box(window_information['vmss_info']);

	window_information['system'] = create_window(6, 38, 43, 160); 
	box(window_information['system']);
	panel_information['system'] = new_panel(window_information['system']);
	wmove(window_information['system'], 0, 5); waddstr(window_information['system'], " SYSTEM INFO ", color_pair(3));

	window_information['status'] = create_window(3, 25, 2, 2); 
	panel_information['status'] = new_panel(window_information['status']);
	box(window_information['status']);
	wmove(window_information['status'], 0, 13); waddstr(window_information['status'], " STATUS ", color_pair(3));
	wmove(window_information['status'], 1, 11); waddstr(window_information['status'], "|          |");

	window_information['virtualmachines'] = create_window(17, 43, 29, 2); 
	panel_information['virtualmachines'] = new_panel(window_information['virtualmachines']);
	box(window_information['virtualmachines']);

	#Window Headers...
	wmove(window_information['virtualmachines'], 0, 2); waddstr(window_information['virtualmachines'], " 1 ");
	wmove(window_information['virtualmachines'], 0, 37); waddstr(window_information['virtualmachines'], " 8 ");
	wmove(window_information['virtualmachines'], 2, 0); waddstr(window_information['virtualmachines'], "1");
	wmove(window_information['virtualmachines'], 14, 0); waddstr(window_information['virtualmachines'], "5");
	wmove(window_information['virtualmachines'], 0, 12); waddstr(window_information['virtualmachines'], " VIRTUAL MACHINES ", color_pair(3));

	window_information['cmd'] = create_window(3, 68, 46, 2); 
	panel_information['cmd'] = new_panel(window_information['cmd']);
	box(window_information['cmd']);
	wmove(window_information['cmd'], 0, 5); waddstr(window_information['cmd'], " PROMPT ", color_pair(3));
	draw_line(window_information['cmd'], 0, 62, 1, ACS_URCORNER);
	draw_line(window_information['cmd'], 0, 63, 1, ACS_ULCORNER);
	draw_line(window_information['cmd'], 1, 62, 2, ACS_VLINE);
	draw_line(window_information['cmd'], 2, 62, 1, ACS_LRCORNER);
	draw_line(window_information['cmd'], 2, 63, 1, ACS_LLCORNER);
	wmove(window_information['cmd'], 1, 3); waddstr(window_information['cmd'], ">", color_pair(4) + A_BOLD);

	#Info header...
	wmove(window_information['vmss_info'], 0, 5); waddstr(window_information['vmss_info'], " GENERAL INFO ", color_pair(3));

	#VM Window...
	window_information['vm'] = create_window(4, 31, 25, 2);
	box(window_information['vm']);
	panel_information['vm'] = new_panel(window_information['vm']);
	hide_panel(panel_information['vm']);
	wmove(window_information['vm'], 0, 5); waddstr(window_information['vm'], " VM ", color_pair(3));
	wmove(window_information['vm'], 1, 2); waddstr(window_information['vm'], "Hostname: ");
	wmove(window_information['vm'], 2, 2); waddstr(window_information['vm'], "State...: ");

	#Help Window...
	window_information['help'] = create_window(12, 32, 21, 166);
	box(window_information['help']);
	panel_information['help'] = new_panel(window_information['help']);
	hide_panel(panel_information['help']);
	#win_animation(panel_information['help'], termsize, 22, 165);
	wmove(window_information['help'], 0, 5); waddstr(window_information['help'], " HELP ", color_pair(3));
	wmove(window_information['help'], 1, 2); waddstr(window_information['help'], "To enter commands, type: ':'");
	wmove(window_information['help'], 3, 2); waddstr(window_information['help'], "  -= Command Examples =-");
	wmove(window_information['help'], 4, 2); waddstr(window_information['help'], "Adding 2 VM's: add vm 2");
	wmove(window_information['help'], 5, 2); waddstr(window_information['help'], "Deleting 1 VM: del vm 1");
	wmove(window_information['help'], 6, 2); waddstr(window_information['help'], "Select VM 8: select vm 8");
	wmove(window_information['help'], 7, 2); waddstr(window_information['help'], "Deselect any VM: deselect");
	wmove(window_information['help'], 9, 2); waddstr(window_information['help'], "Change VMSS:");
	wmove(window_information['help'], 10, 2); waddstr(window_information['help'], "rg <rgname> vmss <vmssname>");

	update_panels();
	doupdate();

	#Our thread that updates all VMSS info (Default Refresh Interval: 60)...
	vmss_monitor_thread(window_information, panel_information, window_continents, panel_continents);
	endwin();
	return 0;

if (__name__ == "__main__"): #{
        main();
#}
