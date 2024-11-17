// src/App.jsx
import React, { useState } from 'react';
import Header from './components/layout/Header/Header';
import ChatBot from './components/ChatBot/ChatBot';
import Welcome from './components/Welcome/Welcome';
import Options from './components/Options/Options';
import MedicationPanel from './components/Medications/MedicationPanel';
import TherapyPanel from './components/Therapy/TherapyPanel';
import './styles/global.css';

const App = () => {
  const [currentView, setCurrentView] = useState('welcome');
  const [userInfo, setUserInfo] = useState(null);

  const renderRightPanel = () => {
    switch(currentView) {
      case 'welcome':
        return <Welcome setView={setCurrentView} setUserInfo={setUserInfo} />;
      case 'options':
        return <Options setView={setCurrentView} />;
      case 'medications':
        return <MedicationPanel setView={setCurrentView} />;
      case 'therapy':
        return <TherapyPanel setView={setCurrentView} />;
      default:
        return <Welcome setView={setCurrentView} setUserInfo={setUserInfo} />;
    }
  };

  return (
    <div className="app">
      <Header />
      <main>
        <div className="left-column">
          <ChatBot />
        </div>
        <div className="right-column">
          {renderRightPanel()}
        </div>
      </main>
    </div>
  );
};

export default App;