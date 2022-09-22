# ./destory_fedml.sh
# read -n1 -p "Press any key to create containers..."
./run_fedml_docker.sh 0 127.0.0.1 4 server
./run_fedml_docker.sh 1 127.0.0.1 4 worker1
./run_fedml_docker.sh 2 127.0.0.1 4 worker2
./run_fedml_docker.sh 2 127.0.0.1 4 worker3
docker start $(docker ps -aq -f status=created)
docker ps -a -f label=fedml
read -n1 -p "Press any key to start monitoring gpu..."
watch -n 1 nvidia-smi
