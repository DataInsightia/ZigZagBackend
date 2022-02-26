#!/bin/sh
#source /home/dataioit/viewsrtualenv/ZigZagBackend/3.8/bin/activate && cd /home/dataioit/ZigZagBackend
source /home/dataioit/virtualenv/ZigZagBackend/3.8/bin/activate && cd /home/dataioit/ZigZagBackend
rm -rf */
rm -rf .??*
git clone https://angappanmuthu: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@github.com/DataInsightia/ZigZagBackend.git .
pip3 install -r requirements.txt
python3 manage.py collectstatic --no-input
python3 manage.py makemigrations
python3 manage.py migrate --fake
python3 manage.py loaddata dumpdata.json