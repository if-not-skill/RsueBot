@echo off
set CWD=%~dp0
set PYTHONPATH=%CWD%
set PYTHONPYCACHEPREFIX=%CWD%\temp
python -B %CWD%rsue_bot.py %*
