#!/bin/bash

CONFIGDIRECTORY="/etc/Parole"

echo "creating directorys..."
mkdir -p "$CONFIGDIRECTORY/WordDatabase"
mkdir -p /opt/Parole

echo "copying all the config files..."
cp -f "Templates/de_DE_frami.txt" "$CONFIGDIRECTORY/WordDatabase"

cp -f "Script/Parole.py" "/opt/Parole"
chmod 755 /opt/Parole/Parole.py

cp -n "Templates/addresses.txt" "$CONFIGDIRECTORY"
cp -n "Templates/host.txt" "$CONFIGDIRECTORY"
cp -n "Templates/dailyPassword.conf" "$CONFIGDIRECTORY"

cp -f "Templates/parole.service" /etc/systemd/system
chmod 644 /etc/systemd/system/parole.service
systemctl daemon-reload