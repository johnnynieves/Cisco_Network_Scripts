import sys
import os
import json
import csv
from pprint import pprint
from napalm import get_network_driver


#open switch database
with open('devices.txt','r') as switch_db:
    for switch in switch_db:
        #set up to connect to a switch from switch_db
        driver = get_network_driver('ios')
        with driver(switch, 'jnieves', 'johnny') as device:
            print('Connecting to... ', switch)
            switch_int_data = device.get_interfaces()
            #Open the matrix and set variables to indexes
            with open('test.csv','r') as matrix:
                matrix_data =  csv.reader(matrix)
                next(matrix_data)
                for line in matrix_data:
                        matrix_interface = line[0]
                        matrix_description = line[1]
                        matrix_mac = line[2]
                        matrix_list = [matrix_interface,matrix_description,matrix_mac]
                        print('Searching for ... ',matrix_list)
                        for interface in switch_int_data:
                            int = interface
                            desc = switch_int_data[interface]['description']
                            mac = switch_int_data[interface]['mac_address']
                            if matrix_mac == mac:
                                print('found it!')
                                if desc != matrix_description:
                                    print(str(int),"'s Needs to be changed")

                            #config = 'CONF T \nINT ' + str(int) + '\nDESC ' + str(matrix_description) + '\nDO WR\n'
                                #print(config)
                                #lines = device.load_merge_candidate(config = 'CONF T \nINT ' + str(int) + '\nDESC ' + str(matrix_description) + $
                                #print('Diff:')
                                #print(device.compare_config())
