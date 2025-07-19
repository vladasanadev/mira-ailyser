"""
Check Weaviate Collection Schema
"""
import os
import weaviate
from weaviate.classes.init import Auth
from dotenv import load_dotenv
import json

load_dotenv()


def check_collection_schema(collection_name="Pdf_for_mira"):
    """Check the schema of a Weaviate collection"""
    
    try:
        # Connect to Weaviate
        weaviate_url = os.environ["WEAVIATE_URL"]
        weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
        openai_key = os.environ.get("OPENAI_APIKEY") or os.environ.get("OPEN_AI_API")
        
        headers = {"X-OpenAI-Api-Key": openai_key}
        
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=weaviate_url,
            auth_credentials=Auth.api_key(weaviate_api_key),
            headers=headers
        )
        
        try:
            print(f"🔍 Checking schema for collection: {collection_name}")
            print("=" * 60)
            
            # Check if collection exists
            if not client.collections.exists(collection_name):
                print(f"❌ Collection '{collection_name}' does not exist!")
                return
            
            print(f"✅ Collection '{collection_name}' exists")
            
            # Get collection
            collection = client.collections.get(collection_name)
            
            # Get collection config/schema
            config = collection.config.get()
            
            print(f"\n📊 Collection Information:")
            print(f"   • Name: {config.name}")
            print(f"   • Description: {config.description or 'None'}")
            
            # Show properties
            print(f"\n📋 Properties:")
            if config.properties:
                for i, prop in enumerate(config.properties, 1):
                    print(f"   {i}. {prop.name}")
                    print(f"      • Type: {prop.data_type}")
                    print(f"      • Description: {prop.description or 'None'}")
                    print(f"      • Indexed: {getattr(prop, 'index_filterable', 'N/A')}")
                    print()
            else:
                print("   No properties found")
            
            # Show vector config
            print(f"📐 Vector Configuration:")
            if config.vector_config:
                if isinstance(config.vector_config, list):
                    for i, vec_config in enumerate(config.vector_config, 1):
                        print(f"   {i}. Name: {vec_config.name}")
                        print(f"      • Vectorizer: {vec_config.vectorizer}")
                else:
                    print(f"   • Vectorizer: {config.vector_config.vectorizer}")
            else:
                print("   No vector configuration found")
            
            # Test a sample query to see what properties are actually available
            print(f"\n🧪 Testing Sample Query:")
            try:
                response = collection.query.fetch_objects(
                    limit=1,
                    return_properties=["*"]  # Return all available properties
                )
                
                if response.objects:
                    sample_obj = response.objects[0]
                    print(f"✅ Found sample object with UUID: {sample_obj.uuid}")
                    print(f"📝 Available properties in actual data:")
                    
                    for key, value in sample_obj.properties.items():
                        print(f"   • {key}: {type(value).__name__} = {str(value)[:100]}{'...' if len(str(value)) > 100 else ''}")
                else:
                    print("❌ No objects found in collection")
                    
            except Exception as e:
                print(f"⚠️ Sample query failed: {e}")
            
        finally:
            client.close()
            
    except Exception as e:
        print(f"❌ Error checking schema: {e}")


def list_all_collections():
    """List all collections in Weaviate"""
    
    try:
        # Connect to Weaviate
        weaviate_url = os.environ["WEAVIATE_URL"]
        weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
        openai_key = os.environ.get("OPENAI_APIKEY") or os.environ.get("OPEN_AI_API")
        
        headers = {"X-OpenAI-Api-Key": openai_key}
        
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=weaviate_url,
            auth_credentials=Auth.api_key(weaviate_api_key),
            headers=headers
        )
        
        try:
            print("📚 All Collections in Weaviate:")
            print("=" * 40)
            
            collections = client.collections.list_all()
            
            if not collections:
                print("❌ No collections found")
                return
            
            for i, collection in enumerate(collections, 1):
                print(f"{i}. {collection.name}")
                # Try to get object count
                try:
                    coll = client.collections.get(collection.name)
                    response = coll.query.fetch_objects(limit=1)
                    count = "Has data" if response.objects else "Empty"
                    print(f"   Status: {count}")
                except:
                    print(f"   Status: Unknown")
            
        finally:
            client.close()
            
    except Exception as e:
        print(f"❌ Error listing collections: {e}")


if __name__ == "__main__":
    print("🔍 WEAVIATE SCHEMA CHECKER")
    print("=" * 60)
    
    while True:
        print("\nChoose an option:")
        print("1. Check specific collection schema")
        print("2. List all collections")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            collection_name = input("Enter collection name (default: Pdf_for_mira): ").strip()
            if not collection_name:
                collection_name = "Pdf_for_mira"
            check_collection_schema(collection_name)
        
        elif choice == "2":
            list_all_collections()
        
        elif choice == "3":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.") 