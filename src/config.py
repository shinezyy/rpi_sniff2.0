import os

class conf:

    def __init__(self):
        self.PC_test = False
        self.server_ip_addr = '172.26.119.237:18000'
        self.send_to_server = True
        self.gathering_time = 90
        self.pi_id = 1
        self.update_interval = 500 #minute
        self.test_in_lab = True
        self.WLAN_SSID = ''
        self.ip_start = ''
        if self.PC_test:
            self.work_dir = './'
        else:
            self.work_dir = '/home/pi/src/'


    def init(self):
        self.pi_id = int(os.environ['pi_id'])
        print self.pi_id
        if self.test_in_lab:
            self.WLAN_SSID = "124"
            self.ip_start = '114'
        else:
            self.WLAN_SSID = "NJU-WLAN"
            self.ip_start = '172'


c = conf()
