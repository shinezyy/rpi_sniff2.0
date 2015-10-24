#monitor mode on

sudo ifconfig wlan0 down
sudo iwconfig wlan0 mode monitor
sudo ifconfig wlan0 up

# gather
sudo python ./gather.py
sleep 5

# monitor mode off
sudo ifconfig wlan0 down
sudo iwconfig wlan0 mode managed
sudo iwconfig wlan0 essid NJU-WLAN
sudo ifconfig wlan0 up
sleep 2
sudo dhclient wlan0

#send
python ./send.py
