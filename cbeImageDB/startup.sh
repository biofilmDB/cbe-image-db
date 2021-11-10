python manage.py migrate
python manage.py populatetesting
# build the elasticsearch index
python manage.py search_index --create
# run passenger on the specified port
# $PORT is a changing port number on heroku
passenger start --port $PORT
