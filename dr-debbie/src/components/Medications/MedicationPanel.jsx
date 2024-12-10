import React, { useState } from 'react';
import MedicationItem from './MedicationItem';
import PrescriptionScanner from './PrescriptionScanner';
import './Medications.css';

const MedicationPanel = ({ setView }) => {
  const [medications, setMedications] = useState([]);
  const [scanningMode, setScanningMode] = useState(false);

  const addMedication = () => {
    setMedications([...medications, {
      name: '',
      days: [false, false, false, false, false, false, false],
      time: 'Morning',
      image: null
    }]);
  };

  const handlePrescriptionResult = (prescriptionData) => {
    // Add medications from prescription scan
    const newMedications = prescriptionData.map(med => ({
      name: med.name,
      days: [true, true, true, true, true, true, true], // Default to every day
      time: med.timing || 'Morning',
      dosage: med.dosage,
      notes: med.instructions
    }));

    setMedications([...medications, ...newMedications]);
    setScanningMode(false);
  };

  const handleSubmit = () => {
    // Handle medication submission
    console.log('Submitting medications:', medications);
  };

  return (
    <div className="meds-panel">
      <h2>Medication Tracker</h2>
      <div className="input-methods">
        <button id="add-medication" onClick={addMedication}>
          Add Medication Manually
        </button>
        <button 
          id="scan-prescription" 
          onClick={() => setScanningMode(true)}
          className="scan-button"
        >
          Scan Prescription
        </button>
      </div>

      {scanningMode && (
        <PrescriptionScanner 
          onResult={handlePrescriptionResult}
          onClose={() => setScanningMode(false)}
        />
      )}

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

      {medications.length > 0 && (
        <button id="submit-log" onClick={handleSubmit}>
          Submit Log
        </button>
      )}
      
      <button className="back-button" onClick={() => setView('options')}>
        Back
      </button>
    </div>
  );
};

export default MedicationPanel;