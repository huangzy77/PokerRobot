#!/bin/bash
echo "This shell will start adb !"
sudo service udev restart
sudo adb kill-server
sudo adb start-server

