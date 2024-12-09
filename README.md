# Bluetooth Snoop Log Tracker and Report Generation Tool

This project aims to capture and study data packets from bluetooth low energy (BLE) devices connecting to an Android smartphone. This tool will identify the types of devices connecting to the smartphone, the types of communication protocols used, and the timeframe over which the devices were connected. The output here will be a PDF report of all the packet information within the timeframe of which the reports have been generated.

## Hardware Requirements

The hardware needed for this project are:
- An Android phone, ideally running Android 14 as this code was developed and confirmed to work with a device running this version.
- A laptop running a Debian-based Linux distribution. Ubuntu has the best support.
- A USB connector that allows data transfer.

## Software Requirements

The following packages are required for the program to work as expected.

- `unzip`: This package is used to decompress zip files and may not always be present in every linux installation. It can be installed with the following command.

- `adb`: Android Debug Bridge (adb) is a tool used by developers to iterface with an Android device and perform a variety of functions such as installing apps, debugging issues and, as per our use case, generate logs from the device all through a Unix shell. The following command can be used to install adb in Linux.

- `tshark`: A CLI took which works as a network protocol analyzer.

```bash
sudo apt install unzip adb tshark
```

The report generation part of this project is in Python 3.12.7.

## Setting up an Environment and Installing the Python Requirements

The code can be run in an anaconda virtual environment which can be set up and activated with the following commands.

```bash
conda create --name <env_name>
conda activate <env_name>
```

Once this is done, install pip into the current environment.

```bash
conda install pip
```

Now you will be able to install the packages for this project from the `requirements.txt` file as follows.

```bash
pip install -r requirements_pip.txt
```

You can also do the same in a single line through the following command:

```bash
conda create --name <env_name> --file requirements_conda.txt
```

Finally, the bash script running our code will need execution permissions. In a terminal, move into the src folder of the project and run the below line:

```bash
chmod +x run_scripts.sh
```
## Preparing the Android Device

Once the packages have been installed and the environment set up and activated, you can now run the code. However, we need to set up the mobile phone whose bluetooth reports we want to generate so that it works as expected. We need to ensure that the Android phone used has its USB debugging and HCI Snoop log generation features enabled. This is only available if developer mode is enabled, the instructions for which varies for different Android devices and versions. The general process is as follows:

1. Go through your phone settings to find the build number. The general path to finding it is `Settings > About Phone > Build Number`.
2. Tapping the build number a few times will enable the developer options, which This is what allows for generating the bluetooth packet capture report files.
3. Go back to the Settings homepage and scroll down to find the Developer Options and enable it.
5. In the Developer Options screen, look for the `Enable USB Debugging` and `Enable Bluetooth HCI snoop log` options and enable them.

It is advised to disable these options once you are done working with this tool.

## Running the Tool and Generating the Reports

Once the environment has been set up and the device has the required developer options enabled, follow the steps below to run the tool and generate the Bluetooth packet report.

1. Connect your Android device to the laptop on which the repository and environment is set up.
2. Check your mobile device. A prompt will show up asking if you would like to allow bluetooth debugging with your laptop. Click "yes".
3. If the prompt in the previous step doesn't show up, try disconnecting and reconnecting the device. Sometimes this prompt might appear even later (Refer to step 6).
4. Open a shell terminal and navigate to the `src` folder in the project repository.
5. Run the `run_scripts.sh` file with the following command.
  ```bash
  ./run_scripts.sh
  ```
6. If the popup step 2 has not occurred yet, it should show up now on your mobile device. Select "yes".
7. Wait for the code to execute. This can take upto a minute.

The above process will run the shell script that does the following:

- Using ADB, the tool will extract the latest bug reports from the phone in a zip file.
- It will then extracts the Bluetooth logs from the zip file.
- Using tshark, the tool filters relevant information from the logs.
- It then executes the `bluetooth_report_generator.py` python script to generate the reports from the file.
- Outputs of the reports will be generated in the `src/outputs` folder.
