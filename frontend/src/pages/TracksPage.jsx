import React, { useState, useEffect } from 'react';
import { tracksAPI } from '../services/api';

export default function TracksPage() {
  const [tracks, setTracks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    artist: '',
    bpm: 120,
    key: '8A',
    energy_level: 5,
    genre: '',
    duration_seconds: '',
    tags: [],
  });

  useEffect(() => {
    loadTracks();
  }, []);

  const loadTracks = async () => {
    try {
      const response = await tracksAPI.getAll();
      setTracks(response.data);
    } catch (error) {
      console.error('Failed to load tracks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await tracksAPI.create(formData);
      setFormData({ title: '', artist: '', bpm: 120, key: '8A', energy_level: 5, genre: '', duration_seconds: '', tags: [] });
      setShowForm(false);
      loadTracks();
    } catch (error) {
      console.error('Failed to create track:', error);
      alert('Failed to create track');
    }
  };

  const handleDelete = async (id) => {
    if (confirm('Delete this track?')) {
      try {
        await tracksAPI.delete(id);
        loadTracks();
      } catch (error) {
        console.error('Failed to delete track:', error);
      }
    }
  };

  if (loading) return <div>Loading tracks...</div>;

  return (
    <div>
      <div className="flex-between mb-4">
        <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>Music Library</h2>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Add Track'}
        </button>
      </div>

      {showForm && (
        <div className="card mb-4">
          <h3 className="mb-4">Add New Track</h3>
          <form onSubmit={handleSubmit} className="grid grid-2">
            <div>
              <label className="text-sm text-secondary">Title *</label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                required
              />
            </div>
            <div>
              <label className="text-sm text-secondary">Artist *</label>
              <input
                type="text"
                value={formData.artist}
                onChange={(e) => setFormData({ ...formData, artist: e.target.value })}
                required
              />
            </div>
            <div>
              <label className="text-sm text-secondary">BPM *</label>
              <input
                type="number"
                step="0.1"
                value={formData.bpm}
                onChange={(e) => setFormData({ ...formData, bpm: parseFloat(e.target.value) })}
                required
              />
            </div>
            <div>
              <label className="text-sm text-secondary">Key (Camelot) *</label>
              <select
                value={formData.key}
                onChange={(e) => setFormData({ ...formData, key: e.target.value })}
                required
              >
                {['1A','2A','3A','4A','5A','6A','7A','8A','9A','10A','11A','12A',
                  '1B','2B','3B','4B','5B','6B','7B','8B','9B','10B','11B','12B'].map(k => (
                  <option key={k} value={k}>{k}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-sm text-secondary">Energy Level (1-10) *</label>
              <input
                type="number"
                min="1"
                max="10"
                value={formData.energy_level}
                onChange={(e) => setFormData({ ...formData, energy_level: parseInt(e.target.value) })}
                required
              />
            </div>
            <div>
              <label className="text-sm text-secondary">Genre</label>
              <input
                type="text"
                value={formData.genre}
                onChange={(e) => setFormData({ ...formData, genre: e.target.value })}
              />
            </div>
            <div>
              <label className="text-sm text-secondary">Duration (seconds)</label>
              <input
                type="number"
                step="0.1"
                value={formData.duration_seconds}
                onChange={(e) => setFormData({ ...formData, duration_seconds: parseFloat(e.target.value) || null })}
              />
            </div>
            <div style={{ display: 'flex', alignItems: 'flex-end' }}>
              <button type="submit" className="btn-primary" style={{ width: '100%' }}>
                Add Track
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="grid">
        {tracks.map(track => (
          <div key={track.id} className="card">
            <div className="flex-between">
              <div>
                <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold' }}>{track.title}</h3>
                <p className="text-secondary">{track.artist}</p>
              </div>
              <button className="btn-secondary" onClick={() => handleDelete(track.id)}>
                Delete
              </button>
            </div>
            <div className="flex gap-2 mt-4" style={{ flexWrap: 'wrap' }}>
              <span className="badge badge-primary">{track.bpm} BPM</span>
              <span className="badge badge-primary">{track.key}</span>
              <span className="badge badge-secondary">Energy: {track.energy_level}/10</span>
              {track.genre && <span className="badge badge-secondary">{track.genre}</span>}
            </div>
          </div>
        ))}
        {tracks.length === 0 && (
          <div className="card text-secondary" style={{ textAlign: 'center', padding: '3rem' }}>
            No tracks yet. Add your first track to get started!
          </div>
        )}
      </div>
    </div>
  );
}
