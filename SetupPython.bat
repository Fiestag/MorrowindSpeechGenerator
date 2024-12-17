@echo off

echo Download Python 3.10...
curl -o python-3.10.0.exe https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe

echo Install Python 3.10...
start /wait python-3.10.0.exe 

echo Restart Computer for complete Python Installation ? (O/N)
set /p choice=
if /i "%choice%"=="O" (
    shutdown /r /t 0
) else (
    echo Restart Canceled.
)

del python-3.10.0.exe
