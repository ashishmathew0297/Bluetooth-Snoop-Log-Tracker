#!/bin/bash

GREEN=$(tput setaf 2)
NORMAL=$(tput sgr0)
YELLOW=$(tput setaf 3)
BOLD=$(tput bold)

timestamp=$(date +"%d%m%Y_%H%M")
new_filename="btsnoop_hci_${timestamp}.log"
zip_filename="bugreports_${timestamp}"

printf "%s%sPlease Wait%s\n" "${BOLD}" "${YELLOW}" "${NORMAL}"

adb bugreport ./temp/$(zip_filename)
yes | unzip -j bugreports FS/data/misc/bluetooth/logs/btsnoop_hci.log -d bt_logfiles
mv bt_logfiles/btsnoop_hci.log bt_logfiles/"${new_filename}"

tshark -r ./bt_logfiles/${new_filename} -T json \
-e frame.number \
-e frame.time_epoch \
-e frame.len \
-e frame.protocols \
-e hci_h4.type \
-e hci_h4.direction \
-e bthci_cmd \
-e bthci_cmd.device_name \
-e bthci_evt.code \
-e bthci_evt \
-e bthci_evt.num_command_packets \
-e bthci_evt.status \
-e bthci_evt.command_in_frame \
-e bthci_acl.chandle \
-e bthci_acl.length \
-e bthci_acl.src.bd_addr \
-e bthci_acl.src.name \
-e bthci_acl.dst.bd_addr \
-e bthci_acl.dst.name \
-e btl2cap.cid \
-e btl2cap.length > ./temp/pcap.json

rm ./temp/${zip_filename}

printf "%s%sCompleted:%s The output can be found in ./outputs\n" "${BOLD}" "${GREEN}" "${NORMAL}"
