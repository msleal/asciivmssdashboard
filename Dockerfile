#Dockerfile for ASCiiVMSSDashboard
#Copyright(c) 2016, Marcelo Leal

#To build it, type (example):
#>sudo docker build -t msleal/asciivmssdashboard:test .
FROM ubuntu:14.04
MAINTAINER Marcelo Leal <msl@eall.com.br>
RUN apt-get update
RUN apt-get install -y git && apt-get install -y wget
RUN apt-get install -y unzip && apt-get install -y python-pip
RUN pip install azurerm
RUN pip install --upgrade urllib3 && pip install --upgrade requests
RUN cd /tmp/ && wget https://sourceforge.net/projects/pyunicurses/files/latest/download -O unicurses.zip
RUN cd /tmp/ && unzip unicurses.zip
RUN cd /tmp/ && cd UniCurses-* && python setup.py install
RUN adduser --disabled-password --gecos "" architect
RUN su - architect -c "git clone https://github.com/msleal/asciivmssdashboard.git"
