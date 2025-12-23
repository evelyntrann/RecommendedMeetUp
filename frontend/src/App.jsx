import React, { useState } from 'react';
import axios from 'axios';
import { Coffee, MapPin, Star, Info } from 'lucide-react';

function App() {
  const [coords, setCoords] = useState({
    user_a_lat: 37.7749, user_a_lon: -122.4194,
    user_b_lat: 37.7849, user_b_lon: -122.4094
  });
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFindMeetup = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/v1/calculate-meetup', coords);
      setResults(response.data);
    } catch (error) {
      console.error("Error fetching meetup:", error);
      alert("Backend connection failed. Make sure FastAPI is running!");
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif', maxWidth: '600px', margin: '0 auto' }}>
      <h1>📍 Meetup Tester</h1>
      
      <div style={{ display: 'grid', gap: '10px', marginBottom: '20px', border: '1px solid #ddd', padding: '15px', borderRadius: '8px' }}>
        <h3>Enter Coordinates</h3>
        <div>
          User A: 
          <input type="number" value={coords.user_a_lat} onChange={e => setCoords({...coords, user_a_lat: parseFloat(e.target.value)})} />
          <input type="number" value={coords.user_a_lon} onChange={e => setCoords({...coords, user_a_lon: parseFloat(e.target.value)})} />
        </div>
        <div>
          User B: 
          <input type="number" value={coords.user_b_lat} onChange={e => setCoords({...coords, user_b_lat: parseFloat(e.target.value)})} />
          <input type="number" value={coords.user_b_lon} onChange={e => setCoords({...coords, user_b_lon: parseFloat(e.target.value)})} />
        </div>
        <button onClick={handleFindMeetup} disabled={loading} style={{ padding: '10px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
          {loading ? 'Searching...' : 'Find Meetup Spots'}
        </button>
      </div>

      {results && (
        <div>
          <h3>Results</h3>
          <p><strong>Midpoint:</strong> {results.midpoint.latitude.toFixed(4)}, {results.midpoint.longitude.toFixed(4)}</p>
          {results.recommendations.map((venue, index) => (
            <div key={index} style={{ borderBottom: '1px solid #eee', padding: '10px 0' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Coffee size={18} />
                <strong>{venue.name}</strong>
              </div>
              <div style={{ fontSize: '0.9em', color: '#666' }}>{venue.address}</div>
              <div style={{ display: 'flex', gap: '10px', marginTop: '5px' }}>
                <span style={{ fontSize: '0.8em', backgroundColor: '#f0f0f0', padding: '2px 6px', borderRadius: '4px' }}>
                  ⭐ {venue.google_rating}
                </span>
                {venue.tags.map(tag => (
                  <span key={tag} style={{ fontSize: '0.8em', backgroundColor: '#e3f2fd', color: '#1976d2', padding: '2px 6px', borderRadius: '4px' }}>
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;