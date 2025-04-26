"use server";

import { getLogs, getLogsPerPage, getTotalLogsPages, createLog } from "../lib/data";
import { PopulatedLog, ILog } from "../lib/models";

export const getLogsAction = async () => {
  try {
    const logs = await getLogs();
    return logs as PopulatedLog[];
  } catch (error) {
    console.error(error);
    throw new Error("Failed to get logs");
  }
};

export const getLogsPerPageAction = async (page: number, limit: number) => {
  try {
    const logs = await getLogsPerPage(page, limit);
    return logs as PopulatedLog[];
  } catch (error) {
    console.error(error);
    throw new Error("Failed to get logs");
  }
};

export const getTotalLogsPagesAction = async (limit: number) => {
  try {
    const logs = await getTotalLogsPages(limit);
    return logs;
  } catch (error) {
    console.error(error);
    throw new Error("Failed to get logs");
  }
};

export const createLogAction = async (log: ILog) => {
  try {
    const loga = await createLog(log);
    console.log(loga);
    return { success: "Log created successfully" };
  } catch (error) {
    console.error(error);
    throw new Error("Failed to create log");
  }
};
