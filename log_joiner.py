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

from math import comb
from struct import pack
from digi.xbee.devices import XBeeDevice
import time
import pathlib
import os

global txCount
txCount = 0;
global lastTime 
global log_id
log_id = 0
CWD = os.path.dirname(os.path.realpath(__file__))


def main():
    
    global lastTime 
    global log_id
    lastTime = time.time()
    
    path1 = os.path.join(CWD,"logs","gps_logs","log_0.txt")
    path2 = os.path.join(CWD,"logs","morning","log_2.txt")
    outputPath = os.path.join(CWD,"logs","comb","log_0.txt")
    

    
    gps_lines = []
    combined = []
    with open(path1) as file:
        for line in file:
            dataLine = line.rstrip();
            dataLineSplit = dataLine.split("#")
            arbID = dataLineSplit[0]
            dataStr = dataLineSplit[1]
            split = dataStr.split(" ")
            if("0x3" in arbID):
                gps_lines.append(line.rstrip())
            
    max_idx = len(gps_lines)
    idx = 0
    with open(path2) as file:
        for line in file:
            dataLine = line.rstrip();
            dataLineSplit = dataLine.split("#")
            arbID = dataLineSplit[0]
            dataStr = dataLineSplit[1]
            split = dataStr.split(" ")
            if("0x3" in arbID):
                gps_lines.append(line)
                #gps_lines.append(line)
                combined.append(gps_lines[idx])
                idx+=1
                if(not idx < max_idx):
                    idx = 0

            elif("0x8" in arbID):
                combined.append("0x8#00 00 00 00 00 AC E4 00")
            else:
                combined.append(line.rstrip())

    tot_lines = len(combined)
    f=open(outputPath,'w+')

    for i in range(0,tot_lines):
        f.write(combined[i]+"\n")
        
        if i %100==0:
            f.flush()
            time.sleep(0.5)



if __name__ == '__main__':
    main()
