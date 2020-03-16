#!/bin/bash

git clone git@github.com:flooo6297/Parole.git Parole
cd Parole || exit
sh copy_files.sh
cd ..
rm -Rf Parole

echo "start with -> sudo systemctl start parole"