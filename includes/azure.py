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
import logging
import requests
from logtail import *
from unicurses import *
from windows import *
from datacenters import *

# Load Azure app defaults
try:
	with open('asciivmssdashboard.json') as configFile:
		configData = json.load(configFile)
except FileNotFoundError:
	print("Error: Expecting asciivmssdashboard.json in current folder")
	sys.exit()

try:
	tenant_id = configData['tenantId']
	app_id = configData['appId']
	app_secret = configData['appSecret']
	subscription_id = configData['subscriptionId']
	# this is the resource group, VM Scale Set to monitor..
	rgname = configData['resourceGroup']
	vmssname = configData['vmssName']
	vmsku = configData['vmSku']
	tier = configData['tier']
	purgeLog = configData['purgeLog']
	logName = configData['logName']
	logLevel = configData['logLevel']
	interval = configData['interval']
	insightsAppId = configData['insightsAppId']
	insightsKey = configData['insightsKey']
	insightsUrl = configData['insightsUrl']
	insightsOneEnabled = configData['insightsOneEnabled']
	insightsOneUrl = configData['insightsOneUrl']
	insightsOneMetric = configData['insightsOneMetric']
	insightsOneTitle = configData['insightsOneTitle']
	insightsTwoEnabled = configData['insightsTwoEnabled']
	insightsTwoUrl = configData['insightsTwoUrl']
	insightsTwoMetric = configData['insightsTwoMetric']
	insightsTwoTitle = configData['insightsTwoTitle']
	insightsInterval = configData['insightsInterval']
	configFile.close()
except:
	print("Missing configuration parameter. You can disable some features, but the config option must be present.")
	print("Use the asciivmssdashboard.json.tmpl file as a template to fill in your custom values...")
	configFile.close()
	sys.exit()

#Region...
region=""

#Just a high number, so we can test and see if it was not updated yet...
capacity=999999
#VM
vm_selected = [999999, 999999];
insights_flag = 0;

#Window VM
countery=0
window_vm = []; panel_vm = []; instances_deployed = [];
vm_details = ""; vm_nic = "";
page = 1;

#Flag to quit...
quit = 0;

#Remove old log file if requested (default behavior)...
if (purgeLog.lower() == "yes"):
	if (os.path.isfile(logName)):
		os.remove(logName);

#DEMO Assets...
VMSSGET_DEMO = json.dumps({"name": "dashdemo", "id": "/subscriptions/99999999-aaaa-bbbb-cccc-888888888888/resourceGroups/dashdemo/providers/Microsoft.Compute/virtualMachineScaleSets/dashdemo", "type": "Microsoft.Compute/virtualMachineScaleSets", "location": "brazilsouth", "sku": {"name": "Standard_A2", "tier": "Standard", "capacity": 1}, "properties": {"singlePlacementGroup": True, "upgradePolicy": {"mode": "Manual", "automaticOSUpgrade": False}, "virtualMachineProfile": {"osProfile": {"computerNamePrefix": "dashdemo", "adminUsername": "blackpanther", "linuxConfiguration": {"disablePasswordAuthentication": False}, "secrets": []}, "storageProfile": {"osDisk": {"vhdContainers": ["https://ababababababcdashdemosa.blob.core.windows.net/dashdemovhd", "https://ababababababcdashdemosa.blob.core.windows.net/dashdemovhd", "https://8765432123456dashdemosa.blob.core.windows.net/dashdemovhd", "https://ababababababcdashdemosa.blob.core.windows.net/dashdemovhd", "https://ababababababcdashdemosa.blob.core.windows.net/dashdemovhd"], "name": "dashdemoosdisk", "createOption": "FromImage", "caching": "ReadOnly"}, "imageReference": {"publisher": "Canonical", "offer": "UbuntuServer", "sku": "16.04.0-LTS", "version": "latest"}}, "networkProfile": {"networkInterfaceConfigurations": [{"name": "dashdemonic", "properties": {"primary": True, "ipConfigurations": [{"name": "dashdemoipconfig", "properties": {"subnet": {"id": "/subscriptions/99999999-aaaa-bbbb-cccc-888888888888/resourceGroups/VMSSDASH/providers/Microsoft.Network/virtualNetworks/dashdemovnet/subnets/dashdemosubnet"}}}]}}]}}, "provisioningState": "Succeeded", "overprovision": False, "uniqueId": "88888888-cccc-bbbb-aaaa-999999999999"}})
 
NET_DEMO = json.dumps({"value": [{"name": "dashdemopip", "id": "/subscriptions/99999999-aaaa-bbbb-cccc-888888888888/resourceGroups/VMSSDASH/providers/Microsoft.Network/publicIPAddresses/dashdemopip", "etag": "W/\'77777777-cccc-aaaa-bbbb-666666666666\'", "location": "brazilsouth", "properties": {"provisioningState": "Succeeded", "resourceGuid": "55555555-vvvv-nnnn-rrrr-444444444444", "ipAddress": "999.999.999.999", "publicIPAddressVersion": "IPv4", "publicIPAllocationMethod": "Dynamic", "idleTimeoutInMinutes": 4, "dnsSettings": {"domainNameLabel": "dashdemo", "fqdn": "dashdemo.brazilsouth.cloudapp.azure.com"}, "ipTags": [], "ipConfiguration": {"id": "/subscriptions/99999999-aaaa-bbbb-cccc-888888888888/resourceGroups/VMSSDASH/providers/Microsoft.Network/networkInterfaces/dashdemojboxnic/ipConfigurations/dashdemojboxipconfig"}}, "type": "Microsoft.Network/publicIPAddresses", "sku": {"name": "Basic"}}]})

