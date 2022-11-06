from re import T
import sys
import os
import random
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
import pyqtgraph as pg
from communication import Communication
from telemetry import Telemetry
from dataBase import data_base
from PyQt5.QtWidgets import QPushButton
from graphs.graph_acceleration import graph_acceleration
from graphs.graph_altitude import graph_altitude
from graphs.graph_battery import graph_battery
from graphs.graph_free_fall import graph_free_fall
from graphs.graph_gyro import graph_gyro
from graphs.graph_pressure import graph_pressure
from graphs.graph_speed import graph_speed
from graphs.graph_temperature import graph_temperature
from graphs.graph_time import graph_time
from graphs.graph_GenGauge import graph_GenGauge
from graphs.graph_4gauge import graph_4gauge
from graphs.graph_GPS import graph_GPS


pg.setConfigOption('background', (23, 23, 33))
pg.setConfigOption('foreground', (197, 198, 199))
# Interface variables
dir=os.getcwd()
log_dir = os.path.join(dir,"logs")
available_events = next(os.walk(log_dir))[1]
print("Available events: ", available_events)
event_valid = False
event_name = input("What event would you like to view? ")  
event_valid = event_name in available_events     
while(not event_valid): 
    print("\tEvent:",event_name," invalid")
    event_name = input("What event would you like to view? ")   
    event_valid = event_name in available_events
print("\t\t Displaying ",event_name)


app = QtWidgets.QApplication(sys.argv)
view = pg.GraphicsView()
Layout = pg.GraphicsLayout()
view.setCentralItem(Layout)
view.show()
view.setWindowTitle('VMS Dashboard')
view.resize(1200, 700)

# declare object for serial Communication
#ser = Communication()
tel = Telemetry(event_name)
# declare object for storage in CSV
data_base = data_base()
# Fonts for text items
font = QtGui.QFont()
fontSM = QtGui.QFont()
font.setPixelSize(90)
fontSM.setPixelSize(30)

# buttons style
style = "background-color:rgb(229, 114, 0);color:rgb(0,0,0);font-size:19px;"


# Declare graphs
# Button 1
proxy = QtWidgets.QGraphicsProxyWidget()
save_button = QtWidgets.QPushButton('Virginia Motorsports Telemetry Dashboard')
save_button.setStyleSheet(style)
save_button.clicked.connect(data_base.start)
proxy.setWidget(save_button)

# Button 2
#proxy2 = QtWidgets.QGraphicsProxyWidget()
#end_save_button = QtWidgets.QPushButton('Stop Lap')
#end_save_button.setStyleSheet(style)
#end_save_button.clicked.connect(data_base.stop)
#proxy2.setWidget(end_save_button)


IMUAccel = graph_acceleration()
IMUGyro = graph_gyro()
IMUGPS = graph_GPS()


'''
CoolantTemp = graph_coolant(font=font)
FuelPressure = graph_fuelpres(font=font)
OilPressure = graph_oilpres(font=font)
OilTemp = graph_oiltemp(font=font)
CoolantTemp = graph_GenGauge(font=font,title="CoolantTemp")
FuelPressure = graph_GenGauge(font=font,title="FuelPressure")
OilPressure = graph_GenGauge(font=font,title="OilPressure")
OilTemp = graph_GenGauge(font=font,title="OilTemp")
'''



x4_msg = graph_4gauge(font=fontSM, labelArr=["Baro  ","MAP","MAT","CLT"],title="0x5F2")
x5_msg = graph_4gauge(font=fontSM, labelArr=["F.Pres","RL ","RR ","StrAngl"],title="0x5FD")
x6_msg = graph_4gauge(font=fontSM, labelArr=["FR"    ,"FL" ,"####","OilPres"],title="0x5FE")
x7_msg = graph_4gauge(font=fontSM, labelArr=["TPS","Batt","OilTemp","EGO2"],title="0x5F3")
x8_msg = graph_GenGauge(font=fontSM,title="RPM")
#x9_msg = graph_4gauge(font=fontSM, labelArr=["s9","s10","s11","s12"],title="0x5FF")

'''
CoolantTemp.update(0.3)
FuelPressure.update(0.3)
OilPressure.update(0.3)
OilTemp.update(0.3)
'''



## Setting the graphs in the layout 
# Title at top
'''
text = """
Flight monitoring interface for cansats and OBC's <br>
developed at the Universidad Distrital FJC.
"""
'''
text = """
Virginia Motorsport Telemetry Dashboard
"""

#Layout.addLabel(text, col=1, colspan=21,font=font)
#Layout.nextRow()

