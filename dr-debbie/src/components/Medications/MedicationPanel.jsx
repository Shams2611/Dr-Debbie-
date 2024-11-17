// src/components/Medications/MedicationPanel.jsx
import React, { useState } from 'react';
import MedicationItem from './MedicationItem';
import './Medications.css';

const MedicationPanel = ({ setView }) => {
  const [medications, setMedications] = useState([]);

  const addMedication = () => {
    setMedications([...medications, {
      name: '',
      days: [false, false, false, false, false, false, false],
      time: 'Morning',
      image: null
    }]);
  };

  const handleSubmit = () => {
    // Handle medication submission
    console.log('Submitting medications:', medications);
  };

  return (
    <div className="meds-panel">
      <h2>Medication Tracker</h2>
      <button id="add-medication" onClick={addMedication}>
        Add Medication
      </button>
      <div id="medication-list">
        {medications.map((med, index) => (
          <MedicationItem 
            key={index}
            medication={med}
            onChange={(updatedMed) => {
              const newMeds = [...medications];
              newMeds[index] = updatedMed;
              setMedications(newMeds);
            }}
          />
        ))}
      </div>
      <button id="submit-log" onClick={handleSubmit}>
        Submit Log
      </button>
      <button className="back-button" onClick={() => setView('options')}>
        Back
      </button>
    </div>
  );
};

export default MedicationPanel;