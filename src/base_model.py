from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    Input,
    Embedding,
    Dot,
    Flatten,
    Dense,
    Activation,
    BatchNormalization,
)

from src.logger import get_logger
from src.custom_exception import CustomException
from utils.common import read_yaml

logger = get_logger(__name__)


class BaseModel:
    def __init__(self, config_path):
        try:
            self.config = read_yaml(config_path)
            logger.info("Loaded configuration from config.yaml")
        except Exception as e:
            raise CustomException("Error loading configuration", e)

    def RecommenderNet(self, n_users, n_anime):
        try:
            embedding_size = self.config["model"]["embedding_size"]

            # User embedding layer
            user = Input(name="user", shape=[1])
            user_embedding = Embedding(
                name="user_embedding", input_dim=n_users, output_dim=embedding_size
            )(user)

            # Anime embedding layer
            anime = Input(name="anime", shape=[1])
            anime_embedding = Embedding(
                name="anime_embedding", input_dim=n_anime, output_dim=embedding_size
            )(anime)

            # Dot product of user and anime embeddings to get the normalized (better) similarity score between them
            x = Dot(name="dot_product", normalize=True, axes=2)(
                [user_embedding, anime_embedding]
            )

            # Flatten the output
            x = Flatten()(x)

            # Dense layer
            x = Dense(1, kernel_initializer="he_normal")(x)

            # Batch normalization
            x = BatchNormalization()(x)

            # Activation function
            x = Activation("sigmoid")(x)

            # The input was separated into user and anime for this purpose
            model = Model(inputs=[user, anime], outputs=x)

            # Compile the model
            model.compile(
                loss=self.config["model"]["loss"],
                optimizer=self.config["model"]["optimizer"],
                metrics=self.config["model"]["metrics"],
            )

            logger.info("Model created successfully")
            return model
        except Exception as e:
            logger.error(f"Error occurred during model architecture {e}")
            raise CustomException("Failed to create model", e)
