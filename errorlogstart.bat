@echo off
SET FIVEM_SERVER_EXECUTABLE_PATH=insertserverstartupfilepathhere

python "monitor_fivem.py"

"%FIVEM_SERVER_EXECUTABLE_PATH%" +set serverProfile "default"

pause
