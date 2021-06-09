# Santiago Tobon & Cody Jeffries
# CS410 - Comp, Sound, and Music
# Spring 2021
import argparse
import sounddevice as sd
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, sosfilt, convolve, sosfiltfilt
from scipy.io.wavfile import write

def play_sound_file(filename):
    """
    Attempts to play a sound file given a filename.
    :param filename: str
        .wav file
    :return: N/A no return
    """
    # Extract data and sampling rate from file 
    data, fs = sf.read(filename)
    sd.play(data, fs)
    sd.wait()  # Wait until file is done playing

def sine_wave(freq):
    """
    generates a sine wave given a specific frequency.
    freq: float
    :return: numpy array
    """
    fs = 48000  # Sample rate
    seconds = 1  # Duration of recording
    frequency = freq
    x = np.linspace(0, seconds * 2 * np.pi, int(seconds * fs))
    sine_wave_data = np.sin(frequency * x) 
    sine_wave_data = np.int16(sine_wave_data * 8192)
    return sine_wave_data

def bandpass_filter(data, fs, filter_args):
    nyq = filter_args[0] * fs
    frequency_low = filter_args[1] / nyq
    frequency_high = filter_args[2] / nyq
    seconds = filter_args[3]
    sos = butter(5, [frequency_low, frequency_high], btype='bandpass', output='sos')
    y = sosfiltfilt(sos, data)
    return y, fs

def reverb(data, fs, delay, decay_factor):

    normal = np.copy(data)
    comb1 = comb_filt(data, delay, decay_factor, fs)
    comb2 = comb_filt(data, (delay - 11.73), (decay_factor - 0.1313), fs)
    comb3 = comb_filt(data, (delay + 19.31), (decay_factor - 0.2743), fs)
    comb4 = comb_filt(data, (delay - 7.97), (decay_factor - 0.31), fs)

    combed = sum([comb1, comb2, comb3, comb4])

    for points in combed:
        i = 0
        # print('1:', combed[i])
        combed[i] = (normal[i] * 0.5) + (points * 0.5)
        # print('2:', combed[i])
    #     if points > 1:
    #         print('Points being mixed: ', points)
    # print('Here: ', max(combed))

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
            # print('max before: ', max_val)
            # print('sample:', abs(sample))
            max_val = abs(sample)
            # print('max after: ', max_val)

    for sample in data:
        i = 0
        test = sample
        data[i] = (value + (test - value)) / max_val

    return data

def main(args):

    # # Example for using bandpass_filter
    # # Plays sine wave first followed by filtered sine wave which is now sounds like white noise

    # sample_rate = 48000
    # sine = sine_wave(440)
    # sd.play(sine, sample_rate)
    # sd.wait()
    # write('testing_sine.wav', sample_rate, sine)
    # sine, sample_rate = bandpass_filter(sine, sample_rate, 0.1, 500, 1000, 1)
    # sd.play(sine, sample_rate)
    # sd.wait()
    # write('testing_bandpass.wav', sample_rate, sine)

    data, fs = sf.read(args.file)
    # play_sound_file('Recorded Wav Files/gc.wav')
    data = reverb(data, fs, 100, 0.5)
    write('testing_reverb.wav', fs, data)
    # play_sound_file('testing_reverb.wav')
    if args.filter:
        if not args.file:
            print('No file submitted using sine wave')
        else:
            data, fs = sf.read(args.file)
            data, fs = bandpass_filter(data, fs, args.filter)
            write(args.file, fs, data)

    print("Goodbye")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Audio Effects',
                                description='Simple Audio Effects'
                                ' program for sound and music',
                                allow_abbrev=False)
    parser.add_argument('-r', '--record',
                    type=str,
                    default='temp-file',
                    help='Audio filename to save recording')
    parser.add_argument('-lf', '--load_file',
                    type=str,
                    help='Audio file to load')
    parser.add_argument('-f', '--file',
                    type=str,
                    help='new file name to save audio')
    parser.add_argument('-ft', '--filter',
                    nargs='+',
                    help='Filter you want to apply to audio file'
                    'Must include following arguments'
                    '-ft <nyq low high seconds>')
    parser.add_argument('-p', '--play',
                    type=str,
                    help='Audio file you want to play')

    args = parser.parse_args()

    try:
        main(args)
    except KeyboardInterrupt:
        print('Goodbye!')
