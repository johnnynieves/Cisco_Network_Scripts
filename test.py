from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from getpass import getpass
from netmiko import NetMikoAuthenticationException
from os import system
from Network_Menu import creds, get_driver_info


driver = get_network_driver('ios')
auth_error = 'Auth Error for '
cannot_connect = 'Could not connect to '


def get_link_status():
    driver_info = get_driver_info()
    option = int(input('(0) Print to screen \n(1) Write to file '))
    for i in range(int(driver_info[1]), int(driver_info[2])+1):
        try:
            ip = driver_info[0] + str(i)
            device = driver(ip, creds()[0], creds()[1])
            print(f'\nConnecting to {ip}')
            device.open()
            status = device.get_interfaces()
            print('-' * 80)
            down = 0
            up = 0
            upup = []

            statement = f'''
The following port(s) on {ip} are connected to a device:

'''
            if option == 0:
                print(statement)
            for interface in status:
                if interface[0] == "V":
                    up = up
                    down = down

                elif status[interface]['is_up'] and status[interface]['is_enabled']:
                    if option == 0:
                        print(interface, status[interface]['description'])
                    elif option == 1:
                        upup.append(
                            f"{interface}, {status[interface]['description']}")
                    up += 1

                elif status[interface]['is_up'] and not status[interface]['is_enabled']:
                    down += 1

                elif not status[interface]['is_up'] and not status[interface]['is_enabled']:
                    down += 1

                else:
                    down += 1

            all_interfaces = up + down
            interface_port = down - up
            link_status = f'''
You have {interface_port} port(s) NOTCONNECT or DISABLED
You have {up} port(s) in a CONNECT state
Total number of physical port(s) {all_interfaces}\n
'''
            if option == 0:
                print(link_status)
            elif option == 1:
                system("rm Switch_Link_Status.txt")
                f = open('Switch_Link_Status.txt', 'a')
                f.write(statement)
                for i in upup:
                    f.write(f'{i}\n')
                f.write(link_status)
                f.write(' \n')
                f.close()
                print("Written to file.")
                print('-' * 80, '\n')
        except NetMikoAuthenticationException:
            print(auth_error, ip)
            print('-' * 80)
        except ConnectionException:
            print(cannot_connect, ip)
            print('-' * 80)


if __name__ == "__main__":
    get_link_status()
