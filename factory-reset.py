#!/usr/bin/env python3
import os.path
import subprocess
import sys
import time
import urllib.request
import zipfile


def start_adb_server():
    subprocess.check_call(["adb", "start-server"])


def wait_for_device():
    """Block until a device has appeared in the Android Debug Bridge."""
    print("Waiting for a device… ", end="")
    sys.stdout.flush()
    subprocess.check_call(["adb", "wait-for-device"])
    print("found!")


def reboot(target):
    print("Rebooting to {target}.".format(target=target))
    subprocess.check_call(["adb", "reboot", target])


def recovery_wipe_data():
    print("Wiping data.")
    subprocess.check_call(["adb", "shell", "recovery", "--wipe_data"])


def download_chromium(source_url="https://storage.googleapis.com/chromium-browser-continuous/Android/296734/chrome-android.zip",
                      destination_filename="chromium.zip"):
    print("Downloading Chromium… ", end="")
    sys.stdout.flush()
    if os.path.exists(destination_filename):
        print("skipped.")
    else:
        with urllib.request.urlopen(source_url) as source:
            with open(destination_filename, "wb") as destination:
                destination.write(source.read())
        print("done.")


def extract_chromium(zip_filename="chromium.zip", apk_filename="chromium.apk"):
    print("Extracting Chromium… ", end="")
    sys.stdout.flush()
    with zipfile.ZipFile(zip_filename) as file:
        with open(apk_filename, "wb") as apk_out:
            data = file.read("chrome-android/apks/ChromeShell.apk")
            apk_out.write(data)
    print("done.")


if __name__ == "__main__":
    start_adb_server()
    download_chromium()
    extract_chromium()
    while True:
        wait_for_device()
        reboot("recovery")
        input("Press return when device is in recovery mode.")
        recovery_wipe_data()
        input("Press return to reset next device.")
