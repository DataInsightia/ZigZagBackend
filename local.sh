#!/bin/sh
source venv/bin/activate
pip3 install -r requirements.txt
python3 manage.py collectstatic --no-input
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('zigzag', 'datainsightia@gmail.com', '@zigzag123')"
python3 sample_data.py