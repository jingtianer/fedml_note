# 无效
docker cp ~/.local/lib/python3.10/site-packages/fedml/cross_silo/client/fedml_client_master_manager.py server:/usr/local/lib/python3.8/dist-packages/fedml/cross_silo/client/
docker cp ~/.local/lib/python3.10/site-packages/fedml/cross_silo/server/fedml_aggregator.py server:/usr/local/lib/python3.8/dist-packages/fedml/cross_silo/client/
docker cp ~/.local/lib/python3.10/site-packages/fedml/cross_silo/server/fedml_server_manager.py server:/usr/local/lib/python3.8/dist-packages/fedml/cross_silo/client/
docker cp ../yaml-requests/yamlRequests server:/usr/local/lib/python3.8/dist-packages/fedml/cross_silo/

docker cp ~/.local/lib/python3.10/site-packages/fedml/cross_silo/client/fedml_client_master_manager.py worker1:/usr/local/lib/python3.8/dist-packages/fedml/cross_silo/client/
docker cp ~/.local/lib/python3.10/site-packages/fedml/cross_silo/server/fedml_aggregator.py worker1:/usr/local/lib/python3.8/dist-packages/fedml/cross_silo/client/
docker cp ~/.local/lib/python3.10/site-packages/fedml/cross_silo/server/fedml_server_manager.py worker1:/usr/local/lib/python3.8/dist-packages/fedml/cross_silo/client/
docker cp ../yaml-requests/yamlRequests worker1:/usr/local/lib/python3.8/dist-packages/fedml/cross_silo/

docker cp ~/.local/lib/python3.10/site-packages/fedml/cross_silo/client/fedml_client_master_manager.py worker3:/usr/local/lib/python3.8/dist-packages/fedml/cross_silo/client/
docker cp ~/.local/lib/python3.10/site-packages/fedml/cross_silo/server/fedml_aggregator.py worker3:/usr/local/lib/python3.8/dist-packages/fedml/cross_silo/client/
docker cp ~/.local/lib/python3.10/site-packages/fedml/cross_silo/server/fedml_server_manager.py worker3:/usr/local/lib/python3.8/dist-packages/fedml/cross_silo/client/
docker cp ../yaml-requests/yamlRequests worker3:/usr/local/lib/python3.8/dist-packages/fedml/cross_silo/

docker cp ~/.local/lib/python3.10/site-packages/fedml/cross_silo/client/fedml_client_master_manager.py worker2:/usr/local/lib/python3.8/dist-packages/fedml/cross_silo/client/
docker cp ~/.local/lib/python3.10/site-packages/fedml/cross_silo/server/fedml_aggregator.py worker2:/usr/local/lib/python3.8/dist-packages/fedml/cross_silo/client/
docker cp ~/.local/lib/python3.10/site-packages/fedml/cross_silo/server/fedml_server_manager.py worker2:/usr/local/lib/python3.8/dist-packages/fedml/cross_silo/client/
docker cp ../yaml-requests/yamlRequests worker2:/usr/local/lib/python3.8/dist-packages/fedml/cross_silo/

cp ~/.local/lib/python3.10/site-packages/fedml/cross_silo/client/fedml_client_master_manager.py ../fedml_dockerfile_context/fedml_files/
cp ~/.local/lib/python3.10/site-packages/fedml/cross_silo/server/fedml_aggregator.py ../fedml_dockerfile_context/fedml_files/
cp ~/.local/lib/python3.10/site-packages/fedml/cross_silo/server/fedml_server_manager.py ../fedml_dockerfile_context/fedml_files/
cp -r ../yaml-requests/yamlRequests/* ../fedml_dockerfile_context/fedml_files/yamlRequests
