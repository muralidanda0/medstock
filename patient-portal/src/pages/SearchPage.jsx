import { useState, useEffect } from 'react';
import axiosClient from '../api/axiosClient';

function SearchPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axiosClient.get('/inventory/search/', {
        params: { medicine: searchTerm },
      });
      setResults(response.data);
    } catch (err) {
      setError('Something went wrong while searching. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Runs ONCE when SearchPage first appears on screen. Opens a WebSocket
  // connection and keeps it alive for as long as this page is mounted.
  useEffect(() => {
const wsUrl = import.meta.env.VITE_WS_URL || 'ws://127.0.0.1:8000/ws/inventory/';
const socket = new WebSocket(wsUrl);
    socket.onopen = () => {
      console.log('WebSocket connected');
    };

    socket.onmessage = (event) => {
      const update = JSON.parse(event.data);
      console.log('Live inventory update received:', update);

      // Update ONLY the matching item in our current results list, using
      // its functional form of setState — React guarantees `prevResults`
      // is the latest state, avoiding stale-data bugs.
      setResults((prevResults) =>
        prevResults.map((item) =>
          item.id === update.inventory_id
            ? { ...item, quantity: update.quantity, price: update.price }
            : item
        )
      );
    };

    socket.onerror = (err) => {
      console.error('WebSocket error:', err);
    };

    // Cleanup function: runs when the component is removed from the
    // screen (e.g. navigating away). Without this, you'd leak an open
    // WebSocket connection every time this page re-mounts.
    return () => {
      socket.close();
    };
  }, []); // empty array = run this effect only once, on mount

  return (
    <div style={{ maxWidth: 600, margin: '40px auto', fontFamily: 'sans-serif' }}>
      <h1>MedStock — Search Medicines</h1>

      <form onSubmit={handleSearch} style={{ marginBottom: 24 }}>
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search medicine name..."
          style={{ padding: 8, width: '70%', marginRight: 8 }}
        />
        <button type="submit" style={{ padding: 8 }}>
          Search
        </button>
      </form>

      {loading && <p>Searching...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {results.length === 0 && !loading && !error && (
        <p>No results yet — try searching for a medicine above.</p>
      )}

      <ul style={{ listStyle: 'none', padding: 0 }}>
        {results.map((item) => (
          <li
            key={item.id}
            style={{
              border: '1px solid #ccc',
              borderRadius: 8,
              padding: 12,
              marginBottom: 12,
            }}
          >
            <strong>{item.medicine_name}</strong>
            <div>Pharmacy: {item.pharmacy_name} ({item.pharmacy_city})</div>
            <div>Price: ₹{item.price}</div>
            <div>Available: {item.quantity} units</div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default SearchPage;