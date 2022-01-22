#!/bin/bash

# cron-ready
# */1 * * * * eval "export $(egrep -z DBUS_SESSION_BUS_ADDRESS /proc/$(pgrep -u $LOGNAME gnome-session)/environ)"; /usr/bin/flock -n /tmp/my.lockfile /path/to/script.sh

#Minimum available memory limit, MB
THRESHOLD=1500

#Check time interval, sec
INTERVAL=5

while :
do

    used=$(free -m|awk '/^Mem:/{print $3}')
    free=$(free -m|awk '/^Mem:/{print $4}')
    buffers=$(free -m|awk '/^Mem:/{print $6}')
    available=$(free -m | awk '/^Mem:/{print $7}')
    #cached=$(free -m|awk '/^Mem:/{print $7}')
    #available=$(free -m | awk '/^-\/+/{print $7}')

    message="Used: $used"" MB""\\nAvailable: $available"" MB""\\nFree: $free"" MB""\\nBuffers: $buffers"" MB"

    if [ $available -lt $THRESHOLD ]
        then
        notify-send --expire-time=1 --urgency=critical "WARNING! Memory is running out!" "$message"
    fi

    echo $message

    sleep $INTERVAL

done