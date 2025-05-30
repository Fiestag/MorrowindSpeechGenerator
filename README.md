This mod uses the XTTS AI model developed by Coqui.ai to create speech for any ESP/ESM files that work with Morrowind.
# Installation
************* This app needs approximately 10 GB to install all dependencies (Python 3.10, XTTS model and CUDA toolkit)    *************

1.  Extract Morrowind Speech Generator and launch 'SetupPython.bat' (Don't close window!). Once it's complete, it will prompt you to restart your computer. Type in 'o' for yes. 
2.  Once you've restarted, go back into the same folder and launch 'setup.bat'. Once that is complete, it will once again prompt you to restart your computer. Type in 'o' for yes.
3.  Once installation is complete, launch 'MorrowindSpeechGenerator.bat' to open the app.

# Usage
************* It is highly recommended to use NVIDIA GPU for generating speech; it will speed up the process considerably. *************

1.  Open 'Settings'.
1a.  The top directory shown is the Speaker Path. This is where the program will draw audio from. Set it to your audio directory of choice (Example:\Morrowind\Data Files\Sound\Vo).
1b.  The second directory is the Output Path, and as it sounds, this is where the program will save the created audio files. Set this to wherever you like.
2.  Exit settings and run 'Dialogue Extractor' from the main menu. This will extract the dialogue script. Point it to the ESM file you want to export a dialogue script from. (Example:\Morrowind\Data Files\Morrowind.esm)
3.  Run 'Extract Audio' from the main menu. This will convert the mp3 audio files in your Vo folder into wav files needed for speech generation.
4.  Run 'Launch Speech Generation' from the main menu. In the new window, point it to where the extracted script is located (Program location\csv). This process will take time.
5.  Once that is complete, take the contents of your output folder, and copy/paste them into the proper audio folder (Morrowind\Data Files\Sound\Vo\AIV)


# Credits

Thanks to Greatness7 for creates Tes3conv used for convert ESP/ESM files.  
Thanks to coqui AI for XTTS model.  
Thanks to Kezyma  for Voices of Vvardenfell.  
Thanks to S-T-K for his comments and his contribution to script for load the npc of the master file. 
Thanks to Wa2a for fix Polish characters encoding.
