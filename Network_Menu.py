from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from getpass import getpass
from netmiko import NetMikoAuthenticationException
from os import system

driver = get_network_driver('ios')


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
    for i in range(int(driver_info[1]), int(driver_info[2])+1):
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
        print(f'''
Your device's name is {hostname}.
It is made by {vendor} and is a {model}.
It's serial number is {serial}.
The version of ios is {ios}
Your device has {interface} interfaces and {sfp} SFP.
        ''')
        print('-' * 80, '\n')


def get_ios_version():
    driver_info = get_driver_info()
    for i in range(int(driver_info[1]), int(driver_info[2])+1):
        ip = driver_info[0] + str(i)
        device = driver(ip, creds()[0], creds()[1])
        print(f'\nConnecting to {ip}\n')
        device.open()
        info = device.get_facts()
        print('-' * 80)
        ios = info['os_version'].split(',')[1]
        print(f'Your IOS version is {ios}')


def link_status():
    driver_info = get_driver_info()
    for i in range(int(driver_info[1]), int(driver_info[2])+1):
        ip = driver_info[0] + str(i)
        device = driver(ip, creds()[0], creds()[1])
        print(f'\nConnecting to {ip}')
        device.open()
        status = device.get_interfaces()
        print('-' * 80)
        down = 0
        up = 0
        print('The following port(s) are connected to a device\n')
        print('Enabled:')

        for interface in status:
            if interface[0] == "V":
                up = up
                down = down

            elif status[interface]['is_up'] and status[interface]['is_enabled']:
                print(interface, status[interface]['description'])
                up += 1

            elif status[interface]['is_up'] and not status[interface]['is_enabled']:
                down += 1

            elif not status[interface]['is_up'] and not status[interface]['is_enabled']:
                down += 1

            else:
                down += 1

        all_interfaces = up + down
        interface_port = down - up
        print(f'\nYou have {interface_port} port(s) NOTCONNECT or DISABLED')
        print(f'You have {up} port(s) in a CONNECT state')
        print(f'Total number of physical port(s) {all_interfaces}\n')


def get_interface_name():
    driver_info = get_driver_info()
    for i in range(int(driver_info[1]), int(driver_info[2])+1):
        ip = driver_info[0] + str(i)
        device = driver(ip, creds()[0], creds()[1])
        print(f'\nConnecting to {ip}')
        device.open()
        interfaces = device.get_interfaces()
        print('-' * 80)
        for i in interfaces:
            interface = i
            description = interfaces[interface]['description']
            print(interface, description)


def port_security():
    driver_info = get_driver_info()
    for i in range(int(driver_info[1]), int(driver_info[2])+1):
        ip = driver_info[0] + str(i)
        device = driver(ip, creds()[0], creds()[1])
        print(f'\nConnecting to {ip}')
        device.open()
        print('-' * 80)
        print('The following port(s) have tripped port-security \n')
        print(device.device.send_command('sh int status err-disabled'))
    print('-' * 80)


def creds():
    credentials = []
    with open('/home/johnny/creds', 'r') as f:
        credentials = f.read()
    credentials = credentials.strip("").splitlines()
    # print(credentials)
    return credentials


def check_ios():
    driver_info = get_driver_info()
    for i in range(int(driver_info[1]), int(driver_info[2])+1):
        ip = driver_info[0] + str(i)
        device = driver(ip, creds()[0], creds()[1])
        print(f'\nConnecting to {ip}')
        device.open()
        print('-' * 80)
        info = device.get_facts()
        ios_trans = info['os_version'].split(',')[1]
        ios_current = ios_trans.split()[1]
        ios_new = input(
            '\nEnter ios version to for check compliance Example(X.X.X): ')
        print(f'Your current ios is {ios_current}.')
        if ios_current != ios_new:
            print('You may need to update your ios. ')
        if ios_current == ios_new:
            print(f'Your ios {ios_current} is compliant.')


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

        except NetMikoAuthenticationException:
            print('Auth Error for ', ip)

        except ConnectionException:
            print('Could not connect to ', ip)
    device.close()


def tftp_ios():
    network = "10.231.27."  # input('Enter your subnet Example "10.231.27." ')
    minimal = "8"  # input('Enter network beginning host octet: ')
    maximum = "36"  # input(
    # 'Enter broadcast address octet or\nEnter your last host octet: ')
    username = creds()[0]  # input('Please enter your username \n')
    password = creds()[1]  # getpass('Please enter your password \n')
    tftpServer = "168.248.27.71"  # input(
    # "Please enter your tftp server address x.x.x.x: ")
    ios = "c3750_test.bin"  # input("Whats is your ios name: ")
    for switch in range(int(minimal), int(maximum)):
        try:
            ip = str(network) + str(switch)
            device = driver(ip, username, password, timeout=5)
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
            print('Auth Error for ', ip)

        except ConnectionException:
            print('Could not connect to ', ip)


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
        link_status()
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
