#!/bin/bash

LOG_FILE="/home/aron/szakdolgozat-raspberry-pi/error.log"

run_with_logging() {
    "$@" 2>> "$LOG_FILE"
    if [ $? -ne 0 ]; then
        echo "Error occurred while running: $@" >> "$LOG_FILE"
    fi
}

run_with_logging /usr/bin/python /home/aron/szakdolgozat-raspberry-pi/webserver.py &
run_with_logging /usr/local/bin/ngrok http --domain=harmless-toad-remarkably.ngrok-free.app 8080 &
run_with_logging /usr/bin/python /home/aron/szakdolgozat-raspberry-pi/hardware-code/indicate_raspi_on.py &
