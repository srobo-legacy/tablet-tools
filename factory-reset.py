#!/usr/bin/env python3
import subprocess
import sys
import time


def wait_for_device():
    """Block until a device has appeared in the Android Debug Bridge."""
    print("Waiting for a device… ", end="")
    sys.stdout.flush()
    exit_code = subprocess.call(["adb", "wait-for-device"])
    assert exit_code == 0
    print("found!")


def reboot(target):
    print("Rebooting to {target}.".format(target=target))
    exit_code = subprocess.call(["adb", "reboot", target])
    assert exit_code == 0


def recovery_wipe_data():
    print("Wiping data.")
    exit_code = subprocess.call(["adb", "shell", "recovery", "--wipe_data"])
    assert exit_code == 0


while True:
    wait_for_device()
    reboot("recovery")
    # wait_for_device()
    time.sleep(30)
    recovery_wipe_data()
    input("Press return to continue.")
