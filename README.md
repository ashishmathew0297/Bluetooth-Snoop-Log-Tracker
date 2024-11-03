# btsnoop_tracker

This project aims to capture and study data packets from bluetooth low energy (BLE) devices connecting to an android phone. Here, we will be identifying the types of devices connecting to the phone, the types of communication protocols they used, and the timeframe over which they connected. The output here will be a report/dashboard of all the information on the devices that have connected to the phone within the timeframes of which the reports have been generated.

## Devices Used

The devices used in this project are:
- A Google Pixe 7 Pro, running Android 14
- A raspberry pi running debian linux
- A laptop running Ubuntu 24.04 under WSL

The WSL system is only used to develop the report generating application in a linux-like environment. Adb commands do not easily work under WSL as it doesn't support USB reading 

## Linux Packages Used

- `unzip`: This package is used to decompress zip files and may not always be present in every linux installation. It can be installed with the following command.

```bash
sudo apt install unzip
```

- `adb`: Android Debug Bridge (adb) is a tool used by developers to iterface with an Android device and perform a variety of functions such as installing apps, debugging issues and, as per our use case, generate logs from the device all through a Unix shell. The following command can be used to install adb in Linux.

```bash
sudo apt install adb
```

- `tshark`: A CLI took which works as a network protocol analyzer

```bash
sudo apt install tshark
```

## Installing the python package requirements

The python packages for this project can be installed through the `requirements.txt` file as follows.

```bash
pip install -r /path/to/requirements.txt
```
## Running the code

The code requires a python virtual environment which can be set up with the following command

```bash
python/python3 -m venv <env_name>
source <env_name>/bin/activate
```

The requirements.txt file has a lot in it, but the main packages of importance here are
- jupyterlab
- notebook
- btsnoop (by Travis W Peters): The installation for this file was taken directly from git. It can be installed with the command below
```bash
pip install git+https://github.com/traviswpeters/btsnoop.git#egg=btsnoop
```
