# Damn you Forza. Why are you so loud?

from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import time


with open("Settings.config") as inFile:
    settings = dict([line.split(":") for line in inFile])

settings["process"] = settings["process"].strip()
settings["launch volume"] = float(settings["launch volume"])/100
settings["target volume"] = float(settings["target volume"])/100
settings["delay"] = int(settings["delay"])

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

volume.SetMasterVolume(settings["target volume"], None)
