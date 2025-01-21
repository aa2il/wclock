#! /home/joea/miniconda3/envs/aa2il/bin/python -u
#
# NEW: /home/joea/miniconda3/envs/aa2il/bin/python -u
# OLD: /usr/bin/python3 -u 
############################################################################################
#
# World Clock - Rev 2.0
# Copyright (C) 2021-5 by Joseph B. Attili, aa2il AT arrl DOT net
#
# Gui to show current GMT and Gray Line.  This new version uses cartopy
# rather than basemap.
#
# New in version 2.0:
# If user clicks time display widget, display flips over
# to local temperature for 5-seconds.
#
############################################################################################
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
############################################################################################

import sys
import os
from time import sleep
from datetime import timedelta,datetime    # ,UTC - Once we move to python 3.12
from pytz import timezone

try:
    if True:
        # This doesnt work right but I need to figure it out since ...
        # The changes are BS and typical of if it aint broke, let's fix it attitude
        # that keep linux from becoming dominant.  What a disgrace!
        # The main changes relate to the elimination of short-cut names for enum types.
        # I haven't found a definitive listing of the changes - best to serach using error generated.
        # Guessing often works too!
        # What a crock!!!!
        from PyQt6.QtWidgets import *  
        from PyQt6.QtGui import QPalette      # Too many differences from QT5 - ugh! 
        from PyQt6.QtCore import Qt,qVersion
    else:
        # ... there is a bug in PySide6 and this hangs on exit
        from PySide6.QtWidgets import *
        from PySide6.QtGui import QPalette
        from PySide6.QtCore import Qt,qVersion
except ImportError:
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import QPalette
    from PyQt5.QtCore import Qt,qVersion
    
from matplotlib.backends.qt_compat import QtCore, QtWidgets
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.image import imread

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.feature.nightshade import Nightshade

from itertools import chain
import numpy as np
import time
from utilities import find_resource_file

import requests, json
from latlon2maiden import maidenhead2latlon

############################################################################################

VERSION=2.0

############################################################################################

# Object to show a digital clock
class DigitalClock(QLCDNumber):
    def __init__(self, parent=None,wx=None):
        super(DigitalClock, self).__init__(parent)

        self.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)    
        #self.setSegmentStyle(QLCDNumber.Flat)        # Bolder
        self.setDigitCount(8)    # was 8
        self.setMinimumHeight(48)
        
        self.wx=wx
        self.timeout=0
        
        # In Qt6, keep segments from fading out when window is not selected
        print('QT Version=',qVersion())
        if True:
            # This seems a little easier somehow
            self.setStyleSheet("""QLCDNumber { 
            color: black; }""")
            #background-color: white; 
        elif True:    
            # This also works 
            # Set the foreground color (color of the displayed digits)
            palette = self.palette()
            palette.setColor(QPalette.WindowText, Qt.black)
            self.setPalette(palette)

            # Set the background color
            #palette.setColor(QPalette.Window, Qt.black)
            #self.setPalette(palette)

        # Start the ball rolling
        self.show()
        self.show_clock=True
        self.UpdateTime()
        
        # Time to update clock every second
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.UpdateTime)
        timer.start(1000)

    def UpdateTime(self):
        self.show_clock = self.wx==None or self.timeout==0
        if self.show_clock:
            #print('Tic ...',self.timeout)
            now_utc = datetime.now(timezone('UTC'))
            text = now_utc.strftime("%H:%M:%S")
            self.setDigitCount(8) 
            #self.show()
            self.display(text)
        else:
            self.timeout-=1
            #print('... Toc ',self.timeout)

    # Callback if mouse button is pressed while in the LCD display area
    def mousePressEvent(self,event):
        print('mousePressEvent=',event)
        #print(dir(event))
        #print("mousePressEvent:",event.position())
        if self.wx!=None:
            self.timeout=5
            self.setDigitCount(9) 
            self.display(self.wx)
        
############################################################################################

def get_wx(api_key,city=None,lat=None,lon=None):

    if city!=None:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    else:
        url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'        
    response = requests.get(url)
    print(response)

    if response.status_code == 200:
        data = response.json()
        print(data)
        temp_k = data['main']['temp']
        temp_c = temp_k-273
        temp_f = temp_c*9/5+32
        desc = data['weather'][0]['description']
        print(f'Temperature: {temp_k} K = {int(temp_c)} C = {int(temp_f)} F')
        print(f'Description: {desc}')
    else:
        print('Error fetching weather data')

    wx = f"{int(temp_f)}'f {int(temp_c)}'c"
    return wx

############################################################################################

