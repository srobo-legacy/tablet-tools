#!/usr/bin/env python3
import os.path
import subprocess
import sys
import time
import urllib.request
import zipfile


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
    donwload("https://storage.googleapis.com/chromium-browser-continuous/Android/296734/chrome-android.zip",
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
    subprocess.check_call(["adb", "install", apk_filename])
    print("done.")


def write_wifi_file(filename="wifi"):
    """Generate and write a WiFi configuration file for the tablet."""
    print("Writing WiFi file… ", end="")
    ssid = input("WiFi SSID: ")
    password = input("WiFi Password: ")
    with open(filename, "w") as file:
        file.write(ssid)
        file.write("\n")
        file.write(password)
        file.write("\n")
    print("done.")


def push_file_to_tablet(local, remote):
    """Push a file to the tablet."""
    print("Pushing '{}' to the tablet… ", end="")
    subprocess.check_call(["adb", "push", local, remote])


if __name__ == "__main__":
    start_adb_server()
    download_chromium()
    extract_chromium()
    while True:
        wait_for_device()
        reboot("recovery")
        input("Press return when device is in recovery mode.")
        recovery_wipe_data()
        input("Press return when USB debugging has been re-enabled.")
        wait_for_device()
        install_apk("chromium.apk")
        install_apk("app/build/outputs/apk/app-debug.apk")
        write_wifi_file()
        push_file_to_tablet("wifi", "/sdcard/wifi")
        os.remove("wifi")
        input("Press return to reset next device.")