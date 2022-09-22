echo "stopped"
docker container stop $(docker ps -aq -f label=fedml)
echo "destoried"
docker container rm $(docker ps -aq -f label=fedml)