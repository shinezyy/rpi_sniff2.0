pi_path=$1

echo "Remember to add one parameter"
echo "Remember to modify PC_test and test_in_lab in config file"

if [ $pi_path = "" ] ; then
    echo Not allowed;
    exit 1;
else
    echo sudo cp ./interfaces $pi_path/etc/network/
    echo sudo cp ./rc.local $pi_path/etc/
    echo sudo cp ./environment $pi_path/etc/
    echo cp ./start.sh $pi_path/home/pi/
    echo cp ./src $pi_path/home/pi/ -r

    sudo cp ./interfaces $pi_path/etc/network/
    sudo cp ./rc.local $pi_path/etc/
    sudo cp ./environment $pi_path/etc/
    cp ./start.sh $pi_path/home/pi/
    cp ./src $pi_path/home/pi/ -r
fi
