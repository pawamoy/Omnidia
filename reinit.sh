rm db.sqlite3 2>/dev/null
./manage.py migrate
./manage.py createsuperuser

