import pyqtgraph as pg
import numpy as np

class graph_GPS(pg.PlotItem):
     
    def __init__(self, parent=None, name=None, labels=None, title='GPS', viewBox=None, axisItems=None, enableMenu=True, **kargs):
        super().__init__(parent, name, labels, title, viewBox, axisItems, enableMenu, **kargs)
        
        self.addLegend()
        self.hideAxis('bottom')

        self.GPS_Graph = self.plot(pen=(255,255,255),name="Position")


        self.LAT = np.linspace(0, 0)
        self.LONG = np.linspace(0, 0)
        self.ptr = 0

    def setData(self, LAT, LONG):
        self.LAT = LAT
        self.LONG = LONG
    
        self.ptr1 = len(LONG)

        self.GPS_Graph.setData(self.LAT,self.LONG)

          