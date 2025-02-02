import mongoose, { Types } from "mongoose";

export interface IRole {
  _id: Types.ObjectId | string;
  name: string;
  priority: number;
  permissions?: string[];
  __v?: number
}

export interface IUser {
  _id: Types.ObjectId | string;
  username: string;
  password: string;
  roleId: Types.ObjectId | string | IRole;
  __v?: number
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
    type: Types.ObjectId,
    ref: "Role",
    required: true,
  },
});

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



export const User = mongoose.models?.User || mongoose.model("User", userSchema);
export const Role = mongoose.models?.Role || mongoose.model("Role", roleSchema);
