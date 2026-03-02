import pyautogui
import cv2
import sounddevice as sd
from scipy.io.wavfile import write

def screenshot_capture():
    screenshot = pyautogui.screenshot()
    screenshot.save("./screenshot.png")
    print("Screenshot saved")

def webcam_capture():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()

    if ret:
        cv2.imwrite("./webcam.jpg", frame)
        print("captured!")
    else:
        print("failed to capture!")

def audio_capture():
    seconds = 5  # Recording duration
    sample_rate = 44100  # Sample rate of recording
    print("Recording...")
    audio = sd.rec(int(seconds * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait(seconds)  # wait until recording is finished
    write("audio_recording.wav", sample_rate, audio)
    print("Audio recorded!")

def menu():
    print("="*50)
    print("    Test Lab")
    print("="*50)
    print("1) Screenshot capture")
    print("2) Webcam photo capture")
    print("3) Audio capture")
    print("0) Exit")

def main():
    while True:
        menu()
        choice = input("Enter your choice: ")

        match choice:
            case "1":
                print("Capturing Screenshot")
                screenshot_capture()
            case "2":
                print("Capturing webcam photo")
                webcam_capture()
            case "3":
                print("Capturing Audio recording")
                audio_capture()
            case "0":
                exit()
            case _:
                print("Invalid choice")


if __name__ == '__main__':
    main()