import os
import time
import configparser
print("Load TTS...")
from TTS.api import TTS
import pandas as pd
import glob
import tkinter as tk
from tkinter import filedialog, messagebox
from pydub import AudioSegment
import ffmpeg
import torch
test_cuda = torch.cuda.is_available()
root = tk.Tk() 
root.iconbitmap("Icon.ico")
root.geometry("400x300")
root.withdraw()

config = configparser.ConfigParser()
config.read("config.ini")



def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))

if test_cuda == True:
    processor ="cuda"    
else :
    processor = "cpu"
    window = tk.Tk()
    window.withdraw()  

    messagebox.showinfo("CUDA is not loaded", "CUDA is not loaded, the GPU will not be used for generating. This will have a major impact on generation time.(CUDA is only compatible with NVIDIA GPU)")

    window.destroy()

print(f"TTS Loaded")

print(f"Choice a Dialogue File")
csv_path = filedialog.askopenfilename(title="Choice csv Dialogue File", filetypes=(("Csv Files", "*.csv"),))
csv_data = pd.read_csv(csv_path)
treatedIdCount = 0

race_number = csv_data['race'].nunique()
undefined_text = csv_data['race'].isna() & csv_data['sex'].isna()
non_empty_lines = csv_data.dropna(subset=['speaker_id'])
non_empty_lines_number = non_empty_lines.shape[0]


undefined_text_number = undefined_text.sum()
undefined_Total_lines = (race_number * 2) * undefined_text_number
TotalIdCount = undefined_Total_lines + non_empty_lines_number
start_time = time.time()
default_speaker = config.get("Path", "speaker_default")
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")
tts.to(processor)

def racefunction(race):
    def gndr(gender):
        global treatedIdCount
        global TotalIdCount
        global start_time
        global default_speaker
        global tts

        
        gndr_path = "f" if gender == "female" else "m"

        filtered_data = csv_data[
            ((csv_data['race'] == race) | (csv_data['race'].isna())) &
            ((csv_data['sex'] == gender) | (csv_data['sex'].isna()))
        ]

        speaker_path = config.get("Path", "speaker_path").strip('"')
        

        speaker_wav_path_pattern = f"{speaker_path}\\{race}\\{gndr_path}\\*.wav"
        speaker_wav_paths = glob.glob(speaker_wav_path_pattern)
        print(f"Load Wav Files: {speaker_wav_paths}")

        if not speaker_wav_paths:
            default_speaker_wav = f"{speaker_path}\\{default_speaker}\\{gndr_path}\\*.wav"
            speaker_wav_paths = glob.glob(default_speaker_wav)
            print(f"Load Default Wav Files: {speaker_wav_paths}")

        output = config.get("Path", "Output").strip('"')
        if not os.path.exists(output):
            root = tk.Tk()
            root.withdraw()  # Cacher la fenêtre principale
            output = filedialog.askdirectory(title="Choice Output Folder")
            config['Path']['Output'] = output
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
        output_base_path = f"{output}\\{race}\\{gndr_path}"
        output_mp3_path = f"{output}\\{race}\\{gndr_path}"

        if not os.path.exists(output_base_path):
            os.makedirs(output_base_path)
        if not os.path.exists(output_mp3_path):
            os.makedirs(output_mp3_path)

        for index, row in filtered_data.iterrows():
            text = row['text']
            if not isinstance(text, str):
                continue
            split = len(text) >= 180
            speaker_change = False
            info_id = row['id']
            

            speaker_id = row['speaker_id']
            output_creature_path = f"{output}\\Creature\\{speaker_id}"
            if speaker_id in ['dagoth_ur_1', 'dagoth_ur_2']: speaker_id = 'dagoth_ur'
            if speaker_id in ['dagoth araynys', 'dagoth baler', 'dagoth delnus', 'dagoth elam', 'dagoth endus', 
            'dagoth fervas', 'dagoth gares', 'dagoth gilvoth', 'dagoth girer', 'dagoth odros',
            'dagoth ralas', 'dagoth reler', 'dagoth tureynul', 'dagoth ulen', 'dagoth uthol', 'dagoth uvil', 'dagoth vemyn']: speaker_id = 'dagoths'
            
            if pd.isna(row['race']) and not pd.isna(row['speaker_id']):
                output_file = os.path.join(output_creature_path, f"{info_id}.wav")
                output_file_mp3 = os.path.join(output_creature_path, f"{info_id}.mp3")
                speaker_wav_path_creature_pattern = f"{speaker_path}\\Misc\\{speaker_id}\\*.wav"
                speaker_wav_paths = glob.glob(speaker_wav_path_creature_pattern)
                print(f"Load Creature Wav Files {speaker_wav_paths}")
                speaker_change = True
                if not speaker_wav_paths:
                    default_speaker_wav = f"{speaker_path}\\{default_speaker}\\{gndr_path}\\*.wav"
                    speaker_wav_paths = glob.glob(default_speaker_wav)
                    print(f"Load Default Wav Files: {speaker_wav_paths}")
                speaker_change = True

    
            else:
                output_file = os.path.join(output_base_path, f"{info_id}.wav")
                output_file_mp3 = os.path.join(output_mp3_path, f"{info_id}.mp3")

            if not os.path.exists(output_file_mp3):
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                os.makedirs(os.path.dirname(output_file_mp3), exist_ok=True)

                Speaker_language = config.get("Language", "Speaker_language").strip('"')
                
                print(f"Dialog text : ['{text}']")
                
                if not isinstance(speaker_wav_paths, str):
                    raise TypeError(f"Error: no wav files in folder:['{speaker_wav_path_pattern}']")
                tts.tts_to_file(text=text, speaker_wav=speaker_wav_paths, language=Speaker_language, file_path=output_file, split_sentences=split)
                treatedIdCount += 1
            else:
                print(f"The file for Id {info_id} already exist, skip generation")
                TotalIdCount -= 1

            if not os.path.exists(output_file_mp3):
                sound = AudioSegment.from_wav(output_file)
                sound.export(output_file_mp3, format="mp3", bitrate="64k", parameters=["-ac", "1", "-ar", "44100", "-sample_fmt", "s16"])
                print(f"Output file:['{output_file_mp3}']")
                print(f"Generated Files / Total Files: {treatedIdCount}/{TotalIdCount}")
                elapsed_time = time.time() - start_time
                program_time = (elapsed_time / treatedIdCount) * (TotalIdCount - treatedIdCount)
                hours, remainder = divmod(program_time, 3600) 
                minutes, seconds = divmod(remainder, 60)
                prRed(f"Remaining time: {int(hours):03}:{int(minutes):02}:{int(seconds):02}")
            
            
            if  speaker_change == True :
                speaker_wav_paths = glob.glob(speaker_wav_path_pattern)
            if os.path.exists(output_file) :
                os.remove(output_file)
            prGreen("---------------------------------------------------------------------------------------------")


    genders = csv_data['sex'].dropna().unique()
    for gender in genders:
        gndr(gender)

races = csv_data['race'].dropna().unique()
for race in races:
    racefunction(race)
print('All files created')
