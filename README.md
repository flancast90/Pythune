Pythune
=================================================

A Python Command-Line-Interface to make tuning a piano more fun! Part of my Piano + Python mashup!

[![License](https://img.shields.io/badge/License-MIT-lightgray.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Latest release](https://img.shields.io/badge/Release-Latest-orange.svg?style=flat-square)](https://github.com/flancast90/Pythune/releases)


Table of contents
-----------------

* [Introduction](#introduction)
* [Installation](#installation)
* [Usage](#usage)
* [Getting help](#getting-help)
* [Contributing](#contributing)
* [License](#license)
* [Acknowledgments](#acknowledgments)


Introduction
------------

Pythune is a CLI to help tune a piano. The program uses [PyAudio](http://people.csail.mit.edu/hubert/pyaudio/) to map the frequency of a dynamically generated .wav file to the keys on the piano. For reference, the functions to find the frequency and map it are shown below (All functions credit to their respective authors in comments)

The below function finds the frequency:
```python
# http://people.csail.mit.edu/hubert/pyaudio/
def record():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 2
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK)

    frames = []

    cls()
    for i in tqdm.tqdm(range(0, int(RATE / CHUNK * RECORD_SECONDS))):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
```

which is then mapped to the piano keys:
```python
def match_frequency(frequency):
    frequencies =     [27.5000,29.1353,30.8677,32.7032,34.6479,36.7081,38.8909,41.2035,43.6536,46.2493,48.9995,51.9130,55.0000,58.2705,61.7354,65.4064,69.2957,73.4162,77.7817,82.4069,87.3071,92.4986,97.9989,103.826,110.000,116.541,123.471,130.813,138.591,146.832,155.563,164.814,174.614,184.997,195.998,207.652,220.000,233.082,246.942,261.626,277.183,293.665,311.127,329.628,349.228,369.994,391.995,415.305,440.000,466.164,493.883,523.251,554.365,587.330,622.254,659.255,698.456,739.989,783.991,830.609,880.000,932.328,987.767,1046.50,1108.73,1174.66,1244.51,1318.51,1396.91,1479.98,1567.98,1661.22,1760.00,1864.66,1975.53,2093.00,2217.46,2349.32,2489.02,2637.02,2793.83,2959.96,3135.96,3322.44,3520.00,3729.31,3951.07]
    names = ['A0', 'A#0/Bb0', 'B0', 'C1', 'C#1/Db1', 'D1', 'D#1/Eb1', 'E1', 'F1', 'F#1/Gb1', 'G1', 'G#1/Ab1', 'A1', 'A#1/Bb1', 'B1', 'C2', 'C#2/Db2', 'D2', 'D#2/Eb2', 'E2', 'F2', 'F#2/Gb2', 'G2', 'G#2/Ab2', 'A2', 'A#2/Bb2', 'B2', 'C3', 'C#3/Db3', 'D3', 'D#3/Eb3', 'E3', 'F3', 'F#3/Gb3', 'G3', 'G#3/Ab3', 'A3', 'A#3/Bb3', 'B3', 'C4', 'C#4/Db4', 'D4', 'D#4/Eb4', 'E4', 'F4', 'F#4/Gb4', 'G4', 'G#4/Ab4', 'A4', 'A#4/Bb4', 'B4', 'C5', 'C#5/Db5', 'D5', 'D#5/Eb5', 'E5', 'F5', 'F#5/Gb5', 'G5', 'G#5/Ab5', 'A5', 'A#5/Bb5', 'B5', 'C6', 'C#6/Db6', 'D6', 'D#6/Eb6', 'E6', 'F6', 'F#6/Gb6', 'G6', 'G#6/Ab6', 'A6', 'A#6/Bb6', 'B6', 'C7', 'C#7/Db7', 'D7', 'D#7/Eb7', 'E7', 'F7', 'F#7/Gb7', 'G7', 'G#7/Ab7', 'A7', 'A#7/Bb7', 'B7', 'C8']
    closestNum = closest(frequencies, frequency)
    index = frequencies.index(closestNum)
    print("🎹 The frequency was: "+str(frequency)+", which is closest to the note: "+str(names[index])+", with: "+str(closestNum-frequency)+" to go until perfect pitch 🎹")
```

Installation
------------

The non-native dependencies of Pythune are [PyAudio](https://pypi.org/project/pyaudio/), [NumPy](https://pypi.org/project/numpy), [Scipy](https://pypi.org/project/scipy), and [tqdm](https://pypi.org/project/tqdm). For any non-Pythune issue, refer to those libraries for help.

1. To get started with Pythune, first make sure Python is downloaded as per https://www.python.org/downloads/, and then download PIP [here](https://pip.pypa.io/en/stable/cli/pip_download/)
2. Next, make sure that the necessary libraries are installed using Pip
```bash
pip install pyaudio
pip install scipy
pip install numpy
pip install tqdm
```
3. Once these libraries are downloaded, start Pythune as follows:
```bash
cd path/to/Pythune-main
cd src
python pythune.py
```
4. That's it! Refer to the [Usage Section](#usage) for the quick-start guide


Usage
-----

### Getting Started

Once Pythune starts, you should see an output similar to the following:
[![Pythune Start Img](https://i.imgur.com/645StsQ.png)]

Click any key to continue when on that screen!

Next, you should see a nifty progress bar; This means Pythune is recording sound, and waiting for the sound of a piano key!
[![Pythune Recording](https://i.imgur.com/pYXkodm.png)]

Once this progress bar reaches 100% (progress bar courtesy of TQDM), you will get a brief message of the file status, its frequency, as well as the distance needed for the key to be tuned to reach perfect pitch! **Remember that Pythune is not perfect. If its output does not seem correct, try restarting the program, there is no limit on how many recordings can be done!**

### Listening to Past-Pythune Recordings

For ease-of-use, Pythune stores all past audio files in its ```cache``` folder. To get there, just navigate to the ``src`` folder and then to the ``cache`` folder within it. The numbers of the file name follow the Pythune convention of the current hour-minute-millisecond, so finding the correct files is pretty easy. If you are A: a mega-hacker, or B: Lacking a GUI, you can also go to the cache folder via a simple ``cd`` command as shown below:
```
cd path/to/src/folder
cd src
```
The contents can then be listed as follows:
```
dir
```

Getting help
------------

Hopefully you don't need this section, but in case something goes wrong, feel free to drop me an email at ```flancast90@gmail.com```, or [open a new issue on this GitHub Repo](https://github.com/flancast90/Pythune/issues/new). I will do my best to respond ASAP to these problems!


Contributing
------------

Contributions to this file can be done as a [Pull Request](https://github.com/flancast90/Pythune/compare), or by shooting an email to ```flancast90@gmail.com```. If any Python or Music-Savvy person would like to be added as a Collaborator to this repo, please send an email to the same address given above. 


License
-------

This README file is distributed under the terms of the [MIT License](https://opensource.org/licenses/MIT). The license applies to this file and other files in the [GitHub repository](http://github.com/flancast90/Pythune) hosting this file.


Acknowledgments
---------------

Thanks to everyone in the list below! Each of them helped me on my journey to create Pythune, and their knowledge and expertise in the subject of music, music-theory, or programming, respectively, taught me something new that is now implemented in Pythune. You all are awesome!

* https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
* https://music.stackexchange.com/questions/115906/determine-octave-number-given-only-key-num/115919
* https://emojipedia.org/musical-notes/
* http://people.csail.mit.edu/hubert/pyaudio/
* https://stackoverflow.com/questions/892199/detect-record-audio-in-python/892293#892293
* https://stackoverflow.com/questions/5426546/in-python-how-to-change-text-after-its-printed
* https://github.com/badges/shields
* https://github.com/mhucka/readmine/
* http://www.sengpielaudio.com/calculator-notenames.htm
* https://www.geeksforgeeks.org/python-find-closest-number-to-k-in-given-list/
* https://www.programiz.com/python-programming/methods/list/index
* https://emojiterra.com/musical-keyboard/
