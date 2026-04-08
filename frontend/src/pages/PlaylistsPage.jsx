import React, { useState, useEffect } from 'react';
import { playlistsAPI, tracksAPI } from '../services/api';

export default function PlaylistsPage() {
  const [playlists, setPlaylists] = useState([]);
  const [allTracks, setAllTracks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({ name: '', description: '' });
  const [selectedPlaylist, setSelectedPlaylist] = useState(null);
  const [playlistTracks, setPlaylistTracks] = useState([]);
  const [showTrackSelector, setShowTrackSelector] = useState(false);
  const [selectedTracks, setSelectedTracks] = useState([]);

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

  const handleSelectPlaylist = async (playlist) => {
    if (selectedPlaylist?.id === playlist.id) {
      setSelectedPlaylist(null);
      setPlaylistTracks([]);
      return;
    }
    setSelectedPlaylist(playlist);
    try {
      const res = await playlistsAPI.getById(playlist.id);
      setPlaylistTracks(res.data.tracks || []);
    } catch (error) {
      console.error('Failed to load playlist tracks:', error);
    }
  };

  const handleAddTracks = async () => {
    if (!selectedPlaylist || selectedTracks.length === 0) return;
    try {
      for (const trackId of selectedTracks) {
        await playlistsAPI.addTrack(selectedPlaylist.id, trackId);
      }
      setSelectedTracks([]);
      setShowTrackSelector(false);
      const res = await playlistsAPI.getById(selectedPlaylist.id);
      setPlaylistTracks(res.data.tracks || []);
    } catch (error) {
      console.error('Failed to add tracks:', error);
    }
  };

  const handleRemoveTrack = async (trackId) => {
    if (!selectedPlaylist) return;
    try {
      await playlistsAPI.removeTrack(selectedPlaylist.id, trackId);
      setPlaylistTracks(playlistTracks.filter(t => t.id !== trackId));
    } catch (error) {
      console.error('Failed to remove track:', error);
    }
  };

  const toggleTrackSelection = (trackId) => {
    setSelectedTracks(prev => 
      prev.includes(trackId) 
        ? prev.filter(id => id !== trackId)
        : [...prev, trackId]
    );
  };

  const getAvailableTracks = () => {
    const playlistTrackIds = new Set(playlistTracks.map(t => t.id));
    return allTracks.filter(t => !playlistTrackIds.has(t.id));
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

      <div className="grid" style={{ gridTemplateColumns: selectedPlaylist ? '1fr 1fr' : '1fr' }}>
        {/* Playlist List */}
        <div>
          {playlists.map(playlist => (
            <div 
              key={playlist.id} 
              className="card mb-4"
              style={{ 
                cursor: 'pointer',
                border: selectedPlaylist?.id === playlist.id ? '2px solid var(--accent)' : '1px solid var(--border)'
              }}
              onClick={() => handleSelectPlaylist(playlist)}
            >
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

        {/* Selected Playlist Details */}
        {selectedPlaylist && (
          <div>
            <div className="card mb-4">
              <div className="flex-between mb-4">
                <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold' }}>
                  Tracks in "{selectedPlaylist.name}"
                </h3>
                <button 
                  className="btn-primary"
                  onClick={() => setShowTrackSelector(!showTrackSelector)}
                >
                  {showTrackSelector ? 'Cancel' : '+ Add Tracks'}
                </button>
              </div>

              {showTrackSelector && (
                <div className="mb-4" style={{ padding: '1rem', background: 'var(--bg-input)', borderRadius: '0.5rem' }}>
                  <h4 style={{ fontWeight: 'bold', marginBottom: '1rem' }}>Select tracks to add:</h4>
                  <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
                    {getAvailableTracks().length === 0 ? (
                      <p className="text-secondary">All tracks already in playlist!</p>
                    ) : (
                      getAvailableTracks().map(track => (
                        <div 
                          key={track.id}
                          className="flex-between mb-2"
                          style={{ 
                            padding: '0.75rem', 
                            background: selectedTracks.includes(track.id) ? 'var(--accent)' : 'var(--bg-card)',
                            borderRadius: '0.5rem',
                            cursor: 'pointer'
                          }}
                          onClick={() => toggleTrackSelection(track.id)}
                        >
                          <div>
                            <strong>{track.title}</strong> - {track.artist}
                            <div className="text-sm text-secondary">
                              {track.bpm} BPM | {track.key} | Energy: {track.energy}/10
                            </div>
                          </div>
                          <input 
                            type="checkbox" 
                            checked={selectedTracks.includes(track.id)}
                            onChange={() => {}}
                          />
                        </div>
                      ))
                    )}
                  </div>
                  {selectedTracks.length > 0 && (
                    <button 
                      className="btn-primary mt-4"
                      onClick={handleAddTracks}
                    >
                      Add {selectedTracks.length} track{selectedTracks.length > 1 ? 's' : ''}
                    </button>
                  )}
                </div>
              )}

              {playlistTracks.length === 0 ? (
                <p className="text-secondary">No tracks in this playlist yet. Click "Add Tracks" to add some!</p>
              ) : (
                <div>
                  {playlistTracks.map((track, index) => (
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
                      <button 
                        className="btn-danger"
                        onClick={() => handleRemoveTrack(track.id)}
                        style={{ padding: '0.25rem 0.75rem', fontSize: '0.875rem' }}
                      >
                        Remove
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
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
