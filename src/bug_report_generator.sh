#!/bin/bash

GREEN=$(tput setaf 2)
NORMAL=$(tput sgr0)
YELLOW=$(tput setaf 3)
BOLD=$(tput bold)

timestamp=$(date +"%d%m%Y_%H%M")
new_filename="btsnoop_hci_${timestamp}.log"
zip_filename="bugreports_${timestamp}"

# adb bugreport $(zip_filename)

printf "%s%sPlease Wait%s\n" "${BOLD}" "${YELLOW}" "${NORMAL}"
yes | unzip -j bugreports FS/data/misc/bluetooth/logs/btsnoop_hci.log -d bt_logfiles
mv bt_logfiles/btsnoop_hci.log bt_logfiles/"${new_filename}"

printf "%s%sCompleted%s\n" "${BOLD}" "${GREEN}" "${NORMAL}"

# rm bugreports.zip
