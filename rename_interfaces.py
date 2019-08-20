#!/usr/bin/python3
import sys
import os
import json
import csv
from pprint import pprint
from napalm import get_network_driver

#Open the matrix and set variables to indexes
with open('test.csv','r') as matrix:
    matrix_data =  csv.reader(matrix)
    for line in matrix_data:
        matrix_interface = line[0]
        matrix_description = line[1]
        matrix_mac = line[2]
        print(matrix_interface,matrix_description,matrix_mac)
        #open switch database
        with open('devices.txt','r') as switch_db:
            for switch in switch_db:
                #set up to connect to a switch from switch_db
                driver = get_network_driver('ios')
                with driver(switch, 'jnieves', 'johnny') as device:
                    print('Connecting to... ', switch)
                    switch_int_data = device.get_interfaces()
                    for interface in switch_int_data:
                        print(switch_int_data[interface]['description'])
                    #    print(switch)
                    #switch.load_merge_candidate(filename='config.txt')
                    #print(switch.compare_config())


#            for switch in device
#            with driver('192.168.122.250', 'jnieves', 'johnny') as devices:
