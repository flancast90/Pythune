from scipy.io import wavfile
import pyaudio, os, wave, time
import tqdm
import numpy as np
from scipy.fft import *
import datetime
from random import randint

note_freq = 0
timestamp = 0
rec = "false"

quotes = ['Music is the language of the spirit. It opens the secret of life bringing peace, abolishing strife. -Kahlil Gibran', 'Music is the only language in which you cannot say a mean or sarcastic thing. -John Erskine', 'Music is the moonlight in the gloomy night of life. -John Paul Friedrich Richter', 'If Music is a Place — then Jazz is the City, Folk is the Wilderness, Rock is the Road, Classical is a Temple -Vera Nazarin', 'Love is friendship set to music. -Jackson Pollock', 'Music is the universal language of mankind. -Henry Wadsworth Longfellow', 'Music is the literature of the heart; it commences where speech ends. -Alphonse de Lamartine', 'Music is the art which is most nigh to tears and memory. -Oscar Wilde', 'Music is nothing else but wild sounds civilized into time and tune. -Thomas Fuller', 'Music is your own experience, your thoughts, your wisdom. If you don’t live it, it won’t come out of your horn. -Charlie Parker', 'One good thing about music, when it hits you, you feel no pain. -Bob Marley', 'Where words fail, music speaks. -Hans Christian Anderson', 'How is it that music can, without words, evoke our laughter, our fears, our highest aspirations? -Jane Swan', 'Music expresses feeling and thought, without language; it was below and before speech, and it is above and beyond all words. -Robert G. Ingersoll', 'A strange art – music – the most poetic and precise of all the arts, vague as a dream and precise as algebra. -Guy de Maupassant', 'Music is good to the melancholy, bad to those who mourn, and neither good nor bad to the deaf. -Baruch Spinoza']

def cls():
    rand = randint(0, len(quotes))
    os.system('cls' if os.name=='nt' else 'clear')
    print('\x1B[3m 🎵 '+quotes[rand-1]+' 🎶 \x1B[0m \n')

def main_menu():
    global rec
    rand = randint(0, len(quotes))
    print('\x1B[3m 🎵 '+quotes[rand-1]+' 🎶 \x1B[0m')
    input("\r\nWelcome to Pythune, a Command-Line based piano tuner built in Python. Press any key to continue...")
    cls()
    print("\rPythune is listening for sound. Once it has detected a piano note, it will output tuning info for it.")
    cls()
    rec = "true"
    while rec == "true":
        record()
        time.sleep(2)
    

def file_length(name):
    global file_dur
    Fs, data = wavfile.read(name)
    n = data.size
    t = (n / Fs)*1000
    return t

# slightly modified from https://stackoverflow.com/questions/54612204/trying-to-get-the-frequencies-of-a-wav-file-in-python
def freq(file, start_time, end_time):
    global note_freq, timestamp
    # Open the file and convert to mono
    sr, data = wavfile.read(file)
    if data.ndim > 1:
        data = data[:, 0]
    else:
        pass
    # Return a slice of the data from start_time to end_time
    dataToRead = data[int(start_time * sr / 1000) : int(end_time * sr / 1000) + 1]
    # Fourier Transform
    N = len(dataToRead)
    yf = rfft(dataToRead)
    xf = rfftfreq(N, 1 / sr)
    # Get the most dominant frequency and return it
    idx = np.argmax(np.abs(yf))
    freq = xf[idx]
    return freq 

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

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    timestamp = (datetime.datetime.now().time())
    timestamp = str(timestamp).replace(':','').replace('.','')  

    note_freq = freq('output.wav', 0, file_length('output.wav'))
    match_frequency(note_freq)
    os.rename('output.wav', 'cache/'+str(timestamp)+'.wav')

def closest(lst, K):
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]

def match_frequency(frequency):
    frequencies = [27.5000,29.1353,30.8677,32.7032,34.6479,36.7081,38.8909,41.2035,43.6536,46.2493,48.9995,51.9130,55.0000,58.2705,61.7354,65.4064,69.2957,73.4162,77.7817,82.4069,87.3071,92.4986,97.9989,103.826,110.000,116.541,123.471,130.813,138.591,146.832,155.563,164.814,174.614,184.997,195.998,207.652,220.000,233.082,246.942,261.626,277.183,293.665,311.127,329.628,349.228,369.994,391.995,415.305,440.000,466.164,493.883,523.251,554.365,587.330,622.254,659.255,698.456,739.989,783.991,830.609,880.000,932.328,987.767,1046.50,1108.73,1174.66,1244.51,1318.51,1396.91,1479.98,1567.98,1661.22,1760.00,1864.66,1975.53,2093.00,2217.46,2349.32,2489.02,2637.02,2793.83,2959.96,3135.96,3322.44,3520.00,3729.31,3951.07]
    names = ['A0', 'A#0/Bb0', 'B0', 'C1', 'C#1/Db1', 'D1', 'D#1/Eb1', 'E1', 'F1', 'F#1/Gb1', 'G1', 'G#1/Ab1', 'A1', 'A#1/Bb1', 'B1', 'C2', 'C#2/Db2', 'D2', 'D#2/Eb2', 'E2', 'F2', 'F#2/Gb2', 'G2', 'G#2/Ab2', 'A2', 'A#2/Bb2', 'B2', 'C3', 'C#3/Db3', 'D3', 'D#3/Eb3', 'E3', 'F3', 'F#3/Gb3', 'G3', 'G#3/Ab3', 'A3', 'A#3/Bb3', 'B3', 'C4', 'C#4/Db4', 'D4', 'D#4/Eb4', 'E4', 'F4', 'F#4/Gb4', 'G4', 'G#4/Ab4', 'A4', 'A#4/Bb4', 'B4', 'C5', 'C#5/Db5', 'D5', 'D#5/Eb5', 'E5', 'F5', 'F#5/Gb5', 'G5', 'G#5/Ab5', 'A5', 'A#5/Bb5', 'B5', 'C6', 'C#6/Db6', 'D6', 'D#6/Eb6', 'E6', 'F6', 'F#6/Gb6', 'G6', 'G#6/Ab6', 'A6', 'A#6/Bb6', 'B6', 'C7', 'C#7/Db7', 'D7', 'D#7/Eb7', 'E7', 'F7', 'F#7/Gb7', 'G7', 'G#7/Ab7', 'A7', 'A#7/Bb7', 'B7', 'C8']
    closestNum = closest(frequencies, frequency)
    index = frequencies.index(closestNum)
    print("🎹 The frequency was: "+str(frequency)+", which is closest to the note: "+str(names[index])+", with: "+str(closestNum-frequency)+" to go until perfect pitch 🎹")

main_menu()

