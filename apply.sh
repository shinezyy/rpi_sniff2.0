pi_path=$1

if [ $pi_path = "" ] ; then
    echo Not allowed;
    exit 1;
else
    echo sudo cp ./interfaces $pi_path/etc/network/
    echo sudo cp ./rc.local $pi_path/etc/
    echo cp ./start.sh $pi_path/home/pi/
    echo cp ./src $pi_path/home/pi/ -r

    sudo cp ./interfaces $pi_path/etc/network/
    sudo cp ./rc.local $pi_path/etc/
    cp ./start.sh $pi_path/home/pi/
    cp ./src $pi_path/home/pi/ -r
fi
