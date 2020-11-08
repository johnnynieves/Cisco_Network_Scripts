from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from getpass import getpass
from netmiko import NetMikoAuthenticationException
from os import system

# ip = '192.168.122.250'#input("Please enter your ip: ")
# username = 'jnieves'#input("Please enter your Username: ")#
# password = 'johnny'#getpass("Please enter your Password: ")#
driver = get_network_driver('ios')


def get_info(ip, username, password):
    with driver(ip, username, password) as device:
        print(f'\nConnecting to {ip}')
        info = device.get_facts()
        print('-' * 80)
        ios = info['os_version']
        hostname = info['hostname']
        vendor = info['vendor']
        model = info['model']
        serial = info['serial_number']
        interface = 0
        for i in info['interface_list']:
            interface += 1
        print(f'''\nYour device's name is {hostname}.\n
        It is made by {vendor} and is a {model}.\n
        It's serial number is {serial}.\nThe version of ios is\n{ios}\n
        Your device has these interfaces {interface} \n''')
        print('-' * 80, '\n')
    return hostname, vendor, model, serial, ios, interface


def get_ios_version(ip, username, password):
    with driver(ip, username, password) as device:
        print(f'\nConnecting to {ip}')
        info = device.get_facts()
        print('-' * 80)
        trans = info['os_version'].split(',')[1]
        ios = trans.split(' ')[3]
        print(f'Your IOS version is {ios}')


def link_status(ip, username, password):
    with driver(ip, username, password) as device:
        print(f'Connecting to {ip}')
        status = device.get_interfaces()
        print('-' * 80)
        down = 0
        up = 0
        print('The following port(s) are not connected to a device or is(are)')
        print('Disabled:')
        for interface in status:
            if not status[interface]['is_up'] or not status[interface][
                'is_enabled'
            ]:
                print(interface)
                down += 1
            up += 1
        all_interfaces = up
        interface_port = up - down
        print(f'\nYou have {interface_port} port(s) CONNECTED')
        print(f'You have {down} port(s) in NOTCONNECT or DISABLED')
        print(f'Total number of port(s) {all_interfaces}\n')


def get_interface_name(ip, username, password):
    with driver(ip, username, password) as device:
        print(f'Connecting to {ip}')
        interfaces = device.get_interfaces()
        print('-' * 80)
        for i in interfaces:
            interface = i
            description = interfaces[interface]['description']
            print(interface, description)


def port_security(ip, username, password):
    with driver(ip, username, password) as device:
        print(f'Connecting to {ip}\n')
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


def get_enclave_err_disabled():
    username = creds()[0]  # input('Please enter your username \n')
    password = creds()[1]  # getpass('Please enter your password \n')
    network = input('Enter your subnet Example "10.231.27." ')
    minimal = input('Enter network address octet: ')
    maximum = input('Enter broadcast address octet: ')

    for switch in range(int(minimal), int(maximum)):
        try:
            ip = str(network) + str(switch)
            device = driver(ip, username, password, timeout=5)
            device.open()
            print(f'\nConnecting to {ip}')
            print('-' * 80 + '\n')
            data = device.device.send_command('sh int status err-disabled')
            with open(f'/home/johnny/err_disabled/{ip}_err_disable_ports.txt', 'w') as f:
                f.write(data)
            print('Your answers are in the current folder you ran this file from... \n')
            f.close()
            print()
            device.close()
        except NetMikoAuthenticationException:
            print('Auth Error for ', ip)

        except ConnectionException:
            print('Could not connect to ', ip)


def check_ios(ip, username, password):
    with driver(ip, username, password) as device:
        print(f'Connecting to {ip}')
        print('-' * 80)
        info = device.get_facts()
        ios_trans = info['os_version'].split(',')[1]
        ios_current = ios_trans.split()[1]
        ios_new = input(
            '\nEnter ios version to for check compliance Example(X.X.X): ')
        print(f'Your current ios is {ios_current}.')
        if ios_current != ios_new:
            print('You may need to update your ios. ')
        if ios_current is ios_new:
            print(f'Your ios {ios_current} is compliant.')


def ios_upgrade(ip, username, password):
    with driver(ip, username, password) as device:
        print(f'\nConnecting to {ip}')
        print('-' * 80)

        update = input('Would you like to update your ios [Y/N] \n')
        if update.upper() == 'N':
            print('logging off...')

        elif update.upper() == 'Y':
            print('Updating...')
            location = input('What is your tftp/scp server [x.x.x.x] \n')
            source = input('What is your IOS file name [c3750.info.bin] \n')
            destination = source
            config_commands = ['do copy tftp://' + location + '/' + source +
                               ' flash:',
                               source,
                               destination]
            print(device.device.send_config_set(config_commands))
            print('\nFile Copied')
            print('-' * 80)

            set_ios = input(
                '\nWould you like to default to new IOS at startup [Y/N] ')
            if set_ios.upper() == 'N':
                print('Note: You will have to set the IOS at your convinence')
            elif set_ios.upper() == 'Y':
                device.device.send_config_set(['boot system flash:' + source])
                print('Exiting')
            print('-' * 80)

            restart = input('\nWould you like to restart [Y/N] ')
            if restart.upper() == 'N':
                print('Exiting')
            elif restart.upper() == 'Y':
                when = input(
                    '''In how many [HH:MM] would you like to restart?\n
                    NOTE: Time without a ":" will default to minutes: ''')
                device.device.send_config_set(['do reload in ' + when, 'y'])
                print(f'\nRestarting in {when} [HH:MM]\n')
                print('Exiting')


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
    print('10. Error Disabled ports accross the subnet\n')
    print('0. to quit')
    print()
    print('*' * 80)
    print()
    tool = int(input('Enter your selection '))

    if tool == 1:
        ip = input('Please enter your IP x.x.x.x \n')
        username = input('Please enter your username \n')
        password = getpass('Please enter your password \n')
        get_info(ip, username, password)
        input('Press enter to continue\n')
        system('clear')
        menu()

    elif tool == 2:
        ip = input('Please enter your IP x.x.x.x \n')
        username = input('Please enter your username \n')
        password = getpass('Please enter your password \n')
        get_ios_version(ip, username, password)
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
        ip = input('Please enter your IP x.x.x.x \n')
        username = input('Please enter your username \n')
        password = getpass('Please enter your password \n')
        link_status(ip, username, password)
        input('Press enter to continue\n')
        system('clear')
        menu()

    elif tool == 5:
        ip = input('Please enter your IP x.x.x.x \n')
        username = input('Please enter your username \n')
        password = getpass('Please enter your password \n')
        port_security(ip, username, password)
        input('Press enter to continue\n')
        system('clear')
        menu()

    elif tool == 6:
        ip = input('Please enter your IP x.x.x.x \n')
        username = input('Please enter your username \n')
        password = getpass('Please enter your password \n')
        get_interface_name(ip, username, password)
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
        get_enclave_err_disabled()
        input('Press enter to continue\n')
        system('clear')
        menu()

    else:
        print('Good Bye')
        exit()


if __name__ == "__main__":
    menu()
