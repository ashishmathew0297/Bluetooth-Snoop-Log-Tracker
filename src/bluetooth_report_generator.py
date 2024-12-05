
import sys
import json
import time
from datetime import datetime
import requests
from constants import *

import fpdf
from fpdf.enums import XPos, YPos
from fpdf import FPDF
import pandas as pd
import numpy as np
from decimal import Decimal
from datetime import datetime

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

filepath = sys.argv[1]

# with open('./output1.json', 'r') as file:
with open(filepath, 'r') as file:
    data = [x["_source"]["layers"] for x in json.load(file)]


def format_packet_data(data):
    data_input = data
    for packet in data_input:
        packet["Sequence Number"] = packet["frame.number"][0] if "frame.number" in packet else None
        packet["Epoch Timestamp"] = packet["frame.time_epoch"][0] if "frame.time_epoch" in packet else None
        packet["Timestamp"] = datetime.fromtimestamp(int(Decimal(packet["frame.time_epoch"][0]))) if "frame.time_epoch" in packet else None
        packet["Packet Length"] = packet["frame.len"][0] if "frame.len" in packet else None
        packet["LE Protocol"] = PROTOCOL_TYPES[packet["frame.protocols"][0]] if "frame.protocols" in packet else None
        packet["LE Event Code"] = packet["hci_h4.type"][0] if "hci_h4.type" in packet else None
        packet["LE Event Type"] = HCI_LE_EVENT[packet["hci_h4.type"][0]] if "hci_h4.type" in packet else None
        packet["Direction"] = EVENT_DIRECTION[packet["hci_h4.direction"][0]] if "hci_h4.direction" in packet else None
        packet["HCI Command"] = packet["bthci_cmd"][0] if "bthci_cmd" in packet else None
        packet["HCI Event Code"] = packet["bthci_evt.code"][0] if "bthci_evt.code" in packet else None
        packet["HCI Event"] = packet["bthci_evt"][0] if "bthci_evt" in packet else None
        packet["HCI Event Command Packet Count"] = packet["bthci_evt.num_command_packets"][0] if "bthci_evt.num_command_packets" in packet else None
        packet["HCI Event Status"] = packet["bthci_evt.status"][0] if "bthci_evt.status" in packet else None
        packet["HCI Event Command in Frame"] = packet["bthci_evt.command_in_frame"][0] if "bthci_evt.command_in_frame" in packet else None
        packet["HCI ACL chandle"] = packet["bthci_acl.chandle"][0] if "bthci_acl.chandle" in packet else None
        packet["HCI ACL Length"] = packet["bthci_acl.length"][0] if "bthci_acl.length" in packet else None
        packet["Source Device MAC"] = packet["bthci_acl.src.bd_addr"][0] if "bthci_acl.src.bd_addr" in packet else None
        packet["Source Device Name"] = packet["bthci_cmd.device_name"][0] if "bthci_cmd.device_name" in packet else (packet["bthci_acl.src.name"][0] if "bthci_acl.src.name" in packet else None)
        packet["Destination Device MAC"] = packet["bthci_acl.dst.bd_addr"][0] if "bthci_acl.dst.bd_addr" in packet else None
        packet["Destination Device Name"] = packet["bthci_acl.dst.name"][0] if "bthci_acl.dst.name" in packet else None
        packet["L2CAP CID"] = packet["btl2cap.cid"][0] if "btl2cap.cid" in packet else None
        packet["L2CAP Length"] = packet["btl2cap.length"][0] if "btl2cap.length" in packet else None


        if packet["HCI Command"]:
            packet["HCI Command"] = packet["HCI Command"].replace("Bluetooth HCI Command - ", "")

        if packet["HCI Event"]:
            packet["HCI Event"] = packet["HCI Event"].replace("Bluetooth HCI Event - ", "")

        if packet["L2CAP CID"] is not None:
            if packet["L2CAP CID"] in L2CAP_CID_VALUES:
                packet["L2CAP Type"] = L2CAP_CID_VALUES[packet["L2CAP CID"]]
            else:
                packet["L2CAP Type"] = 'Dynamically Allocated'

        for key in PACKET_KEYS:
            if key in packet:
                del packet[key]

        keys_to_delete = [key for key, value in packet.items() if value is None]
        for key in keys_to_delete:
            del packet[key]

    df = pd.DataFrame(data)

    # handling nan values in device name if name already present in the dataframe 
    src_mac_device_dict = df.dropna(subset=['Source Device MAC', 'Source Device Name']).set_index('Source Device MAC')['Source Device Name'].to_dict()
    df['Source Device Name'] = df['Source Device MAC'].map(src_mac_device_dict).fillna(df['Source Device Name'])

    dst_mac_device_dict = df.dropna(subset=['Destination Device MAC', 'Destination Device Name']).set_index('Destination Device MAC')['Destination Device Name'].to_dict()
    df['Destination Device Name'] = df['Destination Device MAC'].map(dst_mac_device_dict).fillna(df['Destination Device Name'])

    df['Source Device Name'] = df['Source Device Name'].replace('', 'Unknown Device')
    df['Source Device Name'] = df['Source Device Name'].fillna('Unknown Device')
    df['Destination Device Name'] = df['Destination Device Name'].replace('', 'Unknown Device')
    df['Destination Device Name'] = df['Destination Device Name'].fillna('Unknown Device')

    return df

