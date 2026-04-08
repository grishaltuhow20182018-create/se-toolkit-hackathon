import axios from 'axios';

const API_BASE = '/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 responses
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
};

export const tracksAPI = {
  getAll: (params = {}) => api.get('/tracks/', { params }),
  getById: (id) => api.get(`/tracks/${id}`),
  create: (data) => api.post('/tracks/', data),
  update: (id, data) => api.put(`/tracks/${id}`, data),
  delete: (id) => api.delete(`/tracks/${id}`),
};

export const playlistsAPI = {
  getAll: () => api.get('/playlists/'),
  getById: (id) => api.get(`/playlists/${id}`),
  create: (data) => api.post('/playlists/', data),
  addTrack: (playlistId, trackId, position) => 
    api.post(`/playlists/${playlistId}/tracks/${trackId}`, null, { params: { position } }),
  removeTrack: (playlistId, trackId) => 
    api.delete(`/playlists/${playlistId}/tracks/${trackId}`),
  delete: (id) => api.delete(`/playlists/${id}`),
};

export const setlistsAPI = {
  getAll: () => api.get('/setlists/'),
  getById: (id) => api.get(`/setlists/${id}`),
  create: (data) => api.post('/setlists/', data),
  delete: (id) => api.delete(`/setlists/${id}`),
};

export const aiAPI = {
  generateSetlist: (data) => api.post('/ai/generate-setlist', data),
  getNextTrack: (data) => api.post('/ai/next-track', data),
};

export default api;
