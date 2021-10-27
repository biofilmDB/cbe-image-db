export PASSANGER_PORT=$PORT
python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
python manage.py populatetesting
echo "port: $PORT"
echo "passanger port: $PASSENGER_PORT"
# commenting out until elatci search works
#python manage.py search_index --create
passenger start --port $PORT
