#!/usr/bin/env python
# ASCii VMSS Console - The power is in the terminal...

"""
Copyright (c) 2016, Marcelo Leal
Description: The power is in the terminal...
License: MIT (see LICENSE.txt file for details)
"""

#import sys
from sys import *
import time
import json
import errno
import random
import azurerm
import logging
import requests
import platform
import threading
from demo import *
from maps import *
from azure import *
from logtail import *
from windows import *
from unicurses import *
from datacenters import *
from os.path import expanduser
import requests.packages.urllib3
