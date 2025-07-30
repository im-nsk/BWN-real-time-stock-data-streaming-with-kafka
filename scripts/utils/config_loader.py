import yaml
import os
from dotenv import load_dotenv

def load_config(config_path="configs/app_config.yaml"):

    # Load .env secrets first
    load_dotenv()

    # Load YAML config
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    
    # Inject secret into config from .env
    config["api"]["api_key"] = os.getenv("API_KEY")
    config["aws"]["access_key_id"] = os.getenv("AWS_ACCESS_KEY")
    config["aws"]["secret_access_key"] = os.getenv("AWS_SECRET_KEY")

    return config

load_config()