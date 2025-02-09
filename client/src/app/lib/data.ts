import { Types } from "mongoose";
import { ILog, IRole, IUser, Log, PopulatedUser, Role, User } from "./models";
import { connectDB } from "./utils";

// User
export const getUser = async (username: string) => {
  try {
    await connectDB();
    const user = await User.findOne({ username }).populate("roleId").lean();
    return user as PopulatedUser;
  } catch (error) {
    console.error(error);
    throw new Error("Failed to get user");
  }
};

export const createUser = async (
  username: string,
  password: string,
  roleId: Types.ObjectId
) => {
  try {
    await connectDB();
    const user = await User.create({ username, password, roleId });
    return user;
  } catch (error) {
    console.error(error);
    throw new Error("Failed to create user");
  }
};

export const getUsers = async () => {
  try {
    await connectDB();
    const users = await User.find()
      .select("-password")
      .populate("roleId")
      .lean();
    return users as PopulatedUser[];
  } catch (error) {
    console.error(error);
    throw new Error("Failed to get users");
  }
};

export const updateUserById = async (
  _id: Types.ObjectId,
  data: Partial<IUser>
) => {
  try {
    await connectDB();
    const user = await User.findOneAndUpdate(
      { _id },
      { $set: data },
      { new: true }
    )
      .select("-password")
      .lean();
    return user as IUser;
  } catch (error) {
    console.error(error);
    throw new Error("Failed to update user");
  }
};

export const deleteUserById = async (_id: Types.ObjectId) => {
  try {
    await connectDB();
    const user = await User.deleteOne({ _id }, { new: true });

    if (user.deletedCount === 0) {
      throw new Error("User not found");
    }

    return user;
  } catch (error) {
    console.error(error);
    throw new Error("Failed to delete user");
  }
};

// Role
export const getRoleByName = async (name: string) => {
  try {
    await connectDB();
    const role = await Role.findOne({ name }).lean();
    return role as IRole;
  } catch (error) {
    console.error(error);
    throw new Error("Failed to find role");
  }
};

export const getRoles = async () => {
  try {
    await connectDB();
    const roles = await Role.find().lean();
    return roles;
  } catch (error) {
    console.error(error);
    throw new Error("Failed to get roles");
  }
};

// Logs
export const getLogs = async () => {
  try {
    await connectDB();
    const logs = await Log.find()
      .populate("userId", "username")
      .populate("roleId", "name")
      .lean()
      .sort({ createdAt: -1 });
    return logs;
  } catch (error) {
    console.error(error);
    throw new Error("Failed to get logs");
  }
};

export const createLog = async (log: ILog) => {
  try {
    await connectDB();
    const newLog = await Log.create(log);
    return newLog;
  } catch (error) {
    console.error(error);
    throw new Error("Failed to create log");
  }
}