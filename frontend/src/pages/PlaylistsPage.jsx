import React, { useState, useEffect } from 'react';
import { playlistsAPI, tracksAPI } from '../services/api';

export default function PlaylistsPage() {
  const [playlists, setPlaylists] = useState([]);
  const [allTracks, setAllTracks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({ name: '', description: '' });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [playlistsRes, tracksRes] = await Promise.all([
        playlistsAPI.getAll(),
        tracksAPI.getAll(),
      ]);
      setPlaylists(playlistsRes.data);
      setAllTracks(tracksRes.data);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await playlistsAPI.create(formData);
      setFormData({ name: '', description: '' });
      setShowForm(false);
      loadData();
    } catch (error) {
      console.error('Failed to create playlist:', error);
    }
  };

  if (loading) return <div>Loading playlists...</div>;

  return (
    <div>
      <div className="flex-between mb-4">
        <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>Playlists</h2>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Create Playlist'}
        </button>
      </div>

      {showForm && (
        <div className="card mb-4">
          <form onSubmit={handleSubmit} className="grid grid-2">
            <div>
              <label className="text-sm text-secondary">Playlist Name *</label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
              />
            </div>
            <div>
              <label className="text-sm text-secondary">Description</label>
              <input
                type="text"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              />
            </div>
            <button type="submit" className="btn-primary">Create Playlist</button>
          </form>
        </div>
      )}

      <div className="grid">
        {playlists.map(playlist => (
          <div key={playlist.id} className="card">
            <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold' }}>{playlist.name}</h3>
            {playlist.description && <p className="text-secondary">{playlist.description}</p>}
            <p className="text-sm text-secondary mt-4">
              Created: {new Date(playlist.created_at).toLocaleDateString()}
            </p>
          </div>
        ))}
        {playlists.length === 0 && (
          <div className="card text-secondary" style={{ textAlign: 'center', padding: '3rem' }}>
            No playlists yet. Create your first playlist!
          </div>
        )}
      </div>

      {allTracks.length === 0 && (
        <div className="card mt-4" style={{ background: 'var(--warning)', color: '#000' }}>
          💡 Tip: Add some tracks in the Tracks page first to build playlists.
        </div>
      )}
    </div>
  );
}
