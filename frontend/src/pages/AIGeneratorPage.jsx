import React, { useState, useEffect } from 'react';
import { aiAPI, tracksAPI, playlistsAPI } from '../services/api';

export default function AIGeneratorPage() {
  const [tracks, setTracks] = useState([]);
  const [playlists, setPlaylists] = useState([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [nextTrackRec, setNextTrackRec] = useState(null);
  const [formData, setFormData] = useState({
    playlist_id: '',
    target_duration_minutes: '',
    vibe: '',
    max_tracks: '',
  });
  const [currentTrackId, setCurrentTrackId] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [tracksRes, playlistsRes] = await Promise.all([
        tracksAPI.getAll(),
        playlistsAPI.getAll(),
      ]);
      setTracks(tracksRes.data);
      setPlaylists(playlistsRes.data);
    } catch (error) {
      console.error('Failed to load data:', error);
    }
  };

  const handleGenerateSetlist = async () => {
    setLoading(true);
    setResult(null);
    try {
      const response = await aiAPI.generateSetlist({
        playlist_id: formData.playlist_id || undefined,
        target_duration_minutes: formData.target_duration_minutes ? parseInt(formData.target_duration_minutes) : undefined,
        vibe: formData.vibe || undefined,
        max_tracks: formData.max_tracks ? parseInt(formData.max_tracks) : undefined,
      });
      setResult(response.data);
    } catch (error) {
      console.error('Failed to generate setlist:', error);
      alert('Failed to generate setlist. Make sure you have tracks in your library.');
    } finally {
      setLoading(false);
    }
  };

  const handleGetNextTrack = async () => {
    if (!currentTrackId) {
      alert('Please select a current track');
      return;
    }
    setLoading(true);
    setNextTrackRec(null);
    try {
      const response = await aiAPI.getNextTrack({
        current_track_id: currentTrackId,
      });
      setNextTrackRec(response.data);
    } catch (error) {
      console.error('Failed to get next track recommendation:', error);
      alert('Failed to get recommendation');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1.5rem' }}>🤖 AI Setlist Generator</h2>

      {/* Generate Full Setlist */}
      <div className="card mb-4">
        <h3 className="mb-4">Generate AI Setlist</h3>
        <div className="grid grid-2">
          <div>
            <label className="text-sm text-secondary">Playlist (optional)</label>
            <select
              value={formData.playlist_id}
              onChange={(e) => setFormData({ ...formData, playlist_id: e.target.value })}
            >
              <option value="">All tracks</option>
              {playlists.map(p => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-sm text-secondary">Vibe/Style</label>
            <select
              value={formData.vibe}
              onChange={(e) => setFormData({ ...formData, vibe: e.target.value })}
            >
              <option value="">Mixed</option>
              <option value="warmup">Warmup</option>
              <option value="building">Building</option>
              <option value="peak">Peak Time</option>
              <option value="cooldown">Cooldown</option>
              <option value="journey">Journey</option>
            </select>
          </div>
          <div>
            <label className="text-sm text-secondary">Target Duration (minutes)</label>
            <input
              type="number"
              value={formData.target_duration_minutes}
              onChange={(e) => setFormData({ ...formData, target_duration_minutes: e.target.value })}
            />
          </div>
          <div>
            <label className="text-sm text-secondary">Max Tracks</label>
            <input
              type="number"
              value={formData.max_tracks}
              onChange={(e) => setFormData({ ...formData, max_tracks: e.target.value })}
            />
          </div>
          <div style={{ gridColumn: '1 / -1' }}>
            <button
              className="btn-primary"
              onClick={handleGenerateSetlist}
              disabled={loading}
              style={{ width: '100%' }}
            >
              {loading ? 'Generating...' : '🎧 Generate Setlist with AI'}
            </button>
          </div>
        </div>
      </div>

      {/* Next Track Recommendation */}
      <div className="card mb-4">
        <h3 className="mb-4">Get Next Track Recommendation</h3>
        <div className="grid grid-2">
          <div>
            <label className="text-sm text-secondary">Currently Playing</label>
            <select
              value={currentTrackId}
              onChange={(e) => setCurrentTrackId(e.target.value)}
            >
              <option value="">Select track...</option>
              {tracks.map(t => (
                <option key={t.id} value={t.id}>{t.title} - {t.artist}</option>
              ))}
            </select>
          </div>
          <div style={{ display: 'flex', alignItems: 'flex-end' }}>
            <button
              className="btn-primary"
              onClick={handleGetNextTrack}
              disabled={loading || !currentTrackId}
              style={{ width: '100%' }}
            >
              {loading ? 'Analyzing...' : '🎯 Get Recommendation'}
            </button>
          </div>
        </div>
      </div>

      {/* Results */}
      {result && (
        <div className="card mb-4">
          <h3 className="mb-4">✅ Generated Setlist</h3>
          <p className="text-secondary">{result.setlist.ai_notes}</p>
          <div className="mt-4">
            <h4 className="mb-4">Track Order:</h4>
            {result.setlist.track_order.map((item, idx) => {
              const track = tracks.find(t => t.id === item.track_id);
              return track ? (
                <div key={idx} className="flex gap-4 mb-4" style={{ padding: '1rem', background: 'var(--bg-input)', borderRadius: '0.5rem' }}>
                  <span style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--primary)' }}>
                    {item.position}
                  </span>
                  <div>
                    <p style={{ fontWeight: 'bold' }}>{track.title} - {track.artist}</p>
                    <p className="text-sm text-secondary">
                      {track.bpm} BPM | {track.key} | Energy: {track.energy_level}/10
                    </p>
                    {item.transition_notes && (
                      <p className="text-sm mt-4" style={{ color: 'var(--success)' }}>
                        💡 {item.transition_notes}
                      </p>
                    )}
                  </div>
                </div>
              ) : null;
            })}
          </div>
          {result.suggestions && result.suggestions.length > 0 && (
            <div className="mt-4">
              <h4 className="mb-4">Suggestions:</h4>
              <ul style={{ paddingLeft: '1.5rem' }}>
                {result.suggestions.map((s, i) => <li key={i} className="text-secondary">{s}</li>)}
              </ul>
            </div>
          )}
        </div>
      )}

      {nextTrackRec && (
        <div className="card">
          <h3 className="mb-4">🎯 Recommended Next Track</h3>
          <div style={{ padding: '1.5rem', background: 'var(--bg-input)', borderRadius: '0.5rem' }}>
            <p style={{ fontSize: '1.25rem', fontWeight: 'bold' }}>
              {nextTrackRec.recommended_track.title} - {nextTrackRec.recommended_track.artist}
            </p>
            <div className="flex gap-2 mt-4" style={{ flexWrap: 'wrap' }}>
              <span className="badge badge-primary">{nextTrackRec.recommended_track.bpm} BPM</span>
              <span className="badge badge-primary">{nextTrackRec.recommended_track.key}</span>
              <span className="badge badge-secondary">Energy: {nextTrackRec.recommended_track.energy_level}/10</span>
            </div>
            <p className="mt-4">{nextTrackRec.reasoning}</p>
            <p className="mt-4" style={{ color: 'var(--success)' }}>
              💡 {nextTrackRec.transition_tips}
            </p>
            <p className="text-sm text-secondary mt-4">
              Compatibility Score: {(nextTrackRec.compatibility_score * 100).toFixed(0)}%
            </p>
          </div>
        </div>
      )}

      {tracks.length === 0 && (
        <div className="card" style={{ background: 'var(--warning)', color: '#000', textAlign: 'center' }}>
          ⚠️ You need to add tracks to your library first before using AI features.
        </div>
      )}
    </div>
  );
}
