"""
View PDF content stored in Weaviate
"""
import os
import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.query import MetadataQuery
from dotenv import load_dotenv

load_dotenv()


def view_all_pdf_chunks(collection_name="Pdf_for_mira", limit=50):
    """View all PDF chunks stored in Weaviate"""
    
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
            print(f"📖 Viewing stored content from collection: {collection_name}")
            print("=" * 80)
            
            collection = client.collections.get(collection_name)
            
            # Fetch all objects (try different property names)
            try:
                response = collection.query.fetch_objects(
                    limit=limit,
                    return_properties=["title", "content"]  # Start with basic properties
                )
            except Exception as e:
                print(f"❌ Error fetching with specific properties: {e}")
                # Try with all properties
                response = collection.query.fetch_objects(
                    limit=limit,
                    return_properties=["*"]  # Get all available properties
                )
            
            if not response.objects:
                print("❌ No content found in the collection")
                return
            
            print(f"📊 Found {len(response.objects)} chunks")
            print(f"📁 Total stored chunks: {len(response.objects)}")
            
            # Sort by chunk_id for proper order
            sorted_objects = sorted(response.objects, key=lambda x: x.properties.get("chunk_id", 0))
            
            for i, obj in enumerate(sorted_objects, 1):
                props = obj.properties
                title = props.get("title", "N/A")
                content = props.get("content", "")
                chunk_id = props.get("chunk_id", "N/A")
                source_file = props.get("source_file", "N/A")
                word_count = props.get("word_count", 0)
                chunk_length = props.get("chunk_length", 0)
                
                print(f"\n📄 CHUNK {i} (ID: {chunk_id})")
                print(f"   Title: {title}")
                print(f"   Source: {source_file}")
                print(f"   Stats: {word_count} words, {chunk_length} characters")
                print(f"   Content:")
                print(f"   {'-' * 60}")
                print(f"   {content}")
                print(f"   {'-' * 60}")
                
                if i >= 10:  # Show first 10 chunks by default
                    show_more = input(f"\nShowing {i} of {len(sorted_objects)} chunks. Continue? (y/n): ").lower()
                    if show_more != 'y':
                        break
            
            print(f"\n✅ Displayed {min(i, len(sorted_objects))} chunks from {collection_name}")
            
        finally:
            client.close()
            
    except Exception as e:
        print(f"❌ Error viewing content: {e}")


def search_pdf_content(query, collection_name="Pdf_for_mira", limit=5):
    """Search for specific content in the stored PDF"""
    
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
            print(f"🔍 Searching for: '{query}' in {collection_name}")
            print("=" * 80)
            
            collection = client.collections.get(collection_name)
            
            response = collection.query.near_text(
                query=query,
                limit=limit,
                return_properties=["title", "content", "chunk_id", "source_file"],
                return_metadata=MetadataQuery(distance=True, score=True)
            )
            
            if not response.objects:
                print("❌ No matching content found")
                return
            
            print(f"📊 Found {len(response.objects)} relevant chunks")
            
            for i, obj in enumerate(response.objects, 1):
                props = obj.properties
                title = props.get("title", "N/A")
                content = props.get("content", "")
                chunk_id = props.get("chunk_id", "N/A")
                source_file = props.get("source_file", "N/A")
                
                score = obj.metadata.score if hasattr(obj.metadata, 'score') else 0
                distance = obj.metadata.distance if hasattr(obj.metadata, 'distance') else 0
                
                print(f"\n🎯 RESULT {i} (Chunk ID: {chunk_id})")
                print(f"   Title: {title}")
                print(f"   Source: {source_file}")
                print(f"   Score: {score:.3f}, Distance: {distance:.3f}")
                print(f"   Content:")
                print(f"   {'-' * 60}")
                print(f"   {content}")
                print(f"   {'-' * 60}")
            
        finally:
            client.close()
            
    except Exception as e:
        print(f"❌ Error searching content: {e}")


def get_pdf_summary(collection_name="Pdf_for_mira"):
    """Get a summary of the PDF content stored in Weaviate"""
    
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
            print(f"📈 Summary of collection: {collection_name}")
            print("=" * 60)
            
            collection = client.collections.get(collection_name)
            
            # Get basic stats - use flexible property fetching
            try:
                response = collection.query.fetch_objects(
                    limit=1000,  # Get all chunks for stats
                    return_properties=["*"]  # Get all available properties
                )
            except Exception as e:
                print(f"❌ Error fetching objects: {e}")
                return
            
            if not response.objects:
                print("❌ No content found")
                return
            
            total_chunks = len(response.objects)
            total_words = sum(obj.properties.get("word_count", 0) for obj in response.objects)
            total_chars = sum(obj.properties.get("chunk_length", 0) for obj in response.objects)
            
            # Get unique files
            files = set(obj.properties.get("source_file", "Unknown") for obj in response.objects)
            
            # Get upload date (should be same for all chunks)
            upload_date = response.objects[0].properties.get("upload_date", "Unknown")
            
            print(f"📊 Collection Statistics:")
            print(f"   • Total chunks: {total_chunks}")
            print(f"   • Total words: {total_words:,}")
            print(f"   • Total characters: {total_chars:,}")
            print(f"   • Source files: {', '.join(files)}")
            print(f"   • Upload date: {upload_date}")
            print(f"   • Average words per chunk: {total_words // total_chunks if total_chunks > 0 else 0}")
            print(f"   • Average chars per chunk: {total_chars // total_chunks if total_chunks > 0 else 0}")
            
        finally:
            client.close()
            
    except Exception as e:
        print(f"❌ Error getting summary: {e}")


if __name__ == "__main__":
    print("📖 WEAVIATE PDF CONTENT VIEWER")
    print("=" * 60)
    
    while True:
        print("\nChoose an option:")
        print("1. View all PDF chunks")
        print("2. Search PDF content")
        print("3. Get PDF summary")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            limit = input("How many chunks to show? (default 10): ").strip()
            limit = int(limit) if limit.isdigit() else 10
            view_all_pdf_chunks(limit=limit)
        
        elif choice == "2":
            query = input("Enter search query: ").strip()
            if query:
                limit = input("How many results? (default 5): ").strip()
                limit = int(limit) if limit.isdigit() else 5
                search_pdf_content(query, limit=limit)
        
        elif choice == "3":
            get_pdf_summary()
        
        elif choice == "4":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.") 