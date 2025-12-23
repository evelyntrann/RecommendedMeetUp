import React, { useState } from 'react';
import axios from 'axios';
import { Coffee, MapPin, Star, Navigation } from 'lucide-react';

function App() {
  const [addresses, setAddresses] = useState({
    user_a_address: "1004 11th NE Street, Bellevue, WA",
    user_b_address: "Pike Place Market, Seattle, WA"
  });
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFindMeetup = async () => {
    setLoading(true);
    try {
      // Sending the addresses object to your updated FastAPI endpoint
      const response = await axios.post('http://127.0.0.1:8000/v1/calculate-meetup', addresses);      
      setResults(response.data);
    } catch (error) {
      console.error("Error fetching meetup:", error);
      alert("Backend connection failed. Make sure FastAPI is running and addresses are valid!");
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif', maxWidth: '700px', margin: '0 auto' }}>
      <h1>📍 Meetup Address Tester</h1>
      
      <div style={{ display: 'grid', gap: '15px', marginBottom: '20px', border: '1px solid #ddd', padding: '20px', borderRadius: '12px', backgroundColor: '#f9f9f9' }}>
        <h3>Enter Locations</h3>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
          <label><strong>User A Address:</strong></label>
          <input 
            type="text" 
            style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
            value={addresses.user_a_address} 
            onChange={e => setAddresses({...addresses, user_a_address: e.target.value})} 
          />
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
          <label><strong>User B Address:</strong></label>
          <input 
            type="text" 
            style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
            value={addresses.user_b_address} 
            onChange={e => setAddresses({...addresses, user_b_address: e.target.value})} 
          />
        </div>

        <button 
          onClick={handleFindMeetup} 
          disabled={loading} 
          style={{ 
            padding: '12px', 
            backgroundColor: loading ? '#ccc' : '#007bff', 
            color: 'white', 
            border: 'none', 
            borderRadius: '6px', 
            cursor: 'pointer',
            fontWeight: 'bold'
          }}
        >
          {loading ? 'Converting Addresses & Searching...' : 'Find Meetup Spots'}
        </button>
      </div>

      {results && (
        <div>
          <div style={{ backgroundColor: '#e8f5e9', padding: '15px', borderRadius: '8px', marginBottom: '20px' }}>
            <h4 style={{ margin: '0 0 10px 0' }}><Navigation size={18} /> Geocoding Result</h4>
            <p style={{ fontSize: '0.9em', margin: '2px 0' }}><strong>Midpoint:</strong> {results.midpoint.latitude.toFixed(4)}, {results.midpoint.longitude.toFixed(4)}</p>
          </div>

          <h3>Recommended Spots</h3>
          {results.recommendations.length > 0 ? (
            results.recommendations.map((venue, index) => (
              <div key={index} style={{ borderBottom: '1px solid #eee', padding: '15px 0' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Coffee size={18} color="#6f4e37" />
                  <strong style={{ fontSize: '1.1em' }}>{venue.name}</strong>
                </div>
                <div style={{ fontSize: '0.9em', color: '#666', marginTop: '4px' }}>
                  <MapPin size={14} style={{ marginRight: '4px' }} />
                  {venue.address}
                </div>
                <div style={{ display: 'flex', gap: '10px', marginTop: '8px' }}>
                  <span style={{ fontSize: '0.8em', backgroundColor: '#fff9c4', color: '#f57f17', padding: '4px 8px', borderRadius: '4px', border: '1px solid #fbc02d' }}>
                    ⭐ {venue.google_rating}
                  </span>
                  {venue.tags.map(tag => (
                    <span key={tag} style={{ fontSize: '0.8em', backgroundColor: '#e3f2fd', color: '#1976d2', padding: '4px 8px', borderRadius: '4px' }}>
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            ))
          ) : (
            <p>No cafes found near this midpoint. Try increasing the search radius in the backend!</p>
          )}
        </div>
      )}
    </div>
  );
}

export default App;