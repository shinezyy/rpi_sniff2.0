pi_path=$1

if [ $pi_path = "" ] ; then
    echo Not allowed;
    exit 1;
fi

echo sudo cp ./interfaces $pi_path/etc/network/
echo sudo cp ./rc.local $pi_path/etc/
echo cp ./start.sh $pi_path/home/pi/
echo rm $pi_path/home/pi/rpi_sniff2.0 -rf
echo cp ./rpi_sniff2.0 $pi_path/home/pi/ -r

sudo cp ./interfaces $pi_path/etc/network/
sudo cp ./rc.local $pi_path/etc/
cp ./start.sh $pi_path/home/pi/
rm $pi_path/home/pi/rpi_sniff2.0 -rf
cp ./rpi_sniff2.0 $pi_path/home/pi/ -r

