// src/components/Therapy/TherapyPanel.jsx
import React from 'react';
import TherapyButton from './TherapyButton';
import './Therapy.css';

const TherapyPanel = ({ setView }) => {
  const therapyTypes = [
    {
      id: 'spineTherapy',
      image: '/assets/images/ribs.png',
      title: 'Spinal Therapy',
      link: '/video/squat'
    },
    {
      id: 'shoulderTherapy',
      image: '/assets/images/shoulder.png',
      title: 'Shoulder Therapy'
    },
    {
      id: 'hipTherapy',
      image: '/assets/images/hip.png',
      title: 'Hip Therapy'
    },
    {
      id: 'kneeTherapy',
      image: '/assets/images/knee.png',
      title: 'Knee Therapy'
    }
  ];

  const handleTherapyClick = (id) => {
    // Handle therapy selection
    console.log('Selected therapy:', id);
  };

  return (
    <div className="pt-panel">
      <h2>Select Therapy Type</h2>
      <div className="therapy-options">
        {therapyTypes.map((therapy) => (
          <TherapyButton
            key={therapy.id}
            {...therapy}
            onClick={() => handleTherapyClick(therapy.id)}
          />
        ))}
      </div>
      <button className="back-button" onClick={() => setView('options')}>
        Back
      </button>
    </div>
  );
};

export default TherapyPanel;