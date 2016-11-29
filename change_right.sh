#!/bin/bash

sudo chown pi:www-data ../Djangoticia/
sudo chown pi:www-data ./app1/
sudo chown pi:www-data ./db.sqlite3
sudo chown pi:www-data ./log/
sudo chown pi:www-data /var/www/

chmod 775 ../Djangoticia/
chmod 775 ./log/
chmod 775 ./app1/
chmod 775 /var/www/

sudo usermod -a -G dialout www-data

python3 manape.py collectstatic
