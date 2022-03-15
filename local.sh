#!/bin/sh
source venv/bin/activate
pip3 install -r requirements.txt

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('zigzag', 'datainsightia@gmail.com', '@zigzag123')"



rm -rf venv/
scp -P 21098 -r * dataioit@datainsightia.in:/home/dataioit/ZigZagBackend/