#!/usr/bin/env python
# ASCii VMSS Console - The power is in the terminal...

"""
Copyright (c) 2016, Marcelo Leal
Description: The power is in the terminal...
License: MIT (see LICENSE.txt file for details)
"""

from azure import *

#Linux or Windows?
oursystem = platform.system();

#Our Home...
HOMEUSER = expanduser("~") 
HOMEDIR = HOMEUSER + "/.asciivmssdashboard"

# Load Azure app defaults
filepresent = 1
try:
        with open(HOMEDIR + '/asciivmssdashboard.json') as configFile:
                configData = json.load(configFile)
except IOError or FileNotFoundError:
        # ---> In case we do not find our asciivmssdashboard.json config file, we will run in demo mode...
        filepresent = 0
        #sys.exit()

try:
        demoEnabled = configData['demoEnabled']
except:
        demoEnabled = "Yes"
        # ---> "Missing 'demoEnabled' configuration parameter. So, to keep it simple, we will run in demo mode..."
        # ---> "Use the asciivmssdashboard.json.tmpl file as a template to fill in your custom values..."

try:
        animationEnabled = configData['animationEnabled']
        if filepresent: 
            configFile.close()
except:
        if (oursystem == "Linux"):
            animationEnabled = "Yes"
        else:
            animationEnabled = "No"
        # ---> "Missing 'animationEnabled' configuration parameter. Because we like it and was not simple to implement, we will assume you also like it..."
        # ---> "Use the asciivmssdashboard.json.tmpl file as a template to fill in your custom values..."
        if filepresent: 
            configFile.close()
        #sys.exit()

# app state variables
vmssProperties = [];
vmssVmProperties = [];
vmssVmInstanceView = '';
access_token="";

# Curses...
window_continents = {'northandcentralamerica':0,'southamerica':0,'europeandasia':0,'africa':0,'oceania':0};
panel_continents = {'northandcentralamerica':0,'southamerica':0,'europeandasia':0,'africa':0,'oceania':0};
window_information = {'vmss_info':0,'system':0,'status':0,'virtualmachines':0,'vm':0,'monitor':0,'usage':0,'gauge':0,'gaugeas':0,'gaugerc':0,'gaugevm':0,'gaugess':0,'log':0,'insightsone':0,'insightstwo':0,'exit':0,'error':0,'logo':0,'cmd':0,'help':0};
panel_information = {'vmss_info':0,'system':0,'status':0,'virtualmachines':0,'vm':0,'monitor':0,'usage':0,'gauge':0,'gaugeas':0,'gaugerc':0,'gaugevm':0,'gaugess':0,'log':0,'insightsone':0,'insightstwo':0,'exit':0,'error':0,'logo':0,'cmd':0,'help':0};

#Draw Helper...
def draw_helper(geo, termsize):
        #First we create the window in the right location...
	if (animationEnabled.lower() == 'yes'):
            if (geo == 'northandcentralamerica'):
                window_continents['northandcentralamerica'] = create_window(26, 86, 1, termsize[1] + 1);
            if (geo == 'southamerica'):
                window_continents['southamerica'] = create_window(20, 27, 26, termsize[1] + 1);
            if (geo == 'europeandasia'):
                window_continents['europeandasia'] = create_window(26, 109, termsize[0] + 1, 125);
            if (geo == 'africa'):
                window_continents['africa'] = create_window(20, 38, termsize[0] + 1, 121);
            if (geo == 'oceania'):
                window_continents['oceania'] = create_window(15, 48, termsize[0] + 1, 180);
	else:
            if (geo == 'northandcentralamerica'):
                window_continents['northandcentralamerica'] = create_window(26, 86, 1, 39);
            if (geo == 'southamerica'):
                window_continents['southamerica'] = create_window(20, 27, 26, 86);
            if (geo == 'europeandasia'):
                window_continents['europeandasia'] = create_window(26, 109, 3, 125);
            if (geo == 'africa'):
                window_continents['africa'] = create_window(20, 38, 19, 121);
            if (geo == 'oceania'):
                window_continents['oceania'] = create_window(15, 48, 28, 180);

        #Create the other panels...
	panel_continents[geo] = new_panel(window_continents[geo]);
	draw_map(window_continents[geo], geo);
	mark_regions_map(window_continents[geo], geo);

        #Do the animation if needed...
	if (animationEnabled.lower() == 'yes'):
            if (geo == 'northandcentralamerica'):
                win_animation(panel_continents['northandcentralamerica'], termsize, 1, 38);
            if (geo == 'southamerica'):
                win_animation(panel_continents['southamerica'], termsize, 26, 86);
            if (geo == 'europeandasia'):
                win_animation(panel_continents['europeandasia'], termsize, 3, 125);
            if (geo == 'africa'):
                win_animation(panel_continents['africa'], termsize, 19, 121);
            if (geo == 'oceania'):
                win_animation(panel_continents['oceania'], termsize, 28, 180);

