pi_path=$1

echo "Remember to add one parameter"
echo "Remember to modify PC_test and test_in_lab in config file"

if [ $pi_path = "" ] ; then
    echo Not allowed;
    exit 1;
else
    echo cp ./src $pi_path/home/pi/ -r

    cp ./src $pi_path/home/pi/ -r
fi
