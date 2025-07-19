"""
Common Weaviate operations and utilities
"""
import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.query import Filter, MetadataQuery, HybridFusion
from weaviate.classes.data import DataObject
from typing import List, Dict, Any, Optional, Union
import logging

from weaviate_client import get_weaviate_client

logger = logging.getLogger(__name__)


class WeaviateOperations:
    """High-level operations for Weaviate"""
    
    def __init__(self):
        self.client = None
    
    def _get_client(self) -> weaviate.Client:
        """Get or initialize Weaviate client"""
        if self.client is None:
            self.client = get_weaviate_client()
        return self.client
    
    # Collection Management
    def create_collection(self, 
                         name: str,
                         properties: List[Dict[str, Any]],
                         vectorizer: str = "text2vec-openai",
                         generative_model: str = "gpt-3.5-turbo") -> bool:
        """
        Create a new collection with properties
        
        Args:
            name: Collection name
            properties: List of property definitions [{"name": str, "type": str}]
            vectorizer: Vectorizer to use
            generative_model: Generative model for RAG
            
        Returns:
            Success status
        """
        try:
            client = self._get_client()
            
            # Convert property definitions
            weaviate_properties = []
            for prop in properties:
                data_type = getattr(DataType, prop["type"].upper(), DataType.TEXT)
                weaviate_properties.append(
                    Property(name=prop["name"], data_type=data_type)
                )
            
            # Configure vectorizer
            vector_config = None
            if vectorizer == "text2vec-openai":
                vector_config = Configure.Vectors.text2vec_openai()
            elif vectorizer == "text2vec-cohere":
                vector_config = Configure.Vectors.text2vec_cohere()
            
            # Configure generative model
            generative_config = None
            if generative_model.startswith("gpt"):
                generative_config = Configure.Generative.openai(model=generative_model)
            elif generative_model.startswith("command"):
                generative_config = Configure.Generative.cohere(model=generative_model)
            
            client.collections.create(
                name=name,
                properties=weaviate_properties,
                vector_config=vector_config,
                generative_config=generative_config
            )
            
            logger.info(f"Created collection: {name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create collection {name}: {str(e)}")
            return False
    
    def collection_exists(self, name: str) -> bool:
        """Check if collection exists"""
        try:
            client = self._get_client()
            return client.collections.exists(name)
        except Exception as e:
            logger.error(f"Error checking collection existence: {str(e)}")
            return False
    
    def list_collections(self) -> List[str]:
        """List all collection names"""
        try:
            client = self._get_client()
            collections = client.collections.list_all()
            return [collection.name for collection in collections]
        except Exception as e:
            logger.error(f"Error listing collections: {str(e)}")
            return []
    
    def delete_collection(self, name: str) -> bool:
        """Delete a collection"""
        try:
            client = self._get_client()
            client.collections.delete(name)
            logger.info(f"Deleted collection: {name}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete collection {name}: {str(e)}")
            return False
    
    # Data Operations
    def insert_object(self, 
                     collection_name: str,
                     properties: Dict[str, Any],
                     vector: Optional[List[float]] = None,
                     uuid: Optional[str] = None) -> Optional[str]:
        """
        Insert a single object into collection
        
        Args:
            collection_name: Target collection
            properties: Object properties
            vector: Optional custom vector
            uuid: Optional specific UUID
            
        Returns:
            Object UUID if successful
        """
        try:
            client = self._get_client()
            collection = client.collections.get(collection_name)
            
            kwargs = {"properties": properties}
            if vector:
                kwargs["vector"] = vector
            if uuid:
                kwargs["uuid"] = uuid
            
            object_uuid = collection.data.insert(**kwargs)
            logger.info(f"Inserted object into {collection_name}: {object_uuid}")
            return str(object_uuid)
            
        except Exception as e:
            logger.error(f"Failed to insert object into {collection_name}: {str(e)}")
            return None
    
    def batch_insert(self,
                    collection_name: str,
                    objects: List[Dict[str, Any]],
                    batch_size: int = 100) -> Dict[str, Any]:
        """
        Batch insert objects
        
        Args:
            collection_name: Target collection
            objects: List of objects with 'properties' and optional 'vector'
            batch_size: Batch size for insertion
            
        Returns:
            Results summary
        """
        try:
            client = self._get_client()
            collection = client.collections.get(collection_name)
            
            inserted_count = 0
            failed_count = 0
            
            with collection.batch.fixed_size(batch_size=batch_size) as batch:
                for obj in objects:
                    batch.add_object(
                        properties=obj["properties"],
                        vector=obj.get("vector")
                    )
            
            # Check for failed objects after batch completes
            failed_objects = collection.batch.failed_objects
            failed_count = len(failed_objects) if failed_objects else 0
            inserted_count = len(objects) - failed_count
            
            logger.info(f"Batch insert to {collection_name}: {inserted_count} success, {failed_count} failed")
            return {
                "inserted": inserted_count,
                "failed": failed_count,
                "total": len(objects)
            }
            
        except Exception as e:
            logger.error(f"Batch insert failed for {collection_name}: {str(e)}")
            return {"inserted": 0, "failed": len(objects), "total": len(objects)}
    
    def get_object_by_id(self, collection_name: str, object_id: str, include_vector: bool = False) -> Optional[Dict[str, Any]]:
        """Get object by UUID"""
        try:
            client = self._get_client()
            collection = client.collections.get(collection_name)
            obj = collection.query.fetch_object_by_id(object_id, include_vector=include_vector)
            
            result = {"properties": obj.properties}
            if include_vector and hasattr(obj, 'vector'):
                result["vector"] = obj.vector
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to get object {object_id} from {collection_name}: {str(e)}")
            return None
    
    # Search Operations
    def semantic_search(self,
                       collection_name: str,
                       query: str,
                       limit: int = 10,
                       properties: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Perform semantic search using near_text
        
        Args:
            collection_name: Collection to search
            query: Search query
            limit: Number of results
            properties: Properties to return
            
        Returns:
            List of search results
        """
        try:
            client = self._get_client()
            collection = client.collections.get(collection_name)
            
            response = collection.query.near_text(
                query=query,
                limit=limit,
                return_properties=properties,
                return_metadata=MetadataQuery(distance=True, score=True)
            )
            
            results = []
            for obj in response.objects:
                result = {
                    "uuid": str(obj.uuid),
                    "properties": obj.properties,
                    "metadata": {
                        "distance": obj.metadata.distance,
                        "score": obj.metadata.score
                    }
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Semantic search failed for {collection_name}: {str(e)}")
            return []
    
    def keyword_search(self,
                      collection_name: str,
                      query: str,
                      limit: int = 10,
                      properties: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Perform keyword search using BM25
        
        Args:
            collection_name: Collection to search  
            query: Search query
            limit: Number of results
            properties: Properties to search in and return
            
        Returns:
            List of search results
        """
        try:
            client = self._get_client()
            collection = client.collections.get(collection_name)
            
            response = collection.query.bm25(
                query=query,
                query_properties=properties,
                limit=limit,
                return_properties=properties,
                return_metadata=MetadataQuery(score=True)
            )
            
            results = []
            for obj in response.objects:
                result = {
                    "uuid": str(obj.uuid),
                    "properties": obj.properties,
                    "metadata": {
                        "score": obj.metadata.score
                    }
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Keyword search failed for {collection_name}: {str(e)}")
            return []
    
    def hybrid_search(self,
                     collection_name: str,
                     query: str,
                     alpha: float = 0.5,
                     limit: int = 10,
                     properties: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Perform hybrid search (semantic + keyword)
        
        Args:
            collection_name: Collection to search
            query: Search query
            alpha: Balance between semantic (0.0) and keyword (1.0)
            limit: Number of results
            properties: Properties to return
            
        Returns:
            List of search results
        """
        try:
            client = self._get_client()
            collection = client.collections.get(collection_name)
            
            response = collection.query.hybrid(
                query=query,
                alpha=alpha,
                fusion_type=HybridFusion.RELATIVE_SCORE,
                limit=limit,
                return_properties=properties,
                return_metadata=MetadataQuery(score=True)
            )
            
            results = []
            for obj in response.objects:
                result = {
                    "uuid": str(obj.uuid),
                    "properties": obj.properties,
                    "metadata": {
                        "score": obj.metadata.score
                    }
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Hybrid search failed for {collection_name}: {str(e)}")
            return []
    
    # Generative Search (RAG)
    def generative_search(self,
                         collection_name: str,
                         query: str,
                         prompt: str,
                         limit: int = 5) -> Dict[str, Any]:
        """
        Perform generative search (RAG)
        
        Args:
            collection_name: Collection to search
            query: Search query
            prompt: Generation prompt template
            limit: Number of source objects
            
        Returns:
            Generated response with sources
        """
        try:
            client = self._get_client()
            collection = client.collections.get(collection_name)
            
            response = collection.generate.near_text(
                query=query,
                single_prompt=prompt,
                limit=limit
            )
            
            result = {
                "generated_text": response.generated if hasattr(response, 'generated') else None,
                "sources": []
            }
            
            for obj in response.objects:
                source = {
                    "uuid": str(obj.uuid),
                    "properties": obj.properties,
                    "generated": obj.generated.text if hasattr(obj, 'generated') and hasattr(obj.generated, 'text') else None
                }
                result["sources"].append(source)
            
            return result
            
        except Exception as e:
            logger.error(f"Generative search failed for {collection_name}: {str(e)}")
            return {"generated_text": None, "sources": []}


# Global operations instance
weaviate_ops = WeaviateOperations()


# Convenience functions
def create_collection(name: str, properties: List[Dict[str, Any]], **kwargs) -> bool:
    """Create a collection"""
    return weaviate_ops.create_collection(name, properties, **kwargs)


def semantic_search(collection_name: str, query: str, **kwargs) -> List[Dict[str, Any]]:
    """Perform semantic search"""
    return weaviate_ops.semantic_search(collection_name, query, **kwargs)


def insert_object(collection_name: str, properties: Dict[str, Any], **kwargs) -> Optional[str]:
    """Insert an object"""
    return weaviate_ops.insert_object(collection_name, properties, **kwargs) 