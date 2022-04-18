import os
from typing import Type
from dotenv import load_dotenv

load_dotenv()


def get_config() -> Type["Config"]:
    config_obj = DevConfig
    if os.getenv("PROD").lower() == "true":
        config_obj = ProdConfig

    return config_obj


class Config:
    pass


class ProdConfig(Config):
    DEBUG = False
    MONGODB_SETTINGS = {"host": os.getenv("PROD_MONGO_URI")}


class DevConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {"host": os.getenv("DEV_MONGO_URI")}
