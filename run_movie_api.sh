virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements-dev.txt
python manage.py makemigrations
python manage.py migrate
