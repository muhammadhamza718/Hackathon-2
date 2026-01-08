"""
Dapr client integration for the Todo Backend
"""
from typing import Any, Dict, Optional
import dapr
from dapr.clients import DaprClient as DaprGrpcClient
from dapr.ext.grpc import AppCallback, DaprApp
from contextlib import contextmanager
from fastapi import Depends
import asyncio
import logging

logger = logging.getLogger(__name__)


class DaprClient:
    """
    Wrapper class for Dapr client to handle state management and pub/sub
    """

    def __init__(self):
        self.client = None

    def __enter__(self):
        self.client = DaprGrpcClient()
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()

    async def get_state(self, store_name: str, key: str) -> Any:
        """
        Get state from Dapr state store
        """
        with DaprGrpcClient() as client:
            response = client.get_state(store_name, key)
            return response.data

    async def save_state(self, store_name: str, key: str, value: Any) -> None:
        """
        Save state to Dapr state store
        """
        with DaprGrpcClient() as client:
            client.save_state(store_name, key, value)

    async def publish_event(self, pubsub_name: str, topic_name: str, data: Any) -> None:
        """
        Publish an event to Dapr pub/sub
        """
        with DaprGrpcClient() as client:
            client.publish_event(pubsub_name, topic_name, data)

    async def get_secret(self, store_name: str, key: str) -> Dict[str, str]:
        """
        Get secret from Dapr secret store
        """
        with DaprGrpcClient() as client:
            response = client.get_secret(store_name, key)
            return response.data


# Global instance
_dapr_client = DaprClient()


def get_dapr_client() -> DaprClient:
    """
    Get the Dapr client instance
    """
    return _dapr_client