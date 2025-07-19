import weaviate
from weaviate.classes.init import Auth
import os
from weaviate.classes.config import Configure, Property, DataType
from pypdf import PdfReader
from typing import List, Dict, Any
from dotenv import load_dotenv


load_dotenv()

# Best practice: store your credentials in environment variables
weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
open_ai_key = os.environ["OPEN_AI_API"]

headers = {
    "X-OpenAI-Api-Key": open_ai_key,
}
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,                       # `weaviate_url`: your Weaviate URL
    auth_credentials=Auth.api_key(weaviate_api_key),      # `weaviate_key`: your Weaviate API key
    headers=headers
)

print(client.is_ready())  # Should print: `True`

# Try to get existing collection or create new one
try:
    pdf_for_mira = client.collections.get("Pdf_for_mira")
    print("Using existing Pdf_for_mira collection")
except:
    # Create collection if it doesn't exist
    try:
        pdf_for_mira = client.collections.create(
            name="Pdf_for_mira",
            properties=[
                Property(name="text", data_type=DataType.TEXT),
                Property(name="chunk_id", data_type=DataType.INT),
                Property(name="length", data_type=DataType.INT),
                Property(name="word_count", data_type=DataType.INT),
            ],
            # Use the text2vec-openai vectorizer
            vectorizer_config=weaviate.classes.config.Configure.Vectorizer.text2vec_openai()
        )
        print("Created new Pdf_for_mira collection")
    except Exception as e:
        print(f"Error creating collection: {e}")
        # If that fails too, try without vectorizer config
        pdf_for_mira = client.collections.create(
            name="Pdf_for_mira",
            properties=[
                Property(name="text", data_type=DataType.TEXT),
                Property(name="chunk_id", data_type=DataType.INT),
                Property(name="length", data_type=DataType.INT),
                Property(name="word_count", data_type=DataType.INT),
            ]
        )
        print("Created collection without vectorizer config")


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
        
        reader = PdfReader(pdf_path)
        pages = reader.pages
        for page in pages:
            text_content += page.extract_text()
        
        print(f"Extracted {len(text_content)} characters from PDF")
        return text_content.strip()
        
    except Exception as e:
        print(f"Failed to extract text from PDF: {e}")
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


def process_user_pdf(pdf_path: str) -> Dict[str, Any]:
    """
    Process a user-uploaded PDF file and upload to Weaviate
    
    Args:
        pdf_path: Path to the user-uploaded PDF file
        
    Returns:
        Processing results with success status and details
    """
    try:
        pdf_for_mira = client.collections.get("Pdf_for_mira")

        with pdf_for_mira.batch.fixed_size(batch_size=200) as batch:
            # Extract text and chunk it
            extracted_text = extract_pdf_text(pdf_path)
            chunks = chunk_text(extracted_text)
            
            # Add chunks to batch
            for chunk in chunks:
                batch.add_object({
                    "text": chunk["text"],
                    "chunk_id": chunk["chunk_id"],
                    "length": chunk["length"],
                    "word_count": chunk["word_count"],
                })
                
                if batch.number_errors > 10:
                    print("Batch import stopped due to excessive errors.")
                    break

        # Check for failed objects
        failed_objects = pdf_for_mira.batch.failed_objects
        failed_count = len(failed_objects) if failed_objects else 0
        success_count = len(chunks) - failed_count
        
        result = {
            "success": True,
            "total_chunks": len(chunks),
            "successful_uploads": success_count,
            "failed_uploads": failed_count,
            "extracted_text_length": len(extracted_text),
            "message": f"Successfully processed PDF with {len(chunks)} chunks"
        }
        
        if failed_objects:
            print(f"Number of failed imports: {failed_count}")
            print(f"First failed object: {failed_objects[0]}")
            result["error_details"] = f"Failed to upload {failed_count} chunks"
            
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to process PDF: {str(e)}"
        }


# Backward compatibility - keep the old function name but make it require a path
def test_pdf_upload_direct_weaviate(pdf_path: str):
    """
    Legacy function - now requires pdf_path parameter
    """
    return process_user_pdf(pdf_path)
