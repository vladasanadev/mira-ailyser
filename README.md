# Mira AI CV Analyzer 🚀

A modern AI-powered CV analysis platform that helps users understand their career risk from AI automation and provides personalized career guidance.

## Features ✨

- 🎯 **AI Risk Assessment**: Analyze how likely your role is to be replaced by AI
- 📄 **PDF Upload**: Upload your CV for AI-powered analysis
- 🤖 **Smart Processing**: Extract and chunk text using pypdf and Weaviate
- 💬 **Interactive Chat**: AI assistant integration for career guidance
- 📊 **Modern UI**: Clean, responsive 2-column layout
- ⚡ **Real-time Processing**: Immediate feedback on CV uploads

## Architecture 🏗️

### Frontend (Next.js + React)
- Modern React components with TypeScript
- Tailwind CSS for styling
- Drag & drop PDF upload interface  
- Responsive 2-column layout
- Real-time file upload with progress feedback

### Backend (Python + Flask)
- Flask API server for file processing
- pypdf for PDF text extraction
- Weaviate vector database for embeddings
- OpenAI integration for AI analysis
- Comprehensive error handling and logging

## Quick Start 🚀

### Option 1: Use the Startup Script (Recommended)

```bash
# Clone the repository
git clone https://github.com/vladasanadev/mira-ailyser.git
cd mira-ailyser

# Create backend environment file
cp backend/.env.example backend/.env
# Edit backend/.env with your credentials

# Run both frontend and backend
./start-dev.sh
```

### Option 2: Manual Setup

1. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt

# Create .env file with:
# WEAVIATE_URL=your_weaviate_cluster_url
# WEAVIATE_API_KEY=your_weaviate_api_key  
# OPEN_AI_API=your_openai_api_key

python api_server.py
```

2. **Frontend Setup**
```bash
# In a new terminal
npm install
npm run dev
```

## Environment Setup 🔧

### Required Environment Variables

Create `backend/.env` with:

```env
WEAVIATE_URL=your_weaviate_cluster_url
WEAVIATE_API_KEY=your_weaviate_api_key
OPEN_AI_API=your_openai_api_key
```

### Get Your Credentials

1. **Weaviate Cloud**: Sign up at [console.weaviate.cloud](https://console.weaviate.cloud)
2. **OpenAI API**: Get your key from [platform.openai.com](https://platform.openai.com)

## Usage 📖

### 1. Access the Application
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:5000`

### 2. Upload Your CV
- Drag and drop a PDF file or click to browse
- Maximum file size: 16MB
- Supported format: PDF only

### 3. AI Analysis
- The system extracts text from your PDF
- Text is chunked and processed with AI embeddings
- Results are stored in Weaviate for analysis
- Get personalized career insights

### 4. Interactive Chat
- Use the left-side chat interface
- Ask questions about your career
- Get AI-powered recommendations

## API Endpoints 🔌

### Health Check
```bash
curl http://localhost:5000/health
```

### Upload PDF
```bash
curl -X POST \
  -F "pdf=@your-cv.pdf" \
  http://localhost:5000/upload-pdf
```

## Project Structure 📁

```
mira-ailyser/
├── app/                    # Next.js frontend
│   ├── page.tsx           # Main UI component
│   ├── layout.tsx         # App layout
│   └── globals.css        # Global styles
├── backend/               # Python backend
│   ├── api_server.py      # Flask API server
│   ├── test_pdf_upload_fixed.py  # PDF processing
│   ├── weaviate_client.py # Database client
│   ├── weaviate_operations.py    # DB operations
│   ├── requirements.txt   # Python dependencies
│   └── uploads/          # Temporary files
├── public/               # Static assets
├── start-dev.sh         # Development startup script
└── package.json         # Node.js dependencies
```

## Technology Stack 🛠️

### Frontend
- **Next.js 13** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling
- **React Hooks** - State management

### Backend  
- **Flask** - Web API framework
- **pypdf** - PDF text extraction
- **Weaviate** - Vector database
- **OpenAI** - AI embeddings and analysis
- **python-dotenv** - Environment management

### Development
- **Git** - Version control
- **ESLint** - Code linting
- **PostCSS** - CSS processing

## Development 👩‍💻

### File Upload Flow
1. User selects PDF file in frontend
2. File is sent to Flask API via multipart/form-data
3. Backend validates file type and size
4. Text is extracted using pypdf
5. Text is chunked for processing
6. Chunks are uploaded to Weaviate with embeddings
7. Success response returned to frontend
8. Temporary files cleaned up

### Adding New Features
- Frontend components in `app/`
- Backend endpoints in `backend/api_server.py`
- Database operations in `backend/weaviate_operations.py`

## Troubleshooting 🔧

### Common Issues

1. **"Backend server not running"**
   - Make sure Flask server is running on port 5000
   - Check `backend/.env` file exists with credentials

2. **"Failed to upload PDF"**
   - Ensure file is under 16MB
   - Check file is valid PDF format
   - Verify Weaviate connection

3. **"Weaviate connection failed"**
   - Check your `WEAVIATE_URL` and `WEAVIATE_API_KEY`
   - Ensure Weaviate cluster is running

### Logs
- Backend logs: Check terminal running `python api_server.py`
- Frontend logs: Check browser developer console
- Network issues: Check browser Network tab

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License 📄

This project is licensed under the MIT License.

---

**Built with ❤️ for helping professionals navigate the AI revolution**
