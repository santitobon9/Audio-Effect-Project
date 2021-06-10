Team Members Cody Jeffries - jcody@pdx.edu Santiago Tobon - stobon@pdx.edu

Audio-Effect-Project

* Project Description

	* Purpose

		The Audio-Effect-Project is desined to apply filters, effects, and other DSP features. User will be loading or creating wav audio files	they wish to apply one of the implementd DSP features. The features implemented so far include recording audio, bandpass filter, reverb, chorus, flanger, and tremolo. The repository also has utility functions for loading, playing, and saving wav files. 

	* Building

		The project has a few dependencies to be installed first

		```
		pip install -r requirments.txt
		```
		After that the program is can be ran with the following command
		```
		python3 main.py
		```
	* Testing
	
		The main testing method was comparison of audio files in audacity. Using this system we could view the wave shape or listen for the desired effect. For example when testing the bandpass filter Audacity was used to verify the atenuation of a wave at a certain frequency.

* Examples
	
	Example audio files with desired effects and filters are located in the Recorded Wav Files directory.

	The code that created them is in main.py commented out.

* Retro-Spective

	The process of learning and understanding what digital sound processing or DSP made up a large portion of this project. This process meant first understanding what an effect is, how it effects a signal, and then how to implement that in code. 
	
	This worked well for the effect features tremelo, flanger, and choras. The bandpass filter also went well, but the reverb effect didn't. Reverb was the last effect implemented and needed more time to understand and implement. The process of learning how the code interacts with the signal has been exciting for the group memembers and want to keep working out some of the kinks with this effect. In the future it would be nice to finish the reverb effect and add other tools.

	In the end we are happy with the results acheived. Both team members learned new things about signal processing and future potential projects to add. Neither had worked with sound and music before digitally but now we see areas of application in our respective fields of interest.

* License

	https://github.com/santitobon9/Audio-Effect-Project/blob/main/LICENSE

* References

	https://pythonaudiosynthesisbasics.com/

	https://github.com/wybiral/python-musical/blob/master/musical/audio/effect.py

	https://github.com/pdx-cs-sound/fft-filter/blob/main/fft-filter.py

	https://github.com/wybiral/python-musical/blob/master/musical/audio/source.py

	https://www2.cs.uic.edu/~i101/SoundFiles/

	https://www.ee.columbia.edu/~dpwe/sounds/music/

	https://www.electronics-tutorials.ws/filter/filter_4.html

	https://medium.com/the-seekers-project/coding-a-basic-reverb-algorithm-an-introduction-to-audio-programming-d5d90ad58bde