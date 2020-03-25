#!/usr/bin/env python
# All uniCurses routines to ASCii Effects representation on the terminal are here (or should be)...

"""
Copyright (c) 2016, Marcelo Leal
Description: The power is in the terminal...
License: MIT (see LICENSE.txt file for details)
"""

import time
import logging
from subprocess import call
from unicurses import *

#Insights sample counter...
sample_one = 0; sample_two = 0;

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
	init_pair(10, COLOR_BLUE, COLOR_BLACK);
	init_pair(11, COLOR_CYAN, COLOR_BLACK);
	init_pair(12, COLOR_MAGENTA, COLOR_MAGENTA);

#Draw logo...
def draw_logo(window):
	first_square = derwin(window, 3, 6, 1, 1);
	second_square = derwin(window, 3, 6, 1, 8);
	third_square = derwin(window, 3, 6, 4, 1);
	forth_square = derwin(window, 3, 6, 4, 8);
	write_str_color(first_square, 0, 1, "     ", 9, 0);
	write_str_color(first_square, 1, 1, "     ", 9, 0);
	write_str_color(second_square, 0, 1, "     ", 5, 0);
	write_str_color(second_square, 1, 1, "     ", 5, 0);
	write_str_color(third_square, 0, 1, "     ", 1, 0);
	write_str_color(third_square, 1, 1, "     ", 1, 0);
	write_str_color(forth_square, 0, 1, "     ", 2, 0);
	write_str_color(forth_square, 1, 1, "     ", 2, 0);

#Create Windows...
def create_window(x, y, w, z):
        #window = newwin(lines, colunms, startline, startcolunm);
	window = newwin(x, y, w, z);
	#DEBUG
        #box(window);
	return window;

#Draw VM...
def draw_vm(vmc, window, ps, flag):
	if (vmc < 100):
		nr = "%03d" % vmc;
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
		wmove(window, 2, 3); whline(window, ">" , 1);
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
		update_panels();
		doupdate();
	time.sleep(.2);

def win_animation(panel, nasp, xfinal, yfinal):
	xstart = nasp[0];
	ystart = nasp[1];

	while (xstart != xfinal):
		move_panel (panel, xstart, ystart);
		update_panels();
		doupdate();
		xstart -= 1;
		time.sleep(.005);
	while (ystart != yfinal):
		move_panel (panel, xstart, ystart);
		update_panels();
		doupdate();
		ystart -= 1;
		time.sleep(.005);

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

def draw_line(window, a, b, c, char):
	wmove(window, a, b); whline(window, char, c);

def draw_line_color(window, a, b, c, char, cor):
	wmove(window, a, b); wattrset(window, COLOR_PAIR(cor)); whline(window, char, c);
	wattrset(window, A_NORMAL)

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
		b = int(a * 100);
	else:
		b = 0;

        #Now let's draw the graph...
	if (b <= 30):
		write_str_color(window, 3, 1, "    ", 5, 1);
	if (b > 30 and b <= 70):
		write_str_color(window, 3, 1, "    ", 2, 1);
		write_str_color(window, 2, 1, "    ", 2, 1);
	if (b > 70):
		write_str_color(window, 3, 1, "    ", 9, 1);
		write_str_color(window, 2, 1, "    ", 9, 1);
		write_str_color(window, 1, 1, "    ", 9, 1);

