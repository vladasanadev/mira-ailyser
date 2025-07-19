from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
from werkzeug.utils import secure_filename
from test_pdf_upload_fixed import process_user_pdf
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "PDF Upload API is running"
    })

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    """
    Upload and process PDF file
    
    Expected: multipart/form-data with 'pdf' file field
    Returns: JSON with processing results
    """
    try:
        # Check if the post request has the file part
        if 'pdf' not in request.files:
            return jsonify({
                "success": False,
                "error": "No file uploaded",
                "message": "Please select a PDF file to upload"
            }), 400

        file = request.files['pdf']
        
        # If user does not select file, browser submits empty part without filename
        if file.filename == '':
            return jsonify({
                "success": False,
                "error": "No file selected",
                "message": "Please select a PDF file to upload"
            }), 400

        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # Reset file pointer
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({
                "success": False,
                "error": "File too large",
                "message": f"File size ({file_size / 1024 / 1024:.1f}MB) exceeds maximum allowed size (16MB)"
            }), 400

        if file and allowed_file(file.filename):
            # Secure the filename
            filename = secure_filename(file.filename)
            
            # Create temporary file to store uploaded PDF
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf', dir=UPLOAD_FOLDER) as temp_file:
                file.save(temp_file.name)
                temp_file_path = temp_file.name
            
            logger.info(f"Saved uploaded file to: {temp_file_path}")
            
            try:
                # Process the PDF using the updated function
                result = process_user_pdf(temp_file_path)
                
                # Clean up temporary file
                os.unlink(temp_file_path)
                
                logger.info(f"Processing result: {result}")
                
                if result["success"]:
                    return jsonify({
                        "success": True,
                        "message": "PDF processed successfully!",
                        "data": {
                            "filename": filename,
                            "file_size_mb": round(file_size / 1024 / 1024, 2),
                            "total_chunks": result["total_chunks"],
                            "successful_uploads": result["successful_uploads"],
                            "failed_uploads": result["failed_uploads"],
                            "extracted_text_length": result["extracted_text_length"]
                        }
                    }), 200
                else:
                    return jsonify({
                        "success": False,
                        "error": result.get("error", "Unknown error"),
                        "message": result.get("message", "Failed to process PDF")
                    }), 500
                    
            except Exception as e:
                # Clean up temporary file on error
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                
                logger.error(f"Error processing PDF: {str(e)}")
                return jsonify({
                    "success": False,
                    "error": str(e),
                    "message": "Failed to process the PDF file"
                }), 500
        else:
            return jsonify({
                "success": False,
                "error": "Invalid file type",
                "message": "Only PDF files are allowed"
            }), 400

    except Exception as e:
        logger.error(f"Unexpected error in upload_pdf: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "An unexpected error occurred"
        }), 500

@app.route('/search-cv', methods=['POST'])
def search_cv():
    """
    Search processed CV content
    
    Expected JSON: {"query": "search query"}
    Returns: Search results from Weaviate
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                "success": False,
                "error": "Missing query parameter",
                "message": "Please provide a search query"
            }), 400
        
        query = data['query']
        
        # TODO: Implement search functionality using weaviate_operations
        # For now, return a placeholder response
        return jsonify({
            "success": True,
            "message": "Search functionality coming soon",
            "query": query,
            "results": []
        }), 200
        
    except Exception as e:
        logger.error(f"Error in search_cv: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to perform search"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 