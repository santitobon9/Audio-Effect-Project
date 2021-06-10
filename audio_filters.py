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
from scipy.signal import butter, sosfilt, convolve, sosfiltfilt

def bandpass_filter(data, fs, filter_args):
    nyq = filter_args[0] * fs
    frequency_low = filter_args[1] / nyq
    frequency_high = filter_args[2] / nyq
    seconds = filter_args[3]
    sos = butter(5, [frequency_low, frequency_high], btype='bandpass', output='sos')
    y = sosfiltfilt(sos, data)
    return y, fs

def reverb(data, fs=44100, delay=100, decay_factor=0.5):

    normal = np.copy(data)
    comb1 = comb_filt(data, delay, decay_factor, fs)
    comb2 = comb_filt(data, (delay - 11.73), (decay_factor - 0.1313), fs)
    comb3 = comb_filt(data, (delay + 19.31), (decay_factor - 0.2743), fs)
    comb4 = comb_filt(data, (delay - 7.97), (decay_factor - 0.31), fs)

    combed = sum([comb1, comb2, comb3, comb4])

    for points in combed:
        i = 0
        combed[i] = (normal[i] * 0.5) + (points * 0.5)

    pass1 = allpass_filt(combed, fs)
    pass2 = allpass_filt(pass1, fs)

    return pass2

def comb_filt(data, delay, decay_factor, sample_rate):
    delay_samples = int(delay * (sample_rate/1000))
    for sample in data:
        i = 0
        data[i + delay_samples] += data[i] * decay_factor
    return data

def allpass_filt(data, sample_rate):
    delay_samples = int(89.27 * (sample_rate/1000))
    decay_factor = 0.131
    max_val = 0.0

    for sample in data:
        i = 0
        if (i - delay_samples >= 0):
            data[i] += -decay_factor * data[i-delay_samples]
        if (i - delay_samples >= 1):
            data[i] += decay_factor * data[i+20-delay_samples]
        i += 1
    
    value = data.flat[0]
    for sample in data:
        if abs(sample) > max_val:
            max_val = abs(sample)

    for sample in data:
        i = 0
        test = sample
        data[i] = (value + (test - value)) / max_val

    return data

def sine_wave(freq, length, rate=44100, phase=0.0):
    data = generate_wave_input(freq, length, rate, phase)
    return np.sin(data)

def generate_wave_input(freq, length, rate=44100, phase=0.0):
    length = int(length * rate)
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
    for i in range(len(data)-1):
        index = int(i - modwave[i])
        if index >= 0 and index < len(data):
            out[i] = data[i] * dry + data[index] * wet
    return out


def feedback_modulated_delay(data, modwave, dry, wet):
    ''' Use LFO "modwave" as a delay modulator (with feedback)
    '''
    out = data.copy()
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
    return (data * dry) + ((data * modwave) * wet)
