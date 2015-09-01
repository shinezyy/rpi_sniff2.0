#monitor mode on

sudo wpa_cli disconnect
sudo ifconfig wlan0 down
sudo iwconfig wlan0 mode monitor
sudo ifconfig wlan0 up

# gather
sudo python ./gather.py
sleep 5

# monitor mode off
sudo ifconfig wlan0 down
sudo iwconfig wlan0 mode managed
sudo ifconfig wlan0 up

sudo wpa_cli reassociate
sleep 5
sudo dhclient wlan0

#send
python ./send.py
