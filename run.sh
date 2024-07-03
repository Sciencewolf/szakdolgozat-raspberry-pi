#!/usr/bin/env bash

echo off
/usr/bin/python /home/aron/szakdolgozat-raspberry-pi/webserver.py &
/usr/local/bin/ngrok http --domain=hippo-immense-plainly.ngrok-free.app 8080 &
