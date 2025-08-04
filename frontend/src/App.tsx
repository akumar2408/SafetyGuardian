import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import Profile from './components/Profile';
import Settings from './components/Settings';
import Notifications from './components/Notifications';
import Login from './components/Login';
import Register from './components/Register';
import AIFeatures from './components/AIFeatures';

const App: React.FC = () => {
  return (
    <Router>
      <nav style={{ padding: '1rem', backgroundColor: '#222', color: '#fff' }}>
        <Link to="/" style={{ marginRight: '1rem', color: '#fff' }}>Dashboard</Link>
        <Link to="/profile" style={{ marginRight: '1rem', color: '#fff' }}>Profile</Link>
        <Link to="/settings" style={{ marginRight: '1rem', color: '#fff' }}>Settings</Link>
        <Link to="/notifications" style={{ marginRight: '1rem', color: '#fff' }}>Notifications</Link>
        <Link to="/ai" style={{ marginRight: '1rem', color: '#fff' }}>AI Features</Link>
        <Link to="/login" style={{ marginRight: '1rem', color: '#fff' }}>Login</Link>
        <Link to="/register" style={{ marginRight: '1rem', color: '#fff' }}>Register</Link>
      </nav>
      <main style={{ padding: '1rem' }}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/notifications" element={<Notifications />} />
          <Route path="/ai" element={<AIFeatures />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </main>
    </Router>
  );
};

export default App;
