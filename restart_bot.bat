@echo off
:restart
cls
python bot.py
timeout /t 2 /nobreak
goto restart