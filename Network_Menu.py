from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from getpass import getpass
from netmiko import NetMikoAuthenticationException
from pprint import pprint


# ip = '192.168.122.250'#input("Please enter your ip: ")
#username = 'jnieves'#input("Please enter your Username: ")#
#password = 'johnny'#getpass("Please enter your Password: ")#
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
        print(f'''\nYour device's name is {hostname}.\nIt is made by {vendor} and is a {model}.\n
It's serial number is {serial}.\nThe version of ios is\n{ios}\n
Your device has these interfaces {interface} \n''')
        print('-' * 80, '\n')
    return hostname, vendor, model, serial, ios, interface


def get_ios_version(ip, username, password):
    with driver(ip, username, password) as device:
        x = ''
        print(f'\nConnecting to {ip}')
        info = device.get_facts()
        print('-' * 80)
        trans = info['os_version'].split(',')[1]
        ios = trans.split(' ')[3]
        print(f'Your IOS version is {ios}')
        return x


def link_status(ip, username, password):
    with driver(ip, username, password) as device:
        print(f'Connecting to {ip}')
        status = device.get_interfaces()
        print('-' * 80)
        down = 0
        up = 0
        print('The following port(s) are not connected to a device or is(are) Disabled:\n')
        for interface in status:
            if status[interface]['is_up'] == False or status[interface]['is_enabled'] == False:
                print(interface)
                down += 1
            up += 1
        all_interfaces = up
        interface_port = up - down
        print(f'\nYou have {interface_port} port(s) CONNECTED')
        print(f'You have {down} port(s) in NOTCONNECT or DISABLED')
        print(f'Total number of port(s) {all_interfaces}\n')
        x = ''
        return x


def get_interface_name(ip, username, password):
    with driver(ip, username, password) as device:
        print(f'Connecting to {ip}')
        interfaces = device.get_interfaces()
        print('-' * 80)
        for i in interfaces:
            interface = i
            description = interfaces[interface]['description']
            print(interface, description)
    x = ''
    return x


def port_security(ip, username, password):
    with driver(ip, username, password) as device:
        print(f'Connecting to {ip}\n')
        print('-' * 80)
        print('The following port(s) have tripped port-security \n')
        print(device.device.send_command('sh int status err-disabled'))
    print('-' * 80)


def check_ios(ip, username, password):
    with driver(ip, username, password) as device:
        x = ''
        print(f'Connecting to {ip}')
        print('-' * 80)
        info = device.get_facts()
        ios_trans = info['os_version'].split(',')[1]
        ios_current = ios_trans.split()[1]
        ios_new = input(
            '\nPlease enter ios version to for check compliance Example(X.X.X): ')
        print(f'Your current ios is {ios_current}.')
        if ios_current != ios_new:
            print('You may need to update your ios. ')
        if ios_current is ios_new:
            print(f'Your ios {ios_current} is compliant.')
        return x


def ios_upgrade(ip, username, password):
    with driver(ip, username, password) as device:
        x = ''
        print(f'\nConnecting to {ip}')
        print('-' * 80)

        update = input('Would you like to update your ios [Y/N] \n')
        if update.upper() == 'N':
            print('logging off...')
            return x
        elif update.upper() == 'Y':
            print('Updating...')
            location = input('What is your tftp/scp server [x.x.x.x] \n')
            source = input('What is your IOS file name [c3750.info.bin] \n')
            destination = source
            config_commands = ['do copy tftp://' + location + '/' + source + ' flash:',
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
                    'In how many [HH:MM] would you like to restart?\nNOTE: Time without a ":" will default to minutes: ')
                device.device.send_config_set(['do reload in ' + when, 'y'])
                print(f'\nRestarting in {when} [HH:MM]\n')
                print('Exiting')
    return x


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
        print('Your configs have been made and is located in root of where you ran this program.')


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


def menu():
    x = ''
    print('*' * 80)
    print('*', ' ' * 30, ' Network Tools ', ' ' * 29, '*')
    print('*' * 80)
    print()
    print()
    print('*' * 80)
    print()
    print('Please Select a tool')
    print()
    print('1. Get device info')
    print('2. Get IOS Version')
    print('3. IOS Upgrade')
    print('4. Link status for your Device')
    print('5. Check port-security')
    print('6. Check Interface Names')
    print('7. Make "Golden" Configs')
    print('8. Verify configs against "Golden" configs')
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
        menu()

    elif tool == 2:
        ip = input('Please enter your IP x.x.x.x \n')
        username = input('Please enter your username \n')
        password = getpass('Please enter your password \n')
        get_ios_version(ip, username, password)
        input('Press enter to continue\n')
        menu()

    elif tool == 3:
        ip = input('Please enter your IP x.x.x.x \n')
        username = input('Please enter your username \n')
        password = getpass('Please enter your password \n')
        ios_upgrade(ip, username, password)
        input('Press enter to continue\n')
        menu()

    elif tool == 4:
        ip = input('Please enter your IP x.x.x.x \n')
        username = input('Please enter your username \n')
        password = getpass('Please enter your password \n')
        link_status(ip, username, password)
        input('Press enter to continue\n')
        menu()

    elif tool == 5:
        ip = input('Please enter your IP x.x.x.x \n')
        username = input('Please enter your username \n')
        password = getpass('Please enter your password \n')
        port_security(ip, username, password)
        input('Press enter to continue\n')
        menu()

    elif tool == 6:
        ip = input('Please enter your IP x.x.x.x \n')
        username = input('Please enter your username \n')
        password = getpass('Please enter your password \n')
        get_interface_name(ip, username, password)
        input('Press enter to continue\n')
        menu()

    elif tool == 7:
        ip = input('Please enter your IP x.x.x.x \n')
        username = input('Please enter your username \n')
        password = getpass('Please enter your password \n')
        make_golden_configs(ip, username, password)
        input('Press enter to continue\n')
        menu()

    elif tool == 8:
        ip = input('Please enter your IP x.x.x.x \n')
        username = input('Please enter your username \n')
        password = getpass('Please enter your password \n')
        verify_configs(ip, username, password)
        input('Press enter to continue\n')
        menu()

    else:
        print('Good Bye')
        exit()
    return x


if __name__ == "__main__":
    menu()