# The overall gui
class WCLOCK_GUI(QMainWindow):

    def __init__(self,args,parent=None,api_key=None,gridsq=None):
        super(WCLOCK_GUI, self).__init__(parent)

        print('Init GUI ...\n')
        self.wx=None
        self.api_key=api_key
        self.gridsq=gridsq

        # Timer to update the map every 15 minutes
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.UpdateMap)
        timer.start(15*60*1000)

        # Start by putting up the root window
        self.win = QtWidgets.QWidget()
        self.setCentralWidget(self.win)
        self.setWindowTitle('World Clock by AA2IL')

        # Place window into lower right corner
        geo=args.geo
        if geo==None:
            #screen_resolution = app.desktop().screenGeometry()
            screen_resolution = app.primaryScreen().size()
            width  = screen_resolution.width()
            height = screen_resolution.height()
            print("Screen Res:",screen_resolution,width, height)
            h=300   # 210
            w=300
            x=width-w
            y=height-h            
        else:
            # WWWxHHH+XXX+YYY
            #wclock.py -geo 390x360+1110+710
            print('geo=',geo)
            geo2=geo.split('+')
            print('geo2=',geo2)
            geo3=geo2[0].split('x')
            print('geo3=',geo3)
            w=int( geo3[0] )
            h=int( geo3[1] )
            x=int( geo2[1] )
            y=int( geo2[2] )
        print('geo=',geo,'\tx=',x,'\ty=',y,'\tw=',w,'\th=',h)
        self.setGeometry(x,y,w,h)

        # We use a simple grid to layout controls
        self.grid = QGridLayout(self.win)
        nrows=3
        ncols=1

        # Get weather
        if True:    # args.wx:
            print('grid=',self.grid)
            self.lat, self.lon = maidenhead2latlon(self.gridsq)
            print('lat=',self.lat,'\tlon=',self.lon)
            self.wx=get_wx(self.api_key,lat=self.lat,lon=self.lon)
            print('WX=',self.wx)

        # The clock
        row=0
        col=0
        self.clock = DigitalClock(wx=self.wx)
        self.grid.addWidget(self.clock,row,col,2,ncols)
        #self.clock.show()
        #self.show_clock=True
        
        sizePolicy = QSizePolicy( QSizePolicy.Policy.Minimum, 
                                  QSizePolicy.Policy.Minimum)
        self.clock.setSizePolicy(sizePolicy)
        #print('Clock hint=',self.clock.sizeHint(),'\tsize=',self.clock.geometry())
        self.clock.setMinimumSize(200,50)
        
        # The Canvas where we will put the map
        row=2
        self.fig = Figure()
        self.canv = FigureCanvas(self.fig)
        self.grid.addWidget(self.canv,row,col,1,ncols)

        # Allow canvas size to change when we resize the window
        # but make is always visible
        #sizePolicy = QSizePolicy( QSizePolicy.MinimumExpanding, 
        #                          QSizePolicy.MinimumExpanding)
        sizePolicy = QSizePolicy( QSizePolicy.Policy.Expanding,
                                  QSizePolicy.Policy.Expanding)
        self.canv.setSizePolicy(sizePolicy)

        # Draw the map
        self.draw_map()
        self.UpdateMap()

        # Let's roll!
        self.show()
        if args.desktop!=None:
            #cmd1='wmctrl -r "World Clock" -t '+str(args.desktop)
            #print(cmd1)
            cmd2='wmctrl -r "'+self.windowTitle()+'" -t '+str(args.desktop)
            #print(cmd2)
            os.system(cmd2)
        
    # Function to update the map
    def UpdateMap(self):
        
        # Shade the night areas
        date1 = datetime.utcnow()
        #date1 = datetime.now(UTC)     # Once we move to python 3.12

        print('Updating map @ ',date1)

        if self.nightmap:
            self.nightmap.remove()
        self.nightmap=self.ax.add_feature(Nightshade(date1, alpha=0.5))

        # refresh canvas
        self.canv.draw()

    # Draw a shaded-relief image
    def draw_map(self,scale=0.01):

        self.ax = self.fig.add_subplot(111, projection=ccrs.PlateCarree())
        if False:
            # This doesn't work under pyinstaller ...
            self.ax.stock_img()
            #self.fig.canvas.draw()
        else:
            # ... so we load image directly instead
            # Need figure out where it is since this varies from linux to windoz
            fname=find_resource_file('50-natural-earth-1-downsampled.png')
            img = imread(fname)
            self.ax.imshow(img, origin='upper', transform=ccrs.PlateCarree(), extent=[-180, 180, -90, 90])
        
        self.ax.set_aspect('auto')
        self.fig.tight_layout(pad=0)

        # Create a feature for States/Admin 1 regions at 1:50m from Natural Earth
        states_provinces = cfeature.NaturalEarthFeature(
            category='cultural',
            name='admin_1_states_provinces_lines',
            scale='50m',
            facecolor='none')

        # Draw politcal boundaries
        self.ax.add_feature(cfeature.LAND)
        self.ax.add_feature(cfeature.COASTLINE)
        self.ax.add_feature(cfeature.BORDERS)
        self.ax.add_feature(states_provinces, edgecolor='gray')

        #self.ax.set_xticks( np.linspace(-90, 90, 13) )
        #self.ax.set_yticks( np.linspace(-180, 180, 13) )
        self.ax.gridlines(linestyle=':')

        self.ax.set_aspect('auto')
        self.fig.tight_layout(pad=0)

        self.nightmap=None
        
        
############################################################################################

# If the program is run directly or passed as an argument to the python
# interpreter then create a gui instance and show it
if __name__ == "__main__":
    import argparse
    
    print('\n****************************************************************************')
    print('\n   World Clock',VERSION,'beginning ...\n')

    # Command line args
    arg_proc = argparse.ArgumentParser(description='World Clock')
    arg_proc.add_argument('-geo',type=str,default=None,
                          help='Geometry')
    arg_proc.add_argument('-desktop',type=int,default=None,
                          help='Desk Top Work Space No.')
    #arg_proc.add_argument('-wx', action='store_true',
    #                      help='Toggle between time and weather')
    args = arg_proc.parse_args()

    # Get Open Weather Map API key and my grid square
    RCFILE=os.path.expanduser("~/.keyerrc")
    with open(RCFILE) as f:
        SETTINGS = json.load(f)
    print(SETTINGS)
    
    app  = QApplication(sys.argv)
    gui  = WCLOCK_GUI(args,api_key=SETTINGS['MY_OWM_API_KEY'],gridsq=SETTINGS['MY_GRID'])

    print('And away we go !')
    #sys.exit(app.exec())
    app.exec()
    print('Thats all folks!')
    sys,exit(0)
    print('Thats all folks!')
    
