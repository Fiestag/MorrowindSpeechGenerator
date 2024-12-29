import os
import tkinter as tk
from tkinter import filedialog
import configparser
import subprocess
import ctypes

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("icon.ico")

def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.iconbitmap("icon.ico")

    def browse_speaker_path():
        path = filedialog.askdirectory()
        if path:
            speaker_path_entry.delete(0, tk.END)
            speaker_path_entry.insert(0, path)

    def browse_output_path():
        path = filedialog.askdirectory()
        if path:
            output_entry.delete(0, tk.END)
            output_entry.insert(0, path)

    def save_settings():
        config['Path']['speaker_path'] = speaker_path_entry.get()
        config['Path']['output'] = output_entry.get()
        config['Language']['Speaker_language'] = language_var.get()
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        settings_window.destroy()

    tk.Label(settings_window, text="Speakers Path:").grid(row=1, column=0, padx=10, pady=5)
    speaker_path_entry = tk.Entry(settings_window, width=50)
    speaker_path_entry.grid(row=1, column=1, padx=10, pady=5)
    speaker_path_entry.insert(0, config['Path']['speaker_path'])
    browse_speaker_button = tk.Button(settings_window, text="Browse", command=browse_speaker_path)
    browse_speaker_button.grid(row=1, column=2, padx=10, pady=5)

    tk.Label(settings_window, text="Output Path:").grid(row=2, column=0, padx=10, pady=5)
    output_entry = tk.Entry(settings_window, width=50)
    output_entry.grid(row=2, column=1, padx=10, pady=5)
    output_entry.insert(0, config['Path']['output'])
    browse_output_button = tk.Button(settings_window, text="Browse", command=browse_output_path)
    browse_output_button.grid(row=2, column=2, padx=10, pady=5)

    tk.Label(settings_window, text="Default Speaker:").grid(row=3, column=0, padx=10, pady=5)
    speaker_var = tk.StringVar(settings_window)
    speaker_var.set(config['Path']['speaker_default'])  # valeur par défaut
    speaker_options = ["Argonian", "Breton", "Dark Elf", "High Elf", "Imperial", "Khajiit", "Nord", "Orc", "Redguard", "Wood Elf"]
    speaker_menu = tk.OptionMenu(settings_window, speaker_var, *speaker_options)
    speaker_menu.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(settings_window, text="Speakers Language:").grid(row=4, column=0, padx=10, pady=5)
    language_var = tk.StringVar(settings_window)
    language_var.set(config['Language']['Speaker_language'])  # valeur par défaut
    language_options = ["en", "es", "fr", "de", "it", "pt", "pl", "tr", "ru", "nl", "cs", "ar", "zh-cn", "ja", "hu", "ko"]
    language_menu = tk.OptionMenu(settings_window, language_var, *language_options)
    language_menu.grid(row=4, column=1, padx=10, pady=5)

    save_button = tk.Button(settings_window, text="Save", command=save_settings)
    save_button.grid(row=5, columnspan=3, pady=10)

def run_script():
    subprocess.call(["python", "Main.py"])

def run_extractor():
    subprocess.call(["python", "tes3convsettings.py"])

def run_extractaudio():
    subprocess.call(["python", "extractaudio.py"])

def open_readme():
    if os.path.isfile("README.md"):
        os.system("notepad README.md")
    else:
        tk.messagebox.showerror("Error", "README.md file not found")

config = configparser.ConfigParser()
config.read("config.ini")

if 'Path' not in config:
    config['Path'] = {
        'speaker_path': '',
        'output': ''
    }
if 'Language' not in config:
    config['Language'] = {
        'Speaker_language': 'en'
    }

with open('config.ini', 'w') as configfile:
    config.write(configfile)

root = tk.Tk()
root.title("Morrowind Speech Generator")
root.iconbitmap("icon.ico")
root.geometry("400x300")

settings_button = tk.Button(root, text="Settings", command=open_settings)
settings_button.pack(pady=10)

extractor_button = tk.Button(root, text='Run Dialogue Extractor', command=run_extractor)
extractor_button.pack(pady=10)

extractaudio_button = tk.Button(root, text="Extract Audio", command=run_extractaudio)
extractaudio_button.pack(pady=10)

run_button = tk.Button(root, text="Launch Speech Generation", command=run_script)
run_button.pack(pady=10)

help_button = tk.Button(root, text="Help", command=open_readme)
help_button.pack(pady=10)

root.mainloop()
