#!/bin/sh
TEST=`pwd`'/server/discord_bot.py'
echo $TEST

sudo apt upgrade
sudo apt install
sudo apt install pip
pip install discord.py
pip install beautifulsoup4

echo Discord Bot Starting............

python3 $TEST
