import React, { useState } from 'react';
import { authAPI } from './services/api';

export default function LoginPage({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const res = await authAPI.login({ username, password });
      const { access_token, user } = res.data;
      localStorage.setItem('token', access_token);
      localStorage.setItem('user', JSON.stringify(user));
      onLogin(user);
    } catch (err) {
      const detail = err.response?.data?.detail;
      if (typeof detail === 'string') {
        setError(detail);
      } else if (Array.isArray(detail)) {
        setError(detail.map(e => e.msg || e.detail).join(', '));
      } else {
        setError('Invalid username or password');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-dark)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div className="card" style={{ maxWidth: '400px', width: '100%', padding: '2rem' }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h1 style={{ fontSize: '2rem', fontWeight: 'bold' }}>🎧 DJ Setlist AI</h1>
          <p className="text-secondary">Sign in to your account</p>
        </div>

        <form onSubmit={handleSubmit}>
          {error && (
            <div style={{ background: '#fee2e2', color: '#dc2626', padding: '0.75rem', borderRadius: '0.5rem', marginBottom: '1rem' }}>
              {error}
            </div>
          )}

          <div style={{ marginBottom: '1rem' }}>
            <label className="text-sm text-secondary">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              style={{ width: '100%', marginTop: '0.25rem' }}
            />
          </div>

          <div style={{ marginBottom: '1.5rem' }}>
            <label className="text-sm text-secondary">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              style={{ width: '100%', marginTop: '0.25rem' }}
            />
          </div>

          <button type="submit" className="btn-primary" style={{ width: '100%' }} disabled={loading}>
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <p style={{ textAlign: 'center', marginTop: '1.5rem', color: 'var(--text-secondary)' }}>
          Don't have an account?{' '}
          <a href="#/register" style={{ color: 'var(--primary)', fontWeight: 'bold' }}>
            Register
          </a>
        </p>
      </div>
    </div>
  );
}
