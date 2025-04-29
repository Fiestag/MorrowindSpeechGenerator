import os
import zipfile
import shutil
print("Don't close Window!...")

if not os.path.exists('config.ini'):
    shutil.copy('config.example.ini', 'config.ini')
    print('Initialization of the config file.')
else:
    print('The config file already exists.')

try:
    import requests
    print('requests already installed')
except ImportError:
    os.system("pip install requests")
    import requests

def install_ffmpeg():
    print("Downloading ffmpeg for Windows...")
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = "ffmpeg.zip"
    os.system(f"curl -L {url} -o {zip_path}")
    os.system("pip install ffmpeg")
    print("Install ffmpeg")

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall()

    # Dynamically find the name of the extracted folder
    extracted_folder = next((name for name in os.listdir() if os.path.isdir(name) and 'ffmpeg' in name.lower()), None)
    if extracted_folder:
        ffmpeg_path = os.path.join(os.getcwd(), extracted_folder, "bin")
        powershell_command = f"[Environment]::SetEnvironmentVariable('PATH', [Environment]::GetEnvironmentVariable('PATH', 'Machine') + ';{ffmpeg_path}', 'Machine')"
        os.system(f"powershell -Command \"{powershell_command}\"")
        os.remove("ffmpeg.zip")
        print("ffmpeg installed and added to the user PATH.")
    else:
        print("Error: Unable to find the extracted folder containing ffmpeg.")

def download_cuda_toolkit(version):
    url = f"https://developer.download.nvidia.com/compute/cuda/11.8.0/network_installers/cuda_11.8.0_windows_network.exe"
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(f"cuda_{version}_windows_network.exe", "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"CUDA Toolkit {version} downloaded successfully!")
        os.system("cuda_11.8.0_windows_network.exe")
    else:
        print(f"Error downloading CUDA Toolkit {version}")
        return None

def install_cuda_toolkit(installer_path):
    if installer_path and os.path.exists(installer_path):
        os.system(installer_path)
        print("CUDA Toolkit installation started.")
    else:
        print("The installation file does not exist.")
print("Install TTS...")
try:
    import TTS
    print('TTS already installed')
except ImportError:
    os.system('pip install coqui-tts')
print("Install Pydub...")
try:
    import pydub
    print('pydub already installed')
except ImportError:
    os.system('pip install pydub')

try:
    import pandas
    print('pandas already installed')
except ImportError:
    os.system('pip install pandas')
try:
    import ffmpeg
    print('ffmpeg already installed')
except ImportError:
    install_ffmpeg()

import torch
Cuda_test = torch.cuda.is_available()
print(f'CUDA installed: {Cuda_test}')
if not Cuda_test:
    import subprocess
    try:
       
        result = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
      
        if result.returncode == 0:
            print("NVIDIA GPU detected")
            os.system('pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118')
            installer_path = download_cuda_toolkit("11.8.0")
            install_cuda_toolkit(installer_path)
        else:
            print("No NVIDIA GPU detected (CUDA is not available)")
    except FileNotFoundError:
        print("No NVIDIA GPU detected (CUDA is not available)")
