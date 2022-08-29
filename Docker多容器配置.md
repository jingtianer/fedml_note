# Docker安装
```bash
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```
- 中间遇到输出，提示建议使用for windows
```sh
WSL DETECTED: We recommend using Docker Desktop for Windows.
Please get Docker Desktop from https://www.docker.com/products/docker-desktop
```

# 创建容器并配置环境
## 验证是否可以使用gpu
- [官方参考](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker)
```sh
docker run --gpus all nvcr.io/nvidia/k8s/cuda-sample:nbody nbody -gpu -benchmark
```
## pull fedml镜像
```sh
docker pull fedml/fedml:cuda-11.4.0-devel-ubuntu20.04
```

## 编写运行脚本并运行
```sh
FEDML_DOCKER_IMAGE=fedml/fedml:cuda-11.4.0-devel-ubuntu20.04
WORKSPACE=~/Desktop/docker_workspace
FEDML_REPO=~/Desktop/FedML
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
```

### 创建两个容器
```sh
bash run_fedml_docker.sh 1 2 127.0.0.1 worker1
bash run_fedml_docker.sh 2 2 127.0.0.1 worker2
```

### 修改GPU MAPPING
```
mapping_default:
  tt: [1]
  worker1: [1]
  worker2: [1]
```

### 初始化fedml
- 分别在两个docker内运行
```sh
sudo /home/code/setup_docker.sh
```
- 更新fedml
- 自带的pytorch支持的gpu算力等级太低，需要更新

### 在主节点下启动server
```sh
bash run_server.sh
```

### 在容器中启动client
```sh
bash run_client.sh 1
bash run_client.sh 2
```
- 可以正常运行，也可以正常调用gpu

# 使用Dockerfile避免setup_docker.sh
- 节省空间
- 避免重复下载环境
## 新建一个空目录，在其中创建文件`Dockerfile`
```sh
FROM fedml/fedml:cuda-11.4.0-devel-ubuntu20.04
RUN python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install --upgrade fedml
```

- 对于算力较高的gpu，更新pytorch

```sh
FROM fedml/fedml:cuda-11.4.0-devel-ubuntu20.04
RUN python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install --upgrade fedml
RUN pip3 uninstall -y torch
RUN pip3 uninstall -y torchaudio
RUN pip3 uninstall -y torchvision
RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116 #3050TI
```
## 在该目录下执行
```sh
sudo docker build -t fedml:tt .
```

## 使用`fedml:tt`创建container
```sh
FEDML_DOCKER_IMAGE=fedml:tt ## 这里
WORKSPACE=~/Desktop/docker_workspace
FEDML_REPO=~/Desktop/FedML
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
```

## 容器创建脚本
- 创建容器并开始观测gpu使用率
```sh
sudo docker stop $(sudo docker ps -a | awk '{ print $1}' | tail -n +2)
sudo docker container prune
read -n1 -p "Press any key to create containers..."
./run_fedml_docker.sh 0 127.0.0.1 3 server
./run_fedml_docker.sh 1 127.0.0.1 3 worker1
./run_fedml_docker.sh 2 127.0.0.1 3 worker2
docker ps -a
read -n1 -p "Press any key to continue..."
watch -n 1 nvidia-smi
```