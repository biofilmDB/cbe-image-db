# CBE machine will have a read only access ssh key
echo -e "\033[1;34mUpdating local from GitHub\033[0m"
git pull

# rebuild the container with new updates
echo -e "\n\033[1;34mRebuilding docker containers\033[0m"
docker-compose -f ../docker-compose.yml -f ../docker-compose-web.yml build
echo -e "\n\033[1;34mStopping all docker containers\033[0m"
docker-compose -f ../docker-compose.yml -f ../docker-compose-web.yml stop
echo -e "\n\033[1;34mRestarting docker\033[0m"
docker-compose -f ../docker-compose.yml -f ../docker-compose-web.yml up
