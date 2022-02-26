#!/bin/sh
#source /home/dataioit/viewsrtualenv/ZigZagBackend/3.8/bin/activate && cd /home/dataioit/ZigZagBackend
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
python3 manage.py loaddata dumpdata.json