# Santiago Tobon & Cody Jeffries
# CS410 - Comp, Sound, and Music
# Spring 2021
# References
# https://pythonaudiosynthesisbasics.com/
# https://github.com/wybiral/python-musical/blob/master/musical/audio/effect.py
# https://github.com/pdx-cs-sound/fft-filter/blob/main/fft-filter.py
# https://github.com/wybiral/python-musical/blob/master/musical/audio/source.py
# https://www2.cs.uic.edu/~i101/SoundFiles/
# https://www.ee.columbia.edu/~dpwe/sounds/music/

import wave
import math
import struct
import sounddevice as sd
import numpy as np 
import time
from numpy import loadtxt
from playsound import playsound
from scipy.io.wavfile import write

"""
def sine_wave(freq, params):
    ampl = .16666
    wave = np.zeros(params.nframes)
    for x in range(params.nframes):
        sin_val = math.sin(2 * math.pi * freq * x / params.nframes)
        wave[x] = np.int16(sin_val * 32767 * ampl)
    return wave
"""

def sine_wave(freq, length, rate=44100, phase=0.0):
    data = generate_wave_input(freq, length, rate, phase)
    return np.sin(data)

def generate_wave_input(freq, length, rate=44100, phase=0.0):
    length = int(length * rate)+1
    #print(length)
    t = np.arange(length) / float(rate)
    omega = float(freq) * 2 * math.pi
    phase *= 2 * math.pi  
    return omega * t + phase

def read_wave(filename):
    with wave.open(filename, "rb") as w:
        nframes = w.getnframes()
        frames = w.readframes(nframes)
        framedata = struct.unpack(f"<{nframes}h", frames)
        samples = [s / (1 << 15) for s in framedata]
        return w.getparams(), samples

def write_wave(filename, samples, params):
    nframes = len(samples)
    framedata = [int(r * (1 << 15)) for r in samples]
    frames = struct.pack(f"<{nframes}h", *framedata)
    with wave.open(filename, "wb") as w:
        w.setparams(params)
        w.writeframes(frames)

def modulated_delay(data, modwave, dry, wet):
    ''' Use LFO "modwave" as a delay modulator (no feedback)
    '''
    out = data.copy()
    #print(len(modwave))
    #print(len(data))
    for i in range(len(data)-1):
        index = int(i - modwave[i])
        if index >= 0 and index < len(data):
            out[i] = data[i] * dry + data[index] * wet
    return out


def feedback_modulated_delay(data, modwave, dry, wet):
    ''' Use LFO "modwave" as a delay modulator (with feedback)
    '''
    out = data.copy()
    #print(len(modwave))
    #print(len(data))
    for i in range(len(data)-2):
        index = int(i - modwave[i])
        if index >= 0 and index < len(data):
            out[i] = out[i] * dry + out[index] * wet
    return out

def chorus(data, freq, dry=0.5, wet=0.5, depth=1.0, delay=25.0, rate=44100):
    length = float(len(data)) / rate
    mil = float(rate) / 1000
    delay *= mil
    depth *= mil
    modwave = (sine_wave(freq, length) / 2 + 0.5) * depth + delay
    return modulated_delay(data, modwave, dry, wet)

def flanger(data, freq, dry=0.5, wet=0.5, depth=20.0, delay=1.0, rate=44100):
    length = float(len(data)) / rate
    mil = float(rate) / 1000
    delay *= mil
    depth *= mil
    modwave = (sine_wave(freq, length) / 2 + 0.5) * depth + delay
    return feedback_modulated_delay(data, modwave, dry, wet)

def tremolo(data, freq, dry=0.5, wet=0.5, rate=44100):
    length = float(len(data)) / rate
    modwave = (sine_wave(freq, length) / 2 + 0.5)
    #print(len(modwave), len(data))
    #print(type(data), type(modwave))
    return (data * dry) + ((data * modwave) * wet)

#playsound("Recorded Wav Files/Fanfare60.wav")
params, samples = read_wave("Sample Wav Files/africa-toto.wav")
#print(params)
samples = np.asarray(samples)
"""
output = chorus(samples, freq=3.14159)
write_wave("Recorded Wav Files/chorus-africa-toto.wav", output, params)
"""
output = flanger(samples, freq=10)
write_wave("Recorded Wav Files/flanger-africa-toto.wav", output, params)

output = tremolo(samples, freq=100)
write_wave("Recorded Wav Files/tremolo-africa-toto.wav", output, params)