def generate_device_piecharts(df, names, title, export_filename):
    fig = px.pie(df, names=names, title=title, hole=0.3, width=750, height=400)
    fig.update_layout(title_font_size=24)
    fig.update_traces(textinfo='percent', texttemplate='%{percent:.2%} (%{value})', textfont_size=18)
    fig.update_layout(legend=dict(x=0.85, y=1.1))
    fig.update_layout(margin=dict(t=50, b=30, l=0, r=220))
    fig.write_image(f'./generated_images/{export_filename}', scale=2)

def generate_hci_cmdevt_plot(df_hci_cmd, df_hci_event, export_filename):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=df_hci_cmd['Timestamp'],
            y=df_hci_cmd['Sequence Number'],
            mode='lines+markers',
            name='HCI Commands',
            line=dict(color='red')),
            secondary_y=False
        )

    fig.add_trace(
        go.Scatter(
            x=df_hci_event['Timestamp'],
            y=df_hci_event['Sequence Number'],
            mode='lines+markers',
            name='HCI Events',
            line=dict(color='blue')),
            secondary_y=True
        )

    fig.update_yaxes(title_text="Sequence Number (HCI Commands)", dtick=200, tickmode='linear', secondary_y=False)
    fig.update_yaxes(title_text="Sequence Number (HCI Events)", dtick=200, tickmode='linear', secondary_y=True)

    fig.update_layout(title='HCI Events and Commands over Time',
                      title_font_size=24,
                      xaxis_title='Timestamp (UTC)',
                      xaxis=dict(tickangle=45),
                      legend=dict(x=0.01, y=0.99),
                      template='plotly_white',
                      width=900,
                      height=600)
    fig.write_image(f'./generated_images/{export_filename}', scale=2)

def get_mac_info(mac_address):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    url = VENDOR_LOOKUP_API + mac_address
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()[0]
    else:
        return None

def generate_mac_info_dataframe(unique_mac_list):
    unique_mac_info_list = []
    for mac in unique_mac_list:
        info = get_mac_info(mac)
        info['mac_address'] = mac
        if info:
            unique_mac_info_list.append(info)
    mac_info_df = pd.DataFrame(unique_mac_info_list)[['mac_address', 'company', 'addressL1', 'addressL2', 'addressL3', 'country']]
    mac_info_df.dropna(axis=1, how='all', inplace=True)
    return mac_info_df

# PDF Report Generation Code
class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', XPos.RIGHT, new_y=YPos.TOP, align='C')

def create_title(pdf, title):
    
    # PDF Title
    pdf.set_font('Helvetica', 'b', 26)  
    pdf.ln(10)
    pdf.write(5, title)
    pdf.ln(10)
    
    # Report Date
    pdf.set_font('Helvetica', '', 20)
    pdf.set_text_color(r=128,g=128,b=128)
    today = time.strftime("%m/%d/%Y")
    pdf.write(4, f'{today}')
    pdf.ln(10)