def get_continent_dc(dc):
	if (dc == "brazilsouth"):
		return 'southamerica';
	if (dc == "southcentralus" or dc == "northcentralus" or dc == "westcentralus" or dc == "eastus" or dc == "eastus2" or dc == "centralus" or dc == "westus" or dc == "westus2" or dc == "canadacentral" or dc == "canadaeast"):
		return 'northandcentralamerica';
	if (dc == "northeurope" or dc == "uksouth" or dc == "ukwest" or dc == "westeurope" or dc == "francecentral" or dc == "francesouth" or dc == "germanycentral" or dc == "germanynorth" or dc == "germanynortheast" or dc == "germanywestcentral" or dc == "switzerlandwest" or dc == "switzerlandnorth" or dc == "eastasia" or dc == "southeastasia" or dc == "japaneast" or dc == "japanwest" or dc == "westindia" or dc == "centralindia" or dc == "southindia" or dc == "chinaeast" or dc == "chinaeast2" or dc == "chinanorth" or dc == "koreacentral" or dc == "koreasouth" or dc == "chinanorth2" or dc == "norwaywest" or dc == "norwayeast"):
		return 'europeandasia';
	if (dc == "uaecentral" or dc == "uaenorth" or dc == "southafricanorth" or dc == "southafricawest"):
		return 'africa';
	if (dc == "australiacentral" or dc == "australiacentral2" or dc == "australiaeast" or dc == "australiasoutheast"):
		return 'oceania';

def resize_terminal():
	#errnr = call(["resize", "-s 55 235 >/dev/null"]);
	errnr = 1;
	return errnr;

def clean_gauge(window):
        #A quick clean up first...
	write_str(window, 3, 1, "    ");
	write_str(window, 2, 1, "    ");
	write_str(window, 1, 1, "    ");

def clean_usage(window):
	write_str_color(window, 2, 2, "[Availability Sets] [     /     ]", 4, 1);
	write_str_color(window, 3, 2, "[ Regional  Cores ] [     /     ]", 4, 1);
	write_str_color(window, 4, 2, "[Virtual  Machines] [     /     ]", 4, 1);
	write_str_color(window, 5, 2, "[  VM Scale Sets  ] [     /     ]", 4, 1);

def clean_monitor_form(window):
	#Window Update Monitor...
	wmove(window['monitor'], 1, 30); wclrtoeol(window['monitor']);
	box(window['monitor']);
	write_str_color(window['monitor'], 0, 5, " VM UPDATE MONITOR ", 3, 0);

def clean_insights(window, cor):
	#Window Insights...
	x, y = getmaxyx(window);
	a = 1;
	while (a < 16):
		wmove(window, a, 1); wclrtoeol(window);
		draw_line_color(window, a, 1, y - 2, ACS_HLINE, cor);
		a += 1;
	box(window);
	write_str(window, 0, 30, " SAMPLE: ");
	write_str(window, 0, 57, " MAX: ");
	write_str(window, 0, 84, " MIN: ");
	write_str(window, 0, 113, " LAST VALUE: ");
	write_str_color(window, 0, 5, " INSIGHTS: ", 3, 0);

def clean_vm(window):
	#Window VM...
	a = 2;
	while (a < 10):
		wmove(window['vm'], a, 17); wclrtoeol(window['vm']);
		a += 1;
	a = 11;
	while (a < 15):
		wmove(window['vm'], a, 12); wclrtoeol(window['vm']);
		a += 1;
	a = 16;
	while (a < 19):
		wmove(window['vm'], a, 11); wclrtoeol(window['vm']);
		a += 1;
	box(window['vm']);
	write_str_color(window['vm'], 0, 5, " VM ", 3, 0);

def clean_forms(window):
	#Let's handle the status window here...
	wmove(window['status'], 1, 22); wclrtoeol(window['status']);
	box(window['status']);
	write_str_color(window['status'], 0, 5, " STATUS ", 3, 0);

	#Window Update Monitor...
	wmove(window['monitor'], 1, 30); wclrtoeol(window['monitor']);
	box(window['monitor']);
	write_str_color(window['monitor'], 0, 5, " VM UPDATE MONITOR ", 3, 0);

def clean_infoandsys(window):
	#Info and Sys Windows...
	a = 1;
	while (a < 5):
		#Clean up lines...
		wmove(window['vmss_info'], a, 1); wclrtoeol(window['vmss_info']);
		wmove(window['system'], a, 1); wclrtoeol(window['system']);
		a += 1;

	#Create Info form...
	create_vmssinfo_form(window['vmss_info']);
	#Create Sys form...
	create_system_form(window['system']);

