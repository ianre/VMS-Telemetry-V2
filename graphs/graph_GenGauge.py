import pyqtgraph as pg
from PyQt5.QtGui import QPainter, QColor, QFont

class graph_GenGauge(pg.PlotItem):
        
    def __init__(self, parent=None, name=None, labels=None, title='Generic Gauge', viewBox=None, axisItems=None, enableMenu=True, font = None,**kargs):
        super().__init__(parent, name, labels, title, viewBox, axisItems, enableMenu, **kargs)

        self.hideAxis('bottom')
        self.hideAxis('left')
        self.time_text = pg.TextItem("test",anchor=(0.5, 0.5), color="w")
        if font != None:
            self.time_text.setFont(font)
        self.addItem(self.time_text)
        #self.enableAutoRange()
        self.setXRange(-2, 2)
        self.setYRange(-2,2)
        
        self.ptr = 0

    def update(self, value):
        self.time_text.setPlainText('{0:.2f}   '.format(value))

    def setFloat(self,flt):
        self.time_text.setText('')
        try:
            self.time_text.setPlainText('{0:.2f}   '.format(flt))
        except Exception:
            self.time_text.setText("Null")

        
        self.time_text.setPos(self.ptr, 0)

    def setText(self,text):
        self.time_text.setText('')
        try:
            self.time_text.setText(str(text))
        except Exception:
            self.time_text.setText("Null")
        
        self.time_text.setPos(self.ptr, 0)
        

'''
    def update(self, value):
        self.time_text.setText('')
        #self.tiempo = round(int(value) / 60000, 2)
        #self.time_text.setText(str(self.tiempo))

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()

    def drawText(self, event, qp):
        qp.setPen(QColor(168, 34, 3))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(event.rect(), Qt.AlignCenter, self.text)

'''