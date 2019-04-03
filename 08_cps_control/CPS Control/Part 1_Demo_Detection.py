#!/usr/bin/env python2

"""
Use pycomm python2 module to communicate with contrologix PLCs

adapted from: examples/test_ab_comm.py
more on: https://github.com/ruscito/pycomm
"""

# import logging
import time
import string
import datetime

from pycomm.ab_comm.clx import Driver as ClxDriver

PLC_IPS = {
    'plc1': '192.168.1.151',
}

def test_plc_read_val(plc_ip, tag_name):
    plc = ClxDriver()
    if plc.open(plc_ip):
        # This read the tag within the Controllogix PLC
        tagg = plc.read_tag(tag_name)
        plc.close()
        return (tagg)
        
    else:
        print("Unable to open", plc_ip)

def test_plc_write(plc_ip, tag_name, value, tag_type):
    """Write a plc tag and print a BOOL status code.    """
    # The "clx" class can be used to communicate with Compactlogix,
    # Controllogix PLCs The "slc" can be used to communicate with Micrologix or SLC PLCs
    plc = ClxDriver()
    if plc.open(plc_ip):
        # This modify the tag within the Controllogix PLC
        print(plc.write_tag(tag_name, value, tag_type))
        plc.close()
    else:
        print("Unable to open", plc_ip)

def main():
    """ Read and write PLCs tags using pycomm.

    DI_P_201* tags are configured as external tags with
    read/write permission. PLC2 will re-scan and re-write
    their value according to a set of state variables.

    dummy and dummy_int are configured as external tags
    with read/write permissions and they serve as a proof
    that pycomm can effectivley read and write tag using
    ENIP.
    """

    while True:
        a = test_plc_read_val(PLC_IPS['plc1'], 'ThresTemp')
        if a[0] != 27.0:
            print("There is an attack to the Temp Threshold")
            test_plc_write(PLC_IPS['plc1'], 'DO_02', 1, 'BOOL')
            test_plc_write(PLC_IPS['plc1'], 'DO_06', 1, 'BOOL')
        time.sleep(5)


if __name__ == '__main__':
    main()
