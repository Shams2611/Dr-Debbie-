// src/components/Medications/MedicationItem.jsx
import React, { useState } from 'react';

const MedicationItem = ({ medication, onChange }) => {
  const [imagePreview, setImagePreview] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target.result);
        onChange({ ...medication, image: file });
      };
      reader.readAsDataURL(file);
    }
  };

  const handleDayChange = (index) => {
    const newDays = [...medication.days];
    newDays[index] = !newDays[index];
    onChange({ ...medication, days: newDays });
  };

  return (
    <div className="medication">
      <input
        type="text"
        placeholder="Medication Name"
        className="medication-name"
        value={medication.name}
        onChange={(e) => onChange({ ...medication, name: e.target.value })}
      />
      <div className="medication-details">
        <div className="medication-schedule">
          <div className="days">
            {['M', 'T', 'W', 'T', 'F', 'S', 'S'].map((day, index) => (
              <label key={index}>
                <input
                  type="checkbox"
                  checked={medication.days[index]}
                  onChange={() => handleDayChange(index)}
                />
                <span>{day}</span>
              </label>
            ))}
          </div>
          <div className="form-row">
            <div className="time-select-wrapper">
              <div className="time-select" data-time={medication.time}>
                <select
                  value={medication.time}
                  onChange={(e) => onChange({ ...medication, time: e.target.value })}
                >
                  <option value="Morning">Morning</option>
                  <option value="Day">Day</option>
                  <option value="Night">Night</option>
                </select>
              </div>
            </div>
            <div className="file-upload-wrapper">
              <input
                type="file"
                accept="image/*"
                className="image-upload"
                onChange={handleImageChange}
              />
              {imagePreview && (
                <div className="image-preview">
                  <img src={imagePreview} alt="Medication" />
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MedicationItem;