#!/usr/bin/env python3
import subprocess
import sys
import time


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


while True:
    wait_for_device()
    reboot("recovery")
    input("Press return when device is in recovery mode.")
    recovery_wipe_data()
    input("Press return to reset next device.")
