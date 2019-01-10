#!/bin/sh
kill -9 `cat save_pid.txt`
rm save_pid.txt
rm -rf ../aetelbot-old
mkdir ../aetelbot-old/
mv * ../aetelbot-old
git clone https://github.com/aetel/aetelbot
mv aetelbot/* .
rm -rf aetelbot
cp ../aetelbot-old/data-and-settings.json .
cp ../aetelbot-old/aetelbot.log .
nohup python aetelbot-main.py &
echo $! > save_pid.txt