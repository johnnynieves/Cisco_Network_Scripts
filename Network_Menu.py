#! /usr/bin/env python3
from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from getpass import getpass
from netmiko import NetMikoAuthenticationException
from os import system

driver = get_network_driver('ios')
auth_error = 'Auth Error for '
cannot_connect = 'Could not connect to '


def creds():
    credentials = []
    with open('/home/johnny/creds', 'r') as f:
        credentials = f.read()
    credentials = credentials.strip("").splitlines()
    # print(credentials)
    return credentials


def get_driver_info():
    network = input('Enter your subnet Example "10.231.27." ')
    minimal = input(
        '''
For entire subnet use enter network first host octet:
If using for a single host enter last octet of host:
''')
    maximum = input(
        '''
For entire subnet use enter network last host octet:
If using for a single host enter last octet of host:
''')
    driver_info = [network, minimal, maximum]
    return driver_info


def get_info():
    driver_info = get_driver_info()
    option = int(input('(0) Print to screen \n(1) Write to file '))
    system("rm Switch_facts.txt")
    f = open('Switch_facts.txt', 'a')
    for i in range(int(driver_info[1]), int(driver_info[2])+1):
        try:
            ip = driver_info[0] + str(i)
            device = driver(ip, creds()[0], creds()[1])
            print(f'\nConnecting to {ip}')
            device.open()
            info = device.get_facts()
            print('-' * 80)
            ios = info['os_version']
            hostname = info['hostname']
            vendor = info['vendor']

            model = info['model']
            serial = info['serial_number']
            interface = 0
            sfp = 0
            for i in info['interface_list']:
                if i[0:18] == "GigabitEthernet1/0":
                    interface += 1
                elif i[0:18] == "GigabitEthernet1/1" or i[0:4] == "Te1/1":
                    sfp += 1
            facts = f'''
Your device's name is {hostname}({ip}).
It is made by {vendor} and is a {model}.
It's serial number is {serial}.
The version of ios is {ios}
Your device has {interface} interfaces and {sfp} SFP.
'''
            if option == 0:
                print(facts)
            elif option == 1:
                f.write(facts)
                print("Written to file.")
                print('-' * 80, '\n')

        except NetMikoAuthenticationException:
            print(auth_error, ip)
            print('-' * 80)
        except ConnectionException:
            print(cannot_connect, ip)
            print('-' * 80)
    f.close()


def get_ios_version():
    driver_info = get_driver_info()
    option = int(input('(0) Print to screen \n(1) Write to file '))
    system("rm Switch_ios.txt")
    f = open('Switch_ios.txt', 'a')
    for i in range(int(driver_info[1]), int(driver_info[2])+1):
        try:
            ip = driver_info[0] + str(i)
            device = driver(ip, creds()[0], creds()[1])
            print(f'\nConnecting to {ip}')
            device.open()
            info = device.get_facts()
            print('-' * 80)
            ios = info['os_version'].split(',')[1]
            ios_version = f"{info['hostname']}({ip}) IOS version is {ios}"

            if option == 0:
                print(ios_version)
            elif option == 1:
                f.write(ios_version)
                f.close()
                print("Written to file.")
                print('-' * 80, '\n')
        except NetMikoAuthenticationException:
            print(auth_error, ip)
            print('-' * 80)
        except ConnectionException:
            print(cannot_connect, ip)
            print('-' * 80)
    f.close()


def get_link_status():
    driver_info = get_driver_info()
    option = int(input('(0) Print to screen \n(1) Write to file '))
    system("rm Switch_Link_Status.txt")
    f = open('Switch_Link_Status.txt', 'a')
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
                f.write(statement)
                for i in upup:
                    f.write(f'{i}\n')
                f.write(link_status)
                f.write(' \n')
                print("Written to file.")
                print('-' * 80, '\n')
        except NetMikoAuthenticationException:
            print(auth_error, ip)
            print('-' * 80)
        except ConnectionException:
            print(cannot_connect, ip)
            print('-' * 80)
    f.close()


def get_interface_name():
    driver_info = get_driver_info()
    option = int(input('(0) Print to screen \n(1) Write to file '))
    system("rm Switch_Interface_Info.txt")
    f = open("Switch_Interface_Info.txt", "a")
    for i in range(int(driver_info[1]), int(driver_info[2])+1):
        try:
            ip = driver_info[0] + str(i)
            device = driver(ip, creds()[0], creds()[1])
            print(f'\nConnecting to {ip}')
            device.open()
            interfaces = device.get_interfaces()
            print('-' * 80)
            for i in interfaces:
                interface = i
                description = interfaces[interface]['description']
                mac = interfaces[interface]['mac_address']
                results = f'{interface}, {description}, {mac}'
                if option == 0:
                    print(results)
                elif option == 1:
                    f.write(f'{results}\n')
            f.close()
            print("Written to file.")
            print('-' * 80, '\n')

        except NetMikoAuthenticationException:
            print(auth_error, ip)
            print('-' * 80)
        except ConnectionException:
            print(cannot_connect, ip)
            print('-' * 80)
    f.close()


