from ingestion_modules.custom_vectorstore.base_method_vectorstore import BaseMethodVectorStore
from config import db_params
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from enum import Enum
from typing import Literal
import qdrant_client

# Define params
# Qdrant service
_QDRANT_TOKEN = db_params.QDRANT_TOKEN
_QDRANT_URL = db_params.QDRANT_URL
_QDRANT_PORT = db_params.QDRANT_PORT
_QDRANT_COLLECTION = db_params.QDRANT_COLLECTION


class QdrantService(BaseMethodVectorStore,QdrantClient):
    def __init__(self,mode : Literal["memory","local","cloud"] = "local",collection_name : str = _QDRANT_COLLECTION, qdrant_token : str = _QDRANT_TOKEN , qdrant_url : str = _QDRANT_URL):
        super().__init__()
        # Init params
        self.qdrant_token = qdrant_token
        self.qdrant_url = qdrant_url
        self.collection_name = collection_name
        self._mode = mode

        # Check type
        assert isinstance(collection_name, str), "Collection name must be a string"
        assert isinstance(qdrant_token, str), "Cloud id must be a string"
        assert isinstance(qdrant_url, str), "API Key must be a string"

        # Init client
        # self._client = None
        # Memory mode
        if self._mode == "memory":
            self._client = qdrant_client.QdrantClient(
                location=":memory:"
            )
        # Local host mode
        elif self._mode == "local":
            self._client = qdrant_client.QdrantClient(
                host="localhost",
                port=_QDRANT_PORT
            )
        elif self._mode == "cloud":
            self._client = qdrant_client.QdrantClient(
                url=self.qdrant_url,
                api_key=self.qdrant_token
            )
        else:
            raise Exception("Wrong qdrant mode")
        # Set vector store
        self.set_vector_store()

    def set_vector_store(self):
        # Define vector store
        self._vector_store = QdrantVectorStore(client=self._client, collection_name=self.collection_name)
        # Print
        print(f"Start Qdrant Vectorstore!")