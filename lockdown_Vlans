from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from getpass import getpass
from netmiko import NetMikoAuthenticationException
from pprint import pprint
import os

driver = get_network_driver('ios')


def lock_port():
    username = 'jnieves'
    password = 'johnny'
    devices = '192.168.122.'

    for sw in range(250, 251):
        try:
            ip = devices + str(sw)
            device = driver(ip, username, password)
            device.open()
            print(f'\nConnecting to {ip}')
            print('-' * 80 + '\n')
            data = device.get_mac_address_table()
            for i in data:
                interface = i['interface']
                vlan = i['vlan']
                if vlan == 1:
                    print(f'{interface} is on {vlan}')
                    print('... Shuting down port')
                    print(device.device.send_config_set(
                        ['interface ' + interface, 'shutdown', 'desc disabled', 'end']))
            print(device.device.send_config_set(['wr', 'Backie22Wacky!!']))
            print()
        except NetMikoAuthenticationException:
            print('Auth Error for ', ip)

        except ConnectionException:
            print('Could not connect to ', ip)
    device.close()


def list_lock_port():
    username = 'jnieves'
    password = 'johnny'
    devices = '192.168.122.'

    for sw in range(250, 251):
        try:
            ip = devices + str(sw)
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
                    print(f'{interface} is on {vlan}')
                    f.write(f'{interface} is on {vlan}')
            f.close()
            print()
        except NetMikoAuthenticationException:
            print('Auth Error for ', ip)

        except ConnectionException:
            print('Could not connect to ', ip)
    device.close()


if __name__ == "__main__":
    list_lock_port()
