import os

import yaml

from src.custom_exception import CustomException
from src.logger import get_logger

logger = get_logger(__name__)


def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found in the given path: {file_path}")

        with open(file_path, "r") as yaml_file:
            config = yaml.safe_load(yaml_file)
            logger.info(f"Succesfully read the YAML file: {file_path}")
            return config

    except Exception as e:
        logger.error(f"Error while reading YAML file: {file_path}")
        raise CustomException("Failed to read YAMl file", e)
