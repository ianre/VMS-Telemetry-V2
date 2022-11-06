# Copyright 2017, Digi International Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from struct import pack
from digi.xbee.devices import XBeeDevice
import time
import pathlib
import os

# TODO: Replace with the serial port where your local module is connected to.
PORT = "COM7"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 9600
global txCount
txCount = 0;
global lastTime 
global log_id
log_id = 0
CWD = os.path.dirname(os.path.realpath(__file__))


def main():
    print(" +-----------------------------------------+")
    print(" | VMS Telemetry - Base Station Dashboard  |")
    print(" +-----------------------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)

    global lastTime 
    global log_id
    lastTime = time.time()
    
    event_name = input("Enter a name for this event:")
    event_path = os.path.join(CWD,"logs",event_name)

    
    f_name = "log.txt"
    if(not os.path.isdir(event_path)):
        path = pathlib.Path(event_path)
        path.mkdir(parents=True, exist_ok=True)
        print("\tStarting new event:" + event_name)
        f_name = os.path.join(CWD,"logs",event_name,"log_"+str(log_id)+".txt")
        f_name_valid = False
        if(os.path.isfile(f_name)):       
            while( not f_name_valid):
                log_id +=1
                f_name = os.path.join(CWD,"logs",event_name,"log_"+str(log_id)+".txt")  
                if( not os.path.isfile(f_name)):
                    f_name_valid = True       
        else:
            pass
        print("\t\tSaving",event_name,"log_"+str(log_id)+".txt")
    else:   
        print("\tEvent:",event_name," already exists.")
        f_name = os.path.join(CWD,"logs",event_name,"log_"+str(log_id)+".txt")
        f_name_valid = False
        if(os.path.isfile(f_name)):       
            while( not f_name_valid):
                log_id +=1
                f_name = os.path.join(CWD,"logs",event_name,"log_"+str(log_id)+".txt")  
                if( not os.path.isfile(f_name)):
                    f_name_valid = True       
        else:
            pass
        print("\t\tSaving",event_name,"log_"+str(log_id)+".txt")

    
    '''
    f_name = "log "+str(log_id)+".txt"
    f_name_valid = False
    if(os.path.isfile(f_name)):       
        while( not f_name_valid):
            log_id +=1
            f_name = "log "+str(log_id)+".txt"    
            if( not os.path.isfile(f_name)):
                f_name_valid = True       
    else:
        pass
    '''

    f = open(f_name, 'a')    
    
    '''
    if(os.path.isfile("log "+ str(log_id)+".txt")):
        os.remove("log.txt")
    '''
    

    try:
        device.open()
        def data_receive_callback(xbee_message):
            addr = xbee_message.remote_device.get_64bit_addr()
            m = xbee_message.data
            #print("M",m)
            currCANID = 0;
            #currByte = 
            #data = [hex(b) for b in m]
            data= [hex(b) for b in m]
            #print("DATA:",data)
            package_size = 0;
            i = 0;
            while( i < len(data) ):
            #for i in range(len(data)):
                #if (i%7==0):
                currCANID = data[i];
                global txCount
                txCount = txCount +1;
                i=i+1
                if currCANID == "0x1":
                    #print("Acc:",data[i:i+6])
                    package_size = 6;
                elif currCANID == "0x2":
                    #print("Gyro:",data[i:i+6])
                    package_size = 6;
                elif currCANID == "0x3":
                    #print("GPS:",data[i:i+8])
                    package_size = 8;
                elif currCANID == "0x4":
                    #print("Coolant:",data[i:i+8])
                    package_size = 8
                elif currCANID == "0x5":
                    #print("Fuel Pressure",data[i:i+8])
                    package_size = 8
                elif currCANID == "0x6":
                    #print("Oil Pressure",data[i:i+8])
                    package_size = 8
                elif currCANID == "0x7":
                    #print("Oil Temp",data[i:i+8])
                    package_size = 8
                elif currCANID == "0x8":
                    package_size = 8
                else:
                    print("Unknown CAN ID: ",data[i-1:i+7])

                #print("\t","[i:i+7]",data[i:i+7])
                if(i + 6 > len(data)):
                    break
                
                #print(type(m[i]),"i",i,":",hex(m[i]))
                #f.write(str(a)+","+) 
                
                #print('0x %d: {0:02x}{:02x}  {0:02x}{:02x} {0:02x}{:02x} '.format(currCANID, data[i],data[i+1],data[i+2],data[i+3],data[i+4],data[i+5]))
                #print(' 0x{:02x}: {:02x} '.format(currCANID, data[i+1]))
                #print('0x{:02x}:'.format(currCANID))
                
                #print("CurrCANID",type(currCANID),currCANID)
                #print("data 0 ",type(data[i]),data[i])
                #print("data 1 ",type(data[i+1]),data[i+1])
                #toSend = currCANID+"#"+" ".join([d[2:] for d in data[i:i+6]])
                toSend = currCANID+"#"+ " ".join(["{0:02x}".format(single) for single in m[i:i+package_size]])
                #print("ToSend",toSend,"\n")
                f.write(toSend+"\n")
                f.flush()
                i=i+package_size

            #txCount = txCount +1;
            #global txCount
            if(txCount%100<15):# 5 if the inner loop does not divide into 100
                newTime=time.time()
                global lastTime
                print(txCount, " messages received. Last 100 in:",newTime-lastTime,time.time())
                #print(txCount, " messages received. Last 100 in:",newTime-lastTime)
                
                lastTime=newTime

            #if(txCount%2==0):
            #    f.flush()

        device.add_data_received_callback(data_receive_callback)

        print("Waiting for data...\n")
        input()

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
