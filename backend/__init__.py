"""
Weaviate Backend Package

This package provides functions to connect to and interact with Weaviate Cloud.
"""

from .weaviate_client import (
    connect_to_weaviate_cloud,
    get_weaviate_client,
    weaviate_connection,
    disconnect_weaviate,
    WeaviateClient
)

from .weaviate_operations import (
    create_collection,
    semantic_search,
    keyword_search,
    hybrid_search,
    generative_search,
    insert_object,
    batch_insert,
    WeaviateOperations
)

from .config import config, WeaviateConfig

__version__ = "1.0.0"
__author__ = "Your Name"

__all__ = [
    # Client functions
    "connect_to_weaviate_cloud",
    "get_weaviate_client", 
    "weaviate_connection",
    "disconnect_weaviate",
    "WeaviateClient",
    
    # Operation functions
    "create_collection",
    "semantic_search",
    "keyword_search", 
    "hybrid_search",
    "generative_search",
    "insert_object",
    "batch_insert",
    "WeaviateOperations",
    
    # Configuration
    "config",
    "WeaviateConfig"
] 