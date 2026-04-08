import React, { useState } from 'react';
import TracksPage from './pages/TracksPage';
import PlaylistsPage from './pages/PlaylistsPage';
import SetlistsPage from './pages/SetlistsPage';
import AIGeneratorPage from './pages/AIGeneratorPage';

function App() {
  const [currentPage, setCurrentPage] = useState('tracks');

  const navItems = [
    { id: 'tracks', label: '📚 Tracks' },
    { id: 'playlists', label: '🎵 Playlists' },
    { id: 'setlists', label: '📝 Setlists' },
    { id: 'ai', label: '🤖 AI Generator' },
  ];

  const renderPage = () => {
    switch (currentPage) {
      case 'tracks':
        return <TracksPage />;
      case 'playlists':
        return <PlaylistsPage />;
      case 'setlists':
        return <SetlistsPage />;
      case 'ai':
        return <AIGeneratorPage />;
      default:
        return <TracksPage />;
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-dark)' }}>
      {/* Header */}
      <header style={{
        background: 'linear-gradient(135deg, var(--primary), var(--secondary))',
        padding: '1.5rem 2rem',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.3)',
      }}>
        <div style={{ maxWidth: '1400px', margin: '0 auto' }}>
          <h1 style={{ fontSize: '2rem', fontWeight: 'bold' }}>🎧 DJ Setlist AI</h1>
          <p style={{ opacity: 0.9, marginTop: '0.25rem' }}>
            AI-powered DJ setlist generator with seamless track matching
          </p>
        </div>
      </header>

      {/* Navigation */}
      <nav style={{
        background: 'var(--bg-card)',
        padding: '1rem 2rem',
        borderBottom: '1px solid var(--border)',
      }}>
        <div style={{ maxWidth: '1400px', margin: '0 auto', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          {navItems.map(item => (
            <button
              key={item.id}
              onClick={() => setCurrentPage(item.id)}
              style={{
                background: currentPage === item.id ? 'var(--primary)' : 'transparent',
                color: 'white',
                padding: '0.5rem 1rem',
                borderRadius: '0.5rem',
                fontWeight: currentPage === item.id ? '600' : '400',
              }}
            >
              {item.label}
            </button>
          ))}
        </div>
      </nav>

      {/* Main Content */}
      <main style={{ maxWidth: '1400px', margin: '0 auto', padding: '2rem' }}>
        {renderPage()}
      </main>
    </div>
  );
}

export default App;
