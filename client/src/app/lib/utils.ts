import { User } from "next-auth";
import mongoose from "mongoose";
import { Permissions } from "./enums";

const connection = {
  isConnected: 0,
};

const MONGODB_URI = process.env.MONGODB_URI;

export const connectDB = async () => {
  try {
    if (!MONGODB_URI) {
      throw new Error(
        "Please define the MONGODB_URI environment variable inside .env.local"
      );
    }
    if (connection.isConnected) {
      console.log("Using existing connection");
      return;
    }
    const db = await mongoose.connect(MONGODB_URI);
    connection.isConnected = db.connections[0].readyState;
    console.log("MongoDB connected");
  } catch (error) {
    console.error(error);
  }
};

export const hasPermission = (user: User, permission: Permissions) =>
  user?.roleId?.permissions?.includes(permission);

export const hasAnyPermission = (user: User, permissions: Permissions[]) =>
  permissions.some(p => user?.roleId?.permissions?.includes(p));