def create_heading(pdf, title):
    pdf.set_left_margin(10)
    pdf.set_font('Helvetica', 'BU', 22,)
    pdf.set_text_color(r=0,g=0,b=0)
    pdf.write(5, title)
    pdf.ln(12)

def create_subheading(pdf, title):
    pdf.set_font('Helvetica', 'BU', 18)
    pdf.set_text_color(r=0,g=0,b=0)
    pdf.write(5, title)
    pdf.ln(8)

def write_to_pdf(pdf, words, bold=False, font_size=14):
    pdf.set_text_color(r=0, g=0, b=0)
    if bold:
        pdf.set_font('Helvetica', 'B', font_size)
    else:
        pdf.set_font('Helvetica', '', font_size)
    pdf.write(5, words)

def generate_pcap_report(summary_stats, hci_command_event_stats, hci_command_event_info, hci_acl_stats, l2cap_acl_packet_counts, host_device_info, controller_device_info):
    pdf = PDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    create_title(pdf, PDF_TITLE)

    create_heading(pdf, "General Information")

    pdf.set_left_margin(15)
    for key, value in summary_stats.items():
        write_to_pdf(pdf, f"{key}: ", True)
        write_to_pdf(pdf, f"{value}")
        pdf.ln(6)
    pdf.set_left_margin(10)
    pdf.ln(6)

    write_to_pdf(pdf, "Bluetooth communication is done through a standardized protocol known as the HCI interface which allows for sending and recieving commands, events and data between hosts and controllers. We will be looking at the breakdown of these between the current host device and the controllers below.")
    pdf.ln(10)

    create_heading(pdf, "HCI Command and Event Packet Details")

    pdf.set_left_margin(15)
    for key, value in hci_command_event_stats.items():
        write_to_pdf(pdf, f"{key}: ", True)
        write_to_pdf(pdf, f"{value}")
        pdf.ln(6)
    pdf.ln(4)

    for key, value in hci_command_event_info.items():
        if isinstance(value, pd.DataFrame):
            create_subheading(pdf, f"{key}: ")
            with pdf.table(text_align="C", padding=-2, borders_layout="SINGLE_TOP_LINE", cell_fill_color=220, cell_fill_mode="ROWS") as table:
                pdf.set_font('Helvetica', 'B', 14)
                row = table.row()
                for col in value.columns:
                    row.cell(col)
                pdf.set_font('Helvetica', '', 12)
                for df_row in value.itertuples():
                    row = table.row()
                    row.cell(df_row[1])
                    row.cell(str(df_row[2]))
        pdf.ln(10)

    pdf.set_left_margin(10)
    write_to_pdf(pdf, "The chart below/on the next page shows the variation of HCI commands and events over the timeframe of packet capture.")
    pdf.ln(10)

    pdf.set_left_margin(10)
    pdf.image("./generated_images/hci_cmd_event_communication.png", x=(PDF_WIDTH - 170)/2, w=170)
    pdf.ln(10)

    pdf.add_page()

    pdf.ln(10)

    create_heading(pdf, "ACL Packet Summary")

    write_to_pdf(pdf, "Bluetooth ACL, which is short for Bluetooth Asynchronous Connection-oriented Logical transport is used for general data transfer between the host and controller when it is not in real-time. It is provided alongside the SCO (Synchronous Connection Oriented) protocol which finds its use in audio and video data transfer in real-time.")
    pdf.ln(10)
    write_to_pdf(pdf, "These packets usually have a higher chance of containing idetifying information about the devices in use such as the device name and mac addresses.")

    pdf.ln(10)

    pdf.set_left_margin(15)
    for key, value in hci_acl_stats.items():
        write_to_pdf(pdf, f"{key}: ", True)
        write_to_pdf(pdf, f"{value}")
        pdf.ln(6)
    pdf.set_left_margin(10)
    pdf.ln(4)

    create_subheading(pdf, "ACL Packet Counts")
    pdf.ln(10)

    with pdf.table(text_align="C", padding=-2, borders_layout="SINGLE_TOP_LINE", cell_fill_color=220, cell_fill_mode="ROWS") as table:
        pdf.set_font('Helvetica', 'B', 14)
        row = table.row()
        for col in l2cap_acl_packet_counts.columns:
            row.cell(col)
        pdf.set_font('Helvetica', '', 12)
        for df_row in l2cap_acl_packet_counts.itertuples():
            row = table.row()
            row.cell(df_row[1])
            row.cell(str(df_row[2]))

    pdf.ln(10)

    write_to_pdf(pdf, "The plots below depict the split up of packets to and from the host and the controllers it has connected to in the given timeframe.")
    pdf.ln(10)

    pdf.image("./generated_images/source_devices_distribution.png", x=(PDF_WIDTH - 170)/2, w=170)
    pdf.ln(5)

    pdf.image("./generated_images/destination_devices_distribution.png", x=(PDF_WIDTH - 170)/2, w=170)
    pdf.ln(10)

    write_to_pdf(pdf, "From the MAC addresses in the ACL protocols, we can identify the device name and manufacturer information of the host and control devices in our capture files.")
    pdf.ln(10)

    create_heading(pdf, "MAC Vendor Information")

    create_subheading(pdf, "Host Device")

    for index, row in host_device_info.iterrows():
        write_to_pdf(pdf, f"Device Name: ", True)
        write_to_pdf(pdf, f"{row['Device Name']}")
        pdf.ln(6)
        write_to_pdf(pdf, f"MAC Address: ", True)
        write_to_pdf(pdf, f"{row['mac_address']}")
        pdf.ln(6)
        write_to_pdf(pdf, f"Manufacturer/Vendor: ", True)
        write_to_pdf(pdf, f"{row['company']}")
        pdf.ln(6)
        write_to_pdf(pdf, f"Address: ", True)
        write_to_pdf(pdf, f"{row['addressL1']}, {row['addressL2']}, {row['addressL3']}, {row['country']}")
        pdf.ln(10)

    create_subheading(pdf, "Controller Devices")

    for index, row in controller_device_info.iterrows():

        write_to_pdf(pdf, f"Controller {index + 1} ", True, 16)
        pdf.ln(7)

        write_to_pdf(pdf, f"Device Name: ", True)
        write_to_pdf(pdf, f"{row['Device Name']}")
        pdf.ln(6)
        write_to_pdf(pdf, f"MAC Address: ", True)
        write_to_pdf(pdf, f"{row['mac_address']}")
        pdf.ln(6)
        write_to_pdf(pdf, f"Manufacturer/Vendor: ", True)
        write_to_pdf(pdf, f"{row['company']}")
        pdf.ln(6)
        write_to_pdf(pdf, f"Address: ", True)
        write_to_pdf(pdf, f"{row['addressL1']}, {row['addressL2']}, {row['addressL3']}, {row['country']}")
        pdf.ln(10)

    current_time = datetime.now().strftime("%Y%m%d_%H%M")
    pdf.output(f"./outputs/report_{current_time}.pdf")

