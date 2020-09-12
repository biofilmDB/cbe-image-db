# CBE machine will have a read only access ssh key
git pull

# rebuild the container with new updates
docker-compose -f ../docker-compose.yml -f ../docker-compose-web.yml build
docker-compose stop
docker-compose -f ../docker-compose.yml -f ../docker-compose-web.yml up
