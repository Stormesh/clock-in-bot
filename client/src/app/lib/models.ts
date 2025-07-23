import mongoose, { Types } from "mongoose";
import { Action, Severity } from "./enums";

// User
export interface IUser {
  _id: Types.ObjectId | string;
  username: string;
  password: string;
  roleId: Types.ObjectId | string | IRole;
  __v?: number
}

const userSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true,
    unique: true,
  },
  password: {
    type: String,
    required: true,
  },
  roleId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "Role",
    required: true,
  },
});

export type PopulatedUser = Omit<IUser, "roleId"> & {
  roleId: IRole
}

export const User = mongoose.models?.User || mongoose.model("User", userSchema);

// Role
export interface IRole {
  _id: Types.ObjectId | string;
  name: string;
  priority: number;
  permissions?: string[];
  __v?: number
}

export interface IRoleNoId {
  name: string;
  priority: number;
  permissions?: string[];
}

const roleSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    unique: true,
  },
  priority: {
    type: Number,
    required: true,
    unique: true,
  },
  permissions: {
    type: [String],
    default: [],
  },
})

export const Role = mongoose.models?.Role || mongoose.model("Role", roleSchema);

// Logs
export interface ILog {
  _id?: Types.ObjectId | string;
  userId: Types.ObjectId | string | IUser;
  roleId: Types.ObjectId | string | IRole;
  action: Action | string;
  description?: string;
  severity: Severity | string;
  createdAt: Date;
  __v?: number
}

const logSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "User",
    required: true,
  },
  roleId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "Role",
    required: true,
  },
  action: {
    type: String,
    required: true,
  },
  severity: {
    type: String,
    required: true,
  },
  createdAt: {
    type: Date,
    required: true,
  },
  description: {
    type: String,
    default: "",
  }
})

export type PopulatedLog = Omit<ILog, "userId" | "roleId"> & {
  userId: IUser,
  roleId: IRole
}

export const Log = mongoose.models?.Log || mongoose.model("Log", logSchema);