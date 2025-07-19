"""
Example usage of Weaviate backend functions
"""
import os
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)

# Import our modules
from weaviate_client import (
    connect_to_weaviate_cloud, 
    weaviate_connection,
    disconnect_weaviate
)
from weaviate_operations import (
    create_collection,
    semantic_search,
    insert_object,
    batch_insert,
    hybrid_search,
    generative_search
)

def example_basic_connection():
    """Example: Basic connection to Weaviate Cloud"""
    print("\n=== Basic Connection Example ===")
    
    try:
        # Connect to Weaviate Cloud
        client = connect_to_weaviate_cloud()
        print("✓ Connected to Weaviate Cloud")
        
        # List existing collections
        collections = client.collections.list_all()
        print(f"✓ Found {len(collections)} collections")
        
        # Disconnect
        disconnect_weaviate()
        print("✓ Disconnected from Weaviate")
        
    except Exception as e:
        print(f"✗ Connection failed: {e}")


def example_context_manager():
    """Example: Using context manager for automatic connection handling"""
    print("\n=== Context Manager Example ===")
    
    try:
        with weaviate_connection() as client:
            print("✓ Connected using context manager")
            collections = client.collections.list_all()
            print(f"✓ Found {len(collections)} collections")
        print("✓ Connection automatically closed")
        
    except Exception as e:
        print(f"✗ Context manager failed: {e}")


def example_collection_management():
    """Example: Creating and managing collections"""
    print("\n=== Collection Management Example ===")
    
    collection_name = "ExampleArticles"
    
    try:
        # Create a collection
        success = create_collection(
            name=collection_name,
            properties=[
                {"name": "title", "type": "text"},
                {"name": "content", "type": "text"},
                {"name": "category", "type": "text"},
                {"name": "published_date", "type": "date"},
                {"name": "word_count", "type": "int"}
            ],
            vectorizer="text2vec-openai",
            generative_model="gpt-3.5-turbo"
        )
        
        if success:
            print(f"✓ Created collection: {collection_name}")
        else:
            print(f"✗ Failed to create collection: {collection_name}")
            
    except Exception as e:
        print(f"✗ Collection management failed: {e}")


def example_data_insertion():
    """Example: Inserting data into collections"""
    print("\n=== Data Insertion Example ===")
    
    collection_name = "ExampleArticles"
    
    # Single object insertion
    try:
        article_id = insert_object(
            collection_name=collection_name,
            properties={
                "title": "Introduction to Vector Databases",
                "content": "Vector databases are specialized databases designed to store and query high-dimensional vectors...",
                "category": "Technology",
                "published_date": "2024-01-15T00:00:00Z",
                "word_count": 1250
            }
        )
        
        if article_id:
            print(f"✓ Inserted single article: {article_id}")
        else:
            print("✗ Failed to insert article")
            
    except Exception as e:
        print(f"✗ Single insertion failed: {e}")
    
    # Batch insertion
    try:
        articles = [
            {
                "properties": {
                    "title": "Machine Learning Fundamentals",
                    "content": "Machine learning is a subset of artificial intelligence that focuses on algorithms...",
                    "category": "AI/ML",
                    "published_date": "2024-01-16T00:00:00Z",
                    "word_count": 2000
                }
            },
            {
                "properties": {
                    "title": "Cloud Computing Trends",
                    "content": "Cloud computing has revolutionized how businesses deploy and scale applications...",
                    "category": "Cloud",
                    "published_date": "2024-01-17T00:00:00Z",
                    "word_count": 1800
                }
            },
            {
                "properties": {
                    "title": "Cybersecurity Best Practices",
                    "content": "In today's digital landscape, cybersecurity is more important than ever...",
                    "category": "Security",
                    "published_date": "2024-01-18T00:00:00Z",
                    "word_count": 1500
                }
            }
        ]
        
        results = batch_insert(
            collection_name=collection_name,
            objects=articles,
            batch_size=10
        )
        
        print(f"✓ Batch insertion: {results['inserted']} success, {results['failed']} failed")
        
    except Exception as e:
        print(f"✗ Batch insertion failed: {e}")


def example_search_operations():
    """Example: Different types of search operations"""
    print("\n=== Search Operations Example ===")
    
    collection_name = "ExampleArticles"
    query = "artificial intelligence machine learning"
    
    # Semantic search
    try:
        results = semantic_search(
            collection_name=collection_name,
            query=query,
            limit=3,
            properties=["title", "category"]
        )
        
        print(f"✓ Semantic search found {len(results)} results:")
        for i, result in enumerate(results[:2], 1):
            title = result["properties"].get("title", "N/A")
            score = result["metadata"].get("score", 0)
            print(f"  {i}. {title} (score: {score:.3f})")
            
    except Exception as e:
        print(f"✗ Semantic search failed: {e}")
    
    # Hybrid search
    try:
        results = hybrid_search(
            collection_name=collection_name,
            query=query,
            alpha=0.5,  # Balance between semantic and keyword
            limit=3,
            properties=["title", "category"]
        )
        
        print(f"✓ Hybrid search found {len(results)} results:")
        for i, result in enumerate(results[:2], 1):
            title = result["properties"].get("title", "N/A")
            score = result["metadata"].get("score", 0)
            print(f"  {i}. {title} (score: {score:.3f})")
            
    except Exception as e:
        print(f"✗ Hybrid search failed: {e}")


def example_generative_search():
    """Example: Generative search (RAG)"""
    print("\n=== Generative Search (RAG) Example ===")
    
    collection_name = "ExampleArticles"
    
    try:
        results = generative_search(
            collection_name=collection_name,
            query="machine learning applications",
            prompt="Based on this article, explain the key concepts in simple terms: {title} - {content}",
            limit=2
        )
        
        if results["generated_text"]:
            print(f"✓ Generated response: {results['generated_text'][:200]}...")
        
        print(f"✓ Used {len(results['sources'])} source articles")
        
    except Exception as e:
        print(f"✗ Generative search failed: {e}")


def main():
    """Run all examples"""
    print("Weaviate Backend Examples")
    print("=" * 50)
    
    # Check environment variables
    required_env_vars = ["WEAVIATE_URL", "WEAVIATE_API_KEY"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("Please set them in a .env file or your environment")
        print("\nExample .env file:")
        print("WEAVIATE_URL=https://your-cluster-id.weaviate.network")
        print("WEAVIATE_API_KEY=your-weaviate-api-key")
        print("OPENAI_API_KEY=your-openai-api-key  # Optional")
        return
    
    # Run examples
    example_basic_connection()
    example_context_manager()
    example_collection_management()
    example_data_insertion()
    example_search_operations()
    example_generative_search()
    
    print("\n" + "=" * 50)
    print("Examples completed!")


if __name__ == "__main__":
    main() 