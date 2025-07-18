@echo off
echo %DATE% %TIME%
echo.
echo Get wclock up and running under Windows 11 using uv:
echo.
echo Install uv:
echo.
echo       powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
echo.
echo Install git client:
echo.
echo        https://git-scm.com/downloads/win
echo.
echo Clone source code:
echo.
        cd %userprofile%
        mkdir Python
        cd Python
        git clone https://github.com/aa2il/wclock
        git clone https://github.com/aa2il/libs
        git clone https://github.com/aa2il/data
echo.
echo Bombs away:
echo.
        cd wclock
        uv run wclock.py
echo.
exit
echo.
echo Older installation methods follow below
echo.
goto BUILD
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
       copy Release_Notes.txt dist
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
echo This is deprecated (it uses basemap) but works under windoz ...
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
