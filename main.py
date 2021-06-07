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

def bandpass_filter(data, fs):
    fs = fs  # Sample rate
    seconds = 1  # Duration of recording
    nyq = 0.1 * fs
    # print(nyq)
    frequency_low = 1 / nyq
    frequency_high = 500 / nyq
    sos = butter(5, [frequency_low, frequency_high], btype='bandpass', output='sos')
    #y = sosfilt(sos, data)
    y = sosfiltfilt(sos, data)
    return y, fs

def main(args):
    data, sample_rate = sf.read(args.load_file)
    play_sound_file(args.load_file)
    # plt.plot(data)
    # plt.show()
    # print('Max: ', max(data), 'Min: ', min(data))
    data, sample_rate = bandpass_filter(data, sample_rate)
    # autocorr = fftconvolve(data, data[::-1], mode='full')
    # print('Max: ', max(data), 'Min: ', min(data))
    # time = np.linspace(0, 1 * 2 * np.pi, sample_rate)
    sd.play(data, sample_rate)
    sd.wait()
    plt.plot(data)
    plt.show()
    write('testing.wav', sample_rate, data)


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
    parser.add_argument('-af', '--apply_filter',
                    type=str,
                    help='Filter you want to apply to audio file')
    parser.add_argument('-p', '--play',
                    type=str,
                    help='Audio file you want to play')

    args = parser.parse_args()

    try:
        main(args)
    except KeyboardInterrupt:
        print('Goodbye!')
