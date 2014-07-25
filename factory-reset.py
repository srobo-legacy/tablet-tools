#!/usr/bin/env python3
import subprocess


def wait_for_device():
    """Block until a device has appeared in the Android Debug Bridge."""
    print("Waiting for a device…")
    exit_code = subprocess.call(["adb", "wait-for-device"])
    assert exit_code == 0


def factory_reset():
    print("Performing factory reset.")
    process = subprocess.Popen(["adb", "shell"], stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate(input="recovery --wipe_data")


while True:
    wait_for_device()
    factory_reset()
    input("Press return to continue.")
