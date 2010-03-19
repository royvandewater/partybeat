#!/bin/bash
NO_ARGS=0
OPTERROR=65

if [ $# -eq "$NO_ARGS" ] 
then
    current_ip='localhost'
else 
    if [ $1 = '-w' ]
    then
        current_ip=`ifconfig wlan0 | egrep -m 1 -o '\b([0-9]+\.){3}[0-9]+\b' | egrep -v '(^255)|(255$)'`
    else
        if [ $1 = '-e' ]
        then
            current_ip=`ifconfig eth0 | egrep -m 1 -o '\b([0-9]+\.){3}[0-9]+\b' | egrep -v '(^255)|(255$)'`
        else
            echo "Invalid parameter, to use current ip, user '-w' for wlan0 or '-e' for eth0, or no params for localhost"
        fi
    fi
fi
echo "Using $current_ip"
sed -i "s/^MEDIA_URL.*$/MEDIA_URL = 'http:\/\/$current_ip\/xd\/media\/'/" settings.py
python manage.py runserver $current_ip:8000
