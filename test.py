from flask.helpers import flash
from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from getpass import getpass
from netmiko import NetMikoAuthenticationException
from os import system
from Network_Menu import creds, get_driver_info
from flask import Flask
from jinja2 import Template


app = Flask(__name__)

driver = get_network_driver('ios')
auth_error = 'Auth Error for '
cannot_connect = 'Could not connect to '


@app.route('/')
def greeting():
    return "<h1> Hello World </h1>"


@app.route('/get_facts')
def get_info():
    driver_info = get_driver_info()
    ip = driver_info[0] + str(i)
    device = driver(ip, creds()[0], creds()[1])
    "<h1> Connecting to {ip} </h1>"
    device.open()
    return device.get_facts()


#     driver_info = get_driver_info()
#     option = int(input('(0) Print to screen \n(1) Write to file '))
#     system("rm Switch_facts.txt")
#     f = open('Switch_facts.txt', 'a')
#     for i in range(int(driver_info[1]), int(driver_info[2])+1):
#         try:
#             ip = driver_info[0] + str(i)
#             device = driver(ip, creds()[0], creds()[1])
#             print(f'\nConnecting to {ip}')
#             device.open()
#             info = device.get_facts()
#             print('-' * 80)
#             ios = info['os_version']
#             hostname = info['hostname']
#             vendor = info['vendor']
#             model = info['model']
#             serial = info['serial_number']
#             interface = 0
#             sfp = 0
#             for i in info['interface_list']:
#                 if i[0:18] == "GigabitEthernet1/0":
#                     interface += 1
#                 elif i[0:18] == "GigabitEthernet1/1" or i[0:4] == "Te1/1":
#                     sfp += 1
#             facts = f'''
# Your device's name is {hostname}({ip}).
# It is made by {vendor} and is a {model}.
# It's serial number is {serial}.
# The version of ios is {ios}
# Your device has {interface} interfaces and {sfp} SFP.
# '''
#             if option == 0:
#                 print(facts)
#             elif option == 1:
#                 f.write(facts)
#                 print("Written to file.")
#                 print('-' * 80, '\n')
#         except NetMikoAuthenticationException:
#             print(auth_error, ip)
#             print('-' * 80)
#         except ConnectionException:
#             print(cannot_connect, ip)
#             print('-' * 80)
#     f.close()
if __name__ == "__main__":
    app.run(debug=True)
