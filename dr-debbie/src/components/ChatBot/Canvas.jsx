// src/components/ChatBot/Canvas.jsx
import React, { useEffect, useRef } from 'react';

const Canvas = () => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    // Initialize Rive animation here
    const riveFilePath = 'https://ucarecdn.com/b4c208f8-0f4d-45f0-98cf-aad85f70b363/';
    
    const initRive = async () => {
      try {
        const { Rive } = await import('@rive-app/canvas');
        new Rive({
          src: riveFilePath,
          canvas: canvas,
          autoplay: true,
          stateMachines: 'State Machine 1',
          fit: 'cover',
          onLoad: (_) => {
            // Handle Rive animation loaded
          },
        });
      } catch (error) {
        console.error('Error loading Rive:', error);
      }
    };

    initRive();
  }, []);

  return <canvas ref={canvasRef} width="200" height="200" />;
};

export default Canvas;