def port_security():
    driver_info = get_driver_info()
    option = int(input('(0) Print to screen \n(1) Write to file '))
    system("rm Switch_errorports.txt")
    f = open('Switch_errorports.txt', 'a')
    for i in range(int(driver_info[1]), int(driver_info[2])+1):
        try:
            ip = driver_info[0] + str(i)
            device = driver(ip, creds()[0], creds()[1])
            print(f'\nConnecting to {ip}')
            device.open()
            print('-' * 80)
            report = f'''
The following port(s) have tripped port-security on {ip}
{device.device.send_command('sh int status err-disabled')}
'''
            if option == 0:
                print(report)
            elif option == 1:
                f.write(report)
            print('-' * 80)
        except NetMikoAuthenticationException:
            print(auth_error, ip)
            print('-' * 80)
        except ConnectionException:
            print(cannot_connect, ip)
            print('-' * 80)
    f.close()


def check_ios():
    driver_info = get_driver_info()
    option = int(input('(0) Print to screen \n(1) Write to file '))
    system("rm Switch_ios_compliance.txt")
    f = open('Switch_ios_compliance.txt', 'a')
    ios_new = input(
        '\nEnter ios version to check compliance for:  Example(X.X.X): ')
    for i in range(int(driver_info[1]), int(driver_info[2])+1):
        try:
            ip = driver_info[0] + str(i)
            device = driver(ip, creds()[0], creds()[1])
            print(f'\nConnecting to {ip}')
            device.open()
            print('-' * 80)
            info = device.get_facts()
            ios_trans = info['os_version'].split(',')[1]
            ios_current = ios_trans.split()[1]
            if option == 0:
                print(f'Your current ios is {ios_current}.')
            elif option == 1:
                f.write(f'Your current ios is {ios_current}.\n')

            if ios_current != ios_new:
                if option == 0:
                    print('You may need to update your ios. ')
                elif option == 1:
                    f.write('You may need to update your ios. \n')
            elif ios_current == ios_new:
                if option == 0:
                    print(f'Your ios {ios_current} is compliant.')
                elif option == 1:
                    f.write(f'Your ios {ios_current} is compliant.\n')
            print("Written to file.")
            print('-' * 80, '\n')
        except NetMikoAuthenticationException:
            print(auth_error, ip)
            print('-' * 80)
        except ConnectionException:
            print(cannot_connect, ip)
            print('-' * 80)
    f.close()


def make_golden_configs(ip, username, password):
    with driver(ip, username, password) as device:
        device = driver(ip, username, password)
        device.open()
        print(f'\nConnecting to {ip}')
        print('~' * 80)
        print('Creating your "Golden" configs')
        print('~' * 80)
        golden_configs = device.get_config(
            retrieve=u'running', full=False)['running']

        with open('Golden_Configs.txt', 'w') as f:
            f.write(golden_configs)
        print('Your configs have been made')
        print('File located in root of where you ran this program.')


def verify_configs(ip, username, password):
    with driver(ip, username, password) as device:
        print(f'\nConnecting to {ip}')
        print('~' * 80)
        print('Retrieving your running configs')
        print('~' * 80)
        get_running = device.get_config(
            retrieve=u'running', full=False)['running']

        with open('Golden_Configs.txt', 'r') as d:
            data = d.read()
        print('Verifying running configs against "Golden" configs .....\n')
        if get_running == data:
            print('Your running configs match the golden configs')
        else:
            print('Your running configs DO NOT match the golden configs')


def enable_portfast(ip, username, password):
    network = input('Example 10.231.27.')
    subnetmin = input('Example Subnet range starts at 1 ')
    subnetmax = input('Example Subnet range ends at 28 ')

    for sw in range(subnetmin, subnetmax):
        try:
            ip = network + str(sw)
            device = driver(ip, username, password)
            device.open()
            print(f'\nConnecting to {ip}')
            print('-' * 80 + '\n')
            data = device.get_interfaces()
            for i in data:
                if i[0] == 'G' and data[i]['is_up'] and data[i][
                        'is_enabled']:
                    print(device.device.send_config_set([
                        'interface ' + i,
                        'spanning-tree portfast edge',
                        'end'
                    ])
                    )
            print(device.device.send_command('wr'))
            device.close()
        except NetMikoAuthenticationException:
            print(auth_error, ip)

        except ConnectionException:
            print(cannot_connect, ip)


