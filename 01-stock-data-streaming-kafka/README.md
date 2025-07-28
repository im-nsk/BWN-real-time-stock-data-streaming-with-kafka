use .env for credential and .gitignore to avoid commiting to git. 

app_config.yaml to store paramater and to avoid hardcode in the script. 

in utility folder, there is config_loader.py file that help to load .env credential and parameter so we can use in the script
- there is library load_dotenv that helps to load the credential from .env and yaml.safe_load() that helps to load parameter from the app_config file.


Run ZooKeeper:
.\bin\windows\zookeeper-server-start.bat .config\zookeeper.properties

Run Server:
.\bin\windows\kafka-server-start.bat .\config\server.properties

C:\major-project\kafka\bin


....continue