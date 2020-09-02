from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from getpass import getpass
from netmiko import NetMikoAuthenticationException
from pprint import pprint
import os

driver = get_network_driver('ios')


def creds():
    credentials = []
    with open('/home/johnny/test.txt', 'r') as f:
        credentials = f.read()
    credentials = credentials.strip("").splitlines()
    # print(credentials)
    return credentials


if __name__ == "__main__":
    print(*creds())
