FEDML_DOCKER_IMAGE=fedml:tt
WORKSPACE=~/Desktop/docker_workspace
FEDML_REPO=~/Desktop/FedML
DATA=~/fedml_data

ID=$1
IP=$2
NUM=$3
HOSTNAME=$4

docker run -itd -v $WORKSPACE:/home/workspace -v $FEDML_REPO:/home/fedml_repo -v $DATA:/root/fedml_data \
-v $WORKSPACE/yaml-requests/config/$HOSTNAME:/home/yaml_requests_config \
--name=$HOSTNAME \
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
-l fedml \
-w /home/workspace/step_by_step \
$FEDML_DOCKER_IMAGE \
/bin/bash 