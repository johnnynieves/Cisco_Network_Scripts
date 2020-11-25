from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from getpass import getpass
from netmiko import NetMikoAuthenticationException
from os import system
from Network_Menu import creds, get_driver_info

driver = get_network_driver('ios')
auth_error = 'Auth Error for '
cannot_connect = 'Could not connect to '


def set_acl():
    driver_info = get_driver_info()
    for i in range(int(driver_info[1]), int(driver_info[2])+1):
        try:
            ip = driver_info[0] + str(i)
            device = driver(ip, creds()[0], creds()[1])
            print(f'\nConnecting to {ip}')
            device.open()
            with open('config', 'r') as f:
                config = f.readlines()
                print('-' * 80)
                print(device.device.send_config_set(config))
                print('-' * 80)
        except NetMikoAuthenticationException:
            print(auth_error, ip)
            print('-' * 80)
        except ConnectionException:
            print(cannot_connect, ip)
            print('-' * 80)
    f.close()


if __name__ == "__main__":
    set_acl()
