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

fs = 44100  # Sample rate
seconds = 3  # Duration of recording
output_file = 'Recorded Wav Files/test.wav'

def record_audio(fs, time, output_file):
    print("Will start recording in 5 seconds!!")
    countdown(mins=0, secs=5)
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write(output_file, fs, myrecording.astype(np.int16))  # Save as WAV file 

record_audio(fs, seconds, output_file)
time.sleep(1)
playsound(output_file)
