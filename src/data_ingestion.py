import os

from google.cloud import storage
import pandas as pd

from src.custom_exception import CustomException
from src.logger import get_logger
from config.paths_config import *
from utils.common import read_yaml


logger = get_logger(__name__)


class DataIngestion:
    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_names = self.config["bucket_file_names"]

        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info(
            f"Data Ingestion started with bucket: {self.bucket_name} and files: {self.file_names}"
        )

    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)

            for file_name in self.file_names:
                file_path = os.path.join(RAW_DIR, file_name)

                if file_name == "animelist.csv":
                    blob = bucket.blob(file_name)
                    with blob.open("r", encoding="utf-8") as gcs_file:
                        data = pd.read_csv(gcs_file, nrows=5_000_000)

                    data.to_csv(file_path, index=False)
                    logger.info("Large file detected downloading 5M rows")
                else:
                    blob = bucket.blob(file_name)
                    blob.download_to_filename(file_path)

                    logger.info(
                        "Downloading smaller files: anime and anime_with_synopsis"
                    )

                logger.info(f"CSV file successfully downloaded to {file_path}")

        except Exception as e:
            logger.error("Error while downloading data from GCP bucket")
            raise CustomException("Failed to download data", e)

    def run(self):
        try:
            logger.info("Starting data ingestion process....")
            self.download_csv_from_gcp()
            logger.info("Data ingestion process completed...")
        except CustomException as ce:
            logger.error(f"CustomException : {str(ce)}")
        finally:
            logger.info("Data ingestion done...")


if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()
