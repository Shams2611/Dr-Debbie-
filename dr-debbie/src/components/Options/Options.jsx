// src/components/Options/Options.jsx
import React from 'react';
import './Options.css';

const Options = ({ setView, userInfo }) => {
  return (
    <div className="options-panel">
      <div className="options-buttons">
        <button onClick={() => setView('therapy')} className="option-button">
          Physical Therapy
        </button>
        <button onClick={() => setView('medications')} className="option-button">
          Medications
        </button>
      </div>
    </div>
  );
};

export default Options;