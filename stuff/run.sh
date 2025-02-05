#!/bin/bash

/usr/bin/python /home/aron/szakdolgozat-raspberry-pi/webserver.py &
/usr/local/bin/ngrok http --domain=hippo-immense-plainly.ngrok-free.app 8080 &
/usr/bin/python /home/aron/szakdolgozat-raspberry-pi/hardware-code/indicate_raspi_on.py &