def tftp_ios():
    driver_info = get_driver_info()
    tftpServer = input(
        "Please enter your tftp server address x.x.x.x: ")
    ios = input("Whats is your new EXACT ios name: ")
    for i in range(int(driver_info[1]), int(driver_info[2])+1):
        try:
            ip = driver_info[0] + str(i)
            device = driver(ip, creds()[0], creds()[1])
            device.open()
            print(f'\nConnecting to {ip}')
            print('-' * 80 + '\n')
            print('Connected')

            '''
            Had to modify the below in Netmiko cisco base connection.py due to 
            tftp timingout.
            File "/usr/local/lib/python3.8/dist-packages/netmiko/base_connection.py", line 1620
            to open in vscode use the below
            sudo code /usr/local/lib/python3.8/dist-packages/netmiko/base_connection.py  --user-data-dir
            
            - My Change
            delay_factor=100,
            max_loops=1000,
            strip_prompt=False,
            strip_command=False,
            config_mode_command=None
            
            I changed these variables
            for tftp timing out
            delay_factor=1, Original
            max_loops=150, Original
            '''

            print('< >' * 25 + '\n')
            print(device.device.send_config_set([
                f"do copy tftp://{tftpServer}/{ios} flash:{ios}",
                f"{ios}",
                " "
            ]))

            print()
            print(device.device.send_config_set([
                "do dir | i .bin",
                "no boot system switch all",
                f"boot system switch all flash:{ios}",
                "do sh boot",
                "do wr",
                "",  # switch password

            ]))
            print('< >' * 25 + '\n')

            print()
            print(f"Disconnecting from {ip}")
            print('-' * 80 + '\n')

            device.close()
        except NetMikoAuthenticationException:
            print(auth_error, ip)

        except ConnectionException:
            print(cannot_connect, ip)


def menu():
    system('clear')
    print('*' * 80)
    print('*', ' ' * 30, ' Network Tools ', ' ' * 29, '*')
    print('*' * 80)
    print()
    print()
    print('*' * 80)
    print()
    print('Please Select a tool')
    print()
    print('1.  Get device info')
    print('2.  Get IOS Version')
    print('3.  IOS Upgrade')
    print('4.  Link status for your Device')
    print('5.  Check port-security')
    print('6.  Check Interface Names')
    print('7.  Make "Golden" Configs')
    print('8.  Verify configs against "Golden" configs')
    print('9.  Enable Portfast')
    print('10. Check ios version compliance\n')
    print('0. to quit')
    print()
    print('*' * 80)
    print()
    tool = int(input('Enter your selection '))

    if tool == 1:
        get_info()
        input('Press enter to continue\n')
        system('clear')
        menu()

    elif tool == 2:
        get_ios_version()
        input('Press enter to continue\n')
        system('clear')
        menu()

    elif tool == 3:
        tftp_ios()
        input('Press enter to continue\n')
        system('clear')
        menu()
        # ip = input('Please enter your IP x.x.x.x \n')
        # username = input('Please enter your username \n')
        # password = getpass('Please enter your password \n')
        # ios_upgrade(ip, username, password)
        # input('Press enter to continue\n')
        # system('clear')
        # menu()

    elif tool == 4:
        get_link_status()
        input('Press enter to continue\n')
        system('clear')
        menu()

    elif tool == 5:
        port_security()
        input('Press enter to continue\n')
        system('clear')
        menu()

    elif tool == 6:
        get_interface_name()
        input('Press enter to continue\n')
        system('clear')
        menu()

    elif tool == 7:
        ip = input('Please enter your IP x.x.x.x \n')
        username = input('Please enter your username \n')
        password = getpass('Please enter your password \n')
        make_golden_configs(ip, username, password)
        input('Press enter to continue\n')
        system('clear')
        menu()

    elif tool == 8:
        ip = input('Please enter your IP x.x.x.x \n')
        username = input('Please enter your username \n')
        password = getpass('Please enter your password \n')
        verify_configs(ip, username, password)
        input('Press enter to continue\n')
        system('clear')
        menu()

    elif tool == 9:
        ip = input('Please enter your IP x.x.x.x \n')
        username = input('Please enter your username \n')
        password = getpass('Please enter your password \n')
        verify_configs(ip, username, password)
        input('Press enter to continue\n')
        system('clear')
        menu()

    elif tool == 10:
        check_ios()
        input('Press enter to continue\n')
        system('clear')
        menu()

    else:
        print('Good Bye')
        exit()


if __name__ == "__main__":
    menu()
