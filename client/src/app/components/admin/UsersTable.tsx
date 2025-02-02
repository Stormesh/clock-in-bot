"use client";

import React, { FC, useState } from "react";
import InputField from "@components/InputField";
import Alert from "../Alert";
import { IRole, PopulatedUser } from "../../lib/models";
import { deleteUserAction, getRoleAction, updateUserAction } from "../../actions/actions";

interface IUsersTableProps {
  users: PopulatedUser[];
}

const UsersTable: FC<IUsersTableProps> = ({ users }) => {
  const [usersList, setUsersList] = useState<PopulatedUser[]>(users);
  const [value, setValue] = useState(users.map((user) => user.roleId.name));
  const [alert, setAlert] = useState({
    show: false,
    text: "",
    onConfirm: () => {},
  });

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

  const resetAlert = () => {
    setAlert({show: false, text: "", onConfirm: () => {}});
  };

  const updateUser = async (id: string, roleName: string) => {
    try {
      const role: IRole = await getRoleAction(roleName);

      if (!role) {
        console.error("Role not found for:", roleName);
        return;
      }

      const updatedUser = await updateUserAction(id, { roleId: role._id });
      setUsersList((prev) => {
        return prev.map((user) => {
          if (user._id.toString() === id) {
            return { ...user, roleId: role };
          }
          return user;
        });
      });
      return updatedUser;
    } catch (error) {
      throw new Error(`Failed to update user: ${error}`);
    }
  };

  const handleUpdateUser = (id: string, roleName: string) => {
    try {
      setAlert({
        show: true,
        text: "Are you sure you want to update this user?",
        onConfirm: async () => {
          await updateUser(id, roleName);
          resetAlert();
        },
      });
    } catch (error) {
      console.error(error);
    }
  };

  const deleteUser = async (id: string) => {
    try {
      await deleteUserAction(id);
      setUsersList((prev) => prev.filter((user) => user._id.toString() !== id));
      setValue((prev) => prev.filter((_, index) => index !== usersList.findIndex((user) => user._id.toString() === id)));
    } catch (error) {
      throw new Error(`Failed to delete user: ${error}`);
    }
  };

  const handleDeleteUser = (id: string) => {
    try {
      setAlert({
        show: true,
        text: "Are you sure you want to delete this user?",
        onConfirm: async () => {
          await deleteUser(id);
          setAlert({show: false, text: "", onConfirm: () => {} });
        },
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
      {alert.show && (
        <Alert
          text={alert.text}
          onConfirm={alert.onConfirm}
          onDismiss={() =>
            setAlert((prev) => ({
              ...prev,
              show: false,
              onConfirm: () => {},
            }))
          }
          alert={alert}
        />
      )}

      <table className="text-xl text-white">
        <thead className="table-header">
          <tr>
            <th className="border-table-border border-2 p-1">Username</th>
            <th className="border-2 border-table-border p-1">Role</th>
            <th className="border-table-border border-2 p-1">Options</th>
          </tr>
        </thead>
        <tbody className="bg-card-bg border-2 border-table-border">
          {usersList.map((user, index) => (
            <tr className="border-2 border-table-border" key={user._id.toString()}>
              <td className="p-1">{user.username}</td>
              <td>
                <InputField
                  name="roleId"
                  select={["User", "Admin"]}
                  onChange={(e) => handleChange(e, index)}
                  value={value[index]}
                />
              </td>
              <td className="select-none">
                <button
                  onClick={() => handleUpdateUser(user._id.toString(), value[index])}
                  className={`bg-green-800 hover:bg-green-600 hover:scale-95 font-bold transition-all rounded-lg p-1 m-1 cursor-pointer`}
                >
                  Update
                </button>
                <button
                  onClick={() => handleDeleteUser(user._id.toString())}
                  className={`bg-red-800 hover:bg-red-600 hover:scale-95 font-bold transition-all rounded-lg p-1 m-1 cursor-pointer`}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
};

export default UsersTable;
