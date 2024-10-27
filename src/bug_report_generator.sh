#! /bin/bash

# rm ./bt_logfiles/btsnoop_hci.log
adb bugreport bugreports
yes | unzip -j bugreports.zip FS/data/misc/bluetooth/logs/btsnoop_hci.log -d bt_logfiles
rm bugreports.zip
