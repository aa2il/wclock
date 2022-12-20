@echo off
echo.
echo Notes about how to run wclock on Windoze 10
echo.
echo Already should have matplotlib, basemap installed from demos
echo.
echo This does not work bx we need cartopy on winbloz
echo   wclock.py
echo.
echo Need to test this under windoz - works under linux
echo   pyinstaller --onefile wclock.py
echo   dist\wclock.exe
echo
echo This works under windoz ...
echo   wclock1.py
echo.
echo ... but this does NOT work  :-(
echo   Problem appears to be with matplotlib
echo   Already have migrated away from basemap so don't worry about it
echo.
echo   pyinstaller --onefile wclock1.py
echo   dist\wclock1.exe
echo.
