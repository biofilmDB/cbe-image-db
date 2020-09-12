# Should this be here since you have to enter cradentials?
# git pull

# rebuild the container with new updates
docker-compose -f ../docker-compose.yml -f ../docker-compose-web.yml build
docker-compose stop
docker-compose -f ../docker-compose.yml -f ../docker-compose-web.yml up
