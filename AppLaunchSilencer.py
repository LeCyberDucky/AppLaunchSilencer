# Damn you Forza. Why are you so loud?

import os
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import time

def volume_to_range(vol):
    # Maps input volume from range [0; 100] to [0; 1]
    return float(vol)/100

with open("Settings.config") as inFile:
    settings = dict([line.split(": ") for line in inFile])

settings["launcher path"] = settings["launcher path"].strip()
settings["process"] = settings["process"].strip()
settings["launch volume"] = int(settings["launch volume"])
settings["target volume"] = int(settings["target volume"])
settings["delay"] = int(settings["delay"])
settings["transition time"] = int(settings["transition time"])

# Execute wanted program
os.startfile(settings["launcher path"])

processFound = False

while not processFound:
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name() == settings["process"]:
            processFound = True
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
    time.sleep(1)

volume.SetMasterVolume(volume_to_range(settings["launch volume"]), None)

if settings["launch volume"] == settings["target volume"]:
    quit()

time.sleep(settings["delay"])

# Gradually turn volume back up
for volume_level in range(settings["launch volume"], settings["target volume"], 1):
    # Make sure process wasn't closed while sleeping
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name() == settings["process"]:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            volume.SetMasterVolume(volume_to_range(volume_level), None)

    time.sleep(settings["transition time"] / (settings["target volume"] - settings["launch volume"]))


# Set final volume level. Make sure process wasn't closed while sleeping
sessions = AudioUtilities.GetAllSessions()
for session in sessions:
    if session.Process and session.Process.name() == settings["process"]:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        volume.SetMasterVolume(volume_to_range(settings["target volume"]), None)


