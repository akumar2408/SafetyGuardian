import React from 'react';

const Notifications: React.FC = () => {
  return (
    <div style={{ padding: '20px' }}>
      <h2>Notifications</h2>
      <p>View recent alerts and messages from the system.</p>
      <ul>
        <li>No new notifications.</li>
      </ul>
    </div>
  );
};

export default Notifications;
