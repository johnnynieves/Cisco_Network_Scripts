from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from getpass import getpass
from netmiko import NetMikoAuthenticationException
from pprint import pprint


#ip = '192.168.122.250'#input("Please enter your ip: ")
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
        print('-' * 80,'\n')
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
        down =0
        up = 0
        print('The following port(s) are not connected to a device or is(are) Disabled:\n')
        for interface in status:
            if status[interface]['is_up'] == False or status[interface]['is_enabled'] == False:
                print(interface)
                down +=1
            up += 1
        all_interfaces = up
        interface_port = up - down
        print(f'\nYou have {interface_port} port(s) in state of CONNECTED')
        print(f'You have {down} port(s) in a state of NOTCONNECT or DISABLED')
        print(f'Total number of port(s) {all_interfaces}\n')
        x = ''
        return x


def port_security(ip, username, password):
    port = 22
    with driver(ip, username, password,port) as device:
        print(f'Connecting to {ip}\n')
        print('-' * 80)
        output = device.device.send_config_set(['do show port-security'])
        print(output)
        print('-' * 80)


def check_ios(ip, username, password):
    with driver(ip, username, password) as device:
        x = ''
        print(f'Connecting to {ip}')
        print('-' * 80)
        info = device.get_facts()
        ios_trans = info['os_version'].split(',')[1]
        ios_current  = ios_trans.split()[1]
        ios_new = input('\nPlease enter ios version to for check compliance Example(X.X.X): ')
        print(f'Your current ios is {ios_current}.')
        if ios_current != ios_new:
            print('You may need to update your ios. ')
        if ios_current is ios_new:
            print(f'Your ios {ios_current} is compliant.')
        return x


def ios_upgrade(ip, username, password):
    with driver(ip, username, password) as device:
        x = ''
        print(f'Connecting to {ip}')
        print('-' * 80)
        update = input('Would you like to update your ios [Y/N] \n')
        if update.upper() == 'N':
            print('logging off...')
            return x
        elif update.upper() == 'Y':
            print('Updating...')
            with open('ios_upgrade.txt','r') as f:
                ios_update = f.read()
                device.load_merge_candidate(config='vlan 20\nname TESTING\nint vlan 20\nip addr 10.0.0.100 255.255.255.0\nend\nwr\n')
                device.commit_config()
                print('...')
                print('Done')
                restart = input('Would you like to restart [Y/N] ')
                if restart.upper() == 'N':
                    print('Exiting')
                elif restart.upper() == 'Y':
                    when = input('Now or Later?')
                    if when.upper() == 'NOW':
                         device.load_merge_candidate(config='do reload\nend\n')
                         device.commit_config()
                         print('Exiting')

                         print('Restarting now')
                    else:
                         time = input('Please enter time [hh:mm] ')
                         day = input('Please enter date [month day] ')
                         reason = input('Reason for reload ')
                         print(f'Restart will execute at {time}.')
                         device.load_merge_candidate(config= f'do reload at {time} {day} {reason} {reason}')
                         device.commit_config()
                         print('Exiting')
    return x


def menu():
    x = ''
    print('*' * 80)
    print('*',' ' * 30,' Network Tools ',' ' * 29,'*')
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
    print('0 to quit')
    print()
    print('*' * 80)
    print()
    tool = int(input('Enter your selection '))

    if tool == 1:
        ip = input('Please enter your IP x.x.x.x \n')
        username = input('Please enter your username \n')
        password = getpass('Please enter your password \n')
        get_info(ip,username,password)
        input('Press enter to continue\n')
        menu()

    elif tool == 2:
        ip = input('Please enter your IP x.x.x.x \n')
        username = input('Please enter your username \n')
        password = getpass('Please enter your password \n')
        get_ios_version(ip,username,password)
        input('Press enter to continue\n')
        menu()

    elif tool == 3:
        ip = input('Please enter your IP x.x.x.x \n')
        username = input('Please enter your username \n')
        password = getpass('Please enter your password \n')
        ios_upgrade(ip,username,password)
        input('Press enter to continue\n')
        menu()

    elif tool == 4:
        ip = input('Please enter your IP x.x.x.x \n')
        username = input('Please enter your username \n')
        password = getpass('Please enter your password \n')
        link_status(ip,username,password)
        input('Press enter to continue\n')
        menu()

    elif tool == 5:
        ip = input('Please enter your IP x.x.x.x \n')
        username = input('Please enter your username \n')
        password = getpass('Please enter your password \n')
        port_security(ip,username,password)
        input('Press enter to continue\n')
        menu()

    else:
        print('Good Bye')
        exit()
    return x


if __name__ == "__main__":
    menu()
