# Bluetooth Log Report Generator

This project aims to capture and study data packets from bluetooth low energy (BLE) devices connecting to an android phone. Here, we will be identifying the types of devices connecting to the phone, the types of communication protocols they used, and the timeframe over which they connected. The output here will be a report/dashboard of all the information on the devices that have connected to the phone within the timeframe of which the reports have been generated.

## Devices Used

The devices needed for this project are:
- An android phone, ideally running Android 14 as this code was developed with a device running that Android version
- A laptop running a Debian-based Linux distribution. Ubuntu has the best support.

## Package installation

- `unzip`: This package is used to decompress zip files and may not always be present in every linux installation. It can be installed with the following command.

- `adb`: Android Debug Bridge (adb) is a tool used by developers to iterface with an Android device and perform a variety of functions such as installing apps, debugging issues and, as per our use case, generate logs from the device all through a Unix shell. The following command can be used to install adb in Linux.

- `tshark`: A CLI took which works as a network protocol analyzer

```bash
sudo apt install unzip adb tshark
```

## Setting up an Environment and Installing the Python Requirements

The code can be run in an anaconda virtual environment which can be set up and activated with the following commands

```bash
conda create --name <env_name>
conda activate <env_name>
```

Once this is done, install pip into the current environment

```bash
conda install pip
```

Now you will be able to install the packages for this project from the `requirements.txt` file as follows.

```bash
pip install -r /path/to/requirements.txt
```

You can also do the same in a single line through the following

```bash
conda create --name <env_name> --file path/to/requirements.txt
```

Finally, the bash script that will be running our code will need execution permissions. In a terminal, move into the src folder of the project and run the below line:

```bash
chmod +e run_scripts.sh
```

## Running the code and generating the reports

Once the packages have been installed and the environment set up and activated you can now run the code. We now set up the mobile phone whose bluetooth reports we want to generate.

### Enabling Developer Options on your android phone

The first step to take is ensuring that your android phone has its USB debugging feature enabled. This is only available if developer mode is enabled, the instructions for which varies for different android devices and versions. The general process is as follows:

1. Go through your phone settings to find the build number. The general path to finding it is `Settings > About Phone > Build Number`.
2. Tapping the build number a few times will enable the developer options, which This is what allows for generating the bluetooth packet capture report files.
3. Go back to the Settings homepage and scroll down to find the Developer Options and enable it.
4. In the Developer Options screen, look for the `USB Debugging` option and enable it.

### Generating Reports

1. Connect your device to the laptop on which the repository and environment is set up.
2. Check your mobile phone. A prompt will show up asking if you would like to allow bluetooth debugging with your laptop. Click yes.
3. If the 
4. Open a shell terminal and navigate to the src folder in the project repository
5. Run the `run_scripts.sh` file with the following command
  ```bash
  ./run_scripts.sh
  ```
6. If the popup step 2 has not occurred yet, it should show up now. Select yes.
- Wait for the code to execute.

The above process will run the shell script that does the following

- Using ADB, it extracts the bug reports from the phone in a zip file.
- Extracts the Bluetooth logs from the zip file
- Uses tshark to filter relevant information from the logs
- Runs the `bluetooth_report_generator.py` python script to generate the reports from the file.
- Outputs the reports in the `src/outputs` folder.
