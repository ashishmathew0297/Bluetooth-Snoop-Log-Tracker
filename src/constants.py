PDF_TITLE = "Bluetooth Packet Capture Report"
PDF_WIDTH = 210
PDF_HEIGHT = 297

HCI_LE_EVENT = {
    "0x01": "Command (HCI_CMD)",
    "0x02": "ACL (HCI_ACL)",
    "0x04": "Event (HCI_EVT)"
}

EVENT_DIRECTION = {
    "0x00": "Host > Controller",
    "0x01": "Controller > Host"
}

L2CAP_CID_VALUES = {
    "0x0004": "Attribute Protocol (ATT)",
    "0x0005": "LE Signaling Channel",
    "0x0006": "Security Manager Protocol (SMP)"
}

PACKET_KEYS = [
    "frame.number",
    "frame.time_epoch",
    "frame.len",
    "frame.protocols",
    "hci_h4.type",
    "hci_h4.direction",
    "bthci_cmd",
    "bthci_evt.code",
    "bthci_evt",
    "bthci_evt.num_command_packets",
    "bthci_evt.status",
    "bthci_evt.command_in_frame",
    "bthci_acl.chandle",
    "bthci_acl.length",
    "bthci_cmd.device_name",
    "bthci_acl.src.bd_addr",
    "bthci_acl.src.name",
    "bthci_acl.dst.bd_addr",
    "bthci_acl.dst.name",
    "btl2cap.cid",
    "btl2cap.length"
]

PROTOCOL_TYPES = {
    "bluetooth:hci_h4:bthci_cmd": "HCI Command",
    "bluetooth:hci_h4:bthci_evt": "HCI Command",
    "bluetooth:hci_h4:bthci_evt:btcommon": "HCI Event (btcommon)",
    "bluetooth:hci_h4:bthci_cmd:bthci_vendor.broadcom": "HCI Command (Vendor Specific)",
    "bluetooth:hci_h4:bthci_evt:bthci_vendor.broadcom": "HCI Event (Vendor Specific)",
    "bluetooth:hci_h4:bthci_cmd:btcommon": "HCI Command (btcommon)",
    "bluetooth:hci_h4:bthci_acl:btl2cap:btatt": "ACL - Attribute Protocol",
    "bluetooth:hci_h4:bthci_acl:btl2cap": "ACL - L2CAP Protocol",
    "bluetooth:hci_h4:bthci_acl:btl2cap:btsdp": "ACL - Service Discovery Protocol",
    "bluetooth:hci_h4:bthci_acl:btl2cap:btavdtp": "ACL - Audio/Video Distribution Transport Protocol",
    "bluetooth:hci_h4:bthci_acl:btl2cap:btrfcomm": "ACL - Radio Frequency Communication",
    "bluetooth:hci_h4:bthci_acl:btl2cap:btrfcomm:bthfp": "ACL - RFComm Hands Free Profile",
    "bluetooth:hci_h4:bthci_acl:btl2cap:btrfcomm:data": "ACL - RFComm Data Transfer",
    "bluetooth:hci_h4:bthci_acl:btl2cap:btavctp:btavrcp": "ACL - Audio/Video Remote Control Profile",
    "bluetooth:hci_h4:bthci_acl:btl2cap:btavdtp:bta2dp:rtp:ldac": "ACL - Lossless Digital Audio Codec"
}

# l2cap_commands = {
#     '0x01':'Command Reject',
#     '0x06':'Disconnection Request',
#     '0x07':'Disconnection Response',
#     '0x0a':'Information Request - not supported',
#     '0x0b':'Information Response - not supported',
#     '0x12':'Connection Parameter Update Request',
#     '0x13':'Connection Parameter Update Response',
#     '0x14':'LE Credit Based Connection Request',
#     '0x15':'LE Credit Based Connection Response',
#     '0x16':'LE Flow Control Credit'
# }

VENDOR_LOOKUP_API = "https://www.macvendorlookup.com/api/v2/"