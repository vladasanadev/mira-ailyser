'use client';

import { useState, useRef, useEffect } from 'react';

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);

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

  const handleAnalyze = async () => {
    if (!selectedFile) return;
    
    setIsAnalyzing(true);
    
    // Simulate AI analysis - replace with actual backend call
    setTimeout(() => {
      setIsAnalyzing(false);
      alert('CV Analysis complete! Check your email for detailed career guidance.');
    }, 3000);
  };

  useEffect(() => {
    // Ensure video plays and loops
    if (videoRef.current) {
      videoRef.current.muted = true;
      videoRef.current.play().catch(console.error);
    }
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-purple-500/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-500/15 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
        <div className="absolute top-1/2 left-1/2 w-80 h-80 bg-pink-500/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '2s' }}></div>
      </div>

      {/* Header */}
      <header className="relative z-10 p-6 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold text-white">
            <span className="bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
              Mira AI
            </span>{' '}
            CV Analyzer
          </h1>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center min-h-[calc(100vh-200px)]">
          
          {/* Left Side - Video Section */}
          <div className="space-y-8">
            <div className="text-left space-y-6">
              <h2 className="text-5xl lg:text-6xl font-bold text-white leading-tight">
                Transform Your
                <br />
                <span className="bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent bg-200% animate-gradient">
                  Career Journey
                </span>
              </h2>
              <p className="text-xl text-gray-300 leading-relaxed max-w-lg">
                Experience the future of career guidance with our AI-powered analysis. 
                Upload your CV and unlock personalized insights that will accelerate your professional growth.
              </p>
            </div>
            
            {/* Video Container */}
            <div className="relative group">
              <div className="absolute -inset-1 bg-gradient-to-r from-cyan-500 via-purple-500 to-pink-500 rounded-3xl blur opacity-75 group-hover:opacity-100 transition duration-300 bg-200% animate-gradient-xy"></div>
              <div className="relative rounded-3xl overflow-hidden bg-black border border-gray-800">
                <video
                  ref={videoRef}
                  className="w-full h-80 lg:h-96 object-cover"
                  loop
                  muted
                  autoPlay
                  playsInline
                  poster="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='800' height='400'%3E%3Cdefs%3E%3ClinearGradient id='grad1' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%23667eea;stop-opacity:1' /%3E%3Cstop offset='100%25' style='stop-color:%23764ba2;stop-opacity:1' /%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='800' height='400' fill='url(%23grad1)'/%3E%3Ctext x='50%25' y='50%25' font-family='Inter, sans-serif' font-size='28' fill='white' text-anchor='middle' dy='.3em'%3EAI Career Assistant%3C/text%3E%3C/svg%3E"
                >
                  <source src="https://files.catbox.moe/der0ln.mp4" type="video/mp4" />
                  Your browser does not support the video tag.
                </video>
              </div>
              
              {/* Floating elements */}
              <div className="absolute -top-3 -right-3 w-16 h-16 bg-gradient-to-r from-cyan-400 to-purple-400 rounded-full opacity-30 blur-xl animate-float"></div>
              <div className="absolute -bottom-3 -left-3 w-20 h-20 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full opacity-25 blur-xl animate-float-delayed"></div>
            </div>

            {/* Feature highlights */}
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/20 hover:bg-white/15 transition-all duration-300 hover:scale-105">
                <div className="w-12 h-12 bg-gradient-to-r from-cyan-400 to-purple-400 rounded-lg mb-3 flex items-center justify-center">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <h3 className="text-white font-semibold mb-1">AI Insights</h3>
                <p className="text-gray-400 text-sm">Deep learning analysis</p>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/20 hover:bg-white/15 transition-all duration-300 hover:scale-105">
                <div className="w-12 h-12 bg-gradient-to-r from-purple-400 to-pink-400 rounded-lg mb-3 flex items-center justify-center">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                  </svg>
                </div>
                <h3 className="text-white font-semibold mb-1">Career Growth</h3>
                <p className="text-gray-400 text-sm">Personalized roadmaps</p>
              </div>
            </div>
          </div>

          {/* Right Side - Upload Form */}
          <div className="w-full">
            <div className="relative">
              <div className="absolute -inset-1 bg-gradient-to-r from-cyan-500 via-purple-500 to-pink-500 rounded-3xl blur-sm opacity-25"></div>
              <div className="relative bg-white/10 backdrop-blur-xl rounded-3xl border border-white/30 p-6 lg:p-8">
                
                {/* Form Header */}
                <div className="text-center mb-8">
                  <div className="w-16 h-16 bg-gradient-to-r from-cyan-400 to-purple-400 rounded-xl mx-auto mb-4 flex items-center justify-center">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                  </div>
                  <h3 className="text-3xl font-bold text-white mb-3">
                    Upload Your CV
                  </h3>
                  <p className="text-gray-300 text-lg">
                    Get instant AI analysis and unlock your career potential
                  </p>
                </div>

                {/* File Upload Area */}
                <div
                  className={`relative border-2 border-dashed rounded-2xl p-8 text-center transition-all duration-300 ${
                    dragActive 
                      ? 'border-cyan-400 bg-cyan-500/20 scale-105' 
                      : selectedFile 
                        ? 'border-green-400 bg-green-500/20' 
                        : 'border-white/40 hover:border-purple-400 hover:bg-purple-500/10 hover:scale-102'
                  }`}
                  onDrop={handleDrop}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                >
                  <input
                    type="file"
                    accept=".pdf"
                    onChange={handleFileInputChange}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    id="cv-upload"
                  />
                  
                  <div className="space-y-4">
                    {selectedFile ? (
                      <>
                        <div className="w-16 h-16 mx-auto bg-green-500/30 rounded-full flex items-center justify-center border-2 border-green-400">
                          <svg className="w-8 h-8 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                        </div>
                        <div>
                          <p className="text-green-400 font-medium text-lg">{selectedFile.name}</p>
                          <p className="text-green-300 text-sm">
                            {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                          </p>
                        </div>
                      </>
                    ) : (
                      <>
                        <div className="w-16 h-16 mx-auto bg-purple-500/30 rounded-full flex items-center justify-center border-2 border-purple-400/60">
                          <svg className="w-8 h-8 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                          </svg>
                        </div>
                        <div>
                          <p className="text-xl font-semibold text-white mb-2">
                            Drag & drop your CV here
                          </p>
                          <p className="text-gray-300 mb-2">
                            or{' '}
                            <label htmlFor="cv-upload" className="text-cyan-400 hover:text-cyan-300 cursor-pointer font-medium underline underline-offset-2 transition-colors">
                              browse files
                            </label>
                          </p>
                          <p className="text-sm text-gray-400">
                            PDF files only, max 10MB
                          </p>
                        </div>
                      </>
                    )}
                  </div>
                </div>

                {/* Analysis Button */}
                <button
                  onClick={handleAnalyze}
                  disabled={!selectedFile || isAnalyzing}
                  className={`w-full mt-8 py-4 px-6 rounded-xl font-bold text-lg transition-all duration-300 ${
                    selectedFile && !isAnalyzing
                      ? 'bg-gradient-to-r from-cyan-500 via-purple-500 to-pink-500 hover:from-cyan-400 hover:via-purple-400 hover:to-pink-400 text-white shadow-lg shadow-purple-500/30 hover:shadow-xl hover:shadow-purple-500/40 hover:scale-105 bg-200%'
                      : 'bg-gray-700/50 text-gray-500 cursor-not-allowed border border-gray-600/50'
                  }`}
                >
                  {isAnalyzing ? (
                    <div className="flex items-center justify-center space-x-3">
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Analyzing CV...</span>
                    </div>
                  ) : (
                    <div className="flex items-center justify-center space-x-2">
                      <span>Analyze My CV</span>
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                      </svg>
                    </div>
                  )}
                </button>

                {/* Features List */}
                <div className="mt-8 space-y-4">
                  <h4 className="font-bold text-white text-lg mb-4">What you'll discover:</h4>
                  <div className="space-y-3">
                    {[
                      { icon: '🎯', title: 'Skills Gap Analysis', desc: 'Identify missing skills in your field' },
                      { icon: '🚀', title: 'Career Path Recommendations', desc: 'Personalized growth roadmap' },
                      { icon: '📊', title: 'Industry Insights', desc: 'Latest trends and opportunities' },
                      { icon: '💡', title: 'Interview Preparation', desc: 'AI-powered interview coaching' },
                      { icon: '💰', title: 'Salary Benchmarking', desc: 'Know your market value' }
                    ].map((feature, index) => (
                      <div key={index} className="flex items-center space-x-4 p-3 rounded-lg bg-white/5 border border-white/10 hover:bg-white/10 transition-all duration-200 hover:scale-105">
                        <div className="text-xl flex-shrink-0">{feature.icon}</div>
                        <div className="flex-grow">
                          <h5 className="text-white font-medium text-sm">{feature.title}</h5>
                          <p className="text-gray-400 text-xs">{feature.desc}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
