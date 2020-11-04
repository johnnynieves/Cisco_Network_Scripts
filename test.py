from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from getpass import getpass
from netmiko import NetMikoAuthenticationException
from os import system


driver = get_network_driver('ios')


def tftp_ios():
    network = input('Enter your subnet Example "10.231.27." ')
    minimal = input('Enter network address octet: ')
    maximum = input('Enter broadcast address octet: ')
    username = creds()[0]  # input('Please enter your username \n')
    password = creds()[1]  # getpass('Please enter your password \n')

    for switch in range(int(minimal), int(maximum)):
        try:
            ip = str(network) + str(switch)
            device = driver(ip, username, password, timeout=5)
            device.open()
            print(f'\nConnecting to {ip}')
            print('-' * 80 + '\n')
            tftpServer = input(
                "Please enter your tftp server address x.x.x.x: ")
            ios = input("Whats is your ios name: ")
            data = device.device.send_config_set([
                f"do copy tftp://{tftpServer}/{ios} flash:{ios}",
                " "
            ])
            print()
            print(device.device.send_command("dir | i .bin"))
            print()
            print(device.device.send_config_set([
                "no boot system switch all",
                f"boot system switch all flash:{ios}",
                "do wr",
                "Backie22Wacky!!",
                "do sh run | i boot"
            ]))
            device.close()
        except NetMikoAuthenticationException:
            print('Auth Error for ', ip)

        except ConnectionException:
            print('Could not connect to ', ip)


if __name__ == "__main__":
    tftp_ios()
