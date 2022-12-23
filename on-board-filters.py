import numpy as np
from digi.xbee.devices import XBeeDevice
from digi.xbee.util import utils
from digi.xbee.models.address import XBee64BitAddress

import time
import os
import can
from datetime import datetime
#Setup can0 on rpi with these parameters
os.system('sudo ip link set can0 type can bitrate 500000')
os.system('sudo ifconfig can0 up')


# TODO: Replace with the serial port where your local module is connected to.
#PORT = "/dev/ttyUSB0" a
PORT = "/dev/ttyUSB0" 
# TODO: Replace with the baud rate of your local module. 9600 for S3B Xbee
BAUD_RATE = 9600 

txCount = 0
filters = [
    {"can_id":0x121,"can_mask":0x7FF,"extended":False}, #1
    {"can_id":0x132,"can_mask":0x7FF,"extended":False}, #2

    # GPS?
    {"can_id":0x175,"can_mask":0x7FF,"extended":False},#3 


    # add 
    # Coolant Temp as clt on ECU
    # decimal 1520 + 2 or 0x5F0 + 2
    # on this message:Baro, MAP, MAT, CLT
    {"can_id":0x5F2,"can_mask":0x7FF,"extended":False}, # 4

    
    # Fuel Pressure on Generic Sensor 1 
    # Bunched in 1520 + 13 or 0x5F0 + D  = 0x5FD
    # +13: Sensor 1, Sens 2 (RL LINPOT), Sens 3 (RR Lin), Sens 4 (Steering Angle)
    {"can_id":0x5FD,"can_mask":0x5FF,"extended":False}, # 5 

    
    # Oil Pressure as Generic 08, 
    # Bunched in 1520 + 14 or 0x5F0 + E = 0x5FE
    # +14: Sensor 5 (FR Lin), Sens 6 (FL Lin), Sens 7  
    {"can_id":0x5FE,"can_mask":0x5FF,"extended":False},  # 6

    # Oil Temp as Generic 09
    # Bunched in 1520 + 15 or 0x5F0 + F = 0x5FF
    # +15: Sensor 9, Sens 10 (accX), Sens 11 (accY), Sens 12 (accZ):
    {"can_id":0x5FD,"can_mask":0x5FF,"extended":False}, # 7

      
    
]
can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan', bitrate=500000,can_filters=filters)


def main():
    print(" +------------------------------------------------+")
    print(" | VMS Teletry System - install before flight     |")
    print(" +------------------------------------------------+\n")
    device = XBeeDevice(PORT, BAUD_RATE)
    device.open()
    print("Found Device! Node_ID",utils.hex_to_string(device.get_pan_id()))
    print(device.get_16bit_addr()," opened")
    txCount = 0

    while(True):
        xbee_network = device.get_network()
        remote_device = xbee_network.discover_device("Coordinator")
        print(xbee_network.get_devices())
        if( remote_device is None):
            print("Could not discover <<Coordinator>>; retrying")
        else:
            break
    
    lastTime = time.time()
    #return 
    Blocking = 0;
    MAXBlock = 20;

    while(True):
        data = bytearray([])
        for i in range(MAXBlock):
            msg=can0.recv()
            #print(msg.arbitration_id)
            arb = msg.arbitration_id
            if(arb == 289): # 0x121
                msg.data.insert(0,1)
                '''
                t_s = datetime.fromtimestamp(msg.timestamp)
                s = ["{0:02x}".format(m) for m in msg.data]
                sample = ' '.join(s)
                sample = "0x{0:02x} ".format(msg.arbitration_id) + sample + " " + str(msg.timestamp)
                sample = " Frame:" + str(txCount%MAXBlock) +" => " +sample
                print("\t",t_s.minute,t_s.second,t_s.microsecond,"ID 0x{0:02x}".format(msg.arbitration_id),sample)
                '''
                data.extend(msg.data)
                txCount = txCount + 1;
                
            elif(arb == 306): # 0x132 
                msg.data.insert(0,2)
                data.extend(msg.data)
                txCount = txCount + 1;
            elif(arb == 373): # 0x175 
                msg.data.insert(0,3)
                data.extend(msg.data)
                txCount = txCount + 1;
            elif(arb == 1522): # Coolant 0x5F2 
                msg.data.insert(0,4)
                data.extend(msg.data)
                txCount = txCount + 1;
            elif(arb == 1533): # Fuel Press 0x5FD 
                msg.data.insert(0,5)
                data.extend(msg.data)
                txCount = txCount + 1;
            elif(arb == 1534): # Oil Pressure 0x5FE 
                msg.data.insert(0,6)
                data.extend(msg.data)
                txCount = txCount + 1;
            elif(arb == 1535): # Oil Temp 0x5FF 
                msg.data.insert(0,7)
                data.extend(msg.data)
                txCount = txCount + 1;

            else:
                print("Unknown CAN Arbitration ID:",msg.arbitration_id)

        device.send_data(remote_device,data)

        if(txCount%100==0):
            newTime = time.time()
            print(txCount," messages sent. Last 100 time=>",newTime - lastTime)
            lastTime = newTime

if __name__ == '__main__':
    main()
