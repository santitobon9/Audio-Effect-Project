# Santiago Tobon & Cody Jeffries
# CS410 - Comp, Sound, and Music
# Spring 2021
import argparse
import sounddevice as sd
import soundfile as sf
import numpy as np
import consolemenu

def menu():
    print('1. Record')

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

def main(args):
    menu = ['Record', 'Play', 'Filter', 'Save']
    if args.play:
        play_sound_file(args.play)
    else:
        selection = consolemenu.SelectionMenu.get_selection(menu)
        print(menu[selection])



if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Audio Effects',
                                description='Simple Audio Effects'
                                ' program for sound and music',
                                allow_abbrev=False)
    parser.add_argument('-r', '--record',
                    type=str,
                    default='temp_file',
                    help='Audio filename to save recording')
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
