#! /usr/bin/python3 -u
############################################################################################
#
# World Clock - Rev 2.0
# Copyright (C) 2021-2 by Joseph B. Attili, aa2il AT arrl DOT net
#
# Gui to show current GMT and Gray Line.  This new version uses cartopy
# rather than basemap.
#
# Notes:
# - Need to install cartopy
#   Linux:
#      sudo apt-get install python3-matplotlib python3-cartopy
#   Windows 10 - Haven't tried it yet ??????
#      pip install cartopy????
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
from time import sleep
from datetime import timedelta,datetime
from pytz import timezone

from PyQt5.QtWidgets import *
from matplotlib.backends.qt_compat import QtCore, QtWidgets

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.feature.nightshade import Nightshade

from itertools import chain
import numpy as np
import time 

############################################################################################

# Object to show a digital clock
class DigitalClock(QLCDNumber):
    def __init__(self, parent=None):
        super(DigitalClock, self).__init__(parent)

        self.setSegmentStyle(QLCDNumber.Filled)
        self.setDigitCount(8)
        self.setMinimumHeight(48)

        # Time to update clock every second
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.UpdateTime)
        timer.start(1000)

        self.UpdateTime()

    def UpdateTime(self):
        now_utc = datetime.now(timezone('UTC'))
        text = now_utc.strftime("%H:%M:%S")
        self.display(text)

############################################################################################

# The overall gui
class WCLOCK_GUI(QMainWindow):

    def __init__(self, parent=None):
        super(WCLOCK_GUI, self).__init__(parent)

        print('Init GUI ...\n')

        # Timer to update the map every 15 minutes
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.UpdateMap)
        timer.start(15*60*1000)

        # Start by putting up the root window
        self.win = QtWidgets.QWidget()
        self.setCentralWidget(self.win)
        self.setWindowTitle('World Clock by AA2IL')

        # Place window into lower right corner
        screen_resolution = app.desktop().screenGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        print("Screen Res:",screen_resolution,width, height)
        h=300   # 210
        self.setGeometry(width-300,height-h,300,h)

        # We use a simple grid to layout controls
        self.grid = QGridLayout(self.win)
        nrows=3
        ncols=1

        # The clock
        row=0
        col=0
        self.clock = DigitalClock()
        self.grid.addWidget(self.clock,row,col,2,ncols)
        self.clock.show()

        # The Canvas where we will put the map
        row=2
        self.fig = Figure()
        self.canv = FigureCanvas(self.fig)
        self.grid.addWidget(self.canv,row,col,1,ncols)

        # Allow canvas size to change when we resize the window
        # but make is always visible
        #sizePolicy = QSizePolicy( QSizePolicy.MinimumExpanding, 
        #                                QSizePolicy.MinimumExpanding)
        #self.canv.setSizePolicy(sizePolicy)

        # Draw the map
        self.draw_map()
        self.UpdateMap()

        # Let's roll!
        self.show()
        
    # Function to update the map
    def UpdateMap(self):
        
        # Shade the night areas
        date1 = datetime.utcnow()
        print('Updating map @ ',date1)

        if self.nightmap:
            self.nightmap.remove()
        self.nightmap=self.ax.add_feature(Nightshade(date1, alpha=0.5))

        # refresh canvas
        self.canv.draw()

    # Draw a shaded-relief image
    def draw_map(self,scale=0.01):

        self.ax = self.fig.add_subplot(111, projection=ccrs.PlateCarree())
        self.ax.stock_img()
        #self.fig.canvas.draw()
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

    print('\n****************************************************************************')
    print('\n   World Clock beginning ...\n')
    
    app  = QApplication(sys.argv)
    gui  = WCLOCK_GUI()
    
    sys.exit(app.exec_())
    
