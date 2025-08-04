import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import Profile from './components/Profile';
import Settings from './components/Settings';
import Notifications from './components/Notifications';

const App: React.FC = () => {
  return (
    <Router>
      <nav style={{ padding: '1rem', backgroundColor: '#222', color: '#fff' }}>
        <Link to="/" style={{ marginRight: '1rem', color: '#fff' }}>Dashboard</Link>
        <Link to="/profile" style={{ marginRight: '1rem', color: '#fff' }}>Profile</Link>
        <Link to="/settings" style={{ marginRight: '1rem', color: '#fff' }}>Settings</Link>
        <Link to="/notifications" style={{ color: '#fff' }}>Notifications</Link>
      </nav>
      <main style={{ padding: '1rem' }}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/notifications" element={<Notifications />} />
        </Routes>
      </main>
    </Router>
  );
};

export default App;
