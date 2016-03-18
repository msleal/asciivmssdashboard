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
#VM
vm_selected = [999999, 999999];
window_vm = [];


#Exec command...
def exec_cmd(acess_token, cap, cmd):
	global subscription_id, rgname, vmssname, vmsku, tier, vm_selected, window_vm;

	#Return codes...
	initerror = 2; syntaxerror = 3; capacityerror = 4;
	execsuccess = 0; execerror = 1;

	#Sanity check on capacity...
	if (cap == "999999"):
		return initerror;
	if not (isinstance(cap, int)):
		return initerror;

	#Syntax check...
	if (len(cmd.split()) != 4 and len(cmd.split()) != 3):
		return syntaxerror;

	counter = 0;
	for c in cmd.split():
		if (counter == 0):
			if (c == "add" or c == "del" or c == "rg" or c == "select"):
				op = c;
			else:
				return syntaxerror;
		if (counter == 1 and c != "vm") and (op == "add" or op == "del" or op == "select"):
			return syntaxerror;
		if (counter == 1 and op == "rg"):
			rgname_new = c;
		if (counter == 2) and (op == "add" or op == "del" or op == "select"): 
			try:
				a = int(c) + 1;
				qtd = int(c);
			#except TypeError:
			except:
				return syntaxerror;
		if (counter == 2 and op == "select"):
			if (int(c) > window_vm.__len__() - 1):
				return syntaxerror;
			vm = int(c);
		if (counter == 2 and op == "rg" and c != "vmss"):
				return syntaxerror;
		if (counter == 3 and op == "rg"):
			vmssname_new = c;
		counter += 1;

	#Execution...
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
			return execsuccess;
		else:
			return execerror;
	elif (op == "select"):
		vm_selected[1] = vm_selected[0];
		vm_selected[0] = vm;
		return execsuccess;
	else:
		#Test to be sure the resource group and vmss provided do exist...
		rgoutput = azurerm.get_vmss(access_token, subscription_id, rgname_new, vmssname_new);
		try:
			test = rgoutput['location'];
			rgname = rgname_new; vmssname = vmssname_new;
			#Just a flag for us to know that we changed the vmss and need to deselect any VM...
			vm_selected[1] = 999998;
			return execsuccess;
		except:
			return execerror;

