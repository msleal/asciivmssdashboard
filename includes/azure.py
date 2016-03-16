#!/usr/bin/env python
# Azure routines...
# Based and inspired by the tool VMSSDashboard from Guy Bowerman - Copyright (c) 2016.

"""
Copyright (c) 2016, Marcelo Leal
Description: The power is in the terminal...
License: MIT (see LICENSE.txt file for details)
"""

import sys
import time
import json
import azurerm
import threading
import platform
from unicurses import *
from windows import *
from datacenters import *

# Load Azure app defaults
try:
	with open('vmssconfig.json') as configFile:
		configData = json.load(configFile)
except FileNotFoundError:
	print("Error: Expecting vmssconfig.json in current folder")
	sys.exit()

#Read the config params...
tenant_id = configData['tenantId']
app_id = configData['appId']
app_secret = configData['appSecret']
subscription_id = configData['subscriptionId']
# this is the resource group, VM Scale Set to monitor..
rgname = configData['resourceGroup']
vmssname = configData['vmssName']
vmsku = configData['vmSku']
tier = configData['tier']
interval = configData['interval']
configFile.close()

#Region...
region=""
countery=0

#Just a high number, so we can test and see if it was not updated yet...
capacity=999999

#Exec command...
def exec_cmd(acess_token, cap, cmd):
	global subscription_id, rgname, vmssname, vmsku, tier;

	counter = 0;
	#Return codes...
	initerror = 2; syntaxerror = 3; capacityerror = 4;
	httpsuccess = 0; httperror = 1;

	#Sanity check on capacity...
	if (cap == "999999"):
		return initerror;
	if not (isinstance(cap, int)):
		return initerror;

	#Syntax check...
	if (len(cmd.split()) != 4 and len(cmd.split()) != 3):
		return syntaxerror;
	for c in cmd.split():
		if (counter == 0):
			if (c == "add" or c == "del" or c == "rg"):
				op = c;
			else:
				return syntaxerror;
		if (counter == 1 and c != "vm") and (op == "add" or op == "del"):
			return syntaxerror;
		if (counter == 2) and (op == "add" or op == "del"): 
			try:
				a = int(c) + 1;
				qtd = int(c);
			#except TypeError:
			except:
				return syntaxerror;
		if (counter == 2 and op == "rg") and (c != "vmss"):
				return syntaxerror;
		counter += 1;

	if (op == "add" or op == "del"):
		if (qtd > 9): 
			return capacityerror;
		#Scale-in or Scale-out...
		if (op == "add"):
   			newCapacity = cap + int(c);
		else:
   			newCapacity = cap - int(c);
		#Ok, everything seems fine, let's do it...
		#Change the VM scale set capacity by 'qtd' (can be positive or negative for scale-out/in)
		scaleoutput = azurerm.scale_vmss(access_token, subscription_id, rgname, vmssname, vmsku, tier, newCapacity);
		if (scaleoutput.status_code == 200):
			return httpsuccess;
		else:
			return httperror;
	else:
		x = 0;
		for c in cmd.split():
			if (x == 1):
				rgname_new = c;
			if (x == 3):
				vmssname_new = c;
			x += 1;
		#Test to be sure the resource group and vmss provided do exist...
		rgoutput = azurerm.get_vmss(access_token, subscription_id, rgname_new, vmssname_new);
		try:
			test = rgoutput['location'];
			rgname = rgname_new; vmssname = vmssname_new;
			return httpsuccess;
		except:
			return httperror;

def create_forms(window_info, window_sys, window_status):
	a = 2; 

	#Let's handle the status wwindow here...
	wmove(window_status, 1, 12); wclrtoeol(window_status);
	box(window_status);
	wmove(window_status, 0, 13); waddstr(window_status, " STATUS ", color_pair(3));
	wmove(window_status, 1, 22); waddstr(window_status, "|");

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

# thread to loop around monitoring the VM Scale Set state and its VMs
# sleep between loops sets the update frequency
def get_vmss_properties(access_token, run_event, window_information, panel_information, window_continents, panel_continents):
	global vmssProperties, vmssVmProperties, countery, capacity, region, tier, vmsku;

	ROOM = 5; DEPLOYED = 0;
	#VM's destination...
	destx = 29; desty = 3;
	#Our window_information arrays...
	window_computer = []; panel_computer = []; window_vm = [];
	window_dc = 0;
	ourhome = platform.system();

	#Our thread loop...
	keeppushing = True;
	#while (keeppushing):
	while run_event.is_set():
		try:
			ourtime = time.strftime("%H:%M:%S");
			wmove(window_information['status'], 1, 2); waddstr(window_information['status'], ourtime);

			#Create Forms...
			create_forms(window_information['vmss_info'], window_information['system'], window_information['status']);

			# get VMSS details
			vmssget = azurerm.get_vmss(access_token, subscription_id, rgname, vmssname);

			#Mark Datacenter where VMSS is deployed...
			old_location = region;
			if (old_location != ""):
				continent_old_location = get_continent_dc(old_location);

			location = vmssget['location'];
			region = location;
			continent_location = get_continent_dc(location);

			if (old_location != ""):
				if (old_location != location):
					#Now switch the datacenter mark on map...
					#For now, no maps or region locations on Windows. The next call throws an exception.
					new_window_dc = mark_vmss_dc(continent_old_location, window_continents[continent_old_location], old_location, window_continents[continent_location], location, window_dc);
					window_dc = new_window_dc;
			else:
				#For now, no maps or region locations on Windows. The next call throws an exception.
				new_window_dc = mark_vmss_dc(continent_location, window_continents[continent_location], location, window_continents[continent_location], location, window_dc);
				window_dc = new_window_dc;

			name = vmssget['name']
			capacity = vmssget['sku']['capacity']
			tier = vmssget['sku']['tier']
			vmsku = vmssget['sku']['name']
			offer = vmssget['properties']['virtualMachineProfile']['storageProfile']['imageReference']['offer']
			sku = vmssget['properties']['virtualMachineProfile']['storageProfile']['imageReference']['sku']
			provisioningState = vmssget['properties']['provisioningState']

			# get public ip address for resource group (don't need to query this in a loop)
			# this gets the first ip address - modify this if your RG has multiple ips
			ips = azurerm.list_public_ips(access_token, subscription_id, rgname);
			dns = ips['value'][0]['properties']['dnsSettings']['fqdn'];
			ipaddr = ips['value'][0]['properties']['ipAddress'];

			#Add General info...
			wmove(window_information['vmss_info'], 2, 14); waddstr(window_information['vmss_info'], rgname.upper());
			wmove(window_information['vmss_info'], 2, 48); waddstr(window_information['vmss_info'], vmssname.upper());
			wmove(window_information['vmss_info'], 2, 76); waddstr(window_information['vmss_info'], tier.upper());
			wmove(window_information['vmss_info'], 3, 14); waddstr(window_information['vmss_info'], ipaddr);
			wmove(window_information['vmss_info'], 3, 37); waddstr(window_information['vmss_info'], location.upper());
			wmove(window_information['vmss_info'], 3, 76); waddstr(window_information['vmss_info'], vmsku);
			wmove(window_information['vmss_info'], 4, 14); waddstr(window_information['vmss_info'], dns);
			wmove(window_information['vmss_info'], 4, 79); waddstr(window_information['vmss_info'], capacity);

			vmssProperties = [name, capacity, location, rgname, offer, sku, provisioningState, dns, ipaddr]
			vmssvms = azurerm.list_vmss_vms(access_token, subscription_id, rgname, vmssname)

			#VMSS Virtual Machines icons...
			counter = 1;
			#All VMs are created in the following coordinates...
			x = 41; y = 3; init_coords = (x, y);
			vmssVmProperties = [];
			qtd = vmssvms['value'].__len__();
			step = qtd / 10;
			if (step < 1): step = 1;	

			#Fill Sys info...
			wmove(window_information['system'], 1, 22); waddstr(window_information['system'], offer);
			wmove(window_information['system'], 2, 22); waddstr(window_information['system'], sku);
			wmove(window_information['system'], 3, 22); waddstr(window_information['system'], qtd);

			cor=6;
			if (provisioningState == "Updating"): cor=7;
			wmove(window_information['system'], 4, 22); waddstr(window_information['system'], provisioningState, color_pair(cor));

			for vm in vmssvms['value']:
				instanceId = vm['instanceId'];
				vmName = vm['name'];
				provisioningState = vm['properties']['provisioningState'];
				vmssVmProperties.append([instanceId, vmName, provisioningState]);
				if (counter > DEPLOYED):
					window_computer.append(DEPLOYED); panel_computer.append(DEPLOYED); window_vm.append(DEPLOYED);
					window_computer[DEPLOYED] = create_window(3, 6, x, y);
					panel_computer[DEPLOYED] = new_panel(window_computer[DEPLOYED]);
					window_vm[DEPLOYED] = derwin(window_computer[DEPLOYED], 3, 4, 0, 1,);
					box(window_vm[DEPLOYED]);
					draw_vm(window_computer[DEPLOYED], provisioningState);
					if countery < 8:
						vm_animation(panel_computer[DEPLOYED], init_coords, destx, desty);
						wrefresh(window_computer[DEPLOYED]);
						desty += ROOM; countery += 1;
					else:
						destx += 3; desty = 3; countery = 1;
						vm_animation(panel_computer[DEPLOYED], init_coords, destx, desty);
						desty += ROOM;
					update_panels();
					doupdate();
					DEPLOYED += 1;
				else:
					draw_vm(window_computer[counter - 1], provisioningState);
				counter += 1;
				do_update_bar(window_information['status'], step, 0);
				step += step;
			do_update_bar(window_information['status'], step, 1);

			#Remove destroyed VMs...
			while (DEPLOYED >= counter):
				lastvm = window_vm.__len__() - 1;	
				vm_coords = getbegyx(window_computer[lastvm]);
				vm_deletion(panel_computer[lastvm], vm_coords, init_coords[0], init_coords[1]);
				if (countery > 0):
					desty -= ROOM; countery -= 1;
				elif (destx > 29):
					destx -= 3; desty = 38; countery = 7;
				#Free up some memory...
				delwin(window_vm[lastvm]); del_panel(panel_computer[lastvm]); delwin(window_computer[lastvm]);
				wobj = window_vm[lastvm]; window_vm.remove(wobj);
				wobj = panel_computer[lastvm]; panel_computer.remove(wobj);
				wobj = window_computer[lastvm]; window_computer.remove(wobj);
				DEPLOYED -= 1;
				update_panels();
				doupdate();
			# sleep before before each loop to avoid throttling...
			ourtime = time.strftime("%H:%M:%S");
			do_update_bar(window_information['status'], step, 1);
			wmove(window_information['status'], 1, 2); waddstr(window_information['status'], ourtime);
			wmove(window_information['status'], 1, 12); waddstr(window_information['status'], "    OK    ");
			update_panels();
			doupdate();

			time.sleep(interval);
		except:
			# this catches errors like throttling from the Azure server
			f = open('error.log', 'w')
			if len(vmssvms) > 0:
				for p in vmssvms.items():
					f.write("%s:%s\n" % p)
			f.close()
			## break out of loop when an error is encountered
			break

