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
    """Read a plc tag and print the rx data"""
    # The "clx" class can be used to communicate with Compactlogix,
    # Controllogix PLCs The "slc" can be used to communicate with Micrologix or SLC PLCs
    plc = ClxDriver()
    if plc.open(plc_ip):
        # This read the tag within the Controllogix PLC
        tagg = plc.read_tag(tag_name)
        plc.close()
        return (tag)

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
    test_plc_write(PLC_IPS['plc1'], 'ThresTemp', 50, 'REAL')

if __name__ == '__main__':
    main()
