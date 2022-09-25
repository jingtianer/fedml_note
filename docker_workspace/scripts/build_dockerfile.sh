# docker image rm fedml:tt
cp ~/.local/lib/python3.10/site-packages/fedml/cross_silo/client/fedml_client_master_manager.py ../fedml_dockerfile_context/fedml_files/
cp ~/.local/lib/python3.10/site-packages/fedml/cross_silo/server/fedml_aggregator.py ../fedml_dockerfile_context/fedml_files/
cp ~/.local/lib/python3.10/site-packages/fedml/cross_silo/server/fedml_server_manager.py ../fedml_dockerfile_context/fedml_files/
cp ~/.local/lib/python3.10/site-packages/fedml/cross_silo/client/message_define.py ../fedml_dockerfile_context/fedml_files/
# cp ~/.local/lib/python3.10/site-packages/fedml/cross_silo/server/message_define.py ../fedml_dockerfile_context/fedml_files/
# 两个文件一样复制一份就好

cp -r ../yaml-requests/yamlRequests/* ../fedml_dockerfile_context/fedml_files/yamlRequests
docker build -t fedml:tt ../fedml_dockerfile_context