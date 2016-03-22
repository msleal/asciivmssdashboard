# ASCii VMSS Dashboard v1.2
Dashboard to show and configure Azure VM Scale Set status and properties

![Image of ASCii VMSS Dashboard](https://raw.githubusercontent.com/msleal/msleal.github.com/master/asciidash-v1-2.png)


## Installation
  1. Install Python 2.x or 3.x.
  2. Install the azurerm REST wrappers for Microsoft Azure: pip install azurerm.
  3. Install [Pyunicurses](https://sourceforge.net/projects/pyunicurses/).
  4. On Windows, Install [pdcurses](http://pdcurses.sourceforge.net/). I have used the: pdc34dllw.zip file. See 'PDCURSES' bellow...
  5. Clone this repo locally.
  6. Register an Azure application, create a service principal and get your tenant id. See "Using ASCiiVMSSDashboard".
  7. Put in values for your application, along with your resource group name, and VM Scale Set name in vmssconfig.json.
  8. Run (on Linux): ./console.py or (on Windows): python console.py.
  9. To Exit the Console, just hit: Ctrl+C or use the command: 'quit' (for a 'clean' exit, we will wait for the update threads to finish).
In the Windows Platform you can just use the command: 'quit' for now (See "CAVEATS" bellow)...

## WATCH THE CONSOLE IN ACTION:
Subtitle/Captions should be enabled by default, but if not, enable them to follow the action (English and Portuguese BR available).

[ASCiiVMSSDashboard Screencast](https://www.youtube.com/watch?v=MomiZ9rU9NU)
Don't forge to subscribe to the channel for updates...

Enjoy some code and loud music!

###TIP #1: 
To not create the .pyc files, I use the following (on Linux): export PYTHONDONTWRITEBYTECODE=1; ./console.py.

###TIP #2:
I have used the console with no issues using a refresh interval of 60 seconds. If you use a more 'agressive'
update interval, keep one eye at the last-update-hour registered at the top-left of the window, to see if the console 
is stil running.  If you notice it stopped, it should have generated an 'error.log' in the current directory. 
Look into it, as it should have the information about AZURE API 'throttling", and so you will need to exit the console
and start it again (with a bigger inteval)...
 
###TIP #3:
As we wait for the threads to finish as you hit 'Ctrl+C' or 'quit' (to exit), the time you will wait to get your prompt
back will be proportional to you refresh interval (e.g.: max=<INTERVAL>). You can change the update interval in the 
'vmssconfig.json' file.

## ASCiiVMSSDashboard Commands
  To issue commands for the Azure Resource Manager API to add and/or delete virtual machines from the Scale Set,
you just need to type ':'. After that, the cursor will appear at (PROMPT window), and you will be able to enter commands.
To see a help window just type ':' (to activate the command PROMPT window), and 'help' again to hide it.

TO ACTIVATE THE PROMPT WINDOW, TYPE: ':'

Commands (v1.2):
- add vm <nr>: Use this command to add virtual machines to your VMSS deployment.
- del vm <nr>: Use this command to delete virtual machines to your VMSS deployment.
- select vm <nr>: Use this command to select a specific virtual machine on your VMSS deployment, and detailed info.
- deselect: Use this command to clear the selection of any specific virtual machine.
- rg <resourcegroupname> vmss <vm scale set name>: Use this command to switch the visualization to another VM Scale Set.
- quit: Use this command to exit the console (Any platform).
- Ctrl+c: Use this key combination to end the ASCiiVMSSDashboard (Not working on windows for now).
- help: Use this command to get help about the dashboard commands (inside the ASCiiVMSSDashboard).

## CAVEATS
- The 'stdscr.nodelay(1)' seems not to be multiplatform (at least does not work on Windows), and we are using it 
as a non-block function when reading user commands. For now, you can use the command 'quit' to end the dashboard on Windows. 
I'm looking for an alternative non-block call to use on windows and fix this. It would be nice to have any feedback of this program 
running on MacOS. 

##PDCURSES
- If you have problems installing pdcurses on windows (not able to load uniCurses: import error), you can just add the DLL directly
on the current directory of the ASCiiVMSSDashboard installation. To run the ASCiiVMSSDashboard on Windows, I have tested it 
just cloning the repo on Windows 10, and copying the 'pdcurses.dll' file to the cloned folder, and it runs without any issues (you
still needs to have the UniCurses installed, but you have the Windows Installer link at the top of this README file). 

## Using ASCiiVMSSDashboard 
To use this app (and in general to access Azure Resource Manager from a program without going through 2 factor authentication), 
you need to register your application with Azure and create a "Service Principal" (an application equivalent of a user). 
Once you've done this you'll have 3 pieces of information: A 'tenant ID', an 'application ID', and an 'application secret'.
You will use these to populate the vmssconfig.json file. 

For more information on how to get this information go here: [Authenticating a service principal with Azure Resource Manager][service-principle].
See also: [Azure Resource Manager REST calls from Python][python-auth].

## Example VMSS ARM Template:
[Ubuntu Linux VM Scale Set integrated with Azure autoscale][arm-template].

[service-principle]: https://azure.microsoft.com/en-us/documentation/articles/resource-group-authenticate-service-principal/
[python-auth]: https://msftstack.wordpress.com/2016/01/05/azure-resource-manager-authentication-with-python
[arm-template]: https://github.com/Azure/azure-quickstart-templates/tree/master/201-vmss-ubuntu-autoscale
