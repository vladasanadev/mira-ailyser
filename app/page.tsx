'use client';

import { useState } from 'react';

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [aiScore, setAiScore] = useState<number | null>(null);
  const [showScore, setShowScore] = useState(false);

  // Function to calculate AI replacement score based on CV text
  const calculateAIScore = (extractedText: string): number => {
    const text = extractedText.toLowerCase();
    let score = 50; // Base score
    
    // Skills that decrease replacement risk
    const safeSkills = ['leadership', 'management', 'creative', 'strategy', 'innovation', 'emotional intelligence', 'communication', 'negotiation', 'mentoring', 'public speaking'];
    const safeCareers = ['ceo', 'director', 'manager', 'consultant', 'teacher', 'therapist', 'artist', 'designer'];
    
    // Skills that increase replacement risk
    const riskSkills = ['data entry', 'repetitive', 'routine', 'automated', 'basic', 'simple tasks', 'administrative'];
    const riskCareers = ['clerk', 'cashier', 'operator', 'assistant'];
    
    safeSkills.forEach(skill => {
      if (text.includes(skill)) score -= Math.random() * 15 + 5;
    });
    
    safeCareers.forEach(career => {
      if (text.includes(career)) score -= Math.random() * 20 + 10;
    });
    
    riskSkills.forEach(skill => {
      if (text.includes(skill)) score += Math.random() * 15 + 5;
    });
    
    riskCareers.forEach(career => {
      if (text.includes(career)) score += Math.random() * 20 + 10;
    });
    
    // Add some randomness for fun
    score += (Math.random() - 0.5) * 20;
    
    return Math.max(5, Math.min(95, Math.round(score)));
  };

  const getScoreColor = (score: number) => {
    if (score < 30) return '#10b981'; // Green
    if (score < 60) return '#f59e0b'; // Yellow
    return '#ef4444'; // Red
  };

  const getScoreEmoji = (score: number) => {
    if (score < 20) return '🦾';
    if (score < 40) return '😎';
    if (score < 60) return '🤔';
    if (score < 80) return '😬';
    return '🤖';
  };

  const getScoreMessage = (score: number) => {
    if (score < 20) return 'You are irreplaceable!';
    if (score < 40) return 'Pretty safe from robots!';
    if (score < 60) return 'Some risk, but adaptable!';
    if (score < 80) return 'Time to upskill!';
    return 'Welcome our robot overlords!';
  };

  const handleFileSelect = (file: File) => {
    if (file.type === 'application/pdf') {
      setSelectedFile(file);
      setShowScore(false); // Hide score when new file is selected
    } else {
      alert('Please select a PDF file.');
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    
    setIsUploading(true);
    
    try {
      // Create FormData to send the file
      const formData = new FormData();
      formData.append('pdf', selectedFile);
      
      // Make API call to backend
      const response = await fetch('http://localhost:5001/upload-pdf', {
        method: 'POST',
        body: formData,
      });
      
      const result = await response.json();
      
      if (response.ok && result.success) {
        // Calculate AI replacement score based on extracted text
        const score = calculateAIScore(result.extracted_text || '');
        setAiScore(score);
        setShowScore(true);
        
        // Clear the selected file after successful upload
        setSelectedFile(null);
      } else {
        throw new Error(result.message || 'Failed to upload PDF');
      }
    } catch (error) {
      console.error('Upload error:', error);
      alert(`Upload failed: ${error instanceof Error ? error.message : 'Unknown error occurred'}
      
Please make sure:
- The backend server is running on http://localhost:5001
- Your PDF file is valid and under 16MB
- You have a stable internet connection`);
    } finally {
      setIsUploading(false);
    }
  };

  const removeFile = () => {
    setSelectedFile(null);
  };

  return (
    <div className="min-h-screen bg-gray-50" style={{ minHeight: '100vh', backgroundColor: '#f9fafb' }}>
      
      {/* Minimalistic Metallic Header */}
      <header className="py-6" style={{ 
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        padding: '24px 0',
        position: 'relative'
      }}>
        <div className="container mx-auto px-6 text-center" style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 24px', textAlign: 'center' }}>
          <h1 style={{ 
            fontSize: 'clamp(2.5rem, 6vw, 3.5rem)', 
            fontWeight: '300', 
            lineHeight: 1.2,
            background: 'linear-gradient(135deg, #e2e8f0 0%, #ffffff 50%, #cbd5e1 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            letterSpacing: '-0.02em',
            fontFamily: 'system-ui, -apple-system, sans-serif'
          }}>
            How likely are you replaced by AI?
          </h1>
        </div>
      </header>

      <div className="container mx-auto p-6" style={{ maxWidth: '1200px', margin: '0 auto', padding: '48px 24px' }}>
        
        {/* AI Score Badge */}
        {showScore && aiScore !== null && (
          <div className="mb-8 flex justify-center">
            <div style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              borderRadius: '20px',
              padding: '24px 32px',
              boxShadow: '0 10px 30px rgba(0,0,0,0.2)',
              transform: 'scale(1.05)',
              animation: 'bounce 0.5s ease-out',
              textAlign: 'center',
              color: 'white',
              minWidth: '300px'
            }}>
              <div style={{ fontSize: '48px', marginBottom: '12px' }}>{getScoreEmoji(aiScore)}</div>
              <div style={{ fontSize: '32px', fontWeight: 'bold', marginBottom: '8px' }}>
                {aiScore}% Risk
              </div>
              <div style={{ fontSize: '18px', fontWeight: '300', opacity: 0.9 }}>
                {getScoreMessage(aiScore)}
              </div>
            </div>
          </div>
        )}
        
        {/* 2-Column Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px' }}>
          
          {/* Left Column - Iframe */}
          <div className="bg-white rounded-lg shadow-md p-4" style={{ backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)', padding: '16px' }}>
            <h2 className="text-xl font-bold text-gray-900 mb-4" style={{ fontSize: '20px', fontWeight: 'bold', color: '#111827', marginBottom: '16px' }}>
              AI Assistant
            </h2>
            <iframe 
              src="https://bey.chat/3090f07a-5a09-4093-9114-d8c1332d7a74" 
              width="100%" 
              height="600px" 
              allowFullScreen
              allow="camera; microphone; fullscreen"
              style={{ border: 'none', width: '100%', height: '600px', borderRadius: '8px' }}
            />
          </div>

          {/* Right Column - PDF Uploader */}
          <div className="bg-white rounded-lg shadow-md p-6" style={{ backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)', padding: '24px' }}>
            <h2 className="text-xl font-bold text-gray-900 mb-6" style={{ fontSize: '20px', fontWeight: 'bold', color: '#111827', marginBottom: '24px' }}>
              Upload PDF
            </h2>
            
            {/* File Upload Area */}
            <div
              className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                dragActive 
                  ? 'border-blue-400 bg-blue-50' 
                  : selectedFile 
                    ? 'border-green-400 bg-green-50' 
                    : 'border-gray-300 hover:border-gray-400'
              }`}
              style={{
                border: dragActive 
                  ? '2px dashed #60a5fa' 
                  : selectedFile 
                    ? '2px dashed #34d399' 
                    : '2px dashed #d1d5db',
                backgroundColor: dragActive 
                  ? '#eff6ff' 
                  : selectedFile 
                    ? '#ecfdf5' 
                    : '#ffffff',
                borderRadius: '8px',
                padding: '32px',
                textAlign: 'center',
                transition: 'all 0.2s',
                cursor: 'pointer'
              }}
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onClick={() => document.getElementById('fileInput')?.click()}
            >
              {selectedFile ? (
                <div style={{ color: '#059669' }}>
                  <div style={{ fontSize: '48px', marginBottom: '16px' }}>📄</div>
                  <p style={{ fontSize: '16px', fontWeight: '500', marginBottom: '8px' }}>
                    {selectedFile.name}
                  </p>
                  <p style={{ fontSize: '14px', color: '#6b7280' }}>
                    {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
                  </p>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      removeFile();
                    }}
                    style={{
                      marginTop: '12px',
                      color: '#dc2626',
                      backgroundColor: 'transparent',
                      border: 'none',
                      fontSize: '14px',
                      cursor: 'pointer',
                      textDecoration: 'underline'
                    }}
                  >
                    Remove file
                  </button>
                </div>
              ) : (
                <div style={{ color: '#6b7280' }}>
                  <div style={{ fontSize: '48px', marginBottom: '16px' }}>📁</div>
                  <p style={{ fontSize: '16px', fontWeight: '500', marginBottom: '8px' }}>
                    {dragActive ? 'Drop your PDF here' : 'Click to upload or drag and drop'}
                  </p>
                  <p style={{ fontSize: '14px' }}>
                    PDF files only (max 16MB)
                  </p>
                </div>
              )}
              
              <input
                id="fileInput"
                type="file"
                accept=".pdf"
                onChange={handleFileInputChange}
                style={{ display: 'none' }}
              />
            </div>

            {/* Upload Button */}
            {selectedFile && (
              <button
                onClick={handleUpload}
                disabled={isUploading}
                style={{
                  width: '100%',
                  marginTop: '24px',
                  backgroundColor: isUploading ? '#9ca3af' : '#3b82f6',
                  color: 'white',
                  padding: '12px 24px',
                  borderRadius: '8px',
                  border: 'none',
                  fontSize: '16px',
                  fontWeight: '500',
                  cursor: isUploading ? 'not-allowed' : 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px',
                  transition: 'background-color 0.2s'
                }}
              >
                {isUploading ? (
                  <>
                    <div style={{
                      width: '16px',
                      height: '16px',
                      border: '2px solid #ffffff',
                      borderTop: '2px solid transparent',
                      borderRadius: '50%',
                      animation: 'spin 1s linear infinite'
                    }}></div>
                    Analyzing...
                  </>
                ) : (
                  <>
                    📤 Get AI Risk Score
                  </>
                )}
              </button>
            )}

            {/* What You'll Get Section */}
            <div style={{ marginTop: '32px', padding: '20px', backgroundColor: '#f8fafc', borderRadius: '8px' }}>
              <h3 style={{ fontSize: '16px', fontWeight: '600', color: '#1f2937', marginBottom: '16px' }}>
                What you'll get:
              </h3>
              <div className="space-y-2" style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <div className="flex items-center space-x-3" style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <div style={{ width: '8px', height: '8px', backgroundColor: '#10b981', borderRadius: '50%' }}></div>
                  <span className="text-gray-700 text-sm" style={{ color: '#374151', fontSize: '14px' }}>AI replacement score</span>
                </div>
                <div className="flex items-center space-x-3" style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <div style={{ width: '8px', height: '8px', backgroundColor: '#10b981', borderRadius: '50%' }}></div>
                  <span className="text-gray-700 text-sm" style={{ color: '#374151', fontSize: '14px' }}>Personalized feedback</span>
                </div>
                <div className="flex items-center space-x-3" style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <div style={{ width: '8px', height: '8px', backgroundColor: '#10b981', borderRadius: '50%' }}></div>
                  <span className="text-gray-700 text-sm" style={{ color: '#374151', fontSize: '14px' }}>Career insights</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Add CSS animations */}
      <style jsx>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        @keyframes bounce {
          0%, 20%, 53%, 80%, 100% { transform: translate3d(0,0,0) scale(1); }
          40%, 43% { transform: translate3d(0,-8px,0) scale(1.05); }
          70% { transform: translate3d(0,-4px,0) scale(1.02); }
          90% { transform: translate3d(0,-1px,0) scale(1.01); }
        }
      `}</style>
    </div>
  );
}
