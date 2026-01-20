import axios from 'axios';

const API_URL = 'http://localhost:8000/account';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');

  const publicEndpoints = ['/token/', '/register/'];

  if (token && !publicEndpoints.includes(config.url)) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export const login = async (credentials) => {
  const response = await apiClient.post('/token/', credentials);
  return response.data;
};

export const register = async (userData) => {
  const response = await apiClient.post('/register/', userData);
  return response.data;
};

export const logout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
};

export const profil = async () => {
  const response = await apiClient.get('/profil')
  return response
}