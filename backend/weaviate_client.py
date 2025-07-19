"""
Weaviate client connection and management functions
"""
import weaviate
from weaviate.classes.init import Auth
from typing import Optional, Dict, Any
import logging
from contextlib import contextmanager

from config import config

logger = logging.getLogger(__name__)


class WeaviateClient:
    """Weaviate client wrapper for cloud connections"""
    
    def __init__(self):
        self.client: Optional[weaviate.Client] = None
        self._is_connected = False
    
    def connect_to_cloud(self, 
                        cluster_url: Optional[str] = None,
                        api_key: Optional[str] = None,
                        headers: Optional[Dict[str, str]] = None) -> weaviate.Client:
        """
        Connect to Weaviate Cloud instance
        
        Args:
            cluster_url: Weaviate cloud cluster URL (defaults to config)
            api_key: Weaviate API key (defaults to config)
            headers: Additional headers (e.g., inference API keys)
            
        Returns:
            Connected Weaviate client
        """
        try:
            # Use provided values or fallback to config
            url = cluster_url or config.weaviate_url
            key = api_key or config.weaviate_api_key
            
            # Prepare headers with inference API keys
            default_headers = {}
            if config.openai_api_key:
                default_headers["X-OpenAI-Api-Key"] = config.openai_api_key
            if config.cohere_api_key:
                default_headers["X-Cohere-Api-Key"] = config.cohere_api_key
            if config.huggingface_api_key:
                default_headers["X-HuggingFace-Api-Key"] = config.huggingface_api_key
            
            # Merge with provided headers
            if headers:
                default_headers.update(headers)
            
            self.client = weaviate.connect_to_weaviate_cloud(
                cluster_url=url,
                auth_credentials=Auth.api_key(key),
                headers=default_headers if default_headers else None
            )
            
            self._is_connected = True
            logger.info(f"Successfully connected to Weaviate cloud: {url}")
            return self.client
            
        except Exception as e:
            logger.error(f"Failed to connect to Weaviate cloud: {str(e)}")
            raise ConnectionError(f"Weaviate connection failed: {str(e)}")
    
    def disconnect(self):
        """Close the Weaviate connection"""
        if self.client and self._is_connected:
            try:
                self.client.close()
                self._is_connected = False
                logger.info("Disconnected from Weaviate")
            except Exception as e:
                logger.error(f"Error disconnecting from Weaviate: {str(e)}")
    
    def is_connected(self) -> bool:
        """Check if client is connected"""
        return self._is_connected and self.client is not None
    
    def get_client(self) -> weaviate.Client:
        """Get the current client instance"""
        if not self.is_connected():
            raise ConnectionError("Not connected to Weaviate. Call connect_to_cloud() first.")
        return self.client
    
    def health_check(self) -> bool:
        """Check if Weaviate instance is healthy"""
        try:
            if not self.is_connected():
                return False
            # Try to list collections as a health check
            self.client.collections.list_all()
            return True
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False


# Global client instance
weaviate_client = WeaviateClient()


# Convenience functions
def get_weaviate_client() -> weaviate.Client:
    """Get connected Weaviate client"""
    if not weaviate_client.is_connected():
        weaviate_client.connect_to_cloud()
    return weaviate_client.get_client()


def connect_to_weaviate_cloud(cluster_url: Optional[str] = None,
                             api_key: Optional[str] = None,
                             headers: Optional[Dict[str, str]] = None) -> weaviate.Client:
    """
    Quick function to connect to Weaviate Cloud
    
    Args:
        cluster_url: Weaviate cloud cluster URL
        api_key: Weaviate API key  
        headers: Additional headers
        
    Returns:
        Connected Weaviate client
    """
    return weaviate_client.connect_to_cloud(cluster_url, api_key, headers)


@contextmanager
def weaviate_connection(cluster_url: Optional[str] = None,
                       api_key: Optional[str] = None,
                       headers: Optional[Dict[str, str]] = None):
    """
    Context manager for Weaviate connections
    
    Usage:
        with weaviate_connection() as client:
            # Use client here
            collections = client.collections.list_all()
    """
    temp_client = WeaviateClient()
    try:
        client = temp_client.connect_to_cloud(cluster_url, api_key, headers)
        yield client
    finally:
        temp_client.disconnect()


def disconnect_weaviate():
    """Disconnect from Weaviate cloud"""
    weaviate_client.disconnect() 