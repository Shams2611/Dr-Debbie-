// src/components/Options/Options.jsx
import React from 'react';
import './Options.css';

const Options = ({ setView }) => {
  return (
    <div className="option-panel">
      <div className="option-buttons">
        <button 
          id="medsButton" 
          onClick={() => setView('medications')}
          aria-label="Medication Tracker"
        ></button>
        <button 
          id="ptButton" 
          onClick={() => setView('therapy')}
          aria-label="Physical Therapy"
        ></button>
      </div>
    </div>
  );
};

export default Options;