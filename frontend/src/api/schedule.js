import { apiClient } from "../config/axios";
const endpoint = "api";
export const getAllScheduleForUser = async () => {
  const res = await apiClient.get(endpoint + "/schedule/");
  return res.data;
};

export const getSchedule = async (id) => {
  const res = await apiClient.get(endpoint + `/schedule/${id}/`);
  return res.data;
};

export const createSchedule = async (schedule) => {
  const res = await apiClient.post(endpoint + "/schedule/", schedule);
  console.log(res)
  return res.data;
};

export const editSchedule = async (schedule) => {
  const res = await apiClient.put(
    endpoint + `/schedule/${schedule.id}/`,
    schedule,
  );
  return res.data;
};

export const deleteSchedule = async (id) => {
  const res = await apiClient.delete(endpoint + `/schedule/${id}/`);
  return res.data;
};

export const getAllSchedules = async () => {
  const res = await apiClient.get(endpoint + '/all-schedules/')
  return res.data
}