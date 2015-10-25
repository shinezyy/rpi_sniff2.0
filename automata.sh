#monitor mode on

sudo poff shinez
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
sudo dhclient wlan0
sudo pon shinez
sudo ip route del default
sudo ip route add default dev ppp0

#send
python ./send_mail.py
