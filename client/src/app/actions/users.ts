"use server";

import { hash } from "bcryptjs";
import {
  getUser,
  getRoleByName,
  createUser,
  getUsers,
  updateUserById,
  deleteUserById,
} from "../lib/data";
import { IRole, IUser, PopulatedUser } from "../lib/models";
import { signUpSchema } from "../lib/zod";
import { Types } from "mongoose";

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


