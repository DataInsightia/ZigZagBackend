#!/bin/sh
source /home/dataioit/virtualenv/ZigZagBackend/3.8/bin/activate && cd /home/dataioit/ZigZagBackend
rm -rf * .??*
git clone https://angappanmuthu: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@github.com/DataInsightia/ZigZagBackend.git .
echo "from django.contrib.auth.models import User; User.objects.create_superuser('zigzag', 'datainsightia@gmail.com', '@zigzag123')" | python manage.py shell
pip3 install -r requirements.txt
python3 manage.py collectstatic --no-input
python3 manage.py makemigrations
python3 manage.py migrate