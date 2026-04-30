import React, { useState } from 'react';
import axios from 'axios';
import { Upload, Target, CheckCircle2, AlertCircle, Sparkles, FileText } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE = 'http://localhost:5000/api';

function App() {
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [jobDesc, setJobDesc] = useState('');
  const [matchData, setMatchData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileUpload = async (e) => {
    const uploadedFile = e.target.files[0];
    if (!uploadedFile) return;
    
    setFile(uploadedFile);
    setLoading(true);
    
    const formData = new FormData();
    formData.append('file', uploadedFile);

    try {
      const res = await axios.post(`${API_BASE}/analyze`, formData);
      setAnalysis(res.data);
    } catch (err) {
      alert("Analysis failed. Make sure the backend is running!");
    } finally {
      setLoading(false);
    }
  };

  const handleMatch = async () => {
    if (!jobDesc) return;
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/match`, { job_description: jobDesc });
      setMatchData(res.data);
    } catch (err) {
      console.error("Match Error:", err);
      alert(`Matching failed: ${err.response?.data?.error || err.message}`);
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="dashboard-container">
      <header className="header">
        <motion.h1 
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8 }}
        >
          AI Resume Assistant
        </motion.h1>
        <p style={{ color: 'var(--text-muted)', marginTop: '0.5rem' }}>
          Production-grade career optimization powered by NLP
        </p>
      </header>

      <div className="grid">
        {/* Upload Section */}
        <motion.div 
          className="glass-card full-width"
          whileHover={{ scale: 1.01 }}
        >
          <div style={{ textAlign: 'center' }}>
            <div style={{ marginBottom: '1.5rem', display: 'flex', justifyContent: 'center' }}>
              <div style={{ padding: '1rem', background: 'rgba(99, 102, 241, 0.1)', borderRadius: '50%' }}>
                <FileText size={48} color="var(--primary)" />
              </div>
            </div>
            <h2 style={{ marginBottom: '1rem' }}>Upload Your Resume</h2>
            <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>
              Drag and drop your PDF or DOCX file to get an instant AI analysis.
            </p>
            <label className="btn-primary" style={{ display: 'inline-flex' }}>
              <Upload size={20} />
              {file ? file.name : "Choose File"}
              <input type="file" hidden onChange={handleFileUpload} />
            </label>
          </div>
        </motion.div>

        {/* Analysis Result */}
        <AnimatePresence>
          {analysis && (
            <>
              <motion.div 
                initial={{ x: -100, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                className="glass-card"
              >
                <div className="score-circle">
                  {analysis.scoring.overall_score}
                </div>
                <h3 style={{ textAlign: 'center', marginTop: '1.5rem' }}>Quality Score</h3>
                <div style={{ marginTop: '2rem' }}>
                  <h4 style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <CheckCircle2 color="#4ade80" size={20} /> Strengths
                  </h4>
                  <ul style={{ list_style: 'none' }}>
                    {analysis.scoring.strengths.map((s, i) => (
                      <li key={i} style={{ fontSize: '0.9rem', marginBottom: '0.5rem', color: 'var(--text-muted)' }}>• {s}</li>
                    ))}
                  </ul>
                </div>
              </motion.div>

              <motion.div 
                initial={{ x: 100, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                className="glass-card"
              >
                <h3>Job Matching</h3>
                <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem', fontSize: '0.9rem' }}>
                  Paste a job description to see how well you align.
                </p>
                <textarea 
                  className="input-glow" 
                  rows="6" 
                  placeholder="Paste JD here..."
                  value={jobDesc}
                  onChange={(e) => setJobDesc(e.target.value)}
                />
                <button 
                  className="btn-primary" 
                  style={{ width: '100%', marginTop: '1rem' }}
                  onClick={handleMatch}
                  disabled={loading}
                >
                  <Target size={20} /> {loading ? "Analyzing..." : "Match Resume"}
                </button>

                {matchData && (
                  <motion.div 
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    style={{ marginTop: '2rem', padding: '1.5rem', background: 'rgba(99, 102, 241, 0.1)', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.3)' }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
                      <span style={{ fontWeight: 'bold' }}>Match Score:</span>
                      <span style={{ color: 'var(--accent)', fontWeight: '800' }}>{matchData.match_score}%</span>
                    </div>
                    <div className="h-2 w-full bg-slate-800 rounded-full" style={{ marginBottom: '1.5rem' }}>
                      <div 
                        className="h-full bg-accent rounded-full" 
                        style={{ width: `${matchData.match_score}%`, transition: 'width 1s ease', height: '4px', background: 'var(--accent)' }}
                      />
                    </div>
                    
                    {matchData.tailored_summary && (
                      <p style={{ fontSize: '0.85rem', color: 'var(--text-main)', marginBottom: '1rem', fontStyle: 'italic' }}>
                        "{matchData.tailored_summary}"
                      </p>
                    )}

                    {matchData.smart_suggestions && (
                      <div style={{ marginTop: '1rem' }}>
                        <h4 style={{ fontSize: '0.9rem', color: 'var(--primary)', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                          <Sparkles size={16} /> AI Suggestions
                        </h4>
                        <ul style={{ listStyle: 'none' }}>
                          {matchData.smart_suggestions.map((s, i) => (
                            <li key={i} style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.4rem' }}>→ {s}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </motion.div>
                )}
              </motion.div>

              {/* Skill Gaps & Action */}
              <motion.div 
                initial={{ y: 50, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                className="glass-card full-width"
              >
                <div>
                  <h3>Strategic Improvements</h3>
                  <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
                    {analysis.scoring.skill_gaps.slice(0, 5).map((gap, i) => (
                      <span key={i} className="badge badge-gap">{gap}</span>
                    ))}
                  </div>
                </div>
              </motion.div>
            </>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

export default App;
