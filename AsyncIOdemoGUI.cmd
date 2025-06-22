@Echo Off
Rem SPDX-License-Identifier: GPL-3.0-or-later
Title AsyncIOdemo GUI
SetLocal

Set HeaderName=comms.h
Set OutputName=PythonGUI\%HeaderName:.h=.py%

Echo # Do not edit - Auto-ported from Arduino C by %~nx0 > %OutputName%
Echo. >> %OutputName%
sed -e "s/const [^ ]* /CONST_/" -e "s/;/	# ;/" -e "s/\/\//# \/\//" %HeaderName% >> %OutputName%

Title Waiting for the GUI to close
python PythonGUI\AsyncIOdemoGUI.py

EndLocal
