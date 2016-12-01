import os

class conf:

    PC_test = True
    server_ip_addr = '172.26.119.237:18000'
    send_to_server = True
    gathering_time = 90
    pi_id = 1
    update_interval = 500 #minute
    test_in_lab = True
    WLAN_SSID = ''
    ip_start = ''

    def init(self):
        self.pi_id = int(os.environ['pi_id'])

        if self.test_in_lab:
            self.WLAN_SSID = "124"
            self.ip_start = '114'
        else:
            self.WLAN_SSID = "NJU-WLAN"
            self.ip_start = '172'


c = conf()
