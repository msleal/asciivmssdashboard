import setuptools

setuptools.setup(name='asciivmssdashboard',
    version='2.0.2',
    description='Terminal Based Dashboard to view and manage Azure VM Scale Sets.',
    long_description='The asciivmssdashboard tool is a terminal based, ascii animated utility, that to provides a graphical representation of the Azure Virtual Machines Scale Sets (VMSS) present in your Azure Subscription. This utility shows the VMSS and Virtual Machines properties, Azure Regions around the globe, and your Azure Subscription Quota. Also, there is an DEMO execution mode where you do not need to have or use your real VMSS to see the tool in action! This is a PERSONAL and INDEPENDENT project and NOT an official tool or implementation from any vendor. Use it at your own risk, and also take a look at the README and License files. The purpose of this tool is to be a handy alternative to view and interact with Azure VMSS in a simple and graphical way, without leaving the terminal. The asciivmssdashboard has a simple command line interface builtin, where you can do things like: a) Create VMs: add vm 10 or b) Select a VM: select vm 5 (these commands will: create 10 Virtual Machines inside the VMSS or select the Virtual Machine ID 5, respectively). Any feedback, comments or bugs, please send directly to the module owner, and go to https://azure.microsoft.com if you are looking for official Microsoft Azure tools',
    url='http://github.com/msleal/asciivmssdashboard',
    keywords='ascii terminal vmss scale dashboard azure virtual curses graphical interface',
    author='msleal',
    author_email='msl@eall.com.br',
    license='MIT',
    scripts=['bin/asciivmssdashboard'],
    packages=['asciivmssdashboard'],
    package_data={"asciivmssdashboard": ["pdc34dll/*"]},
    install_requires=[
        'azurerm',
        'requests',
    ],
    zip_safe=False)
