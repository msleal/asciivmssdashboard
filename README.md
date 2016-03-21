# ASCii VMSS Dashboard v1.2
Dashboard to show and configure Azure VM Scale Set status and properties

![Image of ASCii VMSS Dashboard](https://raw.githubusercontent.com/msleal/msleal.github.com/master/asciidash-v1-2.png)


## Installation
  1. Install Python 3.x.
  2. Install the azurerm REST wrappers for Microsoft Azure: pip install azurerm.
  3. Install [Pyunicurses](https://sourceforge.net/projects/pyunicurses/).
  4. On Windows, Install [pdcurses](http://pdcurses.sourceforge.net/). I have used the: pdc34dllw.zip file...
  5. Clone this repo locally.
  6. Register an Azure application, create a service principal and get your tenant id. See "Using ASCiiVMSSDashboard".
  7. Put in values for your application, along with your resource group name, and VM Scale Set name in vmssconfig.json.
  8. Run (on Linux): ./console.py or (on Windows): python console.py.
  9. To Exit the Console, just hit: Ctrl+C (for a 'clean' exit, we will wait for the update threads to finish). In Windows
you will need to kill the Python process, for now (See "CAVEATS" bellow).

## WATCH THE CONSOLE IN ACTION:
Subtitle/Captions should be enabled by default, but if not, enable them to follow the action...

[ASCiiVMSSDashboard Screencast](https://www.youtube.com/watch?v=MomiZ9rU9NU)

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
As we wait for the threads to finish as you hit 'Ctrl+C' (to exit), the time you will wait to get your prompt
back will be proportional to you refresh interval (e.g.: max=<INTERVAL>). You can change the update interval in the 
'vmssconfig.json' file.

## ASCiiVMSSDashboard Commands
  To issue commands for the Azure Resource Manager API to add and/or delete virtual machines from the Scale Set,
you just need to type ':'. The cursor will appear at the bottom left of the screen (PROMPT window), and you will
be able to enter commands. To see a help window with the commands available, just type ':' (to activate the command
PROMPT window), and 'help'. To hide the help window, just do the same sequence (':' and 'help').

TO ACTIVATE THE PROMPT WINDOW, TYPE: ':'

Comands (v1.0):
- add vm <nr>: Use this command to add virtual machines to your VMSS deployment.
- del vm <nr>: Use this command to delete virtual machines to your VMSS deployment.
- select vm <nr>: Use this command to select a specific virtual machine on your VMSS deployment, and get info.
- deselect: Use this command to clear the selection of any specific virtual machine.
- help: Use this command to get help about the dashboard commands (inside the ASCiiVMSSDashboard).

## CAVEATS
- The 'stdscr.nodelay(1)' seems not to be multiplatform (at least does not work on Windows), and we are using it 
as a non-block function when reading user commands. So, to exit the console on windows I needed to kill the python 
program (or close the CMD or Powershell window)... I'm looking for an alternative non-block call to use on windows
and fix this. It would be nice to have any feedback of this program running on MacOS. 
- If you have problems installing pdcurses on windows (not able to load uniCurses), you can try adding the DLL directly
on the current directory of the ASCiiVMSSDashboard installation. I have tested it just cloning the repo on Windows 10
and copying the pdcurses.dll to the cloned folder, and it runs without any issues. 

## Using ASCiiVMSSDashboard 
To use this app (and in general to access Azure Resource Manager from a program without going through 2 factor
authentication) you need to register your application with Azure and
create a "Service Principal" (an application equivalent of a
user). Once you've done this you'll have 3 pieces of information: A
tenant ID, an application ID, and an application secret. You will use
these to populate the vmssconfig.json file. For more information on
how to get this information go here: [Authenticating a service
principal with Azure Resource Manager][service-principle]. See also:
[Azure Resource Manager REST calls from Python][python-auth].

## Example VMSS ARM Template:
[Linux VM Scale Set integrated with Azure autoscale][arm-template].

[service-principle]: https://azure.microsoft.com/en-us/documentation/articles/resource-group-authenticate-service-principal/
[python-auth]: https://msftstack.wordpress.com/2016/01/05/azure-resource-manager-authentication-with-python
[arm-template]: https://github.com/Azure/azure-quickstart-templates/tree/master/201-vmss-ubuntu-autoscale