def main(): #{
	#Initialize...
	COLSTART=100; SZ = 0;
	oursystem = platform.system();
	stdscr = initscr();
	modo = "REAL";
	if (demoEnabled.lower() == 'yes'):
            modo = "DEMO";

	if (oursystem == "Disabledbecausewasconsuming1proconLinux"):
		# Non-block when waiting for getch (cmd prompt).
		# This does not work on Windows, so we will not be able to exit nicely...
		stdscr.nodelay(1);
	#Just a workaround for the SSL warning...
	cur_version = sys.version_info;
	if (cur_version.major == 2):
		requests.packages.urllib3.disable_warnings()

	termsize = getmaxyx(stdscr);
	if (termsize[0] >= 55 and termsize[1] >= 235):
		SZ = 1;
	else:
		if (oursystem == "Linux"):
			errnr = resize_terminal();
			SZ == errnr;
		else:
			SZ = 0;
	if (SZ == 0):
		endwin();
		print ("You need a terminal at least 55x235...");
		print ("If you are running this application on Linux, you can resize your terminal using: resize -s 55 235.");
		sys.exit(1);

	if (not has_colors()):
		print ("You need to have colors")
		sys.exit(1);
	start_color();
	set_colors();
	noecho();
	curs_set(False);
	keypad(stdscr,True);

        #Our main window with margin and our title...
        #newwin(lines, colunms, startline, startcolunm);
	window = newwin(0, 0, 0, 0);
	box(window);
	panel = new_panel(window);
	#Window Headers...
	write_str(window, 0, 5, "| ASCii VMSS Dashboard - Version: 2.0 |");
	write_str(window, 0, 50, " PYTHON Version: ");
	write_str(window, 0, 67, cur_version.major);
	write_str(window, 0, 68, "x ");
	write_str(window, 0, 77, "| Platform: ");
	write_str(window, 0, 89, oursystem);
	write_str(window, 0, 89 + len(oursystem), " |");
	write_str(window, 0, 108, "| Execution Mode: ");
	if modo == "REAL":
            write_str_color(window, 0, 126, modo, 6, 0);
	else:
            write_str(window, 0, 126, modo);
	write_str(window, 0, 126 + len(modo), " |");
	write_str(window, 0, termsize[1] - 28, " Window Size: ");
	write_str(window, 0, termsize[1] - 14, str(termsize));

	#Here starts our game...
	#Continents create_window(lines, colunms, startline, startcolunm)

	# NORTHAMERICA
	draw_helper('northandcentralamerica', termsize);

	# SOUTHAMERICA
	draw_helper('southamerica', termsize);

	# EUROPEANDASIA
	draw_helper('europeandasia', termsize);

	# AFRICA
	draw_helper('africa', termsize);

	# OCEANIA
	draw_helper('oceania', termsize);

	#Create all information windows...
	window_information['vmss_info'] = create_window(6, 90, 48, 105); 
	panel_information['vmss_info'] = new_panel(window_information['vmss_info']);
	box(window_information['vmss_info']);
	write_str_color(window_information['vmss_info'], 0, 5, " GENERAL INFO ", 3, 0);

	window_information['system'] = create_window(6, 38, 48, 195); 
	box(window_information['system']);
	panel_information['system'] = new_panel(window_information['system']);
	write_str_color(window_information['system'], 0, 5, " SYSTEM INFO ", 3, 0);

	window_information['status'] = create_window(3, 36, 1, 2); 
	panel_information['status'] = new_panel(window_information['status']);
	box(window_information['status']);
	write_str_color(window_information['status'], 0, 5, " STATUS ", 3, 1);
	write_str(window_information['status'], 1, 2, "Updated at");

	window_information['virtualmachines'] = create_window(32, 54, 22, 2); 
	panel_information['virtualmachines'] = new_panel(window_information['virtualmachines']);
	box(window_information['virtualmachines']);
	write_str_color(window_information['virtualmachines'], 0, 18, " VIRTUAL MACHINES ", 3, 0);
	create_virtualmachines_form(window_information['virtualmachines']);

	window_information['monitor'] = create_window(3, 54, 19, 2);
	box(window_information['monitor']);
	panel_information['monitor'] = new_panel(window_information['monitor']);
	write_str_color(window_information['monitor'], 0, 5, " VM UPDATE MONITOR ", 3, 0);
	write_str_color(window_information['monitor'], 1, 2, "Processing Virtual Machine: ", 4, 1);

	window_information['usage'] = create_window(15, 36, 4, 2);
	box(window_information['usage']);
	panel_information['usage'] = new_panel(window_information['usage']);
	write_str_color(window_information['usage'], 0, 5, " COMPUTE USAGE ", 3, 0);
	create_usage_form(window_information['usage']);

	window_information['log'] = create_window(18, 195, 1, 38);
	panel_information['log'] = new_panel(window_information['log']);
	hide_panel(panel_information['log']);
	box(window_information['log']);
	write_str_color(window_information['log'], 0, 5, " LOG ", 3, 0);

	window_information['insightsone'] = create_window(15, 177, 19, 56);
	panel_information['insightsone'] = new_panel(window_information['insightsone']);
	hide_panel(panel_information['insightsone']);
	box(window_information['insightsone']);
	write_str_color(window_information['insightsone'], 0, 5, " INSIGHTS METRIC #1 ", 3, 0);

	window_information['insightstwo'] = create_window(11, 144, 34, 89);
	panel_information['insightstwo'] = new_panel(window_information['insightstwo']);
	hide_panel(panel_information['insightstwo']);
	box(window_information['insightstwo']);
	write_str_color(window_information['insightstwo'], 0, 5, " INSIGHTS METRIC #2 ", 3, 0);

	window_azure = create_window(3, 16, 45, 89);
	panel_azure = new_panel(window_azure);
	write_str_color(window_azure, 1, 1, "    AZURE     ", 3, 0);
	window_information['logo'] = create_window(7, 16, 47, 89);
	panel_information['logo'] = new_panel(window_information['logo']);
	box(window_information['logo']);
	draw_logo(window_information['logo']);

	window_information['exit'] = create_window(8, 57, 22, 88);
	panel_information['exit'] = new_panel(window_information['exit']);
	hide_panel(panel_information['exit']);
	box(window_information['exit']);
	write_str_color(window_information['exit'], 3, 5, "Waiting for Console Update threads to close...", 4, 1);

	window_information['error'] = create_window(3, 128, 42, 105);
	panel_information['error'] = new_panel(window_information['error']);
	hide_panel(panel_information['error']);
	box(window_information['error']);
	write_str_color(window_information['error'], 1, 2, "       ", 9, 0);
	write_str_color(window_information['error'], 1, 9, " ERROR ", 4, 1);
	write_str_color(window_information['error'], 1, 16, "       ", 9, 0);

	window_information['cmd'] = create_window(3, 128, 45, 105); 
	panel_information['cmd'] = new_panel(window_information['cmd']);
	box(window_information['cmd']);
	write_str_color(window_information['cmd'], 0, 5, " PROMPT ", 3, 0);
	write_str_color(window_information['cmd'], 1, 3, ">", 4, 1);
	create_prompt_form(window_information['cmd']);

	window_information['help'] = create_window(20, 33, 34, 56);
	box(window_information['help']);
	panel_information['help'] = new_panel(window_information['help']);
	hide_panel(panel_information['help']);
	write_str_color(window_information['help'], 0, 5, " HELP ", 3, 0);
	create_help_form(window_information['help']);

	window_information['vm'] = create_window(20, 33, 34, 56);
	box(window_information['vm']);
	panel_information['vm'] = new_panel(window_information['vm']);
	hide_panel(panel_information['vm']);
	write_str_color(window_information['vm'], 0, 5, " VM ", 3, 0);
	create_vm_form(window_information['vm']);

	#Gauge Container Window...
	window_information['gauge'] = create_window(7, 34, 11, 3);
	box(window_information['gauge']);
	panel_information['gauge'] = new_panel(window_information['gauge']);
	#Gauge Windows...
	y = 5;
	gaugeaux = "gaugeas gaugerc gaugevm gaugess";
	for x in gaugeaux.split():
		window_information[x] = create_window(5, 6, 12, y);
		box(window_information[x]);
		panel_information[x] = new_panel(window_information[x]);
		y += 8;
	y = 3;
	gaugeaux = "AS RC VM SS";
	for x in gaugeaux.split():
		write_str_color(window_information['gauge'], 6, y, " ", 3, 0);
		write_str_color(window_information['gauge'], 6, y+1, x, 3, 0);
		write_str_color(window_information['gauge'], 6, y+3, " ", 3, 0);
		y += 8;

	#Update the whole thing...
	update_panels();
	doupdate();

        #Are we for real??
    	#Our thread that updates all VMSS info (Default Refresh Interval: 5)...
	vmss_monitor_thread(window_information, panel_information, window_continents, panel_continents, demoEnabled);
	endwin();
	return 0;

if (__name__ == "__main__"): #{
        main();
#}
