import { apiClient } from "../config/axios";
const endpoint = "api";
export const getAllLeaveForUser = async () => {
  const res = await apiClient.get(endpoint + "/leave/");
  return res.data;
};

export const getLeave = async (id) => {
  const res = await apiClient.get(endpoint + `/leave/${id}/`);
  return res.data;
};

export const createLeave = async (Leave) => {
  const res = await apiClient.post(endpoint + "/leave/", Leave);
  console.log(res)
  return res.data;
};

export const editLeave = async (Leave) => {
  const res = await apiClient.put(
    endpoint + `/leave/${Leave.id}/`,
    Leave,
  );
  return res.data;
};

export const deleteLeave = async (id) => {
  const res = await apiClient.delete(endpoint + `/leave/${id}/`);
  return res.data;
};
