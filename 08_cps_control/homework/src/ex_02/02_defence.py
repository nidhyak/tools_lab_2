#!/usr/bin/env python2
"""Exercise 2: Defence

If the threshold temperature is suspiciously different, display an alert to
the administrator.
"""
from time import sleep
from pycomm.ab_comm.clx import Driver as ClxDriver

PLC_IP = '192.168.1.151'
TAG_NAME = 'ThresTemp'
INTENDED_VALUE = 30.0

def monitor_plc(
        plc_ip=PLC_IP,
        tag_name=TAG_NAME,
        intended_value=INTENDED_VALUE
        ):
    while True:
        tag_value = read_plc(plc_ip, tag_name)
        if tag_value != intended_value:
            print("*** ALERT ***")
            print(plc_ip + ": " + tag_name)
            print(
                "Returning " + str(tag_value)
                + " instead of " + str(intended_value)
                )
        sleep(5)

def read_plc(plc_ip, tag_name):
    plc = ClxDriver()
    if plc.open(plc_ip):
        tag_value = plc.read_tag(tag_name)[0]
        plc.close()
        return tag_value
    else:
        print("Unable to open: ", plc_ip)

if __name__ == '__main__':
    monitor_plc()
