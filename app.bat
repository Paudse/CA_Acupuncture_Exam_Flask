@echo off
start /b python ./app.py
timeout /t 5 > nul
start chrome.exe --incognito http://127.0.0.1:5000