# Put vertical label on left side
#Layout.addLabel('TELEMETRY',angle=-90, rowspan=3)
                
#Layout.nextRow()

lb = Layout.addLayout(colspan=21)
lb.addItem(proxy)
#lb.nextCol()
#lb.addItem(proxy2)

Layout.nextRow()

l1 = Layout.addLayout(colspan=20, rowspan=2, border=(255, 80, 80))
l11 = l1.addLayout(rowspan=1)
# Altitude, speed
#l11.nextColumn()
l11.addItem(IMUAccel)
#l11.nextColumn()
l11.addItem(IMUGyro)
l1.nextRow()

# Acceleration, gyro, pressure, temperature
l12 = l1.addLayout(rowspan=1, border=(83, 83, 83))
#l12.addItem(speed)
#l12.addItem(altitude)
#l12.addItem(pressure)
#l12.addItem(temperature)
l12.addItem(IMUGPS)

# Time, battery and free fall graphs
l2 = Layout.addLayout(colspan=1, rowspan=2,border=(83, 83, 83))

l2.addItem(x4_msg)
l2.nextRow()
l2.addItem(x5_msg)
l2.nextRow()
l2.addItem(x6_msg)
l2.nextRow()
l2.addItem(x7_msg)
l2.nextRow()
l2.addItem(x8_msg)
#l2.nextRow()
#l2.addItem(x9_msg)


#l22 = l2.addLayout(colspan=1, border=(83, 83, 83))

'''
l22.addItem(CoolantTemp)
l22.nextRow()
l22.addItem(FuelPressure)
l22.nextRow()
l22.addItem(OilPressure)
l22.nextRow()
l22.addItem(OilTemp)
'''

'''
l2.nextRow()
l2.addItem(free_fall)
'''
'''
l3 = Layout.addLayout(border=(83, 83, 83))
l3.addItem(OilPressure)
l3.nextRow()
l3.addItem(OilTemp)
'''



# you have to put the position of the CSV stored in the value_chain list
# that represent the date you want to visualize
def update():
    try:
        #value_chain = []
        #value_chain = ser.getData()
        # ACCEL_X, ACCEL_Y, ACCEL_Z, PITCH, ROLL, YAW, GPS_LAT, GPS_LONG, x4_msg, x5_msg, x6_msg, x7_msg, x8_msg

        tel.updateValuesFromCAN()
        ax,ay,az,pitch,roll,yaw,gps_lat,gps_long,x4m,x5m,x6m,x7m,x8m= tel.getData()
       
        IMUGyro.setData(pitch,roll,yaw)
        IMUAccel.setData(ax,ay,az)
        IMUGPS.setData(gps_lat,gps_long)
        '''
        CoolantTemp.setText(ax[-1])
        FuelPressure.setText(ax[-1])
        OilPressure.setText(ax[-1])
        OilTemp.setText(ax[-1])
        '''
        
        x4_msg.processCAN(x4m[-1])
        x5_msg.processCAN(x5m[-1])
        x6_msg.processCAN(x6m[-1])
        x7_msg.processCAN(x7m[-1])
        x8_msg.setFloat(x8m[-1])        
        #x9_msg.processCAN(x9m[-1])
        '''
        x4_msg.update(x4m[-1])
        x5_msg.update(x5m[-1])
        x6_msg.update(x6m[-1])
        x7_msg.update(x7m[-1])
        x8_msg.update(x8m[-1])  
        '''
        '''
        value_chain = [0] + random.sample(range(0, 300), 1) + \
            [random.getrandbits(1)] + random.sample(range(0, 20), 8)

        altitude.update(value_chain[1])
        speed.update(value_chain[8], value_chain[9], value_chain[10])
        #time.update(value_chain[0])
        acceleration.update(value_chain[8], value_chain[9], value_chain[10])
        gyro.update(value_chain[5], value_chain[6], value_chain[7])
        pressure.update(value_chain[4])
        temperature.update(value_chain[3])
        '''

        #free_fall.update(value_chain[2])
        #CoolantTemp.update(0.3)
        #FuelPressure.update(0.3)
        #OilPressure.update(0.3)
        #OilTemp.update(0.3)
        #data_base.guardar(value_chain)
    except IndexError as e:
        print('starting, please wait a moment',e)

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(300)
'''
if(ser.isOpen()) or (ser.dummyMode()):
    timer = pg.QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(50)
else:
    print("something is wrong with the update call")
'''

# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtWidgets.QApplication.instance().exec_()
