// src/components/Therapy/TherapyButton.jsx
import React from 'react';

const TherapyButton = ({ id, image, title, link, onClick }) => {
  const handleClick = (e) => {
    if (link) {
      // Handle navigation if link exists
      // You might want to use React Router here
      console.log('Navigating to:', link);
    }
    onClick();
  };

  return (
    <button className="therapy-button" id={id} onClick={handleClick}>
      <img src={image} alt={title} />
      <p>{title}</p>
    </button>
  );
};

export default TherapyButton;