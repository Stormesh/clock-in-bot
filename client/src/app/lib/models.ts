import mongoose from "mongoose";

export interface IRole {
  _id: string;
  name: string;
  priority: number;
  permissions?: string[];
}

export interface IUser {
  _id: string;
  username: string;
  password: string;
  roleId: string | IRole;
}

export type PopulatedUser = Omit<IUser, "roleId"> & {
  roleId: IRole
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
    type: String,
    ref: "Role",
    default: "U00",
    required: true,
  },
});

const roleSchema = new mongoose.Schema({
  _id: {
    type: String,
    required: true,
    unique: true,
  },
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

export const User = mongoose.models?.User || mongoose.model("User", userSchema);
export const Role = mongoose.models?.Role || mongoose.model("Role", roleSchema);
