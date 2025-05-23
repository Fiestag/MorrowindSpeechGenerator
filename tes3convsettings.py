import os
import json
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import csv
import re
import configparser
root = tk.Tk()
root.withdraw()  # Hide the main window
root.iconbitmap("icon.ico")
loaded_files = {}  # Dictionary to store already loaded files
complete_npc_info = {}  # Dictionary to store complete NPC information from all files

config = configparser.ConfigParser()
config.read("config.ini")

language = config.get("Language", "speaker_language")


if (language == 'pl'):
    fix_chars = { 
    "¹": "ą",
    "æ": "ć",
    "Æ": "Ć",
    "ê": "ę",
    "³": "ł",
    "£": "Ł",
    "ñ": "ń",
    "œ": "ś",
    "Œ": "Ś",
    "¿": "ż",
    "¯": "Ż",
    "Ÿ": "ź",
    "": "Ź"
    }
else: 
    fix_chars = {}
def fix_wrong_encoding(text):
    for wrongChar, correctChar in fix_chars.items():
        text = text.replace(wrongChar, correctChar)
    return text


def load_file(file_path):
    """Loads a file, converts it to JSON, and returns its data."""
    output_name = os.path.splitext(os.path.basename(file_path))[0]
    # Convert the file to JSON
    os.system(f'tes3conv.exe "{file_path}" "{output_name}.json"')
    # Load the JSON data
    with open(f'{output_name}.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    # Mark the file as loaded
    loaded_files[file_path] = data
    # Remove the JSON file after loading its contents
    os.remove(f'{output_name}.json')
    return data
# A global structure to keep track of masters that have already been requested
loaded_masters = set()

def process_masters(data):
    """Recursively load master files specified in the JSON data."""
    for item in data:
        if item["type"] == "Header" and "masters" in item:
            for master, _ in item["masters"]:
                # If this master has already been loaded, skip to the next one
                if master in loaded_masters:
                    continue

                # Otherwise, prompt the user to locate the master file
                master_file_path = filedialog.askopenfilename(
                    title=f"Locate master file: {master}",
                    filetypes=(("Esm/Esp Files", "*.esp *.esm"),)
                )
                if master_file_path:
                    # Remember the master file to avoid asking for it again
                    loaded_masters.add(master)
                    # Load the master file's data (make sure you have defined the load_file function)
                    master_data = load_file(master_file_path)
                    # Recursively process the masters found in this file
                    process_masters(master_data)

def collect_npc_info(data):
    """Collect NPC information from the given data."""
    for item in data:
        if item['type'] == 'Npc':
            npc_id = item.get('id', '')
            if npc_id not in complete_npc_info:
                race = item.get('race', '')
                npc_flags = item.get('npc_flags', '')
                sex = 'female' if 'FEMALE' in npc_flags else 'male'
                complete_npc_info[npc_id] = {'race': race, 'sex': sex}
# Prompt the user to select the main ESP/ESM file
input_file = filedialog.askopenfilename(
    title="Select ESP/ESM File", filetypes=(("Esm/Esp Files", "*.esp *.esm"),)
)
# Load the main file and process its masters
if input_file:
    main_data = load_file(input_file)
    process_masters(main_data)
# Collect NPC information from all loaded files
for file_data in loaded_files.values():
    collect_npc_info(file_data)
# Continue with the rest of the script
output_name = os.path.splitext(os.path.basename(input_file))[0]
def remove_string(text):
    # Remove strings starting with %
    text = re.sub(r'%\w+', '', text)
    # Remove content inside brackets
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\(.*?\)', '', text)
    text = re.sub(r'\<.*?\>', '', text)
    re.sub(r'\s+([.,!?;:])', r'\1', text)
    re.sub(r'\s+', '', text)
    text = text.replace(', .', '.')
    return text

# Open a CSV file to write dialogues with race and gender added
if not os.path.exists('csv'):
    os.makedirs('csv')
missing_race_or_sex = []
total_dialogues = 0
with open(f'csv/{output_name}.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    # Write the CSV header
    csv_writer.writerow(['id', 'speaker_id', 'race', 'sex', 'text'])
    # Write the data
    for item in main_data:
        if item['type'] == 'DialogueInfo' and item['data'].get('dialogue_type') != 'Journal' and item.get('speaker_id') != 'dialog placeholder' and item['data'].get('dialogue_type') != 'Voice':
            id_ = item.get('id', '')
            speaker_id = item.get('speaker_id', '')
            text = item.get('text', '').replace('\r\n', ' ')  # Replace \r\n with a space
            text = fix_wrong_encoding(text)
            # Remove specific strings and content inside brackets from the text
            text = remove_string(text).strip()
            race = complete_npc_info.get(speaker_id, {}).get('race', '').strip()
            sex = complete_npc_info.get(speaker_id, {}).get('sex', '').strip()
            # Skip entries with empty text
            if not text:
                continue
            csv_writer.writerow([id_, speaker_id, race, sex, text])
            # Track dialogues with missing race or sex
            if speaker_id and (not race or not sex):
                missing_race_or_sex.append(id_)
            # Count total dialogues
            total_dialogues += 1
print(f'Dialogue extracted in csv/{output_name}.csv successfully')
# Print dialogues with missing race or sex. These will use the default voice, which might not be intended if they are eg creatures
if missing_race_or_sex:
    print("Dialogue IDs with missing race or sex:")
    for dialogue_id in missing_race_or_sex:
        print(dialogue_id)
# Print total number of dialogues
print(f"Total number of dialogues: {total_dialogues}")
# Close the main window
root.destroy()
