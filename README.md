# VMS Telemetry V2
## Hardware Setup:
Base station must be connected via USB to `coordinator` Xbee Radio

Onboard raspberry pi must be connected to USB2CAN and to `router` or `end device` Xbee radio via USB

## Software Setup
* install everything in `requirements.txt`to python >= 3.9 on base station and onboard pi
* `python .\telemetry.py`- Run on the base laptop; responsible for reading logs in `/logs/<event>`, converting CAN messages with different lenths and endianness to the same standard python `float`. Displays values in graphs
* `python .\fast_base_record.py` Run this on the base laptop; responsible for using XBee interface to receive peer-to-peer messages from on-board XBee; saves logs to `/logs/<event>`
* `python3 on-board.py` onboard utility that sends select CAN messages to the base station. Program is started and kept running by `TELEMTRY.sh` on the dashboard pi
