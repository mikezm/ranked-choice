import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Home: React.FC = () => {
  const [apiStatus, setApiStatus] = useState<string>('Loading...');

  useEffect(() => {
    // Check API health when component mounts
    const checkApiHealth = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/health/`);
        if (response.data.status === 'ok') {
          setApiStatus('API is running');
        } else {
          setApiStatus('API returned unexpected response');
        }
      } catch (error) {
        setApiStatus('API is not available');
        console.error('Error checking API health:', error);
      }
    };

    checkApiHealth();
  }, []);

  return (
    <div className="home-container">
      <h1>Ranked Choice Voting App</h1>
      <p>Welcome to the Ranked Choice Voting application!</p>
      <div className="api-status">
        <h3>API Status:</h3>
        <p>{apiStatus}</p>
      </div>
    </div>
  );
};

export default Home;