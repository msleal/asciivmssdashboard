#!/usr/bin/env python
# General functions...

"""
Copyright (c) 2016, Marcelo Leal
Description: The power is in the terminal...
License: MIT (see LICENSE.txt file for details)
"""

from unicurses import *
from subprocess import call

def set_colors():
	init_pair(1, COLOR_BLUE, COLOR_BLUE);
	init_pair(2, COLOR_YELLOW, COLOR_YELLOW);
	init_pair(3, COLOR_BLACK, COLOR_WHITE);
	init_pair(4, COLOR_WHITE, COLOR_BLACK);
	init_pair(5, COLOR_GREEN, COLOR_GREEN);
	init_pair(6, COLOR_GREEN, COLOR_BLACK);
	init_pair(7, COLOR_YELLOW, COLOR_BLACK);
	init_pair(8, COLOR_RED, COLOR_BLACK);

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
