#!/usr/bin/env python3
import argparse
import os
import os.path
import subprocess
import sys
import time
import urllib.request
import zipfile

import yaml


def start_adb_server():
    """Start the ADB server."""
    subprocess.check_call(["adb", "start-server"])


def wait_for_device():
    """Block until a device has appeared in the Android Debug Bridge."""
    print("Waiting for a device… ", end="")
    sys.stdout.flush()
    subprocess.check_call(["adb", "wait-for-device"])
    print("found!")


def reboot(target):
    """Reboot the tablet to a specific target."""
    print("Rebooting to {target}.".format(target=target))
    subprocess.check_call(["adb", "reboot", target])


def recovery_wipe_data():
    """Wipe the data on the tablet when in recovery mode."""
    print("Wiping data… ", end="")
    subprocess.check_call(["adb", "shell", "recovery", "--wipe_data"])
    print("done.")


def download(source_url, destination_filename):
    """Download the a file locally."""
    print("Downloading '{}'… ".format(source_url), end="")
    sys.stdout.flush()
    if os.path.exists(destination_filename):
        print("skipped.")
    else:
        with urllib.request.urlopen(source_url) as source:
            with open(destination_filename, "wb") as destination:
                destination.write(source.read())
        print("done.")


def download_chromium():
    """Download Chromium."""
    download("https://storage.googleapis.com/chromium-browser-continuous/Android/296734/chrome-android.zip",
             "chromium.zip")


def extract_chromium(zip_filename="chromium.zip", apk_filename="chromium.apk"):
    """Extract the Chromium zip file and pull out of the 'ChromeShell' APK."""
    print("Extracting Chromium… ", end="")
    sys.stdout.flush()
    with zipfile.ZipFile(zip_filename) as file:
        with open(apk_filename, "wb") as apk_out:
            data = file.read("chrome-android/apks/ChromeShell.apk")
            apk_out.write(data)
    print("done.")


def install_apk(apk_filename):
    """Install an APK onto a tablet."""
    print("Installing '{}'… ".format(apk_filename), end="")
    sys.stdout.flush()
    subprocess.check_call(["adb", "install", "-r", apk_filename])
    print("done.")


def push_file_to_tablet(local, remote):
    """Push a file to the tablet."""
    print("Pushing '{}' to the tablet… ".format(local), end="")
    sys.stdout.flush()
    subprocess.check_call(["adb", "push", local, remote])
    print("done.")


def write_wifi_file(ssid, password):
    """Generate and write a WiFi configuration file for the tablet."""
    print("Writing WiFi file… ", end="")
    sys.stdout.flush()
    with open("wifi", "w") as file:
        file.write(ssid)
        file.write("\n")
        file.write(password)
        file.write("\n")
    print("done.")
    push_file_to_tablet("wifi", "/sdcard/wifi")
    os.remove("wifi")


def write_tla_file(tla):
    print("Writing TLA file… ", end="")
    sys.stdout.flush()
    with open("tla", "w") as file:
        file.write(tla)
        file.write("\n")
    print("done.")
    push_file_to_tablet("tla", "/sdcard/tla")
    os.remove("tla")


def write_part_code_file(part_code):
    print("Writing Part Code file… ", end="")
    sys.stdout.flush()
    with open("part_code", "w") as file:
        file.write(part_code)
        file.write("\n")
    print("done.")
    push_file_to_tablet("part_code", "/sdcard/part_code")
    os.remove("part_code")


def save_table_info_file(tla, serial_number, part_code):
    print("Saving information about the tablet… ", end="")
    sys.stdout.flush()
    mac_address = subprocess.check_output(["adb", "shell", "cat",
                                           "/sys/class/net/wlan0/address"])
    mac_address = str(mac_address.strip(), "utf-8")
    with open("tablet-{}.yaml".format(tla.upper()), "w") as fd:
        fd.write("serial_number: {}\n".format(serial_number))
        fd.write("mac_address: {}\n".format(mac_address))
        fd.write("part_code: {}\n".format(part_code))
    print("done.")


def create_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("serial_number", help="Serial number of the tablet.")
    parser.add_argument("tla", help="TLA of the team getting the tablet.")
    parser.add_argument("part_code", help="Part code of the tablet.")
    parser.add_argument("--wifi_file", default="wifi.yaml",
                        help="Location of file containing WiFi keys (default" \
                             " to wifi.yaml).")
    return parser


if __name__ == "__main__":
    args = create_argument_parser().parse_args()

    serial_number = args.serial_number
    tla = args.tla

    with open(args.wifi_file) as fd:
        wifi_password = yaml.safe_load(fd.read())[tla]

    print("Using {} as the WiFi password.".format(wifi_password))
    part_code = args.part_code

    os.environ["ANDROID_SERIAL"] = serial_number

    start_adb_server()
    download_chromium()
    extract_chromium()
    wait_for_device()
    reboot("recovery")
    time.sleep(80)

    # for some unknown reason the tablets reset to a serial number of this
    os.environ["ANDROID_SERIAL"] = "0123456789ABCDEF"

    recovery_wipe_data()

    # and back we go
    os.environ["ANDROID_SERIAL"] = serial_number

    time.sleep(10)
    print("!!! Now re-enable USB debugging on the tablet. !!!")
    wait_for_device()
    install_apk("chromium.apk")
    install_apk("../app/app/build/outputs/apk/app-debug.apk")
    write_wifi_file("robot-{}".format(tla.upper()), wifi_password)
    write_tla_file(tla)
    write_part_code_file(part_code)
    print("!!! Now install Student Robotics app to the homescreen. !!!")
    print("!!! Now run the Student Robotics app. !!!")
    input("Press return when done.")
    save_table_info_file(tla, serial_number, part_code)
    print("DONE!")