def create_vmssinfo_form(window):
	box(window);
	write_str_color(window, 0, 5, " GENERAL INFO ", 3, 0);
	write_str_color(window, 2, 2, "RG Name...: ", 4, 1);
	write_str_color(window, 2, 37, "VMSS Name: ", 4 , 1);
	write_str_color(window, 2, 68, "Tier..: ", 4 , 1);
	write_str_color(window, 3, 2, "IP Address: ", 4 , 1);
	write_str_color(window, 3, 37, "Region: ", 4 , 1);
	write_str_color(window, 3, 68, "SKU...: ", 4 , 1);
	write_str_color(window, 4, 68, "Capacity.: ", 4 , 1);
	write_str_color(window, 4, 2, "DNS Name..: ", 4 , 1);

def create_system_form(window):
	box(window);
	write_str_color(window, 0, 5, " SYSTEM INFO ", 3, 0);
	write_str_color(window, 1, 2, "Operating System..: ", 4 , 1);
	write_str_color(window, 2, 2, "Version...........: ", 4 , 1);
	write_str_color(window, 3, 2, "Total VMs.........: ", 4 , 1);
	write_str_color(window, 4, 2, "Provisioning State: ", 4 , 1);

def create_vm_form(window):
	write_str_color(window, 1, 10, "    INSTANCE VIEW     ", 3, 0);
	write_str_color(window, 2, 2, "Instance ID..: ", 4, 1);
	write_str_color(window, 3, 2, "Hostname.....: ", 4, 1);
	write_str_color(window, 4, 2, "Prov. State..: ", 4, 1);
	write_str_color(window, 5, 2, "Prov. Date...: ", 4, 1);
	write_str_color(window, 6, 2, "Prov. Time...: ", 4, 1);
	write_str_color(window, 7, 2, "Power State..: ", 4, 1);
	write_str_color(window, 8, 2, "Update Domain: ", 4, 1);
	write_str_color(window, 9, 2, "Fault Domain.: ", 4, 1);
	write_str_color(window, 10, 10, "    NETWORK           ", 3, 0);
	write_str_color(window, 11, 2, "NIC.....: ", 4, 1);
	write_str_color(window, 12, 2, "MAC.....: ", 4, 1);
	write_str_color(window, 13, 2, "IP......: ", 4, 1);
	write_str_color(window, 14, 2, "Primary.: ", 4, 1);
	write_str_color(window, 15, 10, "    VM Guest Agent    ", 3, 0);
	write_str_color(window, 16, 2, "Version: ", 4, 1);
	write_str_color(window, 17, 2, "Status.: ", 4, 1);
	write_str_color(window, 18, 2, "State..: ", 4, 1);

def create_help_form(window):
	write_str(window, 2, 2, "To enter commands, type: ':'");
	write_str(window, 4, 3, "---= Command Examples =---");
	write_str_color(window, 6, 2, "Adding 2 VM's: ", 4, 1);
	write_str(window, 6, 17, "add vm 2");
	write_str_color(window, 7, 2, "Deleting 1 VM: ", 4, 1);
	write_str(window, 7, 17, "del vm 1");
	write_str_color(window, 8, 2, "Select VM 8: ", 4, 1);
	write_str(window, 8, 15, "select vm 8");
	write_str_color(window, 9, 2, "Deselect any VM: ", 4, 1);
	write_str(window, 9, 19, "deselect");
	write_str_color(window, 10, 2, "Change Page: ", 4, 1);
	write_str(window, 10, 15, "show page 3");
	write_str_color(window, 11, 2, "Show LOG: ", 4, 1);
	write_str(window, 11, 12, "log");
	write_str_color(window, 12, 2, "Show Insights 1: ", 4, 1);
	write_str(window, 12, 19, "insights 1");
	write_str_color(window, 13, 2, "Show Insights 2: ", 4, 1);
	write_str(window, 13, 19, "insights 2");
	write_str_color(window, 14, 2, "Show both Insights: ", 4, 1);
	write_str(window, 14, 23, "insights");
	write_str_color(window, 15, 2, "Show all Windows: ", 4, 1);
	write_str(window, 15, 20, "debug");
	write_str_color(window, 16, 2, "Change VMSS: rg <rgname>", 4, 1);
	write_str(window, 16, 15, "rg <rgname>");
	write_str(window, 17, 2, "vmss <vmssname>");

