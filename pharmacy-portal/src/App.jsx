import { useState } from 'react';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import axiosClient from './api/axiosClient';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('access_token'));

  const handleLoginSuccess = async () => {
    try {
      const response = await axiosClient.get('/pharmacies/me/');
      localStorage.setItem('pharmacy_id', JSON.stringify(response.data.id));
    } catch (err) {
      console.error('Could not fetch pharmacy profile', err);
    }
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('pharmacy_id');
    setIsLoggedIn(false);
  };

  return isLoggedIn ? (
    <DashboardPage onLogout={handleLogout} />
  ) : (
    <LoginPage onLoginSuccess={handleLoginSuccess} />
  );
}

export default App;