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


def get_interface_name(ip, username, password):
    with driver(ip, username, password) as device:
        print(f'Connecting to {ip}')
        interfaces = device.get_interfaces()
        print('-' * 80)
        for interface in interfaces:
            int = interface
            description = interfaces[interface]['description']
            print(int,description)
    x = ''
    return x


def port_security(ip, username, password):
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
            location =  input('What is your tftp/scp server [x.x.x.x] \n')
            source = input('What is your ios file name [c3750.info.bin] \n')
            destination = source
            config_commands = ['copy tftp://'+ location +'/' + source + ' flash:',
                                source,
                                destination]
            device.device.send_config_set(config_commands)
            for switch in range(1,9):
                if switch == True:
                    print('copying ios to sw',switch)
                    line = ['copy flash:' + source + ' flash' + str(switch) + ':']
                    device.device.send_config_set(line)
                else:
                    break

            print('...')
            print('Done')
            restart = input('Would you like to restart [Y/N] ')
            if restart.upper() == 'N':
                print('Exiting')
            elif restart.upper() == 'Y':
                when = input('Now or Later?')
                if when.upper() == 'NOW':
                     device.device.send_command('reload in 1')
                     print('Restarting in 1 minute')
                     print('Exiting')

                else:
                     time_date = input('Please enter time and date [hh:mm][Month Day] ')
                     reason = input('Reason for reload ')
                     print(f'Restart will execute at {time_date}.')
                     output = device.device.send_command('reload at '+ time_date + ' ' +  reason)
                     device.device.send_command('y')
                     print(output)
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
    print('6. Check Interface Names')
    print('0. to quit')
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

    elif tool == 6 :
        ip = input('Please enter your IP x.x.x.x \n')
        username = input('Please enter your username \n')
        password = getpass('Please enter your password \n')
        get_interface_name(ip,username,password)
        input('Press enter to continue\n')
        menu()


    else:
        print('Good Bye')
        exit()
    return x


if __name__ == "__main__":
    menu()
