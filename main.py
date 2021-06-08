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

def bandpass_filter(data, fs, nyq, low, high, seconds):
    fs = fs  # Sample rate
    seconds = seconds  # Duration of recording
    nyq = nyq * fs
    frequency_low = low / nyq
    frequency_high = high / nyq
    sos = butter(5, [frequency_low, frequency_high], btype='bandpass', output='sos')
    y = sosfiltfilt(sos, data)
    return y, fs

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
                    '-ft nyq low high seconds')
    parser.add_argument('-p', '--play',
                    type=str,
                    help='Audio file you want to play')

    args = parser.parse_args()

    try:
        main(args)
    except KeyboardInterrupt:
        print('Goodbye!')
