import React, { useState, useEffect } from 'react';
import { setlistsAPI, tracksAPI } from '../services/api';

export default function SetlistsPage() {
  const [setlists, setSetlists] = useState([]);
  const [allTracks, setAllTracks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedSetlist, setSelectedSetlist] = useState(null);
  const [setlistTracks, setSetlistTracks] = useState([]);

  useEffect(() => {
    loadSetlists();
  }, []);

  const loadSetlists = async () => {
    try {
      const [setlistsRes, tracksRes] = await Promise.all([
        setlistsAPI.getAll(),
        tracksAPI.getAll(),
      ]);
      setSetlists(setlistsRes.data);
      setAllTracks(tracksRes.data);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectSetlist = async (setlist) => {
    if (selectedSetlist?.id === setlist.id) {
      setSelectedSetlist(null);
      setSetlistTracks([]);
      return;
    }
    setSelectedSetlist(setlist);
    
    // Get tracks from the track_order
    const trackIds = setlist.track_order || [];
    const tracks = allTracks.filter(track => trackIds.includes(track.id));
    setSetlistTracks(tracks);
  };

  if (loading) return <div>Loading setlists...</div>;

  return (
    <div>
      <div className="flex-between mb-4">
        <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>Setlists</h2>
      </div>

      <div className="grid" style={{ gridTemplateColumns: selectedSetlist ? '1fr 1fr' : '1fr' }}>
        {/* Setlist List */}
        <div>
          {setlists.map(setlist => (
            <div 
              key={setlist.id} 
              className="card mb-4"
              style={{ 
                cursor: 'pointer',
                border: selectedSetlist?.id === setlist.id ? '2px solid var(--accent)' : '1px solid var(--border)'
              }}
              onClick={() => handleSelectSetlist(setlist)}
            >
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

        {/* Selected Setlist Details */}
        {selectedSetlist && (
          <div>
            <div className="card">
              <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', marginBottom: '1.5rem' }}>
                Tracks in "{selectedSetlist.name}"
              </h3>

              {setlistTracks.length === 0 ? (
                <p className="text-secondary">No tracks in this setlist.</p>
              ) : (
                <div>
                  {setlistTracks.map((track, index) => (
                    <div 
                      key={track.id}
                      className="flex-between mb-2"
                      style={{ 
                        padding: '0.75rem', 
                        background: 'var(--bg-card)',
                        borderRadius: '0.5rem',
                        border: '1px solid var(--border)'
                      }}
                    >
                      <div className="flex gap-4">
                        <span className="text-secondary" style={{ minWidth: '2rem' }}>#{index + 1}</span>
                        <div>
                          <strong>{track.title}</strong> - {track.artist}
                          <div className="text-sm text-secondary">
                            {track.bpm} BPM | {track.key} | Energy: {track.energy}/10 | {track.genre}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
