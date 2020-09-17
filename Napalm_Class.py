from napalm import get_network_driver


class Device:

    def __init__(self, ip, username, password, vendor, hostname):
        self.ip = ip
        self.username = username
        self.password = password
        self.vendor = vendor
        self.hostname = hostname

    def connect(self):
        get_network_driver(self.vendor)
        driver = get_network_driver(self.vendor)
        device = driver(self.ip, self.username, self.password)
        device.open()

    def get_facts(self):
        get_network_driver(self.vendor)
        driver = get_network_driver(self.vendor)
        device = driver(self.ip, self.username, self.password)
        device.open()
        return device.get_facts()

    def get_interfaces(self):
        get_network_driver(self.vendor)
        driver = get_network_driver(self.vendor)
        device = driver(self.ip, self.username, self.password)
        device.open()
        return device.get_interfaces()

    def get_mac_address_table(self):
        get_network_driver(self.vendor)
        driver = get_network_driver(self.vendor)
        device = driver(self.ip, self.username, self.password)
        device.open()
        return device.get_mac_address_table()

    def arp_table(self):
        get_network_driver(self.vendor)
        driver = get_network_driver(self.vendor)
        device = driver(self.ip, self.username, self.password)
        device.open()
        return device.get_arp_table()

    def get_config(self):
        get_network_driver(self.vendor)
        driver = get_network_driver(self.vendor)
        device = driver(self.ip, self.username, self.password)
        device.open()
        return device.get_config
        retrieve = 'running',
        full = False,

    def get_environment(self):
        get_network_driver(self.vendor)
        driver = get_network_driver(self.vendor)
        device = driver(self.ip, self.username, self.password)
        device.open()
        return device.get_environment()

    def get_lldp_details(self):
        get_network_driver(self.vendor)
        driver = get_network_driver(self.vendor)
        device = driver(self.ip, self.username, self.password)
        device.open()
        return device.get_lldp_neighbors_detail()

    def get_ntp_servers(self):
        get_network_driver(self.vendor)
        driver = get_network_driver(self.vendor)
        device = driver(self.ip, self.username, self.password)
        device.open()
        return device.get_ntp_servers()

    def get_users(self):
        get_network_driver(self.vendor)
        driver = get_network_driver(self.vendor)
        device = driver(self.ip, self.username, self.password)
        device.open()
        return device.get_users()

    def get_interface_ip(self):
        get_network_driver(self.vendor)
        driver = get_network_driver(self.vendor)
        device = driver(self.ip, self.username, self.password)
        device.open()
        return device.get_interfaces_ip()
