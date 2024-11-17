// src/components/Welcome/Welcome.jsx
import React, { useState, useEffect } from 'react';
import './Welcome.css';

const Welcome = ({ setView, setUserInfo }) => {
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    sex: ''
  });

  const [showStartButton, setShowStartButton] = useState(false);

  useEffect(() => {
    const isFormComplete = formData.name && formData.age && formData.sex;
    setShowStartButton(isFormComplete);
  }, [formData]);

  const handleSubmit = (e) => {
    e.preventDefault();
    setUserInfo(formData);
    setView('options');
  };

  return (
    <div className="welcome-buttons">
      <img 
        src="/assets/images/logo_penapps_design.png" 
        alt="Dr. Debbie Logo" 
        className="welcome-logo"
      />
      <form id="userForm" onSubmit={handleSubmit}>
        <label htmlFor="name">Name:</label>
        <input
          type="text"
          id="name"
          name="name"
          required
          value={formData.name}
          onChange={(e) => setFormData({...formData, name: e.target.value})}
        />

        <label htmlFor="age">Age:</label>
        <select
          id="age"
          name="age"
          required
          value={formData.age}
          onChange={(e) => setFormData({...formData, age: e.target.value})}
        >
          <option value="">Select your age</option>
          {[...Array(83)].map((_, i) => (
            <option key={i + 18} value={i + 18}>{i + 18}</option>
          ))}
        </select>

        <label htmlFor="sex">Biological Sex:</label>
        <select
          id="sex"
          name="sex"
          required
          value={formData.sex}
          onChange={(e) => setFormData({...formData, sex: e.target.value})}
        >
          <option value="">Select your biological sex</option>
          <option value="male">Male</option>
          <option value="female">Female</option>
          <option value="other">Other</option>
        </select>

        {showStartButton && (
          <button type="submit" id="startButton">
            Let's get started!
          </button>
        )}
      </form>
    </div>
  );
};

export default Welcome;