def get_cmd(access_token, run_event, window_information, panel_information):
	global key, rgname, vmssname;
	
	win_help = 0;
	lock = threading.Lock()
	while run_event.is_set():
		with lock:
			key = getch();
		if (key == 58):
			curs_set(True);
			echo();
			#Clear the old command from our prompt line...
			wmove(window_information['cmd'], 1, 5); wclrtoeol(window_information['cmd']);
			box(window_information['cmd']);
			draw_prompt_corners(window_information['cmd']);
			wmove(window_information['cmd'], 0, 5); waddstr(window_information['cmd'], " PROMPT ", color_pair(3));
			
			#Read the command...
			command = mvwgetstr(window_information['cmd'], 1, 5);
			curs_set(False);
			noecho();
			cor=6;
			if (command == "help"):
				if (win_help):
					hide_panel(panel_information['help']);
					win_help = 0;
				else:
					show_panel(panel_information['help']);
					win_help = 1;
			else:
				cmd_status = exec_cmd(access_token, capacity, command);
				if (cmd_status == 1): cor = 8;
				if (cmd_status == 2): cor = 4;
				if (cmd_status == 3): cor = 7;
				if (cmd_status == 4): cor = 3;
			draw_prompt_corners(window_information['cmd']);
			draw_line(window_information['cmd'], 1, 67, 2, ACS_VLINE);
			wmove(window_information['cmd'], 1, 65); waddstr(window_information['cmd'], "E", color_pair(cor) + A_BOLD);
			update_panels();
			doupdate();

def vmss_monitor_thread(window_information, panel_information, window_continents, panel_continents):
	global access_token;

	run_event = threading.Event()
	run_event.set()

	# start a timer in order to refresh the access token in 10 minutes
	start_time = time.time();

	# get an access token for Azure authentication
	access_token = azurerm.get_access_token(str(tenant_id), str(app_id), str(app_secret));

	# start a VMSS monitoring thread
	vmss_thread = threading.Thread(target=get_vmss_properties, args=(access_token, run_event, window_information, panel_information, window_continents, panel_continents))
	vmss_thread.start()

	time.sleep(.2);

	# start a CMD Interpreter thread
	cmd_thread = threading.Thread(target=get_cmd, args=(access_token, run_event, window_information, panel_information))
	cmd_thread.start()

	try:
        	while 1:
            		time.sleep(.1)
	except KeyboardInterrupt:
		window_exit = create_window(7, 55, 22, 75);
		box(window_exit);
		panel_exit = new_panel(window_exit);
		top_panel(panel_exit);
		wmove(window_exit, 3, 5); waddstr(window_exit, "Waiting for Console Update threads to close...", color_pair(4) + A_BOLD);
		update_panels();
		doupdate();
		run_event.clear()
		vmss_thread.join()
		cmd_thread.join()
		wmove(window_exit, 3, 5); whline(window_exit, "\b", 47);
		wmove(window_exit, 3, 6); waddstr(window_exit, "Console Update threads successfully closed.", color_pair(4) + A_BOLD);
		update_panels();
		doupdate();
