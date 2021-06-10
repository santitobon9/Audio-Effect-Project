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
from os import listdir
from os.path import isfile, join
from playsound import playsound
import audio_filters as af
import audio_recording as ar

def display_samples():
    path = "Sample Wav Files/"
    wav_files = [f for f in listdir(path) if isfile(join(path, f))]
    print("Samples:")
    print(wav_files)
    print()

def display_recorded():
    path = "Recorded Wav Files/"
    wav_files = [f for f in listdir(path) if isfile(join(path, f))]
    print("Recorded:")
    print(wav_files)
    print()

def effects_menu():
    quit = False
    while(quit==False):
        print("Effects Menu:")
        print("1. Apply Chorus")
        print("2. Apply Flanger")
        print("3. Apply Tremolo")
        print("4. Apply Reverb")
        print("5. Apply Bandpass Filter")
        print("6. Back to Main Menu")
        val = input()

        if(val == '1'):
            display_samples()
            display_recorded()
            filename = input("What Wav file would you like to apply the effect to? (ex: test.wav)  ")
            dic = input("Is this in samples or recorded?  ")
            if (dic=="samples"):
                folder = "Sample Wav Files/"
            elif (dic=="recorded"):
                folder = "Recorded Wav Files/"
            else: 
                print("Invalid Input")
                continue
            params, samples = af.read_wave(folder + filename)
            output = af.chorus(np.asarray(samples), freq=3.14159)
            output_file = "Recorded Wav Files/" + "chorus-" + filename
            af.write_wave(output_file, output, params)
        elif(val == '2'):
            display_samples()
            display_recorded()
            filename = input("What Wav file would you like to apply the effect to? (ex: test.wav)  ")
            dic = input("Is this in samples or recorded?  ")
            if (dic=="samples"):
                folder = "Sample Wav Files/"
            elif (dic=="recorded"):
                folder = "Recorded Wav Files/"
            else: 
                print("Invalid Input")
                continue
            params, samples = af.read_wave(folder + filename)
            output = af.flanger(np.asarray(samples), freq=10)
            output_file = "Recorded Wav Files/" + "flanger-" + filename
            af.write_wave(output_file, output, params)
        elif(val == '3'):
            display_samples()
            display_recorded()
            filename = input("What Wav file would you like to apply the effect to? (ex: test.wav)  ")
            dic = input("Is this in samples or recorded?  ")
            if (dic=="samples"):
                folder = "Sample Wav Files/"
            elif (dic=="recorded"):
                folder = "Recorded Wav Files/"
            else: 
                print("Invalid Input")
                continue
            params, samples = af.read_wave(folder + filename)
            output = af.tremolo(np.asarray(samples), freq=100)
            output_file = "Recorded Wav Files/" + "tremolo-" + filename
            af.write_wave(output_file, output, params)
        elif(val == '4'):
            display_samples()
            display_recorded()
            filename = input("What Wav file would you like to apply the effect to? (ex: test.wav)  ")
            dic = input("Is this in samples or recorded?  ")
            if (dic=="samples"):
                folder = "Sample Wav Files/"
            elif (dic=="recorded"):
                folder = "Recorded Wav Files/"
            else: 
                print("Invalid Input")
                continue
            params, samples = af.read_wave(folder + filename)
            output = af.reverb(samples, fs=params.framrate)
            output_file = "Recorded Wav Files/" + "reverb-" + filename
            write(output_file, params.framrate, output)
        elif(val == '5'):
            
            display_samples()
            display_recorded()
            filename = input("What Wav file would you like to apply the effect to? (ex: test.wav)  ")
            dic = input("Is this in samples or recorded?  ")
            if (dic=="samples"):
                folder = "Sample Wav Files/"
            elif (dic=="recorded"):
                folder = "Recorded Wav Files/"
            else: 
                print("Invalid Input")
                continue
            params, samples = af.read_wave(folder + filename)
            fs = params.framerate
            # args: nyq, low freq, high freq, secs
            filter_args = [0.1, 350, 800, 1]
            output, fs = af.bandpass_filter(samples, fs, filter_args)
            output_file = "Recorded Wav Files/" + "bandpass-" + filename
            write(output_file, fs, output)
        elif(val == '6'):
            quit = True

def main():
    print("Welcome to our Audio Effect Program!!!")
    quit = False
    while(quit==False):
        print("Main Menu:")
        print("1. Record Audio")
        print("2. View Sample Wav Files")
        print("3. View Recorded Wav Files")
        print("4. Apply Effects")
        print("5. Listen to a Wav File")
        print("6. Quit")
        val = input()
        if(val == '1'):
            time = input("How long do you want to record?  ")
            filename = input("What would you like the file to be called? (ex: test.wav)  ")
            ar.record_audio(time, filename)
        elif(val == '2'):
            display_samples()
        elif(val == '3'):
            display_recorded()
        elif(val == '4'):
            effects_menu()
        elif(val == '5'):
            filename = input("What Wav file would you like to listen to? (ex: test.wav)  ")
            dic = input("Is this in samples or recorded?  ")
            if (dic=="samples"):
                folder = "Sample Wav Files/"
            elif (dic=="recorded"):
                folder = "Recorded Wav Files/"
            playsound(folder + filename)
        elif(val == '6'):
            quit = True
        else:
            print("Invalid Input")

main()

"""
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
"""