import { User } from "next-auth";
import mongoose from "mongoose";
import { Permissions } from "./enums";
import dotenv from "dotenv";

// Load environment variables from .env.local
dotenv.config({ path: "./.env.local" });

// Track the connection state
const connection = {
  isConnected: 0,
};

// Mongoose connection states
enum ConnectionStates {
  disconnected = 0,
  connected = 1,
  connecting = 2,
  disconnecting = 3,
}

const MONGODB_URI = process.env.MONGODB_URI;

export const connectDB = async () => {
  try {
    if (!MONGODB_URI) {
      throw new Error(
        "Please define the MONGODB_URI environment variable inside .env.local"
      );
    }
    if (connection.isConnected === ConnectionStates.connected) {
      console.log("Using existing connection");
      return;
    }
    const db = await mongoose.connect(MONGODB_URI);
    connection.isConnected = db.connections[0].readyState;
    console.log("MongoDB connected");
  } catch (error) {
    console.error("MongoDB connection error:", error);
    throw error; // Propagate the error to the caller
  }
};

/**
 * Disconnect from MongoDB database
 * Useful for testing environments and cleanup
 */
export const disconnectDB = async () => {
  try {
    if (connection.isConnected === ConnectionStates.disconnected) {
      console.log("No active connection to disconnect");
      return;
    }

    await mongoose.disconnect();
    connection.isConnected = ConnectionStates.disconnected;
    console.log("MongoDB disconnected");
  } catch (error) {
    console.error("MongoDB disconnection error:", error);
    throw error;
  }
};

/**
 * Check if a user has a specific permission
 * @param user The user to check permissions for
 * @param permission The permission to check
 * @returns true if the user has the permission, false otherwise
 */
export const hasPermission = (
  user: User | null | undefined,
  permission: Permissions
): boolean => {
  if (!user || !user.roleId || !user.roleId.permissions) return false;
  return user.roleId.permissions.includes(permission);
};

/**
 * Check if a user has any of the specified permissions
 * @param user The user to check permissions for
 * @param permissions Array of permissions to check
 * @returns true if the user has any of the permissions, false otherwise
 */
export const hasAnyPermission = (
  user: User | null | undefined,
  permissions: Permissions[]
): boolean => {
  if (!user || !user.roleId || !user.roleId.permissions || !permissions.length)
    return false;
  return permissions.some((p) => user.roleId.permissions?.includes(p));
};