def create_virtualmachines_form(window):
	write_str(window, 0, 2, " 1 ");
	write_str(window, 0, 48, " A ");
	write_str(window, 2, 0, "1");
	write_str(window, 2, 53, "1");
	write_str(window, 14, 0, "5");
	write_str(window, 14, 53, "5");
	write_str(window, 29, 0, "A");
	write_str(window, 29, 53, "A");

def create_prompt_form(window):
	box(window);
	draw_line(window, 0, 122, 1, ACS_URCORNER);
	draw_line(window, 0, 123, 1, ACS_ULCORNER);
	draw_line(window, 1, 122, 2, ACS_VLINE);
	draw_line(window, 2, 122, 1, ACS_LRCORNER);
	draw_line(window, 2, 123, 1, ACS_LLCORNER);
	write_str_color(window, 0, 5, " PROMPT ", 3, 0);
	draw_line(window, 1, 122, 2, ACS_VLINE);
	draw_line(window, 1, 127, 1, ACS_VLINE);
	wrefresh(window);

def create_usage_form(window):
	write_str_color(window, 2, 2, "[Availability Sets] [     /     ]", 4, 1);
	write_str_color(window, 3, 2, "[ Regional  Cores ] [     /     ]", 4, 1);
	write_str_color(window, 4, 2, "[Virtual  Machines] [     /     ]", 4, 1);
	write_str_color(window, 5, 2, "[  VM Scale Sets  ] [     /     ]", 4, 1);

def draw_insights(window, values, title, metric, flag):
	global sample_one, sample_two;

	#Which counter should we use?
	if (metric == "One"):
		sample = sample_one;
	else:
		sample = sample_two;

	#If we have a flag, means that we switched RG and VMSS and so we need to reset...
	if (flag): sample = 0;
	sample += 1;

	max_value = max(values);
	min_value = min(values);
	x, y = getmaxyx(window);
	max_lines = x - 2;

	#Print the MAX and MIN values to facilitate graph interpretation...
	write_str(window, 0, 16, title);
	write_str(window, 0, 16 + len(title), " ");
	write_str(window, 0, 39, sample);
	write_str(window, 0, 39 + len(str(sample)), " ");
	write_str(window, 0, 63, max_value);
	write_str(window, 0, 63 + len(str(max_value)), " ");
	write_str(window, 0, 90, min_value);
	write_str(window, 0, 90 + len(str(min_value)), " ");

	vlines = [];
	index = 0;
	for z in values:
		vlines.append(index);	
		if (z > 0):
			prop =  (z * 100.0) / max_value;
			ld = max_lines * (prop / 100.0);
			vlines[index] = int(ld);
		else:
			vlines[index] = 0;
		index += 1;

	index = 0; column = 2;
	while (index < values.__len__()):
		write_str(window, 0, 126, values[index]);
		write_str(window, 0, 126 + len(str(values[index])), " ");
		line = 0;
		while (line < vlines[index]):
			if (line == 0):
				draw_line(window, x - 1, column, 1, ACS_BTEE);
			draw_line(window, max_lines - line, column, 1, ACS_VLINE);
			line += 1;
		index += 1; column += 2;

	if (metric == "One"):
		sample_one = sample;
	else:
		sample_two = sample;
