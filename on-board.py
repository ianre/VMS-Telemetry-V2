import numpy as np
from digi.xbee.devices import XBeeDevice
from digi.xbee.util import utils
from digi.xbee.models.address import XBee64BitAddress

import time
import os
import can

#Setup can0 on rpi with these parameters

os.system('sudo ip link set can0 type can bitrate 500000')
os.system('sudo ifconfig can0 up')


# TODO: Replace with the serial port where your local module is connected to.
PORT = "/dev/ttyUSB0"
# TODO: Replace with the baud rate of your local module. 9600 for S3B Xbee
BAUD_RATE = 9600 

txCount = 0
filters = [
    {"can_id":0x121,"can_mask":0x7FF,"extended":False},
    #{"can_id":0x132,"can_mask":0x7FF,"extended":False}
]
can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan', bitrate=500000,can_filters=filters)


def main():
    print(" +------------------------------------------------+")
    print(" | VMS Teletry System - install before flight     |")
    print(" +------------------------------------------------+\n")
    try:
        device = XBeeDevice(PORT, BAUD_RATE)
        device.open()
        print("Found Device! Node_ID",utils.hex_to_string(device.get_pan_id()))
        print(device.get_16bit_addr()," opened")
        txCount = 0
        while(True):
            try:
                #msg = can0.recv(30.0) # timeout=none, timeout=30
                msg=can0.recv()
                print("ID 0x{0:02x}".format(msg.arbitration_id))
                print("\ttimestamp",msg.timestamp)
                if msg is None:
                    print('No message was received')
                    continue

                #s = [str(m) for m in msg.data]
                s = ["{0:02x}".format(m) for m in msg.data]
                sample = ' '.join(s)
                sample = "0x{0:02x} ".format(msg.arbitration_id) + sample + " " + str(msg.timestamp)
                sample = " Frame:" + str(txCount) +" => " +sample

                print("\tdata",msg.data,":",sample)
                #start = time.time()
                device.send_data_broadcast(sample)
                #end = time.time()
                txCount = txCount + 1;
                #print(txCount, "in" , end - start)
                print()
            except Exception as e:
                print(e)

        print("Success")
    except Exception as ex:
        print(ex)
    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
