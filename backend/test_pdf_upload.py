"""
Test function to upload PDF content to Weaviate
"""
import os
import logging
from typing import List, Dict, Any
from pathlib import Path
import PyPDF2
from datetime import datetime

# Import our Weaviate functions
from weaviate_client import weaviate_connection
from weaviate_operations import (
    create_collection,
    insert_object,
    batch_insert,
    semantic_search,
    collection_exists
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_pdf_text(pdf_path: str) -> str:
    """
    Extract text content from PDF file
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text content
    """
    try:
        text_content = ""
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text.strip():
                        text_content += f"\n--- Page {page_num + 1} ---\n"
                        text_content += page_text
                except Exception as e:
                    logger.warning(f"Could not extract text from page {page_num + 1}: {e}")
        
        return text_content.strip()
        
    except Exception as e:
        logger.error(f"Failed to extract text from PDF: {e}")
        raise


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, Any]]:
    """
    Split text into overlapping chunks
    
    Args:
        text: Text to chunk
        chunk_size: Maximum characters per chunk
        overlap: Characters to overlap between chunks
        
    Returns:
        List of text chunks with metadata
    """
    chunks = []
    words = text.split()
    
    if not words:
        return chunks
    
    current_chunk = []
    current_length = 0
    chunk_id = 0
    
    for word in words:
        word_length = len(word) + 1  # +1 for space
        
        if current_length + word_length > chunk_size and current_chunk:
            # Create chunk
            chunk_text = ' '.join(current_chunk)
            chunks.append({
                "chunk_id": chunk_id,
                "text": chunk_text,
                "length": len(chunk_text),
                "word_count": len(current_chunk)
            })
            
            # Start new chunk with overlap
            overlap_words = current_chunk[-overlap//10:] if overlap > 0 else []
            current_chunk = overlap_words + [word]
            current_length = sum(len(w) + 1 for w in current_chunk)
            chunk_id += 1
        else:
            current_chunk.append(word)
            current_length += word_length
    
    # Add final chunk
    if current_chunk:
        chunk_text = ' '.join(current_chunk)
        chunks.append({
            "chunk_id": chunk_id,
            "text": chunk_text,
            "length": len(chunk_text),
            "word_count": len(current_chunk)
        })
    
    return chunks


def test_pdf_upload(pdf_path: str = "/Users/vladyslavaka/Documents/mira-ailyser/backend/cv-front-end.pdf"):
    """
    Test function to upload PDF content to Weaviate
    
    Args:
        pdf_path: Path to the PDF file to upload
    """
    collection_name = "Documents"
    
    print("🚀 Starting PDF upload test...")
    print(f"📁 PDF Path: {pdf_path}")
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return False
    
    try:
        # Step 1: Extract text from PDF
        print("\n📄 Extracting text from PDF...")
        pdf_text = extract_pdf_text(pdf_path)
        
        if not pdf_text:
            print("❌ No text extracted from PDF")
            return False
        
        print(f"✅ Extracted {len(pdf_text)} characters from PDF")
        print(f"Preview: {pdf_text[:200]}...")
        
        # Step 2: Create collection if it doesn't exist
        print(f"\n🗄️ Setting up collection: {collection_name}")
        
        if not collection_exists(collection_name):
            success = create_collection(
                name=collection_name,
                properties=[
                    {"name": "title", "type": "text"},
                    {"name": "content", "type": "text"},
                    {"name": "chunk_id", "type": "int"},
                    {"name": "source_file", "type": "text"},
                    {"name": "file_size", "type": "int"},
                    {"name": "upload_date", "type": "date"},
                    {"name": "chunk_length", "type": "int"},
                    {"name": "word_count", "type": "int"}
                ],
                vectorizer="text2vec-openai",
                generative_model="gpt-3.5-turbo"
            )
            
            if success:
                print(f"✅ Created collection: {collection_name}")
            else:
                print(f"❌ Failed to create collection: {collection_name}")
                return False
        else:
            print(f"✅ Collection already exists: {collection_name}")
        
        # Step 3: Chunk the text
        print("\n✂️ Chunking text...")
        chunks = chunk_text(pdf_text, chunk_size=800, overlap=100)
        print(f"✅ Created {len(chunks)} chunks")
        
        # Step 4: Prepare documents for batch upload
        print("\n📦 Preparing documents for upload...")
        
        pdf_file = Path(pdf_path)
        file_size = pdf_file.stat().st_size
        upload_date = datetime.now().isoformat()
        
        documents = []
        for chunk in chunks:
            doc = {
                "properties": {
                    "title": f"{pdf_file.stem} - Chunk {chunk['chunk_id'] + 1}",
                    "content": chunk["text"],
                    "chunk_id": chunk["chunk_id"],
                    "source_file": pdf_file.name,
                    "file_size": file_size,
                    "upload_date": upload_date,
                    "chunk_length": chunk["length"],
                    "word_count": chunk["word_count"]
                }
            }
            documents.append(doc)
        
        # Step 5: Upload to Weaviate
        print(f"\n🚀 Uploading {len(documents)} documents to Weaviate...")
        
        results = batch_insert(
            collection_name=collection_name,
            objects=documents,
            batch_size=10
        )
        
        print(f"✅ Upload complete!")
        print(f"   • Successful: {results['inserted']}")
        print(f"   • Failed: {results['failed']}")
        print(f"   • Total: {results['total']}")
        
        # Step 6: Test search functionality
        print("\n🔍 Testing search functionality...")
        
        search_queries = [
            "frontend development",
            "experience",
            "skills",
            "education"
        ]
        
        for query in search_queries:
            print(f"\nSearching for: '{query}'")
            search_results = semantic_search(
                collection_name=collection_name,
                query=query,
                limit=3,
                properties=["title", "content", "chunk_id"]
            )
            
            if search_results:
                print(f"  Found {len(search_results)} results:")
                for i, result in enumerate(search_results[:2], 1):
                    title = result["properties"].get("title", "N/A")
                    content_preview = result["properties"].get("content", "")[:100] + "..."
                    score = result["metadata"].get("score", 0)
                    print(f"    {i}. {title} (score: {score:.3f})")
                    print(f"       Preview: {content_preview}")
            else:
                print("  No results found")
        
        print(f"\n🎉 PDF upload test completed successfully!")
        print(f"📊 Summary:")
        print(f"   • File: {pdf_file.name}")
        print(f"   • Size: {file_size:,} bytes") 
        print(f"   • Text length: {len(pdf_text):,} characters")
        print(f"   • Chunks created: {len(chunks)}")
        print(f"   • Documents uploaded: {results['inserted']}")
        
        return True
        
    except Exception as e:
        logger.error(f"PDF upload test failed: {e}")
        print(f"❌ Test failed: {e}")
        return False


def search_uploaded_pdf(collection_name: str = "Documents", query: str = "frontend"):
    """
    Helper function to search the uploaded PDF content
    
    Args:
        collection_name: Name of the collection to search
        query: Search query
    """
    print(f"\n🔍 Searching for: '{query}'")
    
    try:
        results = semantic_search(
            collection_name=collection_name,
            query=query,
            limit=5,
            properties=["title", "content", "source_file", "chunk_id"]
        )
        
        if results:
            print(f"Found {len(results)} results:")
            for i, result in enumerate(results, 1):
                title = result["properties"].get("title", "N/A")
                source = result["properties"].get("source_file", "N/A")
                chunk_id = result["properties"].get("chunk_id", "N/A")
                content = result["properties"].get("content", "")
                score = result["metadata"].get("score", 0)
                
                print(f"\n{i}. {title}")
                print(f"   Source: {source} (Chunk {chunk_id})")
                print(f"   Score: {score:.3f}")
                print(f"   Content: {content[:200]}...")
        else:
            print("No results found")
            
    except Exception as e:
        print(f"❌ Search failed: {e}")


if __name__ == "__main__":
    # Test the PDF upload
    success = test_pdf_upload()
    
    if success:
        print("\n" + "="*50)
        print("Testing search functionality:")
        
        # Test some searches
        search_uploaded_pdf(query="frontend development")
        search_uploaded_pdf(query="React")
        search_uploaded_pdf(query="experience") 