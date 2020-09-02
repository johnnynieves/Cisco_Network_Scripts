from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from getpass import getpass
from netmiko import NetMikoAuthenticationException
from pprint import pprint
import os

driver = get_network_driver('ios')


def creds():
    return ['jnieves', 'johnny']


def get_err_disabled(username, password):
    network = input('Enter your subnet Example 10.231.27.: ')
    minimal = input('Enter network address octet: ')
    maximum = input('Enter broadcast address: ')

    for switch in range(int(minimal), int(maximum)):
        try:
            ip = str(network) + str(switch)
            device = driver(ip, username, password)
            device.open()
            print(f'\nConnecting to {ip}')
            print('-' * 80 + '\n')
            data = device.device.send_command('sh int status err-disabled')
            f = open(f'{ip}_err_disable_ports.txt', 'w')
            print('Your answers are in the current folder you ran this file from... \n')
            f.close()
            print()
            device.close()
        except NetMikoAuthenticationException:
            print('Auth Error for ', ip)

        except ConnectionException:
            print('Could not connect to ', ip)


if __name__ == "__main__":
    get_err_disabled(*creds())
