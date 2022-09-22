# docker image rm fedml:tt
cp ~/.local/lib/python3.10/site-packages/fedml/cross_silo/client/fedml_client_master_manager.py ../fedml_dockerfile_context/fedml_files/
cp ~/.local/lib/python3.10/site-packages/fedml/cross_silo/server/fedml_aggregator.py ../fedml_dockerfile_context/fedml_files/
cp ~/.local/lib/python3.10/site-packages/fedml/cross_silo/server/fedml_server_manager.py ../fedml_dockerfile_context/fedml_files/
docker build -t fedml:tt ../fedml_dockerfile_context