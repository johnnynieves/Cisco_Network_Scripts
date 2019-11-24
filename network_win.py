from tkinter import *
from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from getpass import getpass
from netmiko import NetMikoAuthenticationException
from pprint import pprint
from os import system, name


app = Tk()

driver = get_network_driver('ios')


def get_info(ip, username, password):
    displaybox.delete(1.0, END)
    with driver(ip, username, password) as device:
        displaybox.insert(END, f'\nConnecting to {ip}\n')
        info = device.get_facts()
        displaybox.insert(END, '-' * 80, '\n')
        ios = info['os_version']
        hostname = info['hostname']
        vendor = info['vendor']
        model = info['model']
        serial = info['serial_number']
        interface = 0
        for i in info['interface_list']:
            interface += 1
        info = f'''\nYour device's name is {hostname}.\nIt is made by {vendor} and is a {model}.\n
It's serial number is {serial}.\nThe version of ios is\n{ios}\n
Your device has these interfaces {interface} \n'''
        displaybox.insert(END, info)


def get_ios_version(ip, username, password):
    displaybox.delete(1.0, END)
    with driver(ip, username, password) as device:
        displaybox.insert(END, f'\nConnecting to {ip}\n')
        info = device.get_facts()
        displaybox.insert(END, '-' * 80, '\n')
        ios = info['os_version'].split(',')[1].split(' ')[2]
        #ios = trans.split(' ')[1]
        displaybox.insert(END, f'Your IOS version is {ios}')


def ios_upgrade(ip, username, password):
    displaybox.delete(1.0, END)
    with driver(ip, username, password) as device:
        displaybox.insert(END, f'Connecting to {ip}\n')
        displaybox.insert(END, 'UPGRADED')


def link_status(ip, username, password):
    displaybox.delete(1.0, END)
    with driver(ip, username, password) as device:
        displaybox.insert(END, f'Connecting to {ip}\n')
        status = device.get_interfaces()
        displaybox.insert(END, '-' * 80, '\n')
        down = 0
        up = 0
        displaybox.insert(
            END, 'The following port(s) are not connected to a device or is(are) Disabled:')

        for interface in status:
            if status[interface]['is_up'] == False or status[interface]['is_enabled'] == False:
                displaybox.insert(END, '\n' + interface)
                down += 1
            up += 1
        all_interfaces = up
        interface_port = up - down
        displaybox.insert(
            END, f'\nYou have {interface_port} port(s) CONNECTED\n')
        displaybox.insert(
            END, f'You have {down} port(s) in NOTCONNECT or DISABLED\n')
        displaybox.insert(END, f'Total number of port(s) {all_interfaces}\n')


def get_interface_name(ip, username, password):
    displaybox.delete(1.0, END)
    with driver(ip, username, password) as device:
        displaybox.insert(END, f'Connecting to {ip}\n')
        interfaces = device.get_interfaces()
        displaybox.insert(END, '-' * 80 + '\n')
        for i in interfaces:
            interface = i
            description = interfaces[interface]['description']
            displaybox.insert(END, interface, description)


def port_security(ip, username, password):
    displaybox.delete(1.0, END)
    with driver(ip, username, password) as device:
        displaybox.insert(END, f'Connecting to {ip}\n')
        displaybox.insert(END, '-' * 80)
        displaybox.insert(
            END, 'The following port(s) have tripped port-security \n')
        displaybox.insert(END, device.device.send_command(
            'do sh int status err-disabled'))
    displaybox.insert(END, '-' * 80)


def check_ios(ip, username, password):
    displaybox.delete(1.0, END)
    with driver(ip, username, password) as device:
        x = ''
        displaybox.insert(END, f'Connecting to {ip}')
        displaybox.insert(END, '-' * 80)
        info = device.get_facts()
        ios_trans = info['os_version'].split(',')[1]
        ios_current = ios_trans.split()[1]
        ios_new = input(
            '\nPlease enter ios version to for check compliance Example(X.X.X): ')
        displaybox.insert(END, f'Your current ios is {ios_current}.')
        if ios_current != ios_new:
            displaybox.insert(END, 'You may need to update your ios. ')
        if ios_current is ios_new:
            displaybox.insert(END, f'Your ios {ios_current} is compliant.')


menu_lable = Label(app, text="MAIN MENU", font=('bold', 16), pady=20)
menu_lable.grid(row=0, column=2, sticky=E+W)


device_info = Button(app, text="Get Device Info", font=('bold', 11), pady=5)
device_info.bind('<Button-1>', lambda event:
                 get_info('10.0.0.123',
                          'jnieves',
                          'johnny'
                          ))
device_info.grid(row=2, column=1, sticky=E+W, )


ios_ver_button = Button(app, text="Get IOS Version", font=('bold', 11), pady=5)
ios_ver_button.bind(
    '<Button-1>', lambda event: get_ios_version('10.0.0.123', 'jnieves', 'johnny'))
ios_ver_button.grid(row=2, column=2, sticky=E+W)


upgrade = Button(app, text="IOS Upgrade", font=('bold', 11), pady=5)
upgrade.bind('<Button-1>', lambda event:
             ios_upgrade('10.0.0.123',
                         'jnieves',
                         'johnny'
                         ))
upgrade.grid(row=2, column=3, sticky=E+W)


link_stat = Button(app, text="Check Link Status",
                   font=('bold', 11), pady=5)
link_stat.bind('<Button-1>', lambda event:
               link_status('10.0.0.123',
                           'jnieves',
                           'johnny'
                           ))
link_stat.grid(row=3, column=1, sticky=E+W)

port_security = Button(app, text="Check Port-Security: Switches Only",
                       font=('bold', 11), pady=5)
port_security.bind('<Button-1>', lambda event:
                   port_security('10.0.0.123',
                                 'jnieves',
                                 'johnny'
                                 ))
port_security.grid(row=3, column=2, sticky=E+W)

int_desc = Button(
    app, text="Check Interface Descriptions", font=('bold', 11), pady=5)
int_desc.bind('<Button-1>', lambda event:
              get_interface_name('10.0.0.123',
                                 'jnieves',
                                 'johnny'
                                 ))
int_desc.grid(row=3, column=3, sticky=E+W)

make_golden = Button(
    app, text='Make "Golden Configs"', font=('bold', 11), pady=5)
make_golden.grid(row=4, column=1, sticky=E+W)

compare_golden = Button(
    app, text='Verify "Golden" Configs"', font=('bold', 11), pady=5)
compare_golden.grid(row=4, column=2, sticky=E+W)

app_close = Button(app, text="Exit", font=(
    'bold', 11), pady=5, command=exit)
app_close.grid(row=4, column=3, sticky=E+W)


displaybox = Text(app, height=15, width=80, border=2, pady=20, padx=20)
displaybox.grid(row=5, column=1, columnspan=4)

'''
display = Listbox(app, height=15, width=100, font=('bold', 11))
display.grid(row=5, column=0, columnspan=4, rowspan=1)
scrollbar = Scrollbar(app)
scrollbar.grid(row=5, column=4)
display.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=display.yview)
'''
app.title('Easy Network Manager')
app.geometry('670x580')


app.mainloop()


if __name__ == "__main__":
    mainloop()
