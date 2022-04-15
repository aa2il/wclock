@echo off
echo.
echo Notes about how to run wclock on Windoze 10
echo.
echo Already should have matplotlib, basemap installed from demos
echo.
echo This works ...
echo    wclock.py
echo.
echo ... but this does NOT work  :-(
echo   Problem appears to be with matplotlib
echo   So we're back to its time to find a replacement for basemap
echo.
echo   pyinstaller --onefile wclock.py
echo   dist\wclock.exe
echo.
