import yaml
import os

config_path = os.getenv("BAROMETER_CONFIG")
if config_path is None:
    config_path = "config.yml"
with open(config_path) as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)


def get_divisions():
    return config.get("divisions")


def get_url():
    return config.get("url")



