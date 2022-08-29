sudo docker stop $(sudo docker ps -a | awk '{ print $1}' | tail -n +2)
sudo docker container prune
read -n1 -p "Press any key to create containers..."
./run_fedml_docker.sh 0 127.0.0.1 3 server
./run_fedml_docker.sh 1 127.0.0.1 3 worker1
./run_fedml_docker.sh 2 127.0.0.1 3 worker2
docker ps -a
read -n1 -p "Press any key to continue..."
watch -n 1 nvidia-smi
