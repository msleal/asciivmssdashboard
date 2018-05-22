# really simple script to install all dependencies and run this project on debian based systems
# to run, give this script the permission with chmod +x setup_script.sh
# then run ./setup_script

sudo apt-get install wget
sudo apt-get install python3
sudo apt-get install python3-pip
sudo pip3 install azurerm
wget https://sourceforge.net/projects/pyunicurses/files/latest/download -O unicurses.zip
unzip unicurses.zip 
mv PURELIB/unicurses.py .
