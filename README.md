# dodi_assessment
This is the django assessment test for dodi

1/ install python 12
install pip
install redis and run it, test with ping
create a venv
clone the repo
pip install -r requirements.txt
python manage.py runserver
celery -A cinema.celery beat --loglevel=info
celery -A cinema.celery worker --pool=solo --loglevel=info