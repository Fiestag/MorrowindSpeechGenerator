@echo off

echo Download tes3conv...
curl -L -o tes3conv.zip https://github.com/Greatness7/tes3conv/releases/download/v0.3.0/windows-latest.zip
powershell -Command "Expand-Archive -Path 'tes3conv.zip'"
xcopy "%cd%\tes3conv" "%cd%" /E /I /Y
del tes3conv.zip
rmdir /S /Q tes3conv

python --version

echo Install Dependencies...
powershell -Command "Start-Process 'python' -ArgumentList 'setup.py' -Verb RunAs -Wait"


echo Restart Computer for complete Installation ? (O/N)
set /p choice=
if /i "%choice%"=="O" (
    shutdown /r /t 0
) else (
    echo Restart Canceled.
)

