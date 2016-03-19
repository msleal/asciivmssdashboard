#!/usr/bin/env python3
# Functions to draw and mark Azure Regions on the global map...

"""
Copyright (c) 2016, Marcelo Leal
Description: The power is in the terminal...
License: MIT (see LICENSE.txt file for details)
"""

import sys
from unicurses import *
from maps import *

#DC Coordinates...
dc_coords = {'brazilsouth':[9,18],'southcentralus':[20,40],'eastus':[17,51],
'eastus2':[18,49],'northcentralus':[18,42],'centralus':[18,40],
'westus':[19,27],'northeurope':[13,1],'westeurope':[13,8],
'eastasia':[20,64],'southeastasia':[24,60],'japaneast':[15,81],
'japanwest':[16,79],'centralindia':[21,47],'westindia':[21,45],
'southindia':[23,47],'chinaeast':[18,70],'chinanorth':[16,67],
'australiaeast':[9,31],'australiasoutheast':[10,29]};

#Do the work...
def do_dcmark(window, coords, cor):
	wmove(window, coords[0], coords[1]); waddstr(window, " ", color_pair(cor) + A_BOLD);

#Mark Datacenters on world map...
def mark_datacenters_map(window, continent):
	if (continent == "southamerica"):
		do_dcmark(window, dc_coords['brazilsouth'], 1);
	if (continent == "northandcentralamerica"):
		do_dcmark(window, dc_coords['southcentralus'], 1);
		do_dcmark(window, dc_coords['eastus'], 1);
		do_dcmark(window, dc_coords['eastus2'], 1);
		do_dcmark(window, dc_coords['northcentralus'], 1);
		do_dcmark(window, dc_coords['centralus'], 1);
		do_dcmark(window, dc_coords['westus'], 1);
	if (continent == "europeandasia"):
		do_dcmark(window, dc_coords['northeurope'], 1);
		do_dcmark(window, dc_coords['westeurope'], 1);
		do_dcmark(window, dc_coords['eastasia'], 1);
		do_dcmark(window, dc_coords['southeastasia'], 1);
		do_dcmark(window, dc_coords['japaneast'], 1);
		do_dcmark(window, dc_coords['japanwest'], 1);
		do_dcmark(window, dc_coords['centralindia'], 1);
		do_dcmark(window, dc_coords['westindia'], 1);
		do_dcmark(window, dc_coords['southindia'], 1);
		do_dcmark(window, dc_coords['chinaeast'], 1);
		do_dcmark(window, dc_coords['chinanorth'], 1);
	if (continent == "oceania"):
		do_dcmark(window, dc_coords['australiaeast'], 1);
		do_dcmark(window, dc_coords['australiasoutheast'], 1);

#Mark Deployment dc...
def mark_vmss_dc(continent, window_old, old_location, window_new, new_location, dc):
	if (new_location != old_location):
		#Free up some memory...
		wclear(dc); delwin(dc);
		draw_map(window_old, continent);
		mark_datacenters_map(window_old, continent);

	do_dcmark(window_new, dc_coords[new_location], 5);
	dc = derwin(window_new, 3, 3, dc_coords[new_location][0] - 1, dc_coords[new_location][1] - 1);
	#Alternative target mark to highlight DC on map...
	#box(dc, 2, 2);
	box(dc);
	wrefresh(dc);
	return dc;
