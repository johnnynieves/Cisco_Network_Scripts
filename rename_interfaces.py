import csv
from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from getpass import getpass
from netmiko import NetMikoAuthenticationException


username = input('username: ')
password = getpass('password: ')
driver = get_network_driver('ios')
with open('lemoore_switchDB.txt','r') as switch_db:
    for switch in switch_db:
    #set up to connect to a switch from switch_db
        try:
            device = driver(str(switch), username, password)
            device.open()
            print('~' * 80)
            print('~' * 80)
            print('  Connecting to... ', switch)
            print('~' * 80)
            switch_int_data = device.get_mac_address_table()

        except NetMikoAuthenticationException:
            print('Authentication Error to',switch)
            print('retry...')
            username = input('username: ')
            password = getpass('password: ')
            device = driver(str(switch), username, password)
            device.open()
            print('~' * 80)
            print('~' * 80)
            print('  Connecting to... ', switch)
            print('~' * 80)
            switch_int_data = device.get_mac_address_table()
        except ConnectionException:
            print('Could not connect to ',switch)

        with open('matrix.csv', 'r') as matrix:
            matrix_data = csv.reader(matrix)
            next(matrix_data)
            for line in matrix_data:
                matrix_interface = line[0]
                matrix_description = line[1]
                matrix_mac = line[2]
                matrix_list = [matrix_interface, matrix_description, matrix_mac]
                print('~' * 80)
                print(' Searching for ... ', matrix_mac)
                for interface in switch_int_data:
                    int = interface['interface']
                    mac = interface['mac']
                    static = interface['static']
                    if static == True and mac.upper() == matrix_mac.upper():
                        try:
                            print(' This one matches the matrix\n')
                            print(' Validating Description...')
                            print(' The matrix has the following description for this mac:', matrix_description)
                            print(' Configuring interface', str(int), "on switch:", switch)
                            config = 'INT ' + str(int) + '\nDESC ' + str(matrix_description) + '\nDO WR\n'
                            pre_config = device.load_merge_candidate(config= config)
                            #print('Diff:')
                            compare = device.compare_config()
                            print(compare)
                            #device.commit_config()
                            #print('Commiting Changes...')
                        except NetMikoAuthenticationException:
                            print('Authentication Error')
                            print('retry...')
                            username = 'jnieves' #input('username: ')
                            password = getpass('password: ')
                            device = driver(str(switch), username, password)
                            device.open()
        # device.commit_config('do wr\n') --commit a do wr before switch closes
        # print("...Saving Changes")
    device.close()
print("~" * 80)
print(" All Ports onsite have been renamed")
print("~" * 80)
