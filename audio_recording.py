# Santiago Tobon & Cody Jeffries
# CS410 - Comp, Sound, and Music
# Spring 2021
# References
# https://realpython.com/playing-and-recording-sound-python/
# https://www.geeksforgeeks.org/create-a-voice-recorder-using-python/

import wave
import math
import struct
import sounddevice as sd
import numpy as np 
import time
from numpy import loadtxt
from playsound import playsound
from scipy.io.wavfile import write
from countdown import countdown

def record_audio(time, output_file, fs=44100,):
    print("Will start recording in 5 seconds!!")
    countdown(mins=0, secs=5)
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write("Recorded Wav Files/"+output_file, fs, myrecording.astype(np.int16))  # Save as WAV file
    print("Recording Complete!") 
