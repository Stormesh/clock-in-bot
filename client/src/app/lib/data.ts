import { Types } from "mongoose";
import { ILog, IRole, IRoleNoId, IUser, Log, PopulatedUser, Role, User } from "./models";
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

export const getRoleNames = async () => {
  try {
    await connectDB();
    const roleNames = await Role.find()
      .select("name")
      .lean()
      .sort({ name: -1 });
    return (roleNames as IRole[])
      .filter((role) => role.name !== "superadmin")
      .map((role) => role.name.charAt(0).toUpperCase() + role.name.slice(1));
  } catch (error) {
    console.error(error);
    throw new Error("Failed to get role names");
  }
};

export const createRole = async (
  name: string,
  priority: number,
  permissions: string[]
) => {
  try {
    await connectDB();
    const role = await Role.create({ name, priority, permissions });
    return role;
  } catch (error) {
    console.error(error);
    throw new Error("Failed to create role");
  }
};

export const createRoles = async (roles: IRoleNoId[]) => {
  try {
    await connectDB();
    const role = await Role.create(roles);
    return role;
  } catch (error) {
    console.error(error);
    throw new Error("Failed to create roles");
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

export const getLogsPerPage = async (page: number, limit: number) => {
  try {
    await connectDB();
    const logs = await Log.find()
      .populate("userId", "username")
      .populate("roleId", "name priority")
      .lean()
      .sort({ createdAt: -1 })
      .skip((page - 1) * limit)
      .limit(limit);
    return logs;
  } catch (error) {
    console.error(error);
    throw new Error("Failed to get logs");
  }
};

export const getTotalLogsPages = async (limit: number) => {
  try {
    await connectDB();
    const totalLogs = await Log.countDocuments();
    return Math.ceil(totalLogs / limit);
  } catch (error) {
    console.error(error);
    throw new Error("Failed to get total logs pages");
  }
};

export const createLog = async (log: ILog) => {
  try {
    await connectDB();
    const newLog = await Log.create(log);
    console.log(newLog);
    return newLog;
  } catch (error) {
    console.error(error);
    throw new Error("Failed to create log");
  }
};
