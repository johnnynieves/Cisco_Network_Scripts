from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from getpass import getpass
from netmiko import NetMikoAuthenticationException
from pprint import pprint
import csv
from csv import DictReader, DictWriter

driver = get_network_driver('ios')


def main():
    username = 'jnieves'
    password = 'johnny'
    devices = '10.231.27.'

    for sw in range(5, 9):
        try:
            ip = devices + str(sw)
            device = driver(ip, username, password)
            device.open()
            print(f'Connecting to {ip} ')
            print('-' * 80)
            data = device.get_interfaces()
            for i in data:
                if i[0] == 'G' and data[i]['is_up'] == True and data[i]['is_enabled'] == True:
                    print(f'{i} is up')
                    print(device.device.send_config_set(
                        ['interface ' + i, 'spanning-tree portfast edge', 'end']))
            print(device.device.send_command('wr'))

        except NetMikoAuthenticationException:
            print('Auth Error for ', ip)
        except ConnectionException:
            print('Could not connect to ', ip)
    device.close()


def listx():
    username = 'jnieves'
    password = 'johnny'
    devices = '10.231.27.'

    for sw in range(5, 9):
        try:
            ip = devices + str(sw)
            device = driver(ip, username, password)
            device.open()
            print(f'Connecting to {ip} ')
            print('-' * 80)
            data = device.get_interfaces()
            # Here open file
            # make in file description title
            # what switch(IP)
            for i in data:
                if i[0] == 'G' and data[i]['is_up'] == True and data[i]['is_enabled'] == True:
                    # write line to file "interface(i),"

        except NetMikoAuthenticationException:
            print('Auth Error for ', ip)
        except ConnectionException:
            print('Could not connect to ', ip)
    device.close()


if __name__ == "__main__":
    main()
