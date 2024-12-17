@echo off

echo Downloading Python 3.10...
curl -L -o python-3.10.0.exe https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe

echo Please select the installation directory for Python 3.10...
powershell -Command "Add-Type -AssemblyName System.Windows.Forms; $folderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog; $result = $folderBrowser.ShowDialog(); if ($result -eq [System.Windows.Forms.DialogResult]::OK) { $folderBrowser.SelectedPath }" > selected_path.txt


set /p TargetDir=<selected_path.txt
if "%TargetDir%"=="" (
    echo No directory selected. Exiting.
    exit /b 1
)

echo Installing Python 3.10 in %TargetDir%...
start /wait python-3.10.0.exe  InstallAllUsers=1 PrependPath=1 AppendPath=1 TargetDir="%TargetDir%" Shortcuts=1 SimpleInstall=1


echo Restart the computer to complete Python installation? (O/N)
set /p choice=
if /i "%choice%"=="O" (
    shutdown /r /t 0
) else (
    echo Restart Canceled.
)

del python-3.10.0.exe
del selected_path.txt
