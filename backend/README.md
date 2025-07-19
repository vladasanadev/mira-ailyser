# Backend API for PDF CV Analysis

This backend API handles PDF file uploads and processes them using Weaviate vector database for AI-powered CV analysis.

## Features

- **PDF Upload**: Accept and process PDF files from users
- **Text Extraction**: Extract text content from PDF using pypdf
- **Text Chunking**: Split text into meaningful chunks for processing
- **Vector Storage**: Store chunks in Weaviate with embeddings
- **API Endpoints**: RESTful API for file upload and search

## Setup

### 1. Environment Variables

Create a `.env` file in the backend directory with:

```env
WEAVIATE_URL=your_weaviate_cluster_url
WEAVIATE_API_KEY=your_weaviate_api_key
OPEN_AI_API=your_openai_api_key
```

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Run the API Server

```bash
python api_server.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Health Check
```
GET /health
```

Returns server status.

### Upload PDF
```
POST /upload-pdf
Content-Type: multipart/form-data

Form Data:
- pdf: PDF file (max 16MB)
```

**Response:**
```json
{
  "success": true,
  "message": "PDF processed successfully!",
  "data": {
    "filename": "example.pdf",
    "file_size_mb": 2.5,
    "total_chunks": 15,
    "successful_uploads": 15,
    "failed_uploads": 0,
    "extracted_text_length": 5420
  }
}
```

### Search CV (Coming Soon)
```
POST /search-cv
Content-Type: application/json

{
  "query": "search query"
}
```

## File Processing Flow

1. **Upload**: User uploads PDF file via API
2. **Validation**: Check file type and size
3. **Text Extraction**: Extract text using pypdf
4. **Chunking**: Split text into overlapping chunks
5. **Vector Storage**: Store chunks in Weaviate with OpenAI embeddings
6. **Cleanup**: Remove temporary files
7. **Response**: Return processing results

## Dependencies

- **Flask**: Web API framework
- **pypdf**: PDF text extraction
- **Weaviate**: Vector database client
- **OpenAI**: Text embeddings
- **python-dotenv**: Environment variables

## Error Handling

The API includes comprehensive error handling for:
- Invalid file types
- File size limits
- PDF processing errors
- Weaviate connection issues
- Temporary file cleanup

## Development

### File Structure
```
backend/
├── api_server.py          # Main Flask API server
├── test_pdf_upload_fixed.py  # PDF processing functions
├── weaviate_client.py     # Weaviate client setup
├── weaviate_operations.py # Database operations
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
└── uploads/              # Temporary upload directory
```

### Testing

You can test the API using curl:

```bash
# Health check
curl http://localhost:5000/health

# Upload PDF
curl -X POST \
  -F "pdf=@your-cv.pdf" \
  http://localhost:5000/upload-pdf
```

## Integration

The backend is designed to work with the Next.js frontend. Make sure both servers are running:

- Frontend: `http://localhost:3000` (Next.js)
- Backend: `http://localhost:5000` (Flask API) 