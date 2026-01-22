import { apiClient } from "../config/axios";

const endpoint = "account";

export const login = async (credentials) => {
  const response = await apiClient.post(endpoint + "/token/", credentials);
  return response.data;
};

export const register = async (userData) => {
  const response = await apiClient.post(endpoint + "/register/", userData);
  return response.data;
};

export const logout = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
};

export const profil = async () => {
  const response = await apiClient.get(endpoint + "/profil");
  return response.data;
};
