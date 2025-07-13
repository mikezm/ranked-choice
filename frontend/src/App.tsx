import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Home from './pages/Home';
import BallotDetail from './pages/BallotDetail';
import BallotResult from './pages/BallotResult';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/ballot/:slug" element={<BallotDetail />} />
          <Route path="/ballot/results/:slug" element={<BallotResult />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
