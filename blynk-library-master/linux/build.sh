#!/bin/bash

case "$1" in
raspberry)
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install build-essential git-core
    sudo git clone git://git.drogon.net/wiringPi
    cd wiringPi
    sudo git pull origin
    ./build
    gpio -v
    cd ..
    sudo make clean all target=raspberry
    exit 0
    ;;
linux)
    sudo make clean all
    exit 0
    ;;
esac

echo "Please specify platform: raspberry, linux"
exit 1
