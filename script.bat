@echo off
set vbscript="%temp%\minimize_windows.vbs"

echo Set objShell = WScript.CreateObject("Shell.Application") > %vbscript%
echo objShell.MinimizeAll >> %vbscript%

cscript /nologo %vbscript%
del %vbscript%
start msgbox.vbs
