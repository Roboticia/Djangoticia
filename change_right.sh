#!/bin/bash

sudo chown pi:www-data ../Djangoticia/
sudo chown pi:www-data ./app1/
sudo chown pi:www-data ./db.sqlite3
sudo chown www-data:pi ./log/
chmod 775 ../Djangoticia/
chmod 766 ./log/
chmod 775 ./app1/

python3 manape.py collectstatic
