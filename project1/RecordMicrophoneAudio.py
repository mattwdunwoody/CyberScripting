import sounddevice as sd
from scipy.io.wavfile import write

# Audio settings
seconds = 5 # Recording duration
sample_rate = 44100 # Sample rate of recording
print("Recording...")
audio = sd.rec(int(seconds * sample_rate), samplerate=sample_rate, channels=1)
sd.wait(seconds) # wait until recording is finished
write("audio_recording.wav", sample_rate, audio)
print("Audio recorded!")