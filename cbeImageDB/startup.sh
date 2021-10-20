python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
# commenting out until elatci search works
#python manage.py search_index --create
passenger start
