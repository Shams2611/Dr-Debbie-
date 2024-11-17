// src/components/layout/Header/Header.jsx
import React from 'react';
import './Header.css';

const Header = () => {
    return (
        <header className="header">
            <img 
                src="/assets/images/logo_penapps_design.png" 
                alt="Dr. Debbie Logo" 
                className="header-image"
            />
            <h1 className="header-text">Dr. Debbie</h1>
        </header>
    );
};

export default Header;