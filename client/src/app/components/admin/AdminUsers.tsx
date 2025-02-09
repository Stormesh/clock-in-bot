"use client";

import React, { FC, Suspense, useState } from "react";
import InputField from "@components/InputField";
import { Action, IRole, PopulatedUser, Severity } from "../../lib/models";
import {
  createLogAction,
  deleteUserAction,
  getRoleAction,
  updateUserAction,
} from "../../actions/actions";
import { Types } from "mongoose";
import { useSession } from "next-auth/react";
import GearSpin from "../GearSpin";
import { usePopupStore } from "../../zustand/popupStore";
import Popup from "../Popup";

interface IUsersTableProps {
  users: PopulatedUser[];
}

const AdminUsers: FC<IUsersTableProps> = ({ users }) => {
  const [usersList, setUsersList] = useState<PopulatedUser[]>(users);
  const [value, setValue] = useState(users.map((user) => user.roleId.name));
  const {show, text, resetPopup, onConfirm, onDismiss} = usePopupStore();

  const {data: session} = useSession();

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
    index: number
  ) => {
    setValue((prev) => {
      const newValues = [...prev];
      newValues[index] = e.target.value;
      return newValues;
    });
  };

  const updateUser = async (id: Types.ObjectId, roleName: string) => {
    try {
      const role: IRole = await getRoleAction(roleName);

      if (!role) {
        console.error("Role not found for:", roleName);
        return;
      }

      const updatedUser = await updateUserAction(id, { roleId: role._id });
      setUsersList((prev) => {
        return prev.map((user) => {
          if (user._id === id) {
            return { ...user, roleId: role };
          }
          return user;
        });
      });
      if (session?.user.id) {
        await createLogAction({
          userId: session.user.id,
          roleId: session.user.roleId._id,
          action: Action.UPDATE,
          severity: Severity.MEDIUM,
          description: `${session.user.name} has updated ${updatedUser.username}'s role to ${role.name}`,
          createdAt: new Date(),
        });
      }
      return updatedUser;
    } catch (error) {
      throw new Error(`Failed to update user: ${error}`);
    }
  };

  const handleUpdateUser = (id: Types.ObjectId, roleName: string) => {
    try {
      usePopupStore.setState({show: true, text: "Are you sure you want to update this user?", onConfirm: async () => {
        await updateUser(id, roleName);
        resetPopup();
      }})
    } catch (error) {
      console.error(error);
    }
  };

  const deleteUser = async (id: Types.ObjectId) => {
    try {
      const deletedUser = usersList.find((user) => user._id === id);
      await deleteUserAction(id);
      setUsersList((prev) => prev.filter((user) => user._id !== id));
      setValue((prev) =>
        prev.filter(
          (_, index) => index !== usersList.findIndex((user) => user._id === id)
        )
      );
      if (session?.user.id) {
        await createLogAction({
          userId: session.user.id,
          roleId: session.user.roleId._id,
          action: Action.DELETE,
          severity: Severity.MEDIUM,
          description: `${session.user.name} has deleted ${deletedUser?.username}`,
          createdAt: new Date(),
        });
      }
    } catch (error) {
      throw new Error(`Failed to delete user: ${error}`);
    }
  };

  const handleDeleteUser = (id: Types.ObjectId) => {
    try {
      usePopupStore.setState({
        show: true, 
        text: "Are you sure you want to delete this user?", 
        onConfirm: async () => {
          await deleteUser(id);
          resetPopup();
        }
      });
    } catch (error) {
      console.error(error);
    }
  };

  if (usersList.length === 0) {
    return <h1 className="text-white text-5xl font-bold">No users found.</h1>;
  }

  return (
    <>
      {show && (
        <Popup
          text={text}
          onConfirm={onConfirm}
          onDismiss={onDismiss}
          show={show}
        />
      )}

      <table className="text-xl w-full text-white">
        <thead className="table-header">
          <tr>
            <th className="border-table-border border-2 p-1">Username</th>
            <th className="border-2 border-table-border p-1">Role</th>
            <th className="border-table-border border-2 p-1">Options</th>
          </tr>
        </thead>
        <tbody className="bg-card-bg border-2 border-table-border">
          {usersList.map((user, index) => (
            <tr
              className="border-2 border-table-border"
              key={user._id.toString()}
            >
              <td className="p-1">{user.username}</td>
              <td>
                <InputField
                  name="roleId"
                  select={["User", "Admin"]}
                  onChange={(e) => handleChange(e, index)}
                  value={value[index]}
                />
              </td>
              <td className="select-none text-center">
                <Suspense fallback={<GearSpin />}>
                  {session?.user?.roleId?.permissions?.includes(
                    "update-user"
                  ) && (
                    <button
                      onClick={() =>
                        handleUpdateUser(user._id as Types.ObjectId, value[index])
                      }
                      className={`bg-green-800 hover:bg-green-600 hover:scale-95 font-bold transition-all rounded-lg p-1 m-1 cursor-pointer`}
                    >
                      Update
                    </button>
                  )}
                  {session?.user?.roleId?.permissions?.includes(
                    "delete-user"
                  ) && (
                    <button
                      onClick={() => handleDeleteUser(user._id as Types.ObjectId)}
                      className={`bg-red-800 hover:bg-red-600 hover:scale-95 font-bold transition-all rounded-lg p-1 m-1 cursor-pointer`}
                    >
                      Delete
                    </button>
                  )}
                </Suspense>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
};

export default AdminUsers;
