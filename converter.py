import json
import csv
import re

# Fonction pour retirer les chaînes de caractères spécifiques
def retirer_chaines(text):
    return re.sub(r'%[^., ]*[., ]', '', text)

# Charger le fichier JSON
with open('Morrowind.json', 'r', encoding='utf-8') as json_file:
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

# Ouvrir un fichier CSV pour écrire les dialogues avec la race et le sexe ajoutés
with open('output_combined.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # Écrire l'en-tête du CSV
    csv_writer.writerow(['id', 'speaker_id','race', 'sex', 'text'])
    
    # Écrire les données
    for item in data:
        if item['type'] == 'DialogueInfo' and item['data'].get('dialogue_type') != 'Journal':
            id_ = item.get('id', '')
            speaker_id = item.get('speaker_id', '')
            text = item.get('text', '')
            # Retirer les chaînes de caractères spécifiques du texte
            text = retirer_chaines(text)
            race = npc_info.get(speaker_id, {}).get('race', '')
            sex = npc_info.get(speaker_id, {}).get('sex', '')
            csv_writer.writerow([id_, speaker_id,race, sex, text])

print("Les données combinées ont été enregistrées dans 'output_combined.csv'")

