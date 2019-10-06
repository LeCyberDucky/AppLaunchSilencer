# Damn you Forza. Why are you so loud?

import os
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import time


with open("Settings.config") as inFile:
    settings = dict([line.split(": ") for line in inFile])

settings["launcher path"] = settings["launcher path"].strip()
settings["process"] = settings["process"].strip()
settings["launch volume"] = float(settings["launch volume"])/100
settings["target volume"] = float(settings["target volume"])/100
settings["delay"] = int(settings["delay"])

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

volume.SetMasterVolume(settings["launch volume"], None)

time.sleep(settings["delay"])

# Make sure process wasn't closed while sleeping
sessions = AudioUtilities.GetAllSessions()
for session in sessions:
    if session.Process and session.Process.name() == settings["process"]:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        volume.SetMasterVolume(settings["target volume"], None)
