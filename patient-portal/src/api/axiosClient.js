import axios from 'axios';

// Vite exposes env vars prefixed with VITE_ via import.meta.env.
// Locally, no VITE_API_URL is set, so it falls back to localhost.
// On Vercel, we'll set VITE_API_URL to your Render backend's URL.
const axiosClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api',
});

export default axiosClient;