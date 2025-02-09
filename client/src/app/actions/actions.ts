"use server";

import { hash } from "bcryptjs";
import {
  getUser,
  getRoleByName,
  createUser,
  getUsers,
  updateUserById,
  deleteUserById,
  getRoles,
  getLogs,
  createLog,
} from "../lib/data";
import { ILog, IRole, IUser, PopulatedLog, PopulatedUser } from "../lib/models";
import { signUpSchema } from "../lib/zod";
import { Types } from "mongoose";

const DISCORD_BOT_URL = process.env.DISCORD_BOT_URL;

if (!DISCORD_BOT_URL) {
  throw new Error("Can't connect to Discord Bot");
}

// Discord
export const getDiscordData = async () => {
  try {
    const response = await fetch(`${DISCORD_BOT_URL}/api/users`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
    throw new Error("Failed to get Discord data");
  }
};

export const dmDiscordUser = async (userId: string, formData: FormData, method = "POST") => {
  try {
    const message = formData.get("message");
    console.log(message);
    await fetch(`${DISCORD_BOT_URL}/api/users/dm/${userId}`, {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: message,
      }),
    });
  } catch (error) {
    console.error(error);
    throw new Error("Failed to warn Discord user");
  }
};

// User
const transformUser = (user: IUser | PopulatedUser) => {
  const transformedUser = {
    ...user,
    _id: user._id.toString(),
  };

  if (user.roleId instanceof Types.ObjectId) {
    return {
      ...transformedUser,
      roleId: user.roleId.toString(),
    };
  }

  if (
    typeof user.roleId === "object" &&
    user.roleId !== null &&
    "_id" in user.roleId
  ) {
    return {
      ...transformedUser,
      roleId: {
        ...user.roleId,
        _id: user.roleId._id.toString(),
      },
    };
  }

  return {
    ...transformedUser,
    roleId: user.roleId.toString(),
  };
};

export const createUserAction = async (formData: FormData) => {
  try {
    const rawFormData = Object.fromEntries(formData.entries());
    const validatedData = await signUpSchema.safeParseAsync(rawFormData);

    if (validatedData.error) {
      const errorMessage = validatedData.error.errors.map(
        (error) => error.message
      );
      return { error: errorMessage.join("\n") };
    }

    const { username, password, role } = validatedData.data;

    if (!username || !password || !role) {
      return { error: "Missing fields" };
    }

    if (await getUser(username)) {
      return { error: "User already exists" };
    }

    const roleId: IRole = await getRoleByName(role);

    if (!roleId) {
      return { error: "Role not found" };
    }

    const hashedPassword = await hash(password, 10);

    if (!hashedPassword) {
      return { error: "Failed to store password" };
    }

    await createUser(username, hashedPassword, roleId._id as Types.ObjectId);

    return { success: "User created successfully" };
  } catch (error) {
    console.error(error);
    return {
      error: error instanceof Error ? error.message : "Failed to create user",
    };
  }
};

export const getUsersAction = async () => {
  try {
    const users = await getUsers();

    const transformedUsers = users.map((user) => transformUser(user));
    return transformedUsers as PopulatedUser[];
  } catch (error) {
    console.error(error);
    throw new Error("Failed to get users");
  }
};

export const getUserAction = async (username: string) => {
  try {
    const user = await getUser(username);
    const transformedUser = transformUser(user);
    return transformedUser;
  } catch (error) {
    console.error(error);
    throw new Error("Failed to get user");
  }
};

export const updateUserAction = async (
  id: Types.ObjectId,
  data: Partial<IUser>
) => {
  try {
    const updatedUser = await updateUserById(id, data);
    const transformedUser = transformUser(updatedUser);
    return transformedUser;
  } catch (error) {
    console.error(error);
    throw new Error("Failed to update user");
  }
};

export const deleteUserAction = async (id: Types.ObjectId) => {
  try {
    if (!id) {
      throw new Error("User ID is required");
    }
    const deletedUser = await deleteUserById(id);
    return deletedUser;
  } catch (error) {
    console.error(error);
    throw new Error(
      error instanceof Error
        ? `Failed to delete user: ${error.message}`
        : "Failed to delete user"
    );
  }
};

// Role
const transformRole = (role: IRole) => {
  return {
    ...role,
    _id: role._id.toString(),
  };
};

export const getRolesAction = async () => {
  try {
    const roles = await getRoles();
    return roles;
  } catch (error) {
    console.error(error);
    throw new Error(
      error instanceof Error
        ? `Failed to get roles: ${error.message}`
        : "Failed to get roles"
    );
  }
};

export const getRoleAction = async (roleName: string) => {
  try {
    const role = await getRoleByName(roleName);

    if (!role) {
      throw new Error("Role not found");
    }

    const transformedRole = transformRole(role);

    return transformedRole;
  } catch (error) {
    console.error(error);
    throw new Error(
      error instanceof Error ? error.message : "Failed to get role"
    );
  }
};

// Log
export const getLogsAction = async () => {
  try {
    const logs = await getLogs();
    return logs as PopulatedLog[];
  } catch (error) {
    console.error(error);
    throw new Error("Failed to get logs");
  }
};

export const createLogAction = async (log: ILog) => {
  try {
    await createLog(log);
    return { success: "Log created successfully" };
  } catch (error) {
    console.error(error);
    throw new Error("Failed to create log");
  }
};
