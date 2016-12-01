import os

PC_test = True
server_ip_addr = '172.26.119.237:18000'
send_to_server = True
gathering_time = 90
pi_id = 1
update_interval = 500 #minute
test_in_lab = True
WLAN_SSID = ''
ip_start = ''


def init():
    global WLAN_SSID
    global ip_start
    pi_id = int(os.environ['pi_id'])

    if test_in_lab:
        WLAN_SSID = "124"
        ip_start = '114'
    else:
        WLAN_SSID = "NJU-WLAN"
        ip_start = '172'
