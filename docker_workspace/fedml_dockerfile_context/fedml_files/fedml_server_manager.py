import json
import logging
import time

from fedml import mlops
from .message_define import MyMessage
from ...core.distributed.communication.message import Message
from ...core.distributed.fedml_comm_manager import FedMLCommManager
from ...core.mlops.mlops_profiler_event import MLOpsProfilerEvent

import threading


class FedMLServerManager(FedMLCommManager):
    def __init__(
        self, args, aggregator, comm=None, client_rank=0, client_num=0, backend="MQTT_S3",
    ):
        super().__init__(args, comm, client_rank, client_num, backend)
        self.args = args
        self.aggregator = aggregator
        self.round_num = args.comm_round
        self.args.round_idx = 0

        self.client_online_mapping = {}
        self.client_real_ids = json.loads(args.client_id_list)

        self.is_initialized = False
        self.client_id_list_in_this_round = None
        self.data_silo_index_list = None

    def run(self):
        super().run()

    def send_init_msg(self):
        global_model_params = self.aggregator.get_global_model_params()
        http_api = self.aggregator.http_api
        ret = http_api.NewRound(None, {"rid":"r{}".format(self.args.round_idx)})
        self.onNewRoundCallBack(ret, global_model_params, self.send_message_init_config)

        mlops.event("server.wait", event_started=True, event_value=str(self.args.round_idx))
        
        logging.info("\n\n==========start {}-th round training===========\n".format(self.args.round_idx))
        
    def register_message_receive_handlers(self):
        logging.info("register_message_receive_handlers------")
        self.register_message_receive_handler(
            MyMessage.MSG_TYPE_CONNECTION_IS_READY, self.handle_messag_connection_ready
        )

        self.register_message_receive_handler(
            MyMessage.MSG_TYPE_C2S_CLIENT_STATUS, self.handle_message_client_status_update,
        )
        
        self.register_message_receive_handler(
            MyMessage.MSG_TYPE_C2S_ADD_MODEL_READY, self.handle_message_add_model_ready,
        )
        
        self.register_message_receive_handler(
            MyMessage.MSG_TYPE_C2S_ADD_MODEL_SEND, self.handle_message_add_model_send,
        )
        
        
    def handle_message_add_model_send(self, msg_params):
        sender_id = msg_params.get(MyMessage.MSG_ARG_KEY_SENDER)
        real_id = self.client_real_ids.index(sender_id)
        if self.client_idx_in_this_round == len(self.client_id_list_in_this_round):
            self.client_idx_in_this_round = 0
        else :
            self.send_next()
        if self.aggregator.add_model_send_result(real_id):
            b_all_received = False
            retry_time = 0
            while not b_all_received:
                time.sleep(1)
                try :
                    b_all_received = self.aggregator.check_whether_all_receive(self.args.round_idx)
                except:
                    pass
                retry_time += 1
                assert retry_time < 15
            self.on_all_received()
            
    def send_next(self):
        self.send_start_add_model(self.client_id_list_in_this_round[self.client_idx_in_this_round])
        self.client_idx_in_this_round += 1
        
        
    def handle_message_add_model_ready(self, msg_params):
        sender_id = msg_params.get(MyMessage.MSG_ARG_KEY_SENDER)
        real_id = self.client_real_ids.index(sender_id)
        if self.aggregator.add_ready_result(real_id):
            self.client_idx_in_this_round = 0
            self.send_next()


    def handle_messag_connection_ready(self, msg_params):
        self.client_id_list_in_this_round = self.aggregator.client_selection(
            self.args.round_idx, self.client_real_ids, self.args.client_num_per_round
        )
        self.data_silo_index_list = self.aggregator.data_silo_selection(
            self.args.round_idx, self.args.client_num_in_total, len(self.client_id_list_in_this_round),
        )
        if not self.is_initialized:
            mlops.log_round_info(self.round_num, -1)

            # check client status in case that some clients start earlier than the server
            client_idx_in_this_round = 0
            for client_id in self.client_id_list_in_this_round:
                try:
                    self.send_message_check_client_status(
                        client_id, self.data_silo_index_list[client_idx_in_this_round],
                    )
                    logging.info("Connection ready for client" + str(client_id))
                except Exception as e:
                    logging.info("Connection not ready for client" + str(client_id))
                client_idx_in_this_round += 1

    def handle_message_client_status_update(self, msg_params):
        client_status = msg_params.get(MyMessage.MSG_ARG_KEY_CLIENT_STATUS)
        if client_status == "ONLINE":
            self.client_online_mapping[str(msg_params.get_sender_id())] = True

            logging.info("self.client_online_mapping = {}".format(self.client_online_mapping))

        mlops.log_aggregation_status(MyMessage.MSG_MLOPS_SERVER_STATUS_RUNNING)

        all_client_is_online = True
        for client_id in self.client_id_list_in_this_round:
            if not self.client_online_mapping.get(str(client_id), False):
                all_client_is_online = False
                break

        logging.info(
            "sender_id = %d, all_client_is_online = %s" % (msg_params.get_sender_id(), str(all_client_is_online))
        )

        if all_client_is_online:
            # send initialization message to all clients to start training
            self.send_init_msg()
            self.is_initialized = True
            

    def on_all_received(self):
        # if hasattr(self.args, "using_mlops") and self.args.using_mlops:
        #     self.mlops_event.log_event_ended(
        #         "server.wait", event_value=str(self.args.round_idx)
        #     )
        #     self.mlops_event.log_event_started(
        #         "server.agg_and_eval", event_value=str(self.args.round_idx)
        #     )
        mlops.event("server.wait", event_started=False, event_value=str(self.args.round_idx))
        mlops.event(
            "server.agg_and_eval", event_started=True, event_value=str(self.args.round_idx),
        )
        tick = time.time()
        global_model_params = self.aggregator.aggregate(self.args.round_idx)
        MLOpsProfilerEvent.log_to_wandb({"AggregationTime": time.time() - tick, "round": self.args.round_idx})

        self.aggregator.test_on_server_for_all_clients(self.args.round_idx)

        mlops.event("server.agg_and_eval", event_started=False, event_value=str(self.args.round_idx))

        # send round info to the MQTT backend
        mlops.log_round_info(self.round_num, self.args.round_idx)

        self.client_id_list_in_this_round = self.aggregator.client_selection(
            self.args.round_idx, self.client_real_ids, self.args.client_num_per_round
        )
        self.data_silo_index_list = self.aggregator.data_silo_selection(
            self.args.round_idx, self.args.client_num_in_total, len(self.client_id_list_in_this_round),
        )

        if self.args.round_idx == 0:
            MLOpsProfilerEvent.log_to_wandb({"BenchmarkStart": time.time()})

        
        
        http_api = self.aggregator.http_api
        model_params = {k:v.tolist() for k,v in global_model_params.items()}
        req = {"weight":model_params}
        req_json = json.dumps(req)
        model = json.dumps(req_json)
        ret = http_api.UpdateGlobal(None, {"model": model})
        self.onUpdateCallBack(ret)
        # todo: 发送一份到区块链

        self.args.round_idx += 1
        if self.args.round_idx == self.round_num:
            self.onNewRoundCallBack(ret, global_model_params, self.send_message_sync_model_to_client)
            mlops.log_aggregation_finished_status()
            logging.info("=============training is finished. Cleanup...============")
            self.cleanup()
        else:
            http_api = self.aggregator.http_api
            ret = http_api.NewRound(None, {"rid":"r{}".format(self.args.round_idx)})
            self.onNewRoundCallBack(ret, global_model_params, self.send_message_sync_model_to_client)
            logging.info("\n\n==========start {}-th round training===========\n".format(self.args.round_idx))
            # if hasattr(self.args, "using_mlops") and self.args.using_mlops:
            #     self.mlops_event.log_event_started(
            #         "server.wait", event_value=str(self.args.round_idx)
            #     )
            mlops.event("server.wait", event_started=True, event_value=str(self.args.round_idx))

    def onUpdateCallBack(self, ret):
        logging.info("=============chaincode model up to date============")
        
    def onNewRoundCallBack(self, ret, global_model_params , funktion):
        # def Run():
        #     client_idx_in_this_round = 0
        #     for receiver_id in self.client_id_list_in_this_round:
        #         funktion(
        #             receiver_id, global_model_params, self.data_silo_index_list[client_idx_in_this_round],
        #         )
        #         time.sleep(1)
        #         client_idx_in_this_round += 1
        # logging.info("=============New Round Created============")
        # # if global_model_params is not None:
        # threading.Thread(target=Run).start()
        
        client_idx_in_this_round = 0
        for receiver_id in self.client_id_list_in_this_round:
            funktion(
                receiver_id, global_model_params, self.data_silo_index_list[client_idx_in_this_round],
            )
            # time.sleep(1)
            client_idx_in_this_round += 1

    def send_start_add_model(self, receive_id):
        tick = time.time()
        message = Message(MyMessage.MSG_TYPE_S2C_START_ADD_MODEL, self.get_sender_id(), receive_id)
        self.send_message(message)
        MLOpsProfilerEvent.log_to_wandb({"Communiaction/Send_Total": time.time() - tick})
        
    def cleanup(self):

        client_idx_in_this_round = 0
        for client_id in self.client_id_list_in_this_round:
            self.send_message_finish(
                client_id, self.data_silo_index_list[client_idx_in_this_round],
            )
            client_idx_in_this_round += 1
        time.sleep(3)
        self.finish()

    def send_message_init_config(self, receive_id, global_model_params, datasilo_index):
        tick = time.time()
        message = Message(MyMessage.MSG_TYPE_S2C_INIT_CONFIG, self.get_sender_id(), receive_id)
        message.add_params(MyMessage.MSG_ARG_KEY_MODEL_PARAMS, global_model_params)
        message.add_params(MyMessage.MSG_ARG_KEY_CLIENT_INDEX, str(datasilo_index))
        message.add_params(MyMessage.MSG_ARG_KEY_CLIENT_OS, "PythonClient")
        self.send_message(message)
        MLOpsProfilerEvent.log_to_wandb({"Communiaction/Send_Total": time.time() - tick})

    def send_message_check_client_status(self, receive_id, datasilo_index):
        message = Message(MyMessage.MSG_TYPE_S2C_CHECK_CLIENT_STATUS, self.get_sender_id(), receive_id)
        message.add_params(MyMessage.MSG_ARG_KEY_CLIENT_INDEX, str(datasilo_index))
        self.send_message(message)

    def send_message_finish(self, receive_id, datasilo_index):
        message = Message(MyMessage.MSG_TYPE_S2C_FINISH, self.get_sender_id(), receive_id)
        message.add_params(MyMessage.MSG_ARG_KEY_CLIENT_INDEX, str(datasilo_index))
        self.send_message(message)
        logging.info(" ====================send cleanup message to {}====================".format(str(datasilo_index)))

    def send_message_sync_model_to_client(self, receive_id, global_model_params, client_index):
        tick = time.time()
        logging.info("send_message_sync_model_to_client. receive_id = %d" % receive_id)
        message = Message(MyMessage.MSG_TYPE_S2C_SYNC_MODEL_TO_CLIENT, self.get_sender_id(), receive_id,)
        message.add_params(MyMessage.MSG_ARG_KEY_MODEL_PARAMS, global_model_params)
        message.add_params(MyMessage.MSG_ARG_KEY_CLIENT_INDEX, str(client_index))
        message.add_params(MyMessage.MSG_ARG_KEY_CLIENT_OS, "PythonClient")
        self.send_message(message)

        MLOpsProfilerEvent.log_to_wandb({"Communiaction/Send_Total": time.time() - tick})

        mlops.log_aggregated_model_info(
            self.args.round_idx + 1, model_url=message.get(MyMessage.MSG_ARG_KEY_MODEL_PARAMS_URL),
        )
