import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Home from './pages/Home';
import BallotDetail from './pages/BallotDetail';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/ballot/:slug" element={<BallotDetail />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
