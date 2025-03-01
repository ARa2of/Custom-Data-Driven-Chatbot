@echo off
set BAT_DIR=%~dp0
"C:\Users\XYZ\miniconda3\python.exe" "D:/Directory/chatbot.py" "%BAT_DIR%chatbot.py"
timeout /t 5 /nobreak >nul
start http://127.0.0.1:7860/
