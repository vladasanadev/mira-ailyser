'use client';

import { useState } from 'react';

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  const handleFileSelect = (file: File) => {
    if (file.type === 'application/pdf') {
      setSelectedFile(file);
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
    
    // TODO: Implement actual file upload to backend
    setTimeout(() => {
      setIsUploading(false);
      alert('PDF uploaded successfully!');
    }, 2000);
  };

  const removeFile = () => {
    setSelectedFile(null);
  };

  return (
    <div className="min-h-screen bg-gray-50" style={{ minHeight: '100vh', backgroundColor: '#f9fafb' }}>
      <div className="container mx-auto p-6" style={{ maxWidth: '1200px', margin: '0 auto', padding: '24px' }}>
        
        {/* 2-Column Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px' }}>
          
          {/* Left Column - Iframe */}
          <div className="bg-white rounded-lg shadow-md p-4" style={{ backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)', padding: '16px' }}>
            <h2 className="text-xl font-bold text-gray-900 mb-4" style={{ fontSize: '20px', fontWeight: 'bold', color: '#111827', marginBottom: '16px' }}>
              AI Assistant
            </h2>
            <iframe 
              src="https://bey.chat/698b3b83-9e6d-4ccd-b0f8-021677c0b6f2" 
              width="100%" 
              height="600px" 
              frameBorder="0" 
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
                    ? '#f0fdf4' 
                    : 'transparent',
                borderRadius: '8px',
                padding: '32px',
                textAlign: 'center',
                transition: 'all 0.2s'
              }}
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
            >
              <input
                type="file"
                accept=".pdf"
                onChange={handleFileInputChange}
                className="hidden"
                style={{ display: 'none' }}
                id="pdf-upload"
              />
              
              {selectedFile ? (
                <div className="space-y-4" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px' }}>
                  <div className="w-12 h-12 mx-auto bg-green-100 rounded-full flex items-center justify-center" style={{ width: '48px', height: '48px', backgroundColor: '#dcfce7', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <svg className="w-6 h-6 text-green-600" style={{ width: '24px', height: '24px', color: '#16a34a' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-green-700 font-medium" style={{ color: '#15803d', fontWeight: '500', marginBottom: '4px' }}>{selectedFile.name}</p>
                    <p className="text-green-600 text-sm" style={{ color: '#16a34a', fontSize: '14px' }}>
                      {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                  <button
                    onClick={removeFile}
                    className="text-red-600 hover:text-red-700 text-sm underline"
                    style={{ color: '#dc2626', fontSize: '14px', textDecoration: 'underline', backgroundColor: 'transparent', border: 'none', cursor: 'pointer' }}
                  >
                    Remove file
                  </button>
                </div>
              ) : (
                <div className="space-y-4" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px' }}>
                  <div className="w-12 h-12 mx-auto bg-gray-100 rounded-full flex items-center justify-center" style={{ width: '48px', height: '48px', backgroundColor: '#f3f4f6', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <svg className="w-6 h-6 text-gray-400" style={{ width: '24px', height: '24px', color: '#9ca3af' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-gray-700 font-medium" style={{ color: '#374151', fontWeight: '500', marginBottom: '8px' }}>
                      Drag and drop your PDF here
                    </p>
                    <p className="text-gray-500 text-sm" style={{ color: '#6b7280', fontSize: '14px', marginBottom: '4px' }}>
                      or{' '}
                      <label htmlFor="pdf-upload" className="text-blue-600 hover:text-blue-700 cursor-pointer underline" style={{ color: '#2563eb', textDecoration: 'underline', cursor: 'pointer' }}>
                        browse files
                      </label>
                    </p>
                    <p className="text-gray-400 text-xs mt-1" style={{ color: '#9ca3af', fontSize: '12px' }}>
                      PDF files only, max 10MB
                    </p>
                  </div>
                </div>
              )}
            </div>

            {/* Upload Button */}
            <button
              onClick={handleUpload}
              disabled={!selectedFile || isUploading}
              className={`w-full mt-6 py-3 px-4 rounded-lg font-medium transition-colors ${
                selectedFile && !isUploading
                  ? 'bg-blue-600 hover:bg-blue-700 text-white'
                  : 'bg-gray-200 text-gray-400 cursor-not-allowed'
              }`}
              style={{
                width: '100%',
                marginTop: '24px',
                padding: '12px 16px',
                borderRadius: '8px',
                fontWeight: '500',
                border: 'none',
                cursor: selectedFile && !isUploading ? 'pointer' : 'not-allowed',
                backgroundColor: selectedFile && !isUploading ? '#2563eb' : '#e5e7eb',
                color: selectedFile && !isUploading ? 'white' : '#9ca3af',
                transition: 'all 0.2s'
              }}
            >
              {isUploading ? (
                <div className="flex items-center justify-center space-x-2" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" style={{ width: '16px', height: '16px', border: '2px solid white', borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin 1s linear infinite' }}></div>
                  <span>Uploading...</span>
                </div>
              ) : (
                'Upload PDF'
              )}
            </button>

            {/* Features List */}
            <div className="mt-8" style={{ marginTop: '32px' }}>
              <h3 className="text-lg font-semibold text-gray-900 mb-4" style={{ fontSize: '18px', fontWeight: '600', color: '#111827', marginBottom: '16px' }}>
                What happens next:
              </h3>
              <div className="space-y-2" style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <div className="flex items-center space-x-3" style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <div style={{ width: '8px', height: '8px', backgroundColor: '#10b981', borderRadius: '50%' }}></div>
                  <span className="text-gray-700 text-sm" style={{ color: '#374151', fontSize: '14px' }}>AI analysis of your CV</span>
                </div>
                <div className="flex items-center space-x-3" style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <div style={{ width: '8px', height: '8px', backgroundColor: '#10b981', borderRadius: '50%' }}></div>
                  <span className="text-gray-700 text-sm" style={{ color: '#374151', fontSize: '14px' }}>Personalized feedback</span>
                </div>
                <div className="flex items-center space-x-3" style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <div style={{ width: '8px', height: '8px', backgroundColor: '#10b981', borderRadius: '50%' }}></div>
                  <span className="text-gray-700 text-sm" style={{ color: '#374151', fontSize: '14px' }}>Career recommendations</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
