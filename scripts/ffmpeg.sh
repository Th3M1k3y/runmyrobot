#!/bin/bash

# This script will remove the stock version of FFMpeg, and replace it with one with the overlay filter on from r3n33

# Clear screen
printf "\ec"
echo -en "\ec"

# Start installing everything needed
echo
echo -e "\e[33mInstalling all the things needed to run the robot\e[39m "
sudo apt-get -y install python-serial python-dev libgnutls28-dev espeak python-smbus python-pip git

echo -e "\e[33mGit clone: FFMpeg\e[39m "
cd ~ &&\

if [ -d "FFmpeg" ]; then
  sudo rm -r FFmpeg
fi

git clone -b dynoverlay --single-branch https://github.com/r3n33/FFmpeg.git &&\

#cd FFmpeg &&\

cd /home/pi/FFmpeg &&\
echo -e "\e[33mCleaning FFMpeg\e[39m "
./configure --arch=armel --target-os=linux --enable-gpl --enable-libx264 --enable-nonfree --enable-gnutls --extra-libs=-ldl --enable-zlib &&\
make clean
echo -e "\e[33mBuilding FFMpeg\e[39m "
make -j4 &&\
sudo make install