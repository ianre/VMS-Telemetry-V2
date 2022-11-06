"""
This example demonstrates many of the 2D plotting capabilities
in pyqtgraph. All of the plots may be panned/scaled by dragging with 
the left/right mouse buttons. Right click on any plot to show a context menu.
"""

import numpy as np
import os
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from gmplot import gmplot
import ctypes
import numpy

import struct
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

class Telemetry:
    '''
    CWD = os.path.dirname(os.path.realpath(__file__))
    LOG_FILE = os.path.join(self.CWD, "log_new b.txt")
    Epoc = []
    ACCEL_X = []
    ACCEL_Y = []
    ACCEL_Z = []

    PITCH = []
    ROLL = []
    YAW = []

    GPS_LAT = []
    GPS_LONG = []

    CoolantTemp = [];
    FuelPressure = [];
    OilPressure = [];
    OilTemp = [];
    '''
    def __init__(self, eventName):
        #idk
        self.CWD = os.path.dirname(os.path.realpath(__file__))

        self.eventName = eventName
        self.eventFold = os.path.join(self.CWD,"logs",self.eventName)

        self.LOG_FILE = self.getLastLogPath(self.eventFold) 
        self.Epoc = []
        
        #0x1
        self.ACCEL_X = [0.0]
        self.ACCEL_Y = [0.0]
        self.ACCEL_Z = [0.0]

        #0x2
        self.PITCH = [0.0]
        self.ROLL = [0.0]
        self.YAW = [0.0]

        #0x3
        self.GPS_LAT = []
        self.GPS_LONG = []

        #0x4
        self.x4_msg = [[0.0,0.0,0.0,0.0]]
        #0x5
        self.x5_msg = [[0.0,0.0,0.0,0.0]]
        #0x6
        self.x6_msg = [[0.0,0.0,0.0,0.0]]
        #0x7
        self.x7_msg = [[0.0,0.0,0.0,0.0]]
        #0x8
        self.x8_msg = [0.0]

        #self.x9_msg = [[0.0,0.0,0.0,0.0]]
        

        self.currentLine = 0;
    
    def getData(self):
        return self.ACCEL_X,self.ACCEL_Y,self.ACCEL_Z,self.PITCH,self.ROLL,self.YAW,self.GPS_LAT,self.GPS_LONG,self.x4_msg,self.x5_msg,self.x6_msg,self.x7_msg,self.x8_msg

    def getLastLogPath(self,eventFold):
        files = os.listdir(eventFold)
        paths = [os.path.join(eventFold, basename) for basename in files]
        return max(paths, key=os.path.getctime)

    def updateValuesFromCAN(self):

        def to_int(val, nbits):
            i = int(val, 16)
            if i >= 2 ** (nbits - 1):
                i -= 2 ** nbits
            return i
        #try:
        with open(self.LOG_FILE,'r') as f:
            lines = f.readlines()
            if(len(lines)>self.currentLine+10):
                for i in range(self.currentLine,len(lines)-1):
                    dataLine = lines[i].rstrip();
                    dataLineSplit = dataLine.split("#")
                    arbID = dataLineSplit[0]
                    dataStr = dataLineSplit[1]
                    split = dataStr.split(" ")
                    #print("arbID",arbID,"split",split)
                    #print(len(split))
                    #quit()
                    
                    if(arbID == "0x1"):
                        ax_raw = split[1]+split[0]
                        ay_raw = split[3]+split[2]
                        az_raw = split[5]+split[4]
                        #print(split[2],split[1],"makes")
                        #acc_dx = float.fromhex(ax_raw)/100
                        acc_dx = to_int(ax_raw, 16)/100
                        #acc_dy = float.fromhex(ay_raw)/100
                        acc_dy = to_int(ay_raw, 16)/100
                        #acc_dz = float.fromhex(az_raw)/100
                        acc_dz = to_int(az_raw, 16)/100
                        self.ACCEL_X.append(acc_dx)
                        self.ACCEL_Y.append(acc_dy)
                        self.ACCEL_Z.append(acc_dz)
                    elif(arbID == "0x2"):
                        gx_raw = split[1]+split[0]
                        gy_raw = split[3]+split[2]
                        gz_raw = split[5]+split[4]
                        gyr_dx = to_int(gx_raw, 16)/100
                        gyr_dy = to_int(gy_raw, 16)/100
                        gyr_dz = to_int(gz_raw, 16)/100
                        self.PITCH.append(gyr_dx)
                        self.ROLL.append(gyr_dy)
                        self.YAW.append(gyr_dz)
                    elif(arbID == "0x3"):
                        GPS_lat_raw = split[2]+split[1]+split[0]
                        GPS_long_raw = split[5]+split[4]+split[3]                        
                        GPS_lat = to_int(GPS_lat_raw, 16)/1000
                        GPS_long= to_int(GPS_long_raw, 16)/1000                        
                        self.GPS_LAT.append(GPS_lat)
                        self.GPS_LONG.append(GPS_long)

                    # all data from ECU is Big-Endian
                    #0x5F2	1522	clt Coolant temperature                     
                    elif(arbID == "0x4"):
                        item1_raw = split[0]+split[1]
                        item2_raw = split[2]+split[3]
                        item3_raw = split[4]+split[5]
                        clt_raw = split[6]+split[7]

                        item1 = to_int(item1_raw,16)/10
                        item2 = to_int(item2_raw,16)/10
                        item3 = to_int(item3_raw,16)/10
                        clt = to_int(clt_raw,16)/10
                        
                        self.x4_msg.append([item1,item2,item3,clt])    

                    #0x5FD	1533	fuel_press1 Fuel pressure 1 
                    elif(arbID == "0x5"):
                        fuel_pres_raw = split[0]+split[1]
                        s2_raw = split[2]+split[3]
                        s3_raw = split[4]+split[5]
                        s4_raw = split[6]+split[7]

                        fuel_pres = to_int(fuel_pres_raw,16)/100
                        s2 = to_int(s2_raw,16)/1000
                        s3 = to_int(s3_raw,16)/1000
                        s4 = to_int(s4_raw,16)/100

                        self.x5_msg.append([fuel_pres,s2,s3,s4])

                    #0x5FE	1534	oil pressure
                    elif(arbID == "0x6"):
                        s5_raw = split[0]+split[1]
                        s6_raw = split[2]+split[3]
                        s7_raw = split[4]+split[5]
                        oil_pres_raw = split[6]+split[7]

                        s5 = to_int(s5_raw,16)/1000
                        s6 = to_int(s6_raw,16)/1000
                        s7 = to_int(s7_raw,16)/1000
                        oil_pres = to_int(oil_pres_raw,16)/1000

                        self.x6_msg.append([s5,s6,s7,oil_pres])
                    
                    #actually in 0x5F3:tps,bat,ego1
                    elif(arbID == "0x7"):
                        tps_raw = split[0]+split[1]
                        bat_raw = split[2]+split[3]
                        ego1_raw = split[4]+split[5]
                        ego2_raw = split[6]+split[7]

                        tps = to_int(tps_raw,16)/10
                        bat = to_int(bat_raw,16)/10
                        ego1 = to_int(ego1_raw,16)/1
                        ego2 = to_int(ego2_raw,16)/10
                        self.x7_msg.append([tps,bat,ego1,ego2])

                    elif(arbID == "0x8"):
                        rpm_raw = split[0]+split[1]+split[2]+split[3]+split[4]+split[5]+split[6]+split[7]

                        rpm = to_int(rpm_raw,16)/1000
                        self.x8_msg.append(rpm)
                    '''
                    elif(arbID == "0x9"):
                        s9_raw = split[0]+split[1]
                        s10_raw = split[2]+split[3]
                        s11_raw = split[4]+split[5]
                        s12_raw = split[6]+split[7]

                        s9 = to_int(tps_raw,16)/10
                        s10 = to_int(bat_raw,16)/10
                        s11 = to_int(ego1_raw,16)/1
                        s12 = to_int(ego2_raw,16)/10
                        self.x9_msg.append([s9,s10,s11,s12])
                    '''

                print("current line:",self.currentLine,"to:",len(lines))
                self.currentLine = len(lines)
        #except Exception as e:
        #    print(e)
    
    def update(self):
        self.updateValuesFromCAN()
        return