# thread to loop around monitoring the VM Scale Set state and its VMs
# sleep between loops sets the update frequency
def get_vmss_properties(access_token, run_event, window_information, panel_information, window_continents, panel_continents):
	global vmssProperties, vmssVmProperties, countery, capacity, region, tier, vmsku, vm_selected, window_vm;

	ROOM = 5; DEPLOYED = 0;

	#VM's destination...
	destx = 22; desty = 4; XS =50;
	window_dc = 0;

	#Our window_information arrays...
	panel_vm = []; window_vm = [];

	#Home...
	ourhome = platform.system();

	#Our thread loop...
	while run_event.is_set():
		try:
			ourtime = time.strftime("%H:%M:%S");
			wmove(window_information['status'], 1, 13); waddstr(window_information['status'], ourtime);

			#Create Forms...
			create_forms(window_information['vmss_info'], window_information['system'], window_information['status'], window_information['vm']);

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
					new_window_dc = mark_vmss_dc(continent_old_location, window_continents[continent_old_location], old_location, window_continents[continent_location], location, window_dc);
					window_dc = new_window_dc;
			else:
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

			#All VMs are created in the following coordinates...
			init_coords = (XS, 4);
			vmssVmProperties = [];
			qtd = vmssvms['value'].__len__();
			step = qtd / 10;
			if (step < 1): step = 1;	
			#We take more time on our VM effect depending on how many VMs we are talking about...
			if (qtd < 20):
				ts = 0.01;
			elif (qtd < 60):
				ts = 0.003;
			else:
				ts = 0.0005;

			#Fill Sys info...
			wmove(window_information['system'], 1, 22); waddstr(window_information['system'], offer);
			wmove(window_information['system'], 2, 22); waddstr(window_information['system'], sku);
			wmove(window_information['system'], 3, 22); waddstr(window_information['system'], qtd);

			cor=6;
			if (provisioningState == "Updating"): cor=7;
			wmove(window_information['system'], 4, 22); waddstr(window_information['system'], provisioningState, color_pair(cor));

			counter = 1;
			#Loop each VM...
			for vm in vmssvms['value']:
				vmsel = 0;
				instanceId = vm['instanceId'];
				vmName = vm['name'];
				provisioningState = vm['properties']['provisioningState'];
				vmssVmProperties.append([instanceId, vmName, provisioningState]);
				if (counter > DEPLOYED):
					window_vm.append(DEPLOYED); panel_vm.append(DEPLOYED);
					window_vm[DEPLOYED] = create_window(3, 4, init_coords[0], init_coords[1]);
					panel_vm[DEPLOYED] = new_panel(window_vm[DEPLOYED]);
					box(window_vm[DEPLOYED]);
					#Creation of the VM, in this case we never have a VM selected...
					draw_vm(DEPLOYED, window_vm[DEPLOYED], provisioningState, vmsel);
					if countery < 10:
						 countery += 1;
					else:
						destx += 3; desty = 4; countery = 1;
					vm_animation(panel_vm[DEPLOYED], init_coords, destx, desty, 1, ts);
					desty += ROOM;
					DEPLOYED += 1;
					update_panels();
					doupdate();
				else:
					#Remove the old mark...
					if (vm_selected[1] == (counter -1) and vm_selected[1] != 999999 and vm_selected[1] != vm_selected[0]):
						box(window_vm[vm_selected[1]]);
					if (vm_selected[0] == (counter -1) and vm_selected[1] != 999998 and vm_selected[0] != vm_selected[1]):
						vmsel = 1;
						#show_panel(panel_information['vm']);
					if (vm_selected[0] == (counter -1) and vm_selected[1] == 999998):
						vmsel = 0;
						#hide_panel(panel_information['vm']);
						vm_selected = [999999, 999999];
					draw_vm((counter - 1), window_vm[(counter - 1)], provisioningState, vmsel);
					if (vm_selected[0] == (counter -1) and vm_selected[0] != 999999 and vm_selected[1] != 999998):
						wmove(window_information['vm'], 1, 12); waddstr(window_information['vm'], vmName);
						cor=7;
						if (provisioningState == "Succeeded"): cor=6;
						wmove(window_information['vm'], 2, 12); waddstr(window_information['vm'], provisioningState, color_pair(cor));

				counter += 1;
				do_update_bar(window_information['status'], step, 0);
				step += step;
			#Last mile...
			do_update_bar(window_information['status'], step, 1);

			#Remove destroyed VMs...
			while (DEPLOYED >= counter):
				lastvm = window_vm.__len__() - 1;	
				vm_coords = getbegyx(window_vm[lastvm]);
				vm_animation(panel_vm[lastvm], vm_coords, init_coords[0], init_coords[1], 0, ts);
				if (countery > 0):
					desty -= ROOM; countery -= 1;
				elif (destx > 22):
					destx -= 3; desty = 49; countery = 9;
				#Free up some memory...
				del_panel(panel_vm[lastvm]); delwin(window_vm[lastvm]);
				wobj = panel_vm[lastvm]; panel_vm.remove(wobj);
				wobj = window_vm[lastvm]; window_vm.remove(wobj);
				DEPLOYED -= 1;
				update_panels();
				doupdate();
			# sleep before before each loop to avoid throttling...
			ourtime = time.strftime("%H:%M:%S");
			do_update_bar(window_information['status'], step, 1);
			wmove(window_information['status'], 1, 13); waddstr(window_information['status'], ourtime);
			wmove(window_information['status'], 1, 22); waddstr(window_information['status'], "     OK     ");
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
	global key, rgname, vmssname, vm_selected;
	
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
			draw_prompt_corners(window_information['cmd']);
			draw_line(window_information['cmd'], 1, 122, 2, ACS_VLINE);

			cor=6;
			if (command == "help"):
				if (win_help):
					hide_panel(panel_information['help']);
					win_help = 0;
				else:
					show_panel(panel_information['help']);
					win_help = 1;
			elif (command == "deselect"):
				vm_selected[1] = 999998;
			else:
				cmd_status = exec_cmd(access_token, capacity, command);
				if (cmd_status == 1): cor = 8;
				if (cmd_status == 2): cor = 4;
				if (cmd_status == 3): cor = 7;
				if (cmd_status == 4): cor = 3;
			wmove(window_information['cmd'], 1, 125); waddstr(window_information['cmd'], "E", color_pair(cor) + A_BOLD);
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
		window_exit = create_window(8, 56, 22, 87);
		box(window_exit);
		panel_exit = new_panel(window_exit);
		top_panel(panel_exit);
		wmove(window_exit, 3, 5); waddstr(window_exit, "Waiting for Console Update threads to close...", color_pair(4) + A_BOLD);
		update_panels();
		doupdate();
		run_event.clear()
		vmss_thread.join()
		cmd_thread.join()
		wmove(window_exit, 3, 5); wclrtoeol(window_exit);
		box(window_exit);
		wmove(window_exit, 3, 6); waddstr(window_exit, "Console Update threads successfully closed.", color_pair(4) + A_BOLD);
		update_panels();
		doupdate();
