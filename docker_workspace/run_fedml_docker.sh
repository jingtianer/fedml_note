FEDML_DOCKER_IMAGE=fedml:tt
WORKSPACE=/mnt/d/Jingtian/桌面/快乐bupt/小组相关/工作/fedml/docker_workspace
FEDML_REPO=/mnt/d/Jingtian/桌面/快乐bupt/小组相关/工作/fedml/FedML
DATA=~/fedml_data

ID=$1
IP=$2
NUM=$3
HOSTNAME=$4

sudo docker run -itd -v $WORKSPACE:/home/workspace -v $FEDML_REPO:/home/fedml_repo -v $DATA:/root/fedml_data \
--shm-size=64g --ulimit nofile=65535 --ulimit memlock=-1 --privileged \
--env FEDML_NODE_INDEX=$ID \
--env WORKSPACE=$WORKSPACE \
--env FEDML_NUM_NODES=$NUM \
--env FEDML_MAIN_NODE_INDEX=0 \
--env FEDML_RUN_ID=$ID \
--env FEDML_MAIN_NODE_PRIVATE_IPV4_ADDRESS=$IP \
--gpus all \
--hostname $HOSTNAME \
-u fedml --net=host \
$FEDML_DOCKER_IMAGE \
/bin/bash 