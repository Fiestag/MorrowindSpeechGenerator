import os
import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment
import shutil
import ctypes
import configparser
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("icon.ico")

root = tk.Tk() 
root.iconbitmap("Icon.ico")


def select_morrowind_path():
    return filedialog.askdirectory(title="Data Files Path")

def select_output_path():
    return filedialog.askdirectory(title="Audio Output Path")

def convert_audio_files(morrowind_path, output_path):
    audio_morrowind_path = os.path.join(morrowind_path,"Sound", "Vo")
    
    if not os.path.exists(audio_morrowind_path):
        print(f"Path {audio_morrowind_path} doesn't exist")
        return
    
    
    folder_mapping = {
        'a': 'Argonian',
        'b': 'Breton',
        'd': 'Dark Elf',
        'k': 'Khajiit',
        'h': 'High Elf',
        'i': 'Imperial',
        'n': 'Nord',
        'o': 'Orc',
        'r': 'Redguard',
        'w': 'Wood Elf'
    }
    
    for root, dirs, files in os.walk(audio_morrowind_path):
        
        dirs[:] = [d for d in dirs if d != "AIV"]
        
        for filename in files:
            if filename.endswith(".mp3"):
                mp3_file_path = os.path.join(root, filename)
                audio = AudioSegment.from_mp3(mp3_file_path)
                
      
                if len(audio) < 4000:  
                    continue
                
                parent_folder_name = os.path.basename(os.path.dirname(root))
                output_folder_name = folder_mapping.get(parent_folder_name, parent_folder_name)
                
         
                output_dir = os.path.join(output_path, output_folder_name, os.path.basename(root))
                
                os.makedirs(output_dir, exist_ok=True)
                wav_file_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".wav")
                
                audio.export(wav_file_path, format="wav")
                print(f"File converted: {wav_file_path}")
            else:
                print(f"Not mp3 file: {filename}")

def convert_audio_files_misc(morrowind_path, output_path):
   
    audio_morrowind_path = os.path.join(morrowind_path, "Sound", "Vo")
    misc_path = os.path.join(audio_morrowind_path, "misc")
    
   
    if not os.path.exists(audio_morrowind_path):
        print(f"Path {audio_morrowind_path} doesn't exist")
        return
    
    
    folder_mapping = {
        'a': 'Argonian',
        'b': 'Breton',
        'd': 'Dark Elf',
        'k': 'Khajiit',
        'h': 'High Elf',
        'i': 'Imperial',
        'n': 'Nord',
        'o': 'Orc',
        'r': 'Redguard',
        'w': 'Wood Elf'
    }
    

    string_mapping = {
        'Viv': 'vivec_god',
        'tr_alm': 'almalexia',
        'Yagrum': 'yagrum bagarn',
        'dagoth_': 'dagoths',
        'Dagoth Ur': 'dagoth_ur'
    }
    
 
    def process_files(root, files, base_path):
        for filename in files:
            if filename.endswith(".mp3") and any(key in filename for key in string_mapping):
                mp3_file_path = os.path.join(root, filename)
                audio = AudioSegment.from_mp3(mp3_file_path)
                
       
                if len(audio) < 4000:  
                    continue
                
                
                parent_folder_name = os.path.basename(os.path.dirname(root))
                output_folder_name = folder_mapping.get(parent_folder_name, parent_folder_name)
                
                for key, value in string_mapping.items():
                    if key in filename:
                        output_folder_name = value
                        break
                
                relative_path = os.path.relpath(root, base_path)
                relative_path_parts = relative_path.split(os.sep)
                if parent_folder_name in relative_path_parts:
                    relative_path_parts[relative_path_parts.index(parent_folder_name)] = output_folder_name
                relative_path = os.path.join(*relative_path_parts)
                output_dir = os.path.join(output_path, relative_path, output_folder_name)
                
                os.makedirs(output_dir, exist_ok=True)
                wav_file_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".wav")
                
                audio.export(wav_file_path, format="wav")
                print(f"File converted: {wav_file_path}")
            else:
                print(f"Not mp3 file or does not contain required string: {filename}")

    for root, dirs, files in os.walk(audio_morrowind_path):
        # Ignorer le dossier "AIV"
        dirs[:] = [d for d in dirs if d != "AIV"]
        process_files(root, files, audio_morrowind_path)



root = tk.Tk()
root.withdraw()

config = configparser.ConfigParser()
config.read("config.ini")

morrowind_path = select_morrowind_path()
output_path = select_output_path()
config['Path']['speaker_path'] = output_path
with open('config.ini', 'w') as configfile:
    config.write(configfile)

print(f"Morrowind Path: {morrowind_path}")
print(f"Output Path: {output_path}")


convert_audio_files(morrowind_path, output_path)
convert_audio_files_misc(morrowind_path, output_path)

