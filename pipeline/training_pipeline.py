from src.data_processor import DataProcessor
from src.model_trainer import ModelTrainer
from config.paths_config import *

'''
Data ingestion will be handled by DVC
DVC stores data in MD5 format (Hashed version for efficient data tracking and control) allowing:
- Faster comparison and tracking of data changes
- No duplications allowed
- Data integrity (as hash would change if data changes)
'''
if __name__ == "__main__":
    data_processor = DataProcessor(ANIMELIST_CSV, PROCESSED_DIR)
    data_processor.run()

    model_trainer = ModelTrainer(PROCESSED_DIR)
    model_trainer.train()
