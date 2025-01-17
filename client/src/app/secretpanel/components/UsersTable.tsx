"use client";

import React, { FC, useState } from "react";
import InputField from "../../login/components/InputField";
import Alert from "../../components/Alert";
import { PopulatedUser } from "../../lib/models";

const baseUrl = process.env.NEXT_PUBLIC_BASE_URL || "http://localhost:3000";

interface UsersTableProps {
  users: PopulatedUser[];
}

const UsersTable: FC<UsersTableProps> = ({ users }) => {
  const [usersList, setUsersList] = useState<PopulatedUser[]>(users);
  const [value, setValue] = useState(users.map((user) => user.roleId.name));
  const [alert, setAlert] = useState({
    show: false,
    text: "",
    onConfirm: () => {},
  });

  console.log(users);

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
      const role = await fetch(`${baseUrl}/api/roles/${roleName}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      const roleData = await role.json();

      if (!roleData) {
        console.error("Role not found for:", roleName);
        return;
      }

      const response = await fetch(`${baseUrl}/api/users/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          roleId: roleData._id,
        }),
      });
      const data = await response.json();
      setUsersList((prev) => {
        return prev.map((user) => {
          if (user._id === id) {
            return { ...user, roleId: roleData };
          }
          return user;
        });
      });
      return data;
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
      await fetch(`${baseUrl}/api/users/${id}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      });
      setUsersList((prev) => prev.filter((user) => user._id !== id));
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
            <th className="border-tableBorder border-2 p-1">Username</th>
            <th className="border-2 border-tableBorder p-1">Role</th>
            <th className="border-tableBorder border-2 p-1">Options</th>
          </tr>
        </thead>
        <tbody className="bg-cardBg border-2 border-tableBorder">
          {usersList.map((user, index) => (
            <tr className="border-2 border-tableBorder" key={user._id}>
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
                  onClick={() => handleUpdateUser(user._id, value[index])}
                  className={`bg-green-800 hover:bg-green-600 hover:scale-95 font-bold transition-all rounded-lg p-1 m-1`}
                >
                  Update
                </button>
                <button
                  onClick={() => handleDeleteUser(user._id)}
                  className={`bg-red-800 hover:bg-red-600 hover:scale-95 font-bold transition-all rounded-lg p-1 m-1`}
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
