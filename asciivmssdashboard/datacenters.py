#!/usr/bin/env python
# Functions to draw and mark Azure Regions on the global map...

"""
Copyright (c) 2016, Marcelo Leal
Description: The power is in the terminal...
License: MIT (see LICENSE.txt file for details)
"""

import sys
import platform
from maps import *
from unicurses import *

#DC Coordinates (row x col)...
# Do not forget to update the mark_regions_map function in this file, and also the file windows.py...
dc_coords = {
             'brazilsouth':[9,18], \
             'southcentralus':[20,39], \
             'northcentralus':[16,45], \
             'westcentralus':[16,30], \
             'eastus':[19,46], \
             'eastus2':[18,49], \
             'centralus':[14,41], \
             'westus':[17,24], \
             'westus2':[15,25], \
             'canadacentral':[14,50], \
             'canadaeast':[13,57], \
             'northeurope':[12,1], \
             'uksouth':[13,2], \
             'ukwest':[12,4], \
             'westeurope':[12,8], \
             'francecentral':[13,6], \
             'francesouth':[14,8], \
             'germanynorth':[11,14], \
             'germanywestcentral':[12,12], \
             'germanynortheast':[12,16], \
             'germanycentral':[13,14], \
             'switzerlandwest':[13,10], \
             'switzerlandnorth':[14,12], \
             'norwaywest':[9,8], \
             'norwayeast':[8,11], \
             'eastasia':[20,64], \
             'southeastasia':[23,60], \
             'japaneast':[15,81], \
             'japanwest':[16,79], \
             'westindia':[20,43], \
             'centralindia':[21,46], \
             'southindia':[23,47], \
             'chinaeast':[18,70], \
             'chinaeast2':[18,68], \
             'chinanorth':[14,67], \
             'chinanorth2':[14,69], \
             'koreacentral':[15,73], \
             'koreasouth':[17,74], \
             'uaecentral':[5,33], \
             'uaenorth':[4,35], \
             'southafricanorth':[16,24], \
             'southafricawest':[18,19], \
             'australiaeast':[8,33], \
             'australiacentral2':[9,29], \
             'australiacentral':[9,31], \
             'australiasoutheast':[10,27]
};

#Linux or Windows?
oursystem = platform.system();


#CONTINENTS
southamerica = ['brazilsouth']
northandcentralamerica = ['southcentralus', 'northcentralus', 'westcentralus', 'eastus', 'eastus2', 'centralus', 'westus', 'westus2', 'canadacentral', 'canadaeast']
europeandasia = ['northeurope', 'uksouth', 'ukwest', 'westeurope', 'francecentral', 'francesouth', 'germanycentral', 'germanynorth', 'germanynortheast', 'germanywestcentral', 'switzerlandwest', 'switzerlandnorth', 'eastasia', 'southeastasia', 'japaneast', 'japanwest', 'centralindia', 'westindia', 'southindia', 'chinaeast', 'chinaeast2', 'chinanorth', 'chinanorth2', 'koreacentral', 'koreasouth', 'norwaywest', 'norwayeast']
africa = ['uaecentral', 'uaenorth', 'southafricanorth', 'southafricawest']
oceania = ['australiaeast', 'australiacentral', 'australiacentral2', 'australiasoutheast']

#Do the work...
def do_dcmark(window, coords, cor=11):
	#SYMBOL
	if (oursystem == "Linux"):
	    dc_symbol = u"\u2588";
	else:
	    cor = 5;
	    dc_symbol = " ";

	if sys.version_info.major >= 3:
		#In Python +3 we can print in unicode a nice and bright block out-of-the-box!
		wmove(window, coords[0], coords[1]); waddstr(window, dc_symbol, color_pair(cor) + A_BOLD);
	else:
		if (oursystem == "Linux"):
		    wmove(window, coords[0], coords[1]); waddstr(window, dc_symbol.encode("utf-8"), color_pair(cor) + A_BOLD);
		else:
		    wmove(window, coords[0], coords[1]); waddstr(window, dc_symbol, color_pair(cor) + A_BOLD);

#Mark Datacenters on world map...
def mark_regions_map(window, continent):
       if (continent != "southamerica" and continent != "northandcentralamerica" and continent != "europeandasia" and continent != "africa" and continent != "oceania"):
          #TODO Handle it properly...
          exit(1)

       if continent == 'southamerica':
           lista = southamerica;
       if continent == 'northandcentralamerica':
           lista = northandcentralamerica;
       if continent == 'europeandasia':
           lista = europeandasia;
       if continent == 'africa':
           lista = africa;
       if continent == 'oceania':
           lista = oceania;

       #Let's paint the globe...
       for region in lista:
           do_dcmark(window, dc_coords[region]);

#Mark Deployment dc...
def mark_vmss_dc(continent, window_old, old_location, window_new, new_location, dc):
	if (new_location != old_location):
		#Free up some memory...
		wclear(dc); delwin(dc);
		draw_map(window_old, continent);
		mark_regions_map(window_old, continent);

	do_dcmark(window_new, dc_coords[new_location], 5);
	dc = derwin(window_new, 3, 3, dc_coords[new_location][0] - 1, dc_coords[new_location][1] - 1);
	#Alternative target mark to highlight DC on map...
	#box(dc, 2, 2);
	box(dc);
	wrefresh(dc);
	return dc;
