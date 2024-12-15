# MorrowindSpeechGenerator

This mod uses the XTTS AI model developed by Coqui.ai to create speech for any ESP/ESM files that work with Morrowind.
Installation

Extract Morrowind Speech Generator and launchsetup.exe
This app needs approximately 6.6 GB to install all dependencies.(Python 3.10, XTTS model and CUDA toolkit)
Hightly recommendend to use NVIDIA GPU for generate speech.
Launch Morrowind Speech Generator to open the app.

Settings
Speaker Path: Location of the audio files used for audio generation.
Output Path: Location where the generated speech is saved.
Default Speaker: Default speaker files used for NPCs without a specified race.
Speaker Language: Language used for speech.
Dialogue Extractor

Extract NPC dialogue from ESP/ESM files to CSV in CSV folder in app folder.

Extract Audio

Extract audio files from your Morrowind Data Files folder to create samples used for speech generation.

Speech Generator

Generate speech for any NPC dialogue from your ESP/ESM files. These files are contained in the Output folder set by the user and require Kezyma Voices of Vvardenfell to play in-game.

Credits

Thanks to Greatness7 for creates Tes3conv used for convert ESP/ESM files.
Thanks to coqui AI for XTTS model.
Thank to Kezyma  for Voices of VVardenfell.
