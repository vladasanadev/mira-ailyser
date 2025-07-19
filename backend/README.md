# Weaviate Backend

This backend provides functions to connect to and interact with Weaviate Cloud.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file from `.env.example` and fill in your credentials:
```bash
cp .env.example .env
```

3. Update the `.env` file with your Weaviate Cloud credentials.

## Quick Start

### Basic Connection

```python
from weaviate_client import connect_to_weaviate_cloud, disconnect_weaviate

# Connect to Weaviate Cloud
client = connect_to_weaviate_cloud()

# Use the client
collections = client.collections.list_all()

# Disconnect when done
disconnect_weaviate()
```

### Using Context Manager

```python
from weaviate_client import weaviate_connection

with weaviate_connection() as client:
    # Client is automatically connected and disconnected
    collections = client.collections.list_all()
```

### High-Level Operations

```python
from weaviate_operations import create_collection, semantic_search, insert_object

# Create a collection
create_collection(
    name="Articles",
    properties=[
        {"name": "title", "type": "text"},
        {"name": "content", "type": "text"},
        {"name": "category", "type": "text"}
    ]
)

# Insert data
insert_object(
    collection_name="Articles",
    properties={
        "title": "AI Revolution",
        "content": "Artificial intelligence is transforming...",
        "category": "Technology"
    }
)

# Search
results = semantic_search(
    collection_name="Articles",
    query="artificial intelligence",
    limit=5
)
```

## Available Functions

### Connection Functions (`weaviate_client.py`)
- `connect_to_weaviate_cloud()` - Connect to Weaviate Cloud
- `get_weaviate_client()` - Get connected client
- `disconnect_weaviate()` - Disconnect from Weaviate
- `weaviate_connection()` - Context manager for connections

### Operations (`weaviate_operations.py`)
- `create_collection()` - Create new collection
- `collection_exists()` - Check if collection exists
- `list_collections()` - List all collections
- `insert_object()` - Insert single object
- `batch_insert()` - Batch insert multiple objects
- `semantic_search()` - Vector-based search
- `keyword_search()` - BM25 keyword search
- `hybrid_search()` - Combined semantic + keyword
- `generative_search()` - RAG with generation

## Environment Variables

Required:
- `WEAVIATE_URL` - Your Weaviate Cloud cluster URL
- `WEAVIATE_API_KEY` - Your Weaviate API key

Optional:
- `OPENAI_API_KEY` - For OpenAI vectorizers/generators
- `COHERE_API_KEY` - For Cohere vectorizers/generators
- `HUGGINGFACE_API_KEY` - For Hugging Face vectorizers

## Error Handling

All functions include comprehensive error handling and logging. Check logs for detailed error information.

## Examples

See `weaviate.txt` for comprehensive examples and advanced usage patterns. 