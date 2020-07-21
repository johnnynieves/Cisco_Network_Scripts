from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from getpass import getpass
from netmiko import NetMikoAuthenticationException
from pprint import pprint
import os

#List and lock ports

driver = get_network_driver('ios')

def creds():
    username = input('Username: ')
    password = getpass('Password')
    return username, password


def list_lock_port(username, password):
    network = input('Enter your subnet Example 10.231.27. ')
    min = input('Enter first usable IP ')
    max = input('Enter last usable IP ')

    for switch in range(int(min), int(max)):
        try:
            ip = str(network) + str(switch)
            device = driver(ip, username, password)
            device.open()
            print(f'\nConnecting to {ip}')
            print('-' * 80 + '\n')
            data = device.get_mac_address_table()
            f = open(f'{ip}_vlan_ports_to_lock.txt', 'w')
            print('These ports need to be secured \n')
            for i in data:
                interface = i['interface']
                vlan = i['vlan']
                if vlan == 1:
                    print(f'{interface} is on vlan {vlan}')
                    f.write(f'{interface} is on vlan {vlan}')
            f.close()
            print()
            device.close()
        except NetMikoAuthenticationException:
            print('Auth Error for ', ip)

        except ConnectionException:
            print('Could not connect to ', ip)



def lock_port(username, password):
    network = input('Enter your subnet Example 10.231.27. ')
    min = input('Enter first usable IP ')
    max = input('Enter last usable IP ')

    for switch in range(int(min), int(max)):
        try:
            ip = str(network) + str(switch)
            device = driver(ip, username, password)
            device.open()
            print(f'\nConnecting to {ip}')
            print('-' * 80 + '\n')
            data = device.get_mac_address_table()
            for i in data:
                interface = i['interface']
                vlan = i['vlan']
                if vlan == 1:
                    print(f'{interface} is on vlan {vlan}')
                    print('... Shuting down port')
                    print(device.device.send_config_set(
                        ['interface ' + interface, 'shutdown', 'desc disabled', 'end']))
            print(device.device.send_config_set(['wr','!Done']))
            print()
            device.close()
        except NetMikoAuthenticationException:
            print('Auth Error for ', ip)

        except ConnectionException:
            print('Could not connect to ', ip)


if __name__ == "__main__":
    list_lock_port(*creds())
