#!/usr/bin/env python
# DEMO payload...

"""
Copyright (c) 2020, Marcelo Leal
Description: The power is in the terminal...
License: MIT (see LICENSE.txt file for details)
"""

import json

rgname = "dashdemo"
vmssname = "dashdemo"
interval = 15
tenantId = "xxx"
insightsAppId = "xxx"
insightsKey = "xxx"
insightsUrl = "xxx"
insightsOneEnabled = "No"
insightsOneUrl = "xxx"
insightsOneMetric = "xxx"
insightsOneTitle = "xxx"
insightsTwoEnabled = "No"
insightsTwoUrl = "xxx"
insightsTwoMetric = "xxx"
insightsTwoTitle = "xxx"
insightsInterval = 10

#DEMO Assets...
VMSSGET_DEMO = json.dumps({"name": "dashdemo", "location": "brazilsouth", "sku": {"name": "Standard_A2", "tier": "Standard", "capacity": 1}, "properties": {"virtualMachineProfile": {"osProfile": {"adminUsername": "blackpanther"}, "storageProfile": {"imageReference": {"publisher": "Canonical", "offer": "UbuntuServer", "sku": "16.04.0-LTS", "version": "latest"}}}, "provisioningState": "Succeeded"}})

NET_DEMO = json.dumps({"value": [{"name": "dashdemopip", "location": "brazilsouth", "properties": {"provisioningState": "Succeeded", "ipAddress": "999.999.999.999", "publicIPAddressVersion": "IPv4", "publicIPAllocationMethod": "Dynamic", "idleTimeoutInMinutes": 4, "dnsSettings": {"domainNameLabel": "dashdemo", "fqdn": "dashdemo.brazilsouth.cloudapp.azure.com"}}, "type": "Microsoft.Network/publicIPAddresses", "sku": {"name": "Basic"}}]})

QUOTA_DEMO = json.dumps({u"value": [{u"currentValue": 0, u"limit": 2000, u"name": {u"localizedValue": u"Availability Sets", u"value": u"availabilitySets"}, u"unit": u"Count"}, {u"currentValue": 4, u"limit": 1000, u"name": {u"localizedValue": u"Total Regional vCPUs", u"value": u"cores"}, u"unit": u"Count"}, {u"currentValue": 2, u"limit": 25000, u"name": {u"localizedValue": u"Virtual Machines", u"value": u"virtualMachines"}, u"unit": u"Count"}, {u"currentValue": 1, u"limit": 2000, u"name": {u"localizedValue": u"Virtual Machine Scale Sets", u"value": u"virtualMachineScaleSets"}, u"unit": u"Count"}]}) 

VMSSPROPERTIES_DEMO = json.dumps([u"dashdemo", 1, u"brazilsouth", u"dashdemo", u"UbuntuServer", u"16.04.0-LTS", u"Succeeded", u"dashdemo.brazilsouth.cloudapp.azure.com", u"999.999.999.999"])

VMSSVMS_DEMO = json.dumps({u"value": [{u"sku": {u"tier": u"Standard", u"name": u"Standard_A2"}, u"name": u"vmssdash_0", u"instanceId": u"0", u"properties": {u"osProfile": {u"adminUsername": u"blackpanther", u"computerName": u"vmssdash000000"}, u"provisioningState": u"Succeeded"}}]})

VMDETAILS_DEMO = json.dumps({u"computerName": u"dashdemo000000", u"disks": [{u"statuses": [{u"time": u"2019-05-03T20:46:26.6712371+00:00", u"code": u"ProvisioningState/succeeded", u"displayStatus": u"Provisioning succeeded", u"level": u"Info"}]}], u"osName": u"ubuntu", u"platformUpdateDomain": 0, u"vmAgent": {u"vmAgentVersion": u"2.2.46", u"statuses": [{u"time": u"2020-03-18T23:03:37+00:00", u"message": u"Guest Agent is running", u"code": u"ProvisioningState/succeeded", u"displayStatus": u"Ready", u"level": u"Info"}]}, u"platformFaultDomain": 0, u"osVersion": u"16.04", u"statuses": [{u"time": u"2019-05-03T20:47:37.2369051+00:00", u"code": u"ProvisioningState/succeeded", u"displayStatus": u"Provisioning succeeded", u"level": u"Info"}, {u"code": u"PowerState/running", u"displayStatus": u"VM running", u"level": u"Info"}]})

VMNIC_DEMO = json.dumps({u"value": [{u"properties": {u"provisioningState": u"Succeeded", u"macAddress": u"00-00-00-00-00-00", u"primary": True, u"enableIPForwarding": False, u"ipConfigurations": [{u"properties": {u"primary": True, u"privateIPAddressVersion": u"IPv4", u"privateIPAllocationMethod": u"Dynamic", u"privateIPAddress": u"10.0.0.5", u"provisioningState": u"Succeeded"}, u"name": u"dashdemoipconfig"}], u"enableAcceleratedNetworking": False}, u"name": u"dashdemonic"}]})
