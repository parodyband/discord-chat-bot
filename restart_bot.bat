@echo off
:restart
python bot.py
timeout /t 2 /nobreak
goto restart