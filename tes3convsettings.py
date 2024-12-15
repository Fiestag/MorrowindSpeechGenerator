import os
import json
import tkinter as tk
from tkinter import filedialog 
from tkinter import simpledialog
import csv
import re

root = tk.Tk()
root.withdraw()  # Masquer la fenêtre principale
root.iconbitmap("icon.ico")


# Demander une entrée utilisateur
Imput_file = filedialog.askopenfilename(title= "Choice ESP/ESM File", filetypes=(("Esm/Esp Files", "*.esp *.esm"),))
Output_name = (os.path.splitext(os.path.basename(Imput_file)))[0]

os.system(f'tes3conv.exe "{Imput_file}" "{Output_name}.json"') 

# Fonction pour retirer les chaînes de caractères spécifiques
def retirer_chaines(text):
    return re.sub(r'%[^., ]*[., ]', '', text)

# Charger le fichier JSON
with open(f'{Output_name}.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Créer un dictionnaire pour stocker les races et le sexe des NPC par leur id
npc_info = {}

# Parcourir les données pour extraire les informations des NPC
for item in data:
    if item['type'] == 'Npc':
        npc_id = item.get('id', '')
        race = item.get('race', '')
        npc_flags = item.get('npc_flags', '')
        sex = 'female' if 'FEMALE' in npc_flags else 'male'
        npc_info[npc_id] = {'race': race, 'sex': sex}

# Créer le sous-dossier 'csv' s'il n'existe pas
if not os.path.exists('csv'):
    os.makedirs('csv')

# Ouvrir un fichier CSV pour écrire les dialogues avec la race et le sexe ajoutés
with open(f'csv/{Output_name}.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    
    # Écrire l'en-tête du CSV
    csv_writer.writerow(['id', 'speaker_id','race', 'sex', 'text'])
    
    # Écrire les données
    for item in data:
        if item['type'] == 'DialogueInfo' and item['data'].get('dialogue_type') != 'Journal' and item.get('speaker_id') != 'dialog placeholder' and item['data'].get('dialogue_type') != 'Voice': 
            id_ = item.get('id', '')
            speaker_id = item.get('speaker_id', '')
            text = item.get('text', '').replace('\r\n', ' ')  # Remplacer \r\n par un espace
            # Retirer les chaînes de caractères spécifiques du texte
            text = retirer_chaines(text)
            race = npc_info.get(speaker_id, {}).get('race', '')
            sex = npc_info.get(speaker_id, {}).get('sex', '')
            csv_writer.writerow([id_, speaker_id,race, sex, text])

os.remove(f'{Output_name}.json')

print(f'Dialogue extracted in csv/{Output_name}.csv with success')

# Fermer la fenêtre principale
root.destroy()
