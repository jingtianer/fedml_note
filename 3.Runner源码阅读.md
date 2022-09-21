# wandb 的使用
- 在wandb官网[project页面](https://wandb.ai/tt_blockchain/projects)创建工程
- 获取wandb_key
## 配置config.yaml
- enable - true
- wandb key
- priject name
```sh
tracking_args:
  log_file_dir: ./log
  enable_wandb: true #enable
  wandb_key: e3be1b9a8ab45f14a6ff454009bc7ca07b8792ba #key
  wandb_project: fedml_mnist_test #project name
  wandb_name: fedml_torch_fedavg_mnist_lr
```
## 运行
- 运行时选择2，将key再输入一次
```sh
wandb: (1) Create a W&B account
wandb: (2) Use an existing W&B account
wandb: (3) Dont visualize my results
wandb: Enter your choice: 2
wandb: You chose 'Use an existing W&B account'
wandb: You can find your API key in your browser here: https://wandb.ai/authorize
wandb: Paste an API key from your profile and hit enter, or press ctrl+c to quit: 
```
## wandb结果
- 在终端输出了
```sh
wandb: Waiting for W&B process to finish... (success).
wandb:                                                                                
wandb: 
wandb: Run history:
wandb:          AggregationTime ▂▃▃▂▂▃▃▃▃▂▃▃▁▃▃▂▃▇▃▃▃▇▂▃▃▂▃▃█▃▂▂▂▃▃▃▃▁▂▂
wandb:           BenchmarkStart ▁
wandb:                 BusyTime ▁▄▄▄▄▃▅▃▂▄▆▃▃▇▄▃▅█▃▆▄▅▅▅▃▂▄▅▄▃▄▃▄▄▃▂▄▃▃█
wandb:    Comm/recieve_delay_s3 ▃▁▂▁▂▂▁▂▂▂▁▂▂▁▃▄▂▄▂▂▁█▂▂▂▂▄▂▁▂▂▂▃▂▃▁▁▂▂▃
wandb:          Comm/send_delay █▃▂▁▁▁▃▂▂▁▂▆▁▄▂▃▅▂▂▂▂▁▁▁▂▁▁▁▁▁▁▃▁▁▂▂▁▁▂▁
wandb:     Comm/send_delay_mqtt ▃▆▆▇▆▆▇▆▆▆▆▆▆▆▂▆▆▆▆▆▆▆▆▁█▆▆▆▆▆▁▆▆▁▁▆▆▆█▁
wandb: Communiaction/Send_Total █▃▂▁▁▁▃▂▂▁▂▆▁▄▂▃▅▂▂▂▂▁▁▁▂▁▁▁▁▁▁▃▁▁▂▂▁▁▂▁
wandb:              ListenStart ▁
wandb:       MessageReceiveTime ▁▁▂▂▂▂▂▂▂▂▂▂▄▄▄▄▄▄▄▄▅▅▅▅▅▅▅▅▇▇▇▇▇▇▇▇▇▇██
wandb:          PickleDumpsTime █▁▅▁▁▁▂▆▃▅▂▃▅▁▁▁▅▁▆▅▁▁▅▅▁▄▅▅▁▅▅▅▁▁▅▅▅▂▅▁
wandb:                 Test/Acc ▁▄▄▅▆▆▆████
wandb:                Test/Loss █▆▅▃▃▂▂▁▁▁▁
wandb:                TotalTime ▁
wandb:                Train/Acc ▁▄▄▅▆▆▆████
wandb:               Train/Loss █▆▅▄▃▂▂▁▁▁▁
wandb:             UnpickleTime █▄▄▃█▄▄▄▄▄▇▇▄▇▄▁▄▇▄▁▄▇▇▄▇▂▄▇▄▄▄▄▄▄▇▄▄▂▁▄
wandb:                    round ▁▁▁▁▂▂▂▂▂▂▃▃▃▃▃▄▄▄▄▅▅▅▅▅▅▅▆▆▆▆▇▇▇▇▇▇▇███
wandb: 
wandb: Run summary:
wandb:          AggregationTime 0.00103
wandb:           BenchmarkStart 1660014268.494
wandb:                 BusyTime 8.49421
wandb:    Comm/recieve_delay_s3 3.13148
wandb:          Comm/send_delay 0.40766
wandb:     Comm/send_delay_mqtt 4e-05
wandb: Communiaction/Send_Total 0.40971
wandb:              ListenStart 1660014198.82541
wandb:       MessageReceiveTime 1660014798.21999
wandb:          PickleDumpsTime 0.00032
wandb:                 Test/Acc 0.80057
wandb:                Test/Loss 1.86352
wandb:                TotalTime 607.89401
wandb:                Train/Acc 0.79653
wandb:               Train/Loss 1.86602
wandb:             UnpickleTime 0.00087
wandb:                    round 49
wandb: 
wandb: Synced exalted-eon-1: https://wandb.ai/tt_blockchain/fedml_mnist_test/runs/3850zs40
wandb: Synced 5 W&B file(s), 0 media file(s), 0 artifact file(s) and 0 other file(s)
wandb: Find logs at: ./wandb/run-20220809_030244-3850zs40/logs
```
- 在网页中输出情况
[report.pdf](./fedml-wandb-test%20_%20fedml_mnist_test%20%E2%80%93%20Weights%20%26%20Biases.pdf)
# FedMLRunner
- 该Runner是通用的runner
- 根据args.training_type进行初始化
  - simulation
  - cross silo
  - cross device
## _init_simulation_runner
- 根据args中的backend构造runner
  - SP -> SimulatorSingleProcess
  - MPI -> SimulatorMPI
  - NCCL -> SimulatorNCCL
## _init_cross_silo_runner
- 根据args.role为 `client`or`server`构造runner
  - client -> Client
  - server -> Sever
## _init_cross_device_runner
- args.role 为 sever，构造ServerMNN，否则raise Exception

# Sever
- FedMLCrossSiloServer
- 若federated_optimizer为FedAvg，trainer = server_initializer.init_server
- 若federated_optimizer为LSA，trainer=FedML_LSA_Horizontal

## server_initializer.init_server
- 创建Aggregator - 聚集器，处理训练相关的任务，将Client的模型聚集并更新全局模型
- 创建FedMLServerManager - 收发网络请求
## FedML_LSA_Horizontal
- 根据client rank init server或client
- init server会创建Aggregator和ServerManager
- init client会创建Trainer和ClientManager，一般role为server，rank也是0，这一步应该不会走到
# Client
- FedMLCrossSiloClient
- 若federated_optimizer为FedAvg，trainer = client_initializer.init_client
- 若federated_optimizer为LSA，trainer=FedML_LSA_Horizontal

# Aggregator
- FedMLAggregator
- 通过cross silo找到的
- 还有FedSegAggregator、BaseLocalAggregator、RobustAggregator等
## 函数
- add_local_trained_result和check_whether_all_receive
  - add_local_trained_result负责记录local的训练结果
  - check_whether_all_receive负责检查是否全部上传本地模型，若是，则将全部flag置为False
- **aggregate**
  - 计算出总的训练样本数目（所有client训练的样本数之和）
  - 根据本地样本数/总训练数计算权值`w`
  - 根据权值算出模型参数的加权平均
  - 更新全局模型
- data_silo_selection
  - 若每轮训练数和总client数相同，则返回`0...n-1`，否则随机从中随机寻找一部分
- client_selection
  - 也是一个随机选择，和上一个差不多
- client_sampling
  - 看起来和data_silo_selection一模一样
- test_on_server_for_all_clients
  - if self.trainer.test_on_the_server : return
  - 每隔n轮一次test 或 最后一轮时进行test(对训练集)
    - 对于每一个client，计算TP+TN，训练个数，loss，并保存
    - 计算总的acc和loss，打log，若启用了wandb，则使用wandb api记录
  - 对测试集进行测试，log，wandb记录

# FedMLServerManager
## 父类 ServerManager
### 函数
- \_\_init__
  - 根据backend具体指定的协议名称构造对应的CommunicationManager
- run
  - 执行register_message_receive_handlers（子类实现），用于注册子类定义的几种消息和消息对应的callback函数，当收到对应消息类型时调用相应函数
  - 执行具体协议对应的CommunicationManager的handle_receive_message
- receive_message
  - 参数，msg_type，msg_params
  - 从一个字典中根据msgType获取callback，并调用，传递msg_params
- send_message
  - 通过CommunicationManager发送
- register_message_receive_handler
  - 维护message_handler_dict，即前面提到的callback字典
  - 注册新的msg_type和他的callback
- finish
  - 将CommunicationManager stop掉

## FedMLServerManager的函数
- run
  - super().run()
- send_init_msg
  - 发送初始化信息
  - 对于本轮中的每一个参与的client，发送初始模型参数，通过函数send_message_init_config
  - send_message_init_config通过父类的send_message实现
- register_message_receive_handlers
  - 注册三类信息的处理函数，通过父类的register_message_receive_handler实现
  - client的connection ready
  - client的status change
    - 当所有的client都online，调用send_init_msg
  - client的model发送
    - 通过Aggregator的add_local_trained_result将参数中的模型参数，训练样本数等信息聚集起来
    - 如果全部发送了模型信息
      - 调用Aggregator的aggregate函数更新全局模型，test_on_server_for_all_clients函数进行模型的测试。
      - 进行下一轮训练，全局模型发送至下一轮的机器中，通过send_message_sync_model_to_client函数
      - 轮数+=1，若轮数达到预定的总轮数，调用cleanup函数
- cleanup
  - 向所有client发送finis信息
  - 延迟3s，调用finish结束自己（父类的finish）
  - 
- 三个handle_*
  - register_message_receive_handlers中注册的三个函数，用于处理客户端的消息
- 几个send_*
  - 在前面都有提到，向客户端发送信息
  
# FedMLCrossSiloClient
- 如果args.scenario
  - HIERARCHICAL，则根据rank，若rank为0，构造ClientMasterManager，否则构造ClientSlaveManager
  - HORIZONTAL，构造ClientMasterManager

## Master客户端的父类--ClientManager
- 与ServerManager类似，根据协议构造CommunicationManager，提供消息类型与回调的注册函数，提供send_message函数
- 不同点在于Server的Host和Port固定，Client从配置中读取

## ClientMasterManager
- 和ServerManager类似，处理网络消息，给server发送信息（如本地模型信息等）
- 训练本地模型
## ClientSlaveManager
- 处理本地训练

# Observer
- 定义抽象函数receive_message，communicationManager会调用observer的这个函数，将受到的消息类型，参数传递给子类，上面的例子中都是使用`消息类型-handle函数`的dict实现对不同类型的消息进行处理

# 结论
> 根据FedML+BlockChain的定义双方之间的通信流程，根据通信流程分别置顶S-C的通信消息，直接基于ClientManager和ServerManager，自定义一个FedMLBlockChainServer和FedMLBlockChainServer，实现这个通信过程。