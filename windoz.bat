@echo off
goto BUILD
echo %DATE% %TIME%
echo.
echo Notes about how to run wclock on Windoze 10
echo.
echo Already should have matplotlib, cartopy/basemap installed from demos
      pip install -r requirements.txt
echo.
echo To run script directly under python:
       wclock.py
:BUILD       
echo.
echo To compile - this takes a long time:
       pyinstaller --onefile wclock.py
       copy ..\data\50-natural-earth-1-downsampled.png dist
echo.
echo To test binary:
       dist\wclock.exe
echo.
echo On linux:
echo   "cp ../data/50-natural-earth-1-downsampled.png dist"
echo   dist/wclock
echo.
echo ---------------------------------------------------------------------
echo.
echo This is deprecated but works under windoz ...
echo   wclock1.py
echo.
echo ... but this does NOT work  :-(
echo   Problem appears to be with matplotlib
echo   Already have migrated away from basemap so don't worry about it
echo.
echo   pyinstaller --onefile wclock1.py
echo   dist\wclock1.exe
echo.
echo %DATE% %TIME%
echo.
