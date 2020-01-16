from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from getpass import getpass
from netmiko import NetMikoAuthenticationException
from pprint import pprint
import os

driver = get_network_driver('ios')


def main():
    print('*' * 80)
    print('*', ' ' * 30, ' Network Tools ', ' ' * 29, '*')
    print('*' * 80)
    print()
    print()
    print('*' * 80)
    print()
    print('Please Select a tool')
    print()
    print('1. List Enabled Ports')
    print('2. Enable portfast on ports in list')
    print('0. to quit')
    print()
    print('*' * 80)
    print()
    tool = int(input('Enter your selection '))

    if tool == 1:
        listx()
        # clear screen
        # if os.system('cls')

    elif tool == 2:
        enable_portfast()

    else:
        print('Good Bye')
        exit()


def enable_portfast():
    username = 'jnieves'
    password = 'johnny'
    devices = '10.231.27.'

    for sw in range(5, 9):
        try:
            ip = devices + str(sw)
            device = driver(ip, username, password)
            device.open()
            print(f'\nConnecting to {ip}')
            print('-' * 80 + '\n')
            data = device.get_interfaces()
            for i in data:
                if i[0] == 'G' and data[i]['is_up'] == True and data[i]['is_enabled'] == True:
                    print(device.device.send_config_set(
                        ['interface ' + i, 'spanning-tree portfast edge', 'end']))
            print(device.device.send_command('wr'))

        except NetMikoAuthenticationException:
            print('Auth Error for ', ip)

        except ConnectionException:
            print('Could not connect to ', ip)
    device.close()
    main()


def listx():
    username = 'jnieves'
    password = 'johnny'
    devices = '10.231.27.'

    for sw in range(5, 9):
        try:
            ip = devices + str(sw)
            device = driver(ip, username, password)
            device.open()
            print(f'\nConnecting to {ip}')
            print('-' * 80 + '\n')
            data = device.get_interfaces()
            f = open(f'{ip}_access_ports_up.txt', 'w')
            f.write('Switch' + ', ' + ip + '\n\n')
            for i in data:
                if i[0] == 'G' and data[i]['is_up'] == True and data[i]['is_enabled'] == True:
                    f.write(
                        f'{i}, ' + f"{data[i]['description']}, " + 'is_up\n')
            print('Making File...')
            f.close()
        except NetMikoAuthenticationException:
            print('Auth Error for ', ip)
        except ConnectionException:
            print('Could not connect to ', ip)
    device.close()
    main()


if __name__ == "__main__":
    main()