def main():
    df_data = format_packet_data(data)

    first_timestamp = df_data['Timestamp'].min()
    last_timestamp = df_data['Timestamp'].max()

    source_mac_info = df_data['Source Device Name'] + "\n(" + df_data['Source Device MAC'] + ")"
    source_mac_info = source_mac_info.dropna()
    df_sources = pd.DataFrame(source_mac_info, columns=['Source Devices'])

    destination_device_info = df_data['Destination Device Name'] + "\n(" + df_data['Destination Device MAC'] + ")"
    destination_device_info = destination_device_info.dropna()
    df_destinations = pd.DataFrame(destination_device_info, columns=['Destination Devices'])

    df_hci_cmd = df_data[df_data['LE Event Type'] == 'Command (HCI_CMD)'].dropna(axis=1, how='all')
    df_hci_event = df_data[df_data['LE Event Type'] == 'Event (HCI_EVT)'].dropna(axis=1, how='all')
    df_hci_event_paired = df_hci_event[df_hci_event['HCI Event Command in Frame'].isin(df_hci_cmd['Sequence Number'])]

    df_acl_le_events = df_data[df_data['LE Event Type'] == 'ACL (HCI_ACL)']
    df_acl_le_events = df_acl_le_events.dropna(axis=1, how='all')

    mac_addresses = pd.DataFrame({
        'MAC Address': np.unique(np.concatenate((df_data['Source Device MAC'].dropna().unique(), df_data['Destination Device MAC'].dropna().unique())))
    })
    mac_vendor_info = generate_mac_info_dataframe(mac_addresses['MAC Address'].tolist())

    host_mac_address = df_data[df_data['Direction'] == 'Host > Controller']['Source Device MAC'].dropna().unique()[0]
    host_device_name = df_data[df_data['Source Device MAC'] == host_mac_address]['Source Device Name'].dropna().unique()[0]
    host_device_company = mac_vendor_info[mac_vendor_info['mac_address'] == host_mac_address]['company'].values[0]
    controller_devices = df_data[df_data['Direction'] == 'Controller > Host'][['Source Device MAC', 'Source Device Name']].dropna().drop_duplicates()

    unique_hci_commands = df_hci_cmd['HCI Command'].unique()
    unique_hci_events = df_hci_event['HCI Event'].unique()
    hci_command_counts = df_hci_cmd['HCI Command'].value_counts().reset_index()
    hci_command_counts.columns = ['HCI Command', 'Count']
    hci_event_counts = df_hci_event['HCI Event'].value_counts().reset_index()
    hci_event_counts.columns = ['HCI Event', 'Count']

    outgoing_commands = df_hci_cmd[df_hci_cmd['Direction'] == 'Host > Controller'].shape[0]
    incoming_events = df_hci_event[df_hci_event['Direction'] == 'Controller > Host'].shape[0]

    outgoing_acl_events = df_acl_le_events[df_acl_le_events['Direction'] == 'Host > Controller'].shape[0]
    incoming_acl_events = df_acl_le_events[df_acl_le_events['Direction'] == 'Controller > Host'].shape[0]
    l2cap_acl_packet_counts = df_acl_le_events['LE Protocol'].value_counts().reset_index()
    l2cap_acl_packet_counts.columns = ['LE Protocol', 'Count']

    mac_vendor_info = mac_vendor_info.merge(df_acl_le_events[['Source Device MAC', 'Source Device Name']].drop_duplicates(), left_on='mac_address', right_on='Source Device MAC', how='left').drop(columns=['Source Device MAC'])
    mac_vendor_info.rename(columns={'Source Device Name': 'Device Name'}, inplace=True)

    host_device_info = mac_vendor_info[mac_vendor_info['mac_address'] == host_mac_address]
    controller_device_info = mac_vendor_info[mac_vendor_info['mac_address'] != host_mac_address]

    

    generate_device_piecharts(df_sources, 'Source Devices', 'Distribution of Source Devices', 'source_devices_distribution.png')
    generate_device_piecharts(df_destinations, 'Destination Devices', 'Distribution of Destination Devices', 'destination_devices_distribution.png')
    generate_hci_cmdevt_plot(df_hci_cmd, df_hci_event_paired, export_filename="hci_cmd_event_communication.png")

    summary_stats = {
        'Capture Start Time': first_timestamp,
        'Capture End Time': last_timestamp,
        'Host Device Name': host_device_name,
        'Host Device MAC Address': host_mac_address,
        'Host Device Vendor': host_device_company,
        'Controller Devices Interacted With': len(controller_devices),
        'Total Number of Packets': len(df_data),
        'HCI Command Packets': len(df_hci_cmd),
        'HCI Event Packets': len(df_hci_event),
        'ACL Packets': len(df_acl_le_events)
    }

    hci_command_event_stats = {
        'Unique HCI Commands': len(unique_hci_commands),
        'Unique HCI Events': len(unique_hci_events),
        'Outgoing Commands': outgoing_commands,
        'Incoming Events': incoming_events
    }

    hci_command_event_info = {
        'HCI Command Counts': hci_command_counts,
        'HCI Event Counts': hci_event_counts
    }

    hci_acl_stats = {
        'ACL LE Protocols Used': df_acl_le_events['LE Protocol'].nunique(),
        'Outgoing Data Packets': outgoing_acl_events,
        'Incoming Data Packets': incoming_acl_events
    }

    generate_pcap_report(summary_stats, hci_command_event_stats, hci_command_event_info, hci_acl_stats, l2cap_acl_packet_counts, host_device_info, controller_device_info)

if __name__=="__main__":
    main()