import React, { useState } from 'react';
import './PrescriptionScanner.css';

const PrescriptionScanner = ({ onResult, onClose }) => {
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (file) {
      setLoading(true);
      setError(null);
      
      try {
        // Convert image to base64
        const base64Image = await fileToBase64(file);
        
        // Call Gemini API
        const response = await fetch('/api/analyze-prescription', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ image: base64Image }),
        });

        if (!response.ok) throw new Error('Failed to analyze prescription');

        const data = await response.json();
        onResult(data.medications);
      } catch (err) {
        setError('Failed to process prescription. Please try again or add medications manually.');
        console.error('Prescription scanning error:', err);
      } finally {
        setLoading(false);
      }
    }
  };

  const fileToBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result.split(',')[1]);
      reader.onerror = error => reject(error);
    });
  };

  return (
    <div className="scanner-overlay">
      <div className="scanner-content">
        <h3>Scan Prescription</h3>
        <input
          type="file"
          accept="image/*"
          onChange={handleImageUpload}
          className="file-input"
        />
        {loading && <div className="loading">Processing prescription...</div>}
        {error && <div className="error">{error}</div>}
        <button onClick={onClose} className="close-button">Cancel</button>
      </div>
    </div>
  );
};

export default PrescriptionScanner;