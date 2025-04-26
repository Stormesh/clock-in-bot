"use server";

import { getRoles, getRoleByName, getRoleNames } from "../lib/data";
import { IRole } from "../lib/models";

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
      `Failed to get roles${error instanceof Error && `: ${error.message}`}`
    );
  }
};

export const getRoleNamesAction = async () => {
  try {
    const roleNames = await getRoleNames();
    return roleNames;
  } catch (error) {
    console.error(error);
    throw new Error(
      `Failed to get role names${
        error instanceof Error && `: ${error.message}`
      }`
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
