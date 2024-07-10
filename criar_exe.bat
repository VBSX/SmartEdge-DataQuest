@echo off
pyinstaller --onefile --windowed --name=DataQuest --icon=images/smartedge.png --add-data="images/*.png;images/" main.py

taskkill /F /IM dataquest.exe

echo Terrminou de compilar

del "C:\Users\Visual Software\Documents\rybak\VBSX PROGRAMS\SmartEdge - DataQuest\DataQuest.exe"
copy "I:\1 - Rybak\2 - Programação Python\python projects\interface_automação\dist\dataquest.exe" "C:\Users\Visual Software\Documents\rybak\VBSX PROGRAMS\SmartEdge - DataQuest\DataQuest.exe"

echo Terminou de copiar para a pasta

pause