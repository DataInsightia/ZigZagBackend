#!/bin/sh
zip -r ZigZagBackend.zip . -x "*/venv/*" -x '*/.DS_Store/*' -x '*.sqlite3' -x '*/static/*' 
scp -P 21098 ZigZagBackend.zip dataioit@datainsightia.in:/home/dataioit/ZigZagBackend/
ssh -o StrictHostKeyChecking=no -l dataioit datainsightia.in "unzip ZigZagBackend.zip; source /home/dataioit/virtualenv/ZigZagBackend/3.8/bin/activate && cd /home/dataioit/ZigZagBackend; pip install -r requirements.txt; python3 manage.py makemigrations api; python3 manage.py migrate api; python3 manage.py collectstatic --no-input"


