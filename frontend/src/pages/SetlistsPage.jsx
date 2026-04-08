import React, { useState, useEffect } from 'react';
import { setlistsAPI } from '../services/api';

export default function SetlistsPage() {
  const [setlists, setSetlists] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSetlists();
  }, []);

  const loadSetlists = async () => {
    try {
      const response = await setlistsAPI.getAll();
      setSetlists(response.data);
    } catch (error) {
      console.error('Failed to load setlists:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading setlists...</div>;

  return (
    <div>
      <div className="flex-between mb-4">
        <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>Setlists</h2>
      </div>

      <div className="grid">
        {setlists.map(setlist => (
          <div key={setlist.id} className="card">
            <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold' }}>{setlist.name}</h3>
            {setlist.description && <p className="text-secondary">{setlist.description}</p>}
            <div className="flex gap-2 mt-4" style={{ flexWrap: 'wrap' }}>
              {setlist.vibe && <span className="badge badge-primary">{setlist.vibe}</span>}
              {setlist.target_duration_minutes && (
                <span className="badge badge-secondary">{setlist.target_duration_minutes} min</span>
              )}
              <span className="badge badge-secondary">{setlist.track_order.length} tracks</span>
            </div>
            {setlist.ai_notes && (
              <div className="mt-4" style={{ padding: '1rem', background: 'var(--bg-input)', borderRadius: '0.5rem' }}>
                <p className="text-sm">{setlist.ai_notes}</p>
              </div>
            )}
          </div>
        ))}
        {setlists.length === 0 && (
          <div className="card text-secondary" style={{ textAlign: 'center', padding: '3rem' }}>
            No setlists yet. Use the AI Generator to create your first setlist!
          </div>
        )}
      </div>
    </div>
  );
}
