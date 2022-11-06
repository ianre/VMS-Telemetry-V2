import pyqtgraph as pg


class graph_4gauge(pg.PlotItem):
        
    def __init__(self, parent=None, name=None, labels=None, title='Generic Gauge', viewBox=None, axisItems=None, enableMenu=True, font = None, labelArr=[],**kargs):
        super().__init__(parent, name, labels, title, viewBox, axisItems, enableMenu, **kargs)

        self.hideAxis('bottom')
        self.hideAxis('left')
        self.four_text = pg.TextItem("test", anchor=(0.5, 0.5), color="w")
        if font != None:
            self.four_text.setFont(font)
        self.addItem(self.four_text)
        self.labelArr = labelArr
        self.setXRange(-2, 2)
        self.setYRange(-2,2)
        
        #self.enableAutoRange()
        
    def processCAN(self, CAN_msg):
        lineText = ""        
        #lineText = '{0:.2f}'.format(CAN_msg[0])
        #"My name is {fname}, I'm {age}".format(fname = "John", age = 36)

        for i in range(0,4):
            lineText+="{data}:".format(data=self.labelArr[i]).ljust(10) + '{0:.2f}         '.format(CAN_msg[i])
            if i == 1:
                lineText+="\n\r"
        self.four_text.setText(lineText)


    def setText(self,text):
        self.four_text.setText(str(text))

    def update(self, value):
        lineText = ""        
        #lineText = '{0:.2f}'.format(CAN_msg[0])
        #"My name is {fname}, I'm {age}".format(fname = "John", age = 36)

        for i in range(0,4):
            lineText+="{data}:".format(data=self.labelArr[i]).ljust(10) + '{0:.2f}         '.format(value[i])
            if i == 1:
                lineText+="\n\r"
        self.four_text.setText(lineText)

'''
    def update(self, value):
        self.four_text.setText('')
        self.tiempo = round(int(value) / 60000, 2)
        self.four_text.setText(str(self.tiempo))
'''