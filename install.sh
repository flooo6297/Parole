#!/bin/bash

mkdir -p /tmp/Parole
git clone git://github.com/flooo6297/Parole.git /tmp/Parole
cd /tmp/Parole || exit
sh copy_files.sh
cd ..
rm -Rf Parole

echo "start with -> sudo systemctl start parole"