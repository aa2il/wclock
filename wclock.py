#! /usr/bin/python3

# Migration to python 3 - doesn't always work under python 3 
# Problem is in basemap - Time to find a replacement

# sudo apt-get install python3-matplotlib python3-mpltoolkits.basemap

############################################################################################

import sys
from time import sleep
from datetime import timedelta,datetime
from pytz import timezone

#from PyQt4.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.qt_compat import QtCore, QtWidgets

# JBA - this fixes a bug? in mpl_toolkits
# It appears that basemaps (& python 2.7) are about to become obsolete so
# it may be time to start looking for an alternative.
import mpl_toolkits
mpl_toolkits.__path__.append('/usr/lib/python2.7/dist-packages/mpl_toolkits/')
from mpl_toolkits.basemap import Basemap

import matplotlib.pyplot as plt
#from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from itertools import chain
import numpy as np
import time 

############################################################################################

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


class WCLOCK_GUI(QMainWindow):

    def __init__(self, parent=None):
        super(WCLOCK_GUI, self).__init__(parent)

        print('Init GUI ...\n')
        self.count=0

        # Timer to update the map every 15 minutes
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.UpdateMap)
        timer.start(15*60*1000)

        # Start by putting up the root window
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        self.setWindowTitle('World Clock by AA2IL')

        # We use a simple grid to layout controls
        self.grid = QGridLayout(self._main)
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
        self.count+=1
        if self.count>1:
            #self.canv.draw()
            for item in self.CS.collections:
                item.remove()
        self.CS=self.m.nightshade(date1,alpha=0.5)

        # refresh canvas
        self.canv.draw()

    # Draw a shaded-relief image
    def draw_map(self,scale=0.01):
        self.ax = self.fig.add_subplot(111)
        self.fig.tight_layout(pad=0)

        lon_offset=30
        if True:
            m = Basemap(projection='cyl', resolution='c',
                        llcrnrlat=-90, urcrnrlat=90,
                        llcrnrlon=-180, urcrnrlon=180,
                        fix_aspect=False, ax=self.ax)
            m.shadedrelief(scale=scale)
            #m.bluemarble(scale=scale)
            #m.etopo(scale=scale)
        elif False:
            # Great circle map - sort of works but grey line is hosed up
            lon_0 = -105; lat_0 = 40
            m = Basemap(projection='aeqd',lat_0=lat_0,lon_0=lon_0,
                        fix_aspect=False, ax=self.ax)
            # fill background.
            m.drawmapboundary(fill_color='aqua')
            # draw coasts and fill continents.
            m.drawcoastlines(linewidth=0.5)
            m.fillcontinents(color='coral',lake_color='aqua')
            # 20 degree graticule.
            #m.drawparallels(np.arange(-80,81,20))
            #m.drawmeridians(np.arange(-180,180,20))
            # draw a black dot at the center.
            xpt, ypt = m(lon_0, lat_0)
            m.plot([xpt],[ypt],'ko')
            self.m = m
            return
        elif False:
            # There is a bug in basemap that prevents the reset of these from working
            # Need to update at some point - seems like a pain though
            # Search on     matplotlib basemap error in warpimage   to see error
            m = Basemap(projection='mill', resolution='c',
                        lon_0=-90,
                        fix_aspect=False, ax=self.ax)
            m.shadedrelief(scale=scale)
        elif False:
            m = Basemap(projection='cyl', resolution='c',
                        lon_0=-90,lat_0=0,
                        fix_aspect=False, ax=self.ax)
        elif False:
            m = Basemap(projection='cass', resolution='c',
                        llcrnrlat=-80, urcrnrlat=80,
                        llcrnrlon=-180, urcrnrlon=180,
                        lon_0=30.,lat_0=10.,
                        fix_aspect=False, ax=self.ax)
        else:
            m = Basemap(projection='eck4', resolution='c',
                        lon_0=30.,
                        fix_aspect=False, ax=self.ax)
        self.m = m
    
        # lats and longs are returned as a dictionary
        lats = m.drawparallels(np.linspace(-90, 90, 13))
        lons = m.drawmeridians(np.linspace(-180, 180, 13))
    
        # keys contain the plt.Line2D instances
        lat_lines = chain(*(tup[1][0] for tup in list(lats.items())))
        lon_lines = chain(*(tup[1][0] for tup in list(lons.items())))
        all_lines = chain(lat_lines, lon_lines)
    
        # cycle through these lines and set the desired style
        for line in all_lines:
            line.set(linestyle='-', alpha=0.3, color='w')

        # Draw politcal boundaries
        m.drawcoastlines()
        m.drawstates()
        m.drawcountries()

        # discards the old graph
        #ax.clear()

        # plot data
        #ax.plot(data, '*-')

        # refresh canvas
        #self.canvas.draw()


############################################################################################

# If the program is run directly or passed as an argument to the python
# interpreter then create a Calendar instance and show it
if __name__ == "__main__":

    print('\n****************************************************************************')
    print('\n   World Clock beginning ...\n')
    
    app  = QApplication(sys.argv)
    gui  = WCLOCK_GUI()
    
    sys.exit(app.exec_())
    