QUOTA_DEMO = json.dumps({u"value": [{u"currentValue": 0, u"limit": 2000, u"name": {u"localizedValue": u"Availability Sets", u"value": u"availabilitySets"}, u"unit": u"Count"}, {u"currentValue": 4, u"limit": 1000, u"name": {u"localizedValue": u"Total Regional vCPUs", u"value": u"cores"}, u"unit": u"Count"}, {u"currentValue": 2, u"limit": 25000, u"name": {u"localizedValue": u"Virtual Machines", u"value": u"virtualMachines"}, u"unit": u"Count"}, {u"currentValue": 1, u"limit": 2000, u"name": {u"localizedValue": u"Virtual Machine Scale Sets", u"value": u"virtualMachineScaleSets"}, u"unit": u"Count"}, {u"currentValue": 4, u"limit": 1000, u"name": {u"localizedValue": u"Standard A0-A7 Family vCPUs", u"value": u"standardA0_A7Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 100, u"name": {u"localizedValue": u"Basic A Family vCPUs", u"value": u"basicAFamily"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 100, u"name": {u"localizedValue": u"Standard A8-A11 Family vCPUs", u"value": u"standardA8_A11Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 100, u"name": {u"localizedValue": u"Standard D Family vCPUs", u"value": u"standardDFamily"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 100, u"name": {u"localizedValue": u"Standard Dv2 Family vCPUs", u"value": u"standardDv2Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 100, u"name": {u"localizedValue": u"Standard DS Family vCPUs", u"value": u"standardDSFamily"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 100, u"name": {u"localizedValue": u"Standard DSv2 Family vCPUs", u"value": u"standardDSv2Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 100, u"name": {u"localizedValue": u"Standard G Family vCPUs", u"value": u"standardGFamily"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 100, u"name": {u"localizedValue": u"Standard GS Family vCPUs", u"value": u"standardGSFamily"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 100, u"name": {u"localizedValue": u"Standard F Family vCPUs", u"value": u"standardFFamily"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 100, u"name": {u"localizedValue": u"Standard FS Family vCPUs", u"value": u"standardFSFamily"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 24, u"name": {u"localizedValue": u"Standard NV Family vCPUs", u"value": u"standardNVFamily"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 48, u"name": {u"localizedValue": u"Standard NC Family vCPUs", u"value": u"standardNCFamily"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 8, u"name": {u"localizedValue": u"Standard H Family vCPUs", u"value": u"standardHFamily"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 100, u"name": {u"localizedValue": u"Standard Av2 Family vCPUs", u"value": u"standardAv2Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 100, u"name": {u"localizedValue": u"Standard LS Family vCPUs", u"value": u"standardLSFamily"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 100, u"name": {u"localizedValue": u"Standard Dv2 Promo Family vCPUs", u"value": u"standardDv2PromoFamily"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 100, u"name": {u"localizedValue": u"Standard DSv2 Promo Family vCPUs", u"value": u"standardDSv2PromoFamily"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 0, u"name": {u"localizedValue": u"Standard MS Family vCPUs", u"value": u"standardMSFamily"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 100, u"name": {u"localizedValue": u"Standard Dv3 Family vCPUs", u"value": u"standardDv3Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 100, u"name": {u"localizedValue": u"Standard DSv3 Family vCPUs", u"value": u"standardDSv3Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 100, u"name": {u"localizedValue": u"Standard Ev3 Family vCPUs", u"value": u"standardEv3Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 100, u"name": {u"localizedValue": u"Standard ESv3 Family vCPUs", u"value": u"standardESv3Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 100, u"name": {u"localizedValue": u"Standard BS Family vCPUs", u"value": u"standardBSFamily"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 100, u"name": {u"localizedValue": u"Standard FSv2 Family vCPUs", u"value": u"standardFSv2Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 0, u"name": {u"localizedValue": u"Standard NDS Family vCPUs", u"value": u"standardNDSFamily"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 0, u"name": {u"localizedValue": u"Standard NCSv2 Family vCPUs", u"value": u"standardNCSv2Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 0, u"name": {u"localizedValue": u"Standard NCSv3 Family vCPUs", u"value": u"standardNCSv3Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 100, u"name": {u"localizedValue": u"Standard LSv2 Family vCPUs", u"value": u"standardLSv2Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 6, u"name": {u"localizedValue": u"Standard PBS Family vCPUs", u"value": u"standardPBSFamily"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 100, u"name": {u"localizedValue": u"Standard EIv3 Family vCPUs", u"value": u"standardEIv3Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 100, u"name": {u"localizedValue": u"Standard EISv3 Family vCPUs", u"value": u"standardEISv3Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 8, u"name": {u"localizedValue": u"Standard DCS Family vCPUs", u"value": u"standardDCSFamily"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 0, u"name": {u"localizedValue": u"Standard NVSv2 Family vCPUs", u"value": u"standardNVSv2Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 0, u"name": {u"localizedValue": u"Standard MSv2 Family vCPUs", u"value": u"standardMSv2Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 0, u"name": {u"localizedValue": u"Standard HBS Family vCPUs", u"value": u"standardHBSFamily"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 0, u"name": {u"localizedValue": u"Standard HCS Family vCPUs", u"value": u"standardHCSFamily"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 0, u"name": {u"localizedValue": u"Standard NVSv3 Family vCPUs", u"value": u"standardNVSv3Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 24, u"name": {u"localizedValue": u"Standard NV Promo Family vCPUs", u"value": u"standardNVPromoFamily"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 48, u"name": {u"localizedValue": u"Standard NC Promo Family vCPUs", u"value": u"standardNCPromoFamily"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 8, u"name": {u"localizedValue": u"Standard H Promo Family vCPUs", u"value": u"standardHPromoFamily"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 0, u"name": {u"localizedValue": u"Standard DAv4 Family vCPUs", u"value": u"standardDAv4Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 0, u"name": {u"localizedValue": u"Standard DASv4 Family vCPUs", u"value": u"standardDASv4Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 0, u"name": {u"localizedValue": u"Standard EAv4 Family vCPUs", u"value": u"standardEAv4Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 0, u"name": {u"localizedValue": u"Standard EASv4 Family vCPUs", u"value": u"standardEASv4Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 0, u"name": {u"localizedValue": u"Standard NDSv3 Family vCPUs", u"value": u"standardNDSv3Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 8, u"name": {u"localizedValue": u"Standard DCSv2 Family vCPUs", u"value": u"standardDCSv2Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 0, u"name": {u"localizedValue": u"Standard NVSv4 Family vCPUs", u"value": u"standardNVSv4Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 0, u"name": {u"localizedValue": u"Standard NDSv2 Family vCPUs", u"value": u"standardNDSv2Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 0, u"name": {u"localizedValue": u"Standard NPS Family vCPUs", u"value": u"standardNPSFamily"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 0, u"name": {u"localizedValue": u"Standard HBrsv2 Family vCPUs", u"value": u"standardHBrsv2Family"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 50000, u"name": {u"localizedValue": u"Standard Storage Managed Disks", u"value": u"StandardDiskCount"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 50000, u"name": {u"localizedValue": u"Premium Storage Managed Disks", u"value": u"PremiumDiskCount"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 50000, u"name": {u"localizedValue": u"StandardSSDStorageDisks", u"value": u"StandardSSDDiskCount"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 1000, u"name": {u"localizedValue": u"UltraSSDStorageDisks", u"value": u"UltraSSDDiskCount"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 50000, u"name": {u"localizedValue": u"StandardStorageSnapshots", u"value": u"StandardSnapshotCount"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 50000, u"name": {u"localizedValue": u"PremiumStorageSnapshots", u"value": u"PremiumSnapshotCount"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 50000, u"name": {u"localizedValue": u"ZrsStorageSnapshots", u"value": u"ZRSSnapshotCount"}, u"unit": u"Count"}, {u"currentValue": 0, u"limit": 16384, u"name": {u"localizedValue": u"UltraSSDTotalSizeInGB", u"value": u"UltraSSDDiskSizeInGB"}, u"unit": u"Count"}]})

VMSSPROPERTIES_DEMO = json.dumps([u"dashdemo", 1, u"brazilsouth", u"dashdemo", u"UbuntuServer", u"16.04.0-LTS", u"Succeeded", u"dashdemo.brazilsouth.cloudapp.azure.com", u"999.999.999.999"])

VMSSVMS_DEMO = json.dumps({"value": [{u"sku": {u"tier": u"Standard", u"name": u"Standard_A2"}, u"name": u"dashdemo_0", u"instanceId": u"0", u"properties": {u"osProfile": {u"adminUsername": u"blackpanther", u"secrets": [], u"computerName": u"dashdemo000000", u"linuxConfiguration": {u"disablePasswordAuthentication": False}}, u"networkProfile": {u"networkInterfaces": [{u"id": u"/subscriptions/99999999-aaaa-bbbb-cccc-888888888888/resourceGroups/dashdemo/providers/Microsoft.Compute/virtualMachineScaleSets/dashdemo/virtualMachines/0/networkInterfaces/dashdemonic"}]}, u"storageProfile": {u"imageReference": {u"sku": u"16.04.0-LTS", u"publisher": u"Canonical", u"version": u"16.04.201903130", u"offer": u"UbuntuServer"}, u"osDisk": {u"osType": u"Linux", u"vhd": {u"uri": u"https://ababababababcdashdemosa.blob.core.windows.net/dashdemovhd/dashdemoosdisk-os-0-1111111111111111111111111111111.vhd"}, u"createOption": u"FromImage", u"name": u"dashdemoosdisk-os-0-11111111111111111111111111111111", u"caching": u"ReadOnly"}}, u"vmId": u"22222222-oooo-uuuu-hhhh-333333333333", u"hardwareProfile": {}, u"latestModelApplied": False, u"provisioningState": u"Succeeded"}, u"location": u"brazilsouth", u"type": u"Microsoft.Compute/virtualMachineScaleSets/virtualMachines", u"id": u"/subscriptions/99999999-aaaa-bbbb-cccc-888888888888/resourceGroups/dashdemo/providers/Microsoft.Compute/virtualMachineScaleSets/dashdemo/virtualMachines/0"}]})

VMDETAILS_DEMO = json.dumps({u"computerName": u"dashdemo000000", u"disks": [{u"name": u"dashdemoosdisk-os-0-11111111112222222222333333333344", u"statuses": [{u"time": u"2019-05-03T20:46:26.6712371+00:00", u"code": u"ProvisioningState/succeeded", u"displayStatus": u"Provisioning succeeded", u"level": u"Info"}]}], u"osName": u"ubuntu", u"platformUpdateDomain": 0, u"vmAgent": {u"vmAgentVersion": u"2.2.46", u"extensionHandlers": [], u"statuses": [{u"time": u"2020-03-18T23:03:37+00:00", u"message": u"Guest Agent is running", u"code": u"ProvisioningState/succeeded", u"displayStatus": u"Ready", u"level": u"Info"}]}, u"platformFaultDomain": 0, u"placementGroupId": u"88888888-4444-4444-4444-121212121212", u"osVersion": u"16.04", u"statuses": [{u"time": u"2019-05-03T20:47:37.2369051+00:00", u"code": u"ProvisioningState/succeeded", u"displayStatus": u"Provisioning succeeded", u"level": u"Info"}, {u"code": u"PowerState/running", u"displayStatus": u"VM running", u"level": u"Info"}]})

VMNIC_DEMO = json.dumps({u"value": [{u"properties": {u"provisioningState": u"Succeeded", u"macAddress": u"00-00-00-00-00-00", u"virtualMachine": {u"id": u"/subscriptions/88888888-4444-4444-4444-121212121212/resourceGroups/vmssdash/providers/Microsoft.Compute/virtualMachineScaleSets/vmssdash/virtualMachines/0"}, u"dnsSettings": {u"internalDomainNameSuffix": u"11111111111111111111111111.nx.internal.cloudapp.net", u"dnsServers": [], u"appliedDnsServers": []}, u"primary": True, u"resourceGuid": u"88888888-4444-4444-4444-121212121212", u"enableIPForwarding": False, u"ipConfigurations": [{u"properties": {u"subnet": {u"id": u"/subscriptions/88888888-4444-4444-4444-121212121212/resourceGroups/DASHDEMO/providers/Microsoft.Network/virtualNetworks/vmssdashvnet/subnets/dashdemosubnet"}, u"primary": True, u"privateIPAddressVersion": u"IPv4", u"privateIPAllocationMethod": u"Dynamic", u"privateIPAddress": u"10.0.0.5", u"provisioningState": u"Succeeded"}, u"etag": u"W/\'88888888-4444-4444-4444-121212121212\'", u"name": u"dashdemoipconfig", u"id": u"/subscriptions/88888888-4444-4444-4444-121212121212/resourceGroups/DASHDEMO/providers/Microsoft.Compute/virtualMachineScaleSets/dashdemo/virtualMachines/0/networkInterfaces/dashdemonic/ipConfigurations/dashdemoipconfig"}], u"enableAcceleratedNetworking": False}, u"etag": u"W/\'88888888-4444-4444-4444-121212121212\'", u"name": u"dashdemonic", u"id": u"/subscriptions/88888888-4444-4444-4444-121212121212/resourceGroups/DASHDEMO/providers/Microsoft.Compute/virtualMachineScaleSets/dashdemo/virtualMachines/0/networkInterfaces/dashdemonic"}]})

#Basic Logging...
#logging.basicConfig(format='%(asctime)s - %(levelname)s:%(message)s', datefmt='%H:%M:%S', level=logLevel, filename=logName)
logging.basicConfig(format='%(asctime)s - %(levelname)s:%(message)s', level=logLevel, filename=logName)

#Exec command...
def exec_cmd(window, access_token, cap, cmd, demo):
	global subscription_id, rgname, vmssname, vmsku, tier, vm_selected, window_vm, panel_vm, vm_details, vm_nic, page, insights_flag;

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
			if (c == "add" or c == "del" or c == "rg" or c == "select" or c == "show"):
				op = c;
			else:
				return syntaxerror;
		if (counter == 1 and op == "show" and c != "page"):
				return syntaxerror;
		if (counter == 1 and c != "vm") and (op == "add" or op == "del" or op == "select"):
			return syntaxerror;
		if (counter == 1 and op == "rg"):
			rgname_new = c;
		if (counter == 2) and (op == "add" or op == "del" or op == "select" or op == "show"): 
			try:
				a = int(c) + 1;
				qtd = int(c);
			except:
				return syntaxerror;
		if (counter == 2 and op == "select"):
			if demo:
                            vm = 0
			else:
				z = 0; ifound = 0;
				while (z < instances_deployed.__len__()):
					if (instances_deployed[z] == int(c)):
						ifound = 1;
						break;
					z += 1;
				if (ifound):
					vm = int(c);
				else:
					return execerror;
		if (counter == 2 and op == "rg" and c != "vmss"):
				return syntaxerror;
		if (counter == 2 and op == "show"):
			try:
				a = int(c) + 1;
				if (int(c) == page):
					return execsuccess; 
				if (int(c) > 1):
					b = ((window_vm.__len__() / (int(c) - 1)));
					if (b <= 100 or (int(c)) <= 0):
						return syntaxerror;
					else:
						page_new = int(c);
				elif (int(c) == 1):
						page_new = int(c);
				else:
						return syntaxerror;
			except:
				return syntaxerror;
		if (counter == 3 and op == "rg"):
			vmssname_new = c;
		counter += 1;

	#Execution...
	if (op == "add" or op == "del"):
		if (qtd > 99): 
			return capacityerror;
		#Scale-in or Scale-out...
		if (op == "add"):
   			newCapacity = cap + int(c);
		else:
   			newCapacity = cap - int(c);
		#Ok, everything seems fine, let's do it...
		#Change the VM scale set capacity by 'qtd' (can be positive or negative for scale-out/in)
		#The interface for scale_vmss changed from 7 to just 5 arguments...
		#scaleoutput = azurerm.scale_vmss(access_token, subscription_id, rgname, vmssname, vmsku, tier, newCapacity);
		scaleoutput = azurerm.scale_vmss(access_token, subscription_id, rgname, vmssname, newCapacity);
		if (scaleoutput.status_code == 200):
			return execsuccess;
		else:
			return execerror;
	elif (op == "select"):
		vm_selected[1] = vm_selected[0];
		vm_selected[0] = vm;
		vm_details_old = vm_details; vm_nic_old = vm_nic;
		if demo:
                    vm_details = json.loads(VMDETAILS_DEMO);
		else:
		    vm_details = azurerm.get_vmss_vm_instance_view(access_token, subscription_id, rgname, vmssname, vm_selected[0]);
		#vm_nic = azurerm.get_vmss_vm_nics(access_token, subscription_id, rgname, vmssname, vm_selected[0]);
		#if (len(vm_details) > 0 and len(vm_nic) > 0):
		if (len(vm_details) > 0):
			return execsuccess;
		else:
			vm_details = vm_details_old;
			vm_nic = vm_nic_old;
			vm_selected[1] = 999998;
			return execerror;
	elif (op == "show"):
		unset_page();
		set_page(window, page_new);
		return execsuccess;
	else:
		#Test to be sure the resource group and vmss provided do exist...
		rgoutput = azurerm.get_vmss(access_token, subscription_id, rgname_new, vmssname_new);
		try:
			test = rgoutput['location'];
			rgname = rgname_new; vmssname = vmssname_new;
			#Just a flag for us to know that we changed the vmss and need to deselect any VM...
			vm_selected[1] = 999998;
			#We need to clear the Insights graph too...
			insights_flag = 1;
			page = 1;
			return execsuccess;
		except:
			return execerror;

def unset_page():
	global page, window_vm, panel_vm;
	old_page = page;

	vmlimit = int(window_vm.__len__());
	blimit = int(int(old_page) * 100);
	b = (blimit - 100);
	while (b < blimit and b < vmlimit):
		hide_panel(panel_vm[b]);
		b += 1;

def set_page(window, page_new):
	global page, window_vm, panel_vm;
	page = page_new;
	snap_page = "%02d" % page_new;

	vmlimit = int(window_vm.__len__());
	blimit = int(int(page) * 100);
	b = (blimit - 100);
	while (b < blimit and b < vmlimit):
		show_panel(panel_vm[b]);
		b += 1;
	write_str(window['virtualmachines'], 31, 45, snap_page);
	update_panels();
	doupdate();

def fill_quota_info(window, quota):
	write_str(window['usage'], 2, 23, quota['value'][0]['currentValue']);
	write_str_color(window['usage'], 2, 29, quota['value'][0]['limit'], 7, 0);
	draw_gauge(window['gaugeas'], quota['value'][0]['currentValue'], quota['value'][0]['limit']);

	write_str(window['usage'], 3, 23, quota['value'][1]['currentValue']);
	write_str_color(window['usage'], 3, 29, quota['value'][1]['limit'], 7, 0);
	draw_gauge(window['gaugerc'], quota['value'][1]['currentValue'], quota['value'][1]['limit']);

	write_str(window['usage'], 4, 23, quota['value'][2]['currentValue']);
	write_str_color(window['usage'], 4, 29, quota['value'][2]['limit'], 7, 0);
	draw_gauge(window['gaugevm'], quota['value'][2]['currentValue'], quota['value'][2]['limit']);

	write_str(window['usage'], 5, 23, quota['value'][3]['currentValue']);
	write_str_color(window['usage'], 5, 29, quota['value'][3]['limit'], 7, 0);
	draw_gauge(window['gaugess'], quota['value'][3]['currentValue'], quota['value'][3]['limit']);

def fill_vmss_info(window, vmssget, net):
	(name, capacity, location, offer, sku, provisioningState, dns, ipaddr) = set_vmss_variables(vmssget, net);

	write_str(window['vmss_info'], 2, 14, rgname.upper());
	write_str(window['vmss_info'], 2, 48, vmssname.upper());
	write_str(window['vmss_info'], 2, 76, tier.upper());
	write_str(window['vmss_info'], 3, 45, location.upper());
	write_str(window['vmss_info'], 3, 76, vmsku);
	write_str(window['vmss_info'], 4, 79, capacity);

	#Sys info...
	write_str(window['system'], 1, 22, offer);
	write_str(window['system'], 2, 22, sku);
	cor=6;
	if (provisioningState == "Updating"): cor=7;
	write_str_color(window['system'], 4, 22, provisioningState, cor, 0);
	write_str(window['vmss_info'], 4, 14, dns);
	write_str(window['vmss_info'], 3, 14, ipaddr);

def update_vm_footer(window, cur_page, tot_pages):
	write_str(window['virtualmachines'], 31, 38, " Page: ");
	write_str(window['virtualmachines'], 31, 45, cur_page);
	write_str(window['virtualmachines'], 31, 47, "/");
	write_str(window['virtualmachines'], 31, 48, tot_pages);
	write_str(window['virtualmachines'], 31, 50, " ");

def fill_vm_details(window, instanceId, vmName, provisioningState):
	global vm_details; 
	write_str(window['vm'], 2, 17, instanceId);
	write_str(window['vm'], 3, 17, vmName);
	cor=7;
	if (provisioningState == "Succeeded"): cor=6;
	write_str_color(window['vm'], 4, 17, provisioningState, cor, 0);
	if (provisioningState == "Succeeded"):
		cdate = vm_details['statuses'][0]['time'];
		vmdate = cdate.split("T")
		vmtime = vmdate[1].split(".")
		write_str(window['vm'], 5, 17, vmdate[0]);
		write_str(window['vm'], 6, 17, vmtime[0]);
		cor=7;
		if (vm_details['statuses'][1]['displayStatus'] == "VM running"): cor=6;
		write_str_color(window['vm'], 7, 17, vm_details['statuses'][1]['displayStatus'], cor, 0);
		write_str(window['vm'], 8, 17, vm_details['platformUpdateDomain']);
		write_str(window['vm'], 9, 17, vm_details['platformFaultDomain']);
		write_str(window['vm'], 11, 12, vm_nic['value'][0]['name']);
		write_str(window['vm'], 12, 12, vm_nic['value'][0]['properties']['macAddress']);
		write_str(window['vm'], 13, 12, vm_nic['value'][0]['properties']['ipConfigurations'][0]['properties']['privateIPAddress']);
		write_str(window['vm'], 14, 12, vm_nic['value'][0]['properties']['ipConfigurations'][0]['properties']['primary']);
		if (vm_details['vmAgent']['statuses'][0]['message'] == "Guest Agent is running"): 
			cor=6;
			agentstatus = "Agent is running";
		elif (vm_details['vmAgent']['statuses'][0]['message'] == "VM Agent is unresponsive."):
			cor=7;
			agentstatus = "Agent is unresponsive";
		else:
			cor=7;
			agentstatus = vm_details['vmAgent']['statuses'][0]['message'];
		write_str(window['vm'], 16, 11, vm_details['vmAgent']['vmAgentVersion']);
		write_str(window['vm'], 17, 11, vm_details['vmAgent']['statuses'][0]['displayStatus']);
		write_str_color(window['vm'], 18, 11, agentstatus, cor, 0);

def deselect_vm(window, panel, instanceId, counter):
	global vm_selected;

	vmsel = 0;
	if (vm_selected[1] == int(instanceId) and vm_selected[1] != vm_selected[0]):
		box(window[int(counter - 1)]);
	if (vm_selected[0] == int(instanceId) and vm_selected[1] != 999998 and vm_selected[0] != vm_selected[1]):
		vmsel = 1;
		show_panel(panel['vm']);
	if (vm_selected[0] == int(instanceId) and vm_selected[1] == 999998):
		vmsel = 0;
		vm_selected = [999999, 999999];
	return (vmsel);

def set_vmss_variables(vmssget, net):
	global vmsku, tier;

	name = vmssget['name']
	capacity = vmssget['sku']['capacity']
	location = vmssget['location'];
	tier = vmssget['sku']['tier']
	vmsku = vmssget['sku']['name']
	offer = vmssget['properties']['virtualMachineProfile']['storageProfile']['imageReference']['offer']
	sku = vmssget['properties']['virtualMachineProfile']['storageProfile']['imageReference']['sku']
	provisioningState = vmssget['properties']['provisioningState']
	dns = net['value'][0]['properties']['dnsSettings']['fqdn'];
	ipaddr = net['value'][0]['properties']['ipAddress'];
	return (name, capacity, location, offer, sku, provisioningState, dns, ipaddr);

# thread to loop around monitoring the VM Scale Set state and its VMs
# sleep between loops sets the update frequency
def get_vmss_properties(access_token, run_event, window_information, panel_information, window_continents, panel_continents, demo):
	global vmssProperties, vmssVmProperties, countery, capacity, region, tier, vmsku, vm_selected, window_vm, panel_vm, instances_deployed, vm_details, vm_nic, page;

	ROOM = 5; DEPLOYED = 0;

	#VM's destination...
	destx = 22; desty = 4; XS =50; YS = 4; init_coords = (XS, YS);
	window_dc = 0;

	#Our window_information arrays...
	panel_vm = []; window_vm = [];

	#Our thread loop...
	while run_event.is_set():
		try:
			#Timestamp...
			ourtime = time.strftime("%H:%M:%S");
			write_str(window_information['status'], 1, 13, ourtime);

			#Clean Forms...
			clean_forms(window_information);

			if demo:
			    #Get DEMO VMSS details
			    vmssget = json.loads(VMSSGET_DEMO);
			    # Get DEMO public ip address for RG (First IP) - modify this if your RG has multiple ips
			    net = json.loads(NET_DEMO);
			else:
			    #Get REAL VMSS details
			    vmssget = azurerm.get_vmss(access_token, subscription_id, rgname, vmssname);
			    # Get public ip address for RG (First IP) - modify this if your RG has multiple ips
			    net = azurerm.list_public_ips(access_token, subscription_id, rgname);

			#Clean Info and Sys Windows...
			clean_infoandsys(window_information);

			#Fill the information...
			fill_vmss_info(window_information, vmssget, net);

			#Set VMSS variables...
			(name, capacity, location, offer, sku, provisioningState, dns, ipaddr) = set_vmss_variables(vmssget, net);

			#Set the current and old location...
			old_location = region;
			if (old_location != ""):
				continent_old_location = get_continent_dc(old_location);

			#New
			region = location;
			continent_location = get_continent_dc(location);

			if demo:
			    #Quota...
			    quota = json.loads(QUOTA_DEMO);
			else:
			    #Quota...
			    quota = azurerm.get_compute_usage(access_token, subscription_id, location);
			fill_quota_info(window_information, quota);

			#Mark Datacenter where VMSS is deployed...
			if (old_location != ""):
				if (old_location != location):
					#Now switch the datacenter mark on map...
					new_window_dc = mark_vmss_dc(continent_old_location, window_continents[continent_old_location], old_location, window_continents[continent_location], location, window_dc);
					window_dc = new_window_dc;
			else:
				new_window_dc = mark_vmss_dc(continent_location, window_continents[continent_location], location, window_continents[continent_location], location, window_dc);
				window_dc = new_window_dc;

			if demo:
			    #Our DEMO arrays...
			    vmssProperties = json.loads(VMSSPROPERTIES_DEMO);
			    vmssvms = json.loads(VMSSVMS_DEMO);
			else:
			    #Our REAL arrays...
			    vmssProperties = [name, capacity, location, rgname, offer, sku, provisioningState, dns, ipaddr];
			    vmssvms = azurerm.list_vmss_vms(access_token, subscription_id, rgname, vmssname);
			vmssVmProperties = [];

			#All VMs are created in the following coordinates...
			qtd = vmssvms['value'].__len__();
			factor = (vmssvms['value'].__len__() / 100);

			write_str(window_information['system'], 3, 22, qtd);

			step = qtd / 10;
			if (step < 1): step = 1;	

			#We take more time on our VM effects depending on how many VMs we are talking about...
			if (qtd < 10): ts = 0.01;
			elif (qtd < 25): ts = 0.002;
			elif (qtd < 50): ts = 0.0002;
			elif (qtd < 101): ts = 0.00002;
			else: ts = 0;

			counter = 1; counter_page = 0; nr_pages = 1;

			snap_page = page;
			page_top = (snap_page * 100);
			page_base = ((snap_page - 1) * 100);

			if (vm_selected[1] == 999998):
				#Clean VM Info...
				clean_vm(window_information);
			#Loop each VM...
			for vm in vmssvms['value']:
				instanceId = vm['instanceId'];
				write_str(window_information['monitor'], 1, 30, instanceId);
				wrefresh(window_information['monitor']);
				vmsel = 0;
				vmName = vm['name'];
				provisioningState = vm['properties']['provisioningState'];
				vmssVmProperties.append([instanceId, vmName, provisioningState]);
				if (counter > DEPLOYED):
					window_vm.append(DEPLOYED); panel_vm.append(DEPLOYED); instances_deployed.append(DEPLOYED);
					instances_deployed[DEPLOYED] = int(instanceId);
					#Prepare the place for the VM icon...
					if countery < 10:
						countery += 1;
					else:
						destx += 3; desty = 4; countery = 1;
					if (counter_page > 99):
						destx = 22; counter_page = 0; nr_pages += 1;
						cur_page = "%02d" % snap_page;
						tot_pages = "%02d" % nr_pages;
						update_vm_footer(window_information, cur_page, tot_pages);
					else:
						counter_page += 1;
					window_vm[DEPLOYED] = create_window(3, 5, init_coords[0], init_coords[1]);
					panel_vm[DEPLOYED] = new_panel(window_vm[DEPLOYED]);
					#Show only VM's that are on the visible window...
					if (page_top > DEPLOYED and DEPLOYED >= page_base):
						show_panel(panel_vm[DEPLOYED]);
					else:
						hide_panel(panel_vm[DEPLOYED]);
					box(window_vm[DEPLOYED]);
					#Creation of the VM icon, in this flow we never have a VM selected...
					draw_vm(int(instanceId), window_vm[DEPLOYED], provisioningState, vmsel);
					vm_animation(panel_vm[DEPLOYED], init_coords, destx, desty, 1, ts);
					desty += ROOM;
					DEPLOYED += 1;
				else:
					instances_deployed[counter - 1] = int(instanceId);
					#Remove the old mark...
					vmsel = deselect_vm(window_vm, panel_information, instanceId, counter);
					#Show only VM's that are on the visible window...
					if (page_top > (counter - 1) and (counter - 1) >= page_base):
						show_panel(panel_vm[counter -1]);
					else:
						hide_panel(panel_vm[counter -1]);
					#Creation of the VM icon...
					draw_vm(int(instanceId), window_vm[counter - 1], provisioningState, vmsel);
					#If a VM is selected, fill the details...
					if (vm_selected[0] == int(instanceId) and vm_selected[1] != 999998):
						if demo:
					            vm_details = json.loads(VMDETAILS_DEMO)
					            vm_nic = json.loads(VMNIC_DEMO)
						else:
						    vm_details = azurerm.get_vmss_vm_instance_view(access_token, subscription_id, rgname, vmssname, vm_selected[0]);
						    vm_nic = azurerm.get_vmss_vm_nics(access_token, subscription_id, rgname, vmssname, vm_selected[0]);
						clean_vm(window_information);
						if (vm_details != "" and vm_nic != ""):
							fill_vm_details(window_information, instanceId, vmName, provisioningState);
				update_panels();
				doupdate();
				counter += 1;
				do_update_bar(window_information['status'], step, 0);
				step += step;
			#Last mile...
			write_str(window_information['monitor'], 1, 30, "Done.");
			do_update_bar(window_information['status'], step, 1);

			#Remove destroyed VMs...
			counter_page = 0;
			if (DEPLOYED >= counter):
				time.sleep(0.5);
				write_str_color(window_information['monitor'], 1, 30, "Removing VM's...", 7, 0);
				wrefresh(window_information['monitor']);
				time.sleep(1);
				clean_monitor_form(window_information);
	
			while (DEPLOYED >= counter):
				write_str(window_information['monitor'], 1, 30, DEPLOYED);
				lastvm = window_vm.__len__() - 1;	
				vm_coords = getbegyx(window_vm[lastvm]);
				vm_animation(panel_vm[lastvm], vm_coords, init_coords[0], init_coords[1], 0, ts);
				if (countery > 0):
					desty -= ROOM; countery -= 1;
				elif (destx > 22):
					destx -= 3; desty = 49; countery = 9;
				if (counter_page > 99):
					destx = 52;
					counter_page = 0;
					nr_pages -= 1;
					tot_pages = "%02d" % nr_pages;
					cur_page = "%02d" % page;
					update_vm_footer(window_information, cur_page, tot_pages);
				else:
					counter_page += 1;
				
				#Clean VM Info...
				if (vm_selected[0] == instances_deployed[lastvm]):
					clean_vm(window_information);
				#Free up some memory...
				del_panel(panel_vm[lastvm]); delwin(window_vm[lastvm]);
				wobj = panel_vm[lastvm]; panel_vm.remove(wobj);
				wobj = window_vm[lastvm]; window_vm.remove(wobj);
				wobj = instances_deployed[lastvm]; instances_deployed.remove(wobj);
				DEPLOYED -= 1;
				update_panels();
				doupdate();
			write_str(window_information['monitor'], 1, 30, "Done.");
			ourtime = time.strftime("%H:%M:%S");
			do_update_bar(window_information['status'], step, 1);
			write_str(window_information['status'], 1, 13, ourtime);
			write_str_color(window_information['status'], 1, 22, "     OK     ", 6, 0);
			update_panels();
			doupdate();
			# sleep before each loop to avoid throttling...
			time.sleep(interval);
		except:
			logging.exception("Getting VMSS Information...")
			write_str(window_information['error'], 1, 24, "Let's sleep for 30 seconds and try to refresh the dashboard again...");
			show_panel(panel_information['error']);
			update_panels();
			doupdate();
			## break out of loop when an error is encountered
			#break
			time.sleep(30);
			hide_panel(panel_information['error']);

def get_cmd(access_token, run_event, window_information, panel_information, demo):
	global key, rgname, vmssname, vm_selected, quit;
	
	win_help = 0; win_log = 0; win_insightsone = 0; win_insightstwo = 0;
	lock = threading.Lock()

	while (run_event.is_set() and quit == 0):
		with lock:
			key = getch();
		if (key == 58):
			curs_set(True);
			echo();
			#Clear the old command from our prompt line...
			wmove(window_information['cmd'], 1, 5); wclrtoeol(window_information['cmd']);
			create_prompt_form(window_information['cmd']);

			#Home...
			ourhome = platform.system();

			#Read the command...
			inputcommand = mvwgetstr(window_information['cmd'], 1, 5);
			if (ourhome == 'Windows'):
				command = inputcommand;
			else:
				command = inputcommand.decode('utf-8');

			curs_set(False);
			noecho();
			create_prompt_form(window_information['cmd']);

			cor=6;
			if (command == "help"):
				if (win_help):
					hide_panel(panel_information['help']);
					win_help = 0;
				else:
					show_panel(panel_information['help']);
					win_help = 1;
			elif (command == "debug"):
				if (win_log and win_insightsone and win_insightstwo):
					hide_panel(panel_information['log']);
					hide_panel(panel_information['insightsone']);
					hide_panel(panel_information['insightstwo']);
					win_log = 0; win_insightsone = 0; win_insightstwo = 0; 
				else:
					show_panel(panel_information['log']);
					show_panel(panel_information['insightsone']);
					show_panel(panel_information['insightstwo']);
					win_log = 1; win_insightsone = 1; win_insightstwo = 1;
			elif (command == "log"):
				if (win_log):
					hide_panel(panel_information['log']);
					win_log = 0;
				else:
					show_panel(panel_information['log']);
					win_log = 1;
			elif (command == "insights"):
				if (win_insightsone and win_insightstwo):
					hide_panel(panel_information['insightsone']);
					hide_panel(panel_information['insightstwo']);
					win_insightsone = 0; win_insightstwo = 0;
				else:
					show_panel(panel_information['insightsone']);
					show_panel(panel_information['insightstwo']);
					win_insightsone = 1; win_insightstwo = 1;
			elif (command == "insights 1"):
				if (win_insightsone):
					hide_panel(panel_information['insightsone']);
					win_insightsone = 0;
				else:
					show_panel(panel_information['insightsone']);
					win_insightsone = 1;
			elif (command == "insights 2"):
				if (win_insightstwo):
					hide_panel(panel_information['insightstwo']);
					win_insightstwo = 0;
				else:
					show_panel(panel_information['insightstwo']);
					win_insightstwo = 1;
			elif (command == "quit" or command == 'exit'):
				quit = 1;
			elif (command == "deselect"):
				vm_selected[1] = 999998;
				hide_panel(panel_information['vm']);
			else:
				cmd_status = exec_cmd(window_information, access_token, capacity, command, demo);
				if (cmd_status == 1): cor = 8;
				if (cmd_status == 2): cor = 4;
				if (cmd_status == 3): cor = 7;
				if (cmd_status == 4): cor = 3;
			write_str_color(window_information['cmd'], 1, 125, "E", cor, 1);
			update_panels();
			doupdate();

def insights_in_window(log, window, run_event):
	global insights_flag, insightsOneUrl, insightsTwoUrl;

	lock = threading.Lock()

	total_values_one = 87; total_values_two = 71;
	#x, y = getmaxyx(window['insightsone']);
	#a, b = getmaxyx(window['insightstwo']);
	values_insightsone = []; values_insightstwo = [];
	index_one = 0; index_two = 0;

	while (run_event.is_set() and quit == 0):
		#Clean the graph area...
		flag = 0;
		#If the user changed the RG and VMSS we need to set the 'flag' before calling the graph routine...
		if (insights_flag): 
			flag = 1;
			insights_flag = 0;
			values_insightsone = []; values_insightstwo = [];
			index_one = 0; index_two = 0;

		#Get the Insights metrics and draw graph...
		customheader = {'X-Api-Key': insightsKey}
		if (insightsOneEnabled.lower() == "yes"):
			clean_insights(window['insightsone'], 10);
			#Open space to a new sample...
			values_insightsone.append(index_one);
			try:
				if (insightsOneUrl == ""):
					insightsOneUrl = insightsUrl + insightsAppId + "/metrics/" + insightsOneMetric + "?timespan=PT" + str(insightsInterval) + "S";

				metricone = requests.get(insightsOneUrl, headers=customheader);
				metriconevalue = metricone.json();
				if (metriconevalue['value'][insightsOneMetric].values()[-1] is not None):
					values_insightsone[index_one] = int(metriconevalue['value'][insightsOneMetric].values()[-1]);
				else:
					values_insightsone[index_one] = 0;
				logging.info("INSIGHTS %s: %s", insightsOneTitle, values_insightsone[index_one]);
				if (index_one == total_values_one):
					values_insightsone.pop(0);
					index_one = (total_values_one - 1);
				index_one += 1;
				draw_insights(window['insightsone'], values_insightsone, insightsOneTitle, "One", flag);
			except:
				logging.exception("Getting Insights Metric: %s", insightsOneTitle);

		if (insightsTwoEnabled.lower() == "yes"):
			clean_insights(window['insightstwo'], 7);
			#Open space to a new sample...
			values_insightstwo.append(index_two);
			try:
				if (insightsTwoUrl == ""):
					insightsTwoUrl = insightsUrl + insightsAppId + "/metrics/" + insightsTwoMetric + "?timespan=PT" + str(insightsInterval) + "S";

				metrictwo = requests.get(insightsTwoUrl, headers=customheader);
				metrictwovalue = metrictwo.json();
				if (metrictwovalue['value'][insightsTwoMetric].values()[-1] is not None):
					values_insightstwo[index_two] = int(metrictwovalue['value'][insightsTwoMetric].values()[-1]);
				else:
					values_insightstwo[index_two] = 0;
				logging.info("INSIGHTS %s: %s", insightsTwoTitle, values_insightstwo[index_two]);
				if (index_two == total_values_two):
					values_insightstwo.pop(0);
					index_two = (total_values_two - 1);
				index_two += 1;
				draw_insights(window['insightstwo'], values_insightstwo, insightsTwoTitle, "Two", flag);
			except:
				logging.exception("Getting Insights Metric: %s", insightsTwoTitle);

		#Sleep a little...
		update_panels();
		doupdate();
		time.sleep(insightsInterval);

# REAL monitor thread...
def vmss_monitor_thread(window_information, panel_information, window_continents, panel_continents, demoEnabled):
	global access_token, insightsOneEnabled, insightsTwoEnabled;

	run_event = threading.Event()
	run_event.set()

	demo = 0;
        #Are we for real??
	if (demoEnabled.lower() == 'yes'):
            demo = 1;

	# start a timer in order to refresh the access token in 10 minutes
	start_time = time.time();
	
	if demo:
	    # This is a DEMO access token...
	    access_token = '--DemoToken-FORTISFORTUNAADIUVAT-DemoToken--';
	else:
	    # get an access token for Azure authentication
	    access_token = azurerm.get_access_token(str(tenant_id), str(app_id), str(app_secret));

	# ---= ASCii Dashboard THREADS =---
	# Logtail Thread...
	log_thread = threading.Thread(target=tail_in_window, args=(logName, window_information['log'], panel_information['log'], run_event))
	log_thread.start()

	# Demo VMSS Monitoring Thread...
	vmss_thread = threading.Thread(target=get_vmss_properties, args=(access_token, run_event, window_information, panel_information, window_continents, panel_continents, demo))
	vmss_thread.start()

	# start a CMD Interpreter thread
	cmd_thread = threading.Thread(target=get_cmd, args=(access_token, run_event, window_information, panel_information, demo))
	cmd_thread.start()

	#Simple consistent check for the Insights configuration...
	if (insightsOneEnabled.lower() == "yes"):
		if ((insightsOneUrl == "" and insightsUrl == "") or (insightsOneTitle == "") or (insightsOneMetric == "")):
			logging.warning("Configuration for insightsOne Graph is inconsistent. You need to configure insightsUrl or insightsOneUrl AND insightsOneTitle AND insightsOneMetric");
			insightsOneEnabled = "No";

	if (insightsTwoEnabled.lower() == "yes"):
		if ((insightsTwoUrl == "" and insightsUrl == "") or (insightsTwoTitle == "") or (insightsTwoMetric == "")):
			logging.warning("Configuration for InsightsTwo Graph is inconsistent. You need to configure insightsUrl or insightsTwoUrl AND insightsTwoTitle AND insightsTwoMetric");
			insightsTwoEnabled = "No";

	# Insights Thread...
	if (insightsOneEnabled.lower() == "yes" or insightsTwoEnabled.lower() == "yes"):
		insights_thread = threading.Thread(target=insights_in_window, args=(logName, window_information, run_event))
		insights_thread.start()

	time.sleep(.2);

	try:
		while (quit == 0):
			time.sleep(.1);
		if (quit == 1):
			raise KeyboardInterrupt
	except KeyboardInterrupt:
		show_panel(panel_information['exit']);
		update_panels();
		doupdate();
		run_event.clear();
		log_thread.join();
		vmss_thread.join();
		cmd_thread.join();
		if (insightsOneEnabled.lower() == "yes" or insightsTwoEnabled.lower() == "yes"):
			insights_thread.join();
		wmove(window_information['exit'], 3, 5); wclrtoeol(window_information['exit']);
		box(window_information['exit']);
		write_str_color(window_information['exit'], 3, 6, "Console Update threads successfully closed.", 4, 1);
		update_panels();
		doupdate();

