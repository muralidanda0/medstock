import { useState, useEffect } from 'react';
import axiosClient from '../api/axiosClient';

function DashboardPage({ onLogout }) {
  const [inventory, setInventory] = useState([]);
  const [selectedItemId, setSelectedItemId] = useState('');
  const [quantity, setQuantity] = useState(1);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const loadInventory = async () => {
    try {
      const response = await axiosClient.get('/inventory/mine/');
      setInventory(response.data);
    } catch (err) {
      setError('Could not load inventory. Are you logged in as a pharmacy user?');
      console.error(err);
    }
  };

  useEffect(() => {
    loadInventory();
  }, []);

  const handleCreateInvoice = async (e) => {
    e.preventDefault();
    setMessage('');
    setError('');

    try {
      const response = await axiosClient.post('/billing/invoices/', {
        pharmacy_id: JSON.parse(localStorage.getItem('pharmacy_id')),
        payment_method: 'CASH',
        items: [
          {
            inventory_item_id: parseInt(selectedItemId),
            quantity: parseInt(quantity),
          },
        ],
      });
      setMessage(`Invoice #${response.data.invoice_id} created — total ₹${response.data.total_amount}`);
      loadInventory();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create invoice — check stock quantity.');
      console.error(err);
    }
  };

  return (
    <div style={{ maxWidth: 700, margin: '40px auto', fontFamily: 'sans-serif' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
        <h1>Pharmacy Dashboard</h1>
        <button onClick={onLogout}>Log Out</button>
      </div>

      <h2>Your Inventory</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ textAlign: 'left' }}>Medicine</th>
            <th style={{ textAlign: 'left' }}>Quantity</th>
            <th style={{ textAlign: 'left' }}>Price</th>
          </tr>
        </thead>
        <tbody>
          {inventory.map((item) => (
            <tr key={item.id}>
              <td>{item.medicine_name}</td>
              <td>{item.quantity}</td>
              <td>₹{item.price}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2 style={{ marginTop: 32 }}>Generate Bill</h2>
      <form onSubmit={handleCreateInvoice}>
        <select
          value={selectedItemId}
          onChange={(e) => setSelectedItemId(e.target.value)}
          style={{ padding: 8, marginRight: 8 }}
          required
        >
          <option value="">Select medicine...</option>
          {inventory.map((item) => (
            <option key={item.id} value={item.id}>
              {item.medicine_name} ({item.quantity} available)
            </option>
          ))}
        </select>
        <input
          type="number"
          min="1"
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
          style={{ padding: 8, width: 80, marginRight: 8 }}
        />
        <button type="submit" style={{ padding: 8 }}>
          Generate Invoice
        </button>
      </form>

      {message && <p style={{ color: 'green', marginTop: 16 }}>{message}</p>}
    </div>
  );
}

export default DashboardPage;