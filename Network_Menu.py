from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from getpass import getpass
from netmiko import NetMikoAuthenticationException
from pprint import pprint


ip = '192.168.222.131'#input("Please enter your ip: ")
username = 'jnieves'#input("Please enter your Username: ")#
password = 'johnny'#getpass("Please enter your Password: ")#
driver = get_network_driver('ios')


def get_info(ip, username, password):
    with driver(ip, username, password) as device:
        print(f'Connecting to {ip}')
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
        print(f'''Your device's name is {hostname}.\nIt is made by {vendor} and is a {model}.\n
It's serial number is {serial}.\nThe version of ios is\n{ios}\n
Your device has these interfaces {interface}.''')
        print('-' * 80)
    return hostname, vendor, model, serial, ios, interface
        

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
        print(f'Total number of port(s) {all_interfaces}')
        x = ''
        return x 


def port_security(ip, username, password):
    with driver(ip, username, password) as device:
        print(f'Connecting to {ip}\n')
        err = device.get_interfaces()
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
        update = input('Would you like to update your ios [Y/N] ')
        if update.upper() == 'N':
            print('logging off...')
            return x
        elif update.upper() == 'Y':
            print('Updating...')
            with open('Napalm/ios_upgrade.txt','r') as f:
                ios_update = f.read()
                print(ios_update)
            #update = device.load_merge_candidate(config=ios_update)
            print('updating ...')
            #device.commit_config()
            print('...')
            print('Done')
            restart = input('Would you like to restart [Y/N] ')    
            if restart.upper() == 'N':
                print('Exiting')
            elif restart.upper() == 'Y':
                when = input('Now or Later?')
                if when.upper() == 'NOW':
                    print('Restarting now')
                else:
                    time = input('Please enter date and time [hh:mm mon:day]')
                    print(f'Restart will execute at {time}.')
    return x


if __name__ == "__main__":
    
    print(ios_upgrade(ip, username, password))
    
    
