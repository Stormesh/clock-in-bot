import { auth } from "@/src/auth";
import Link from "next/link";
import React from "react";
import UsersTable from "./components/UsersTable";
import { PopulatedUser } from "../lib/models";
import Warning from "../components/Warning";

const getBaseUrl = () => {
  if (process.env.NODE_ENV === "production") {
    return process.env.NEXT_PUBLIC_BASE_URL; // Set this in your production environment
  }
  return "http://localhost:3000"; // Default for development
};

const page = async () => {
  const session = await auth();

  const baseUrl = getBaseUrl();

  const fetchUsers = async (): Promise<PopulatedUser[]> => {
    try {
      const response = await fetch(`${baseUrl}/api/users`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch users: ${response.statusText}`);
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      throw new Error(`Failed to fetch users: ${error}`);
    }
  };

  if (!session?.user.roleId.permissions?.some((permission) => permission === "delete-user" || permission === "update-user")) {
    return (
      <Warning
        text="You do not have permission to view this page."
        link="/"
        linkText="Go back"
      />
    );
  }

  // Fetch users
  const users = await fetchUsers();

  const currentUser = {
    username: session?.user.name,
    roleId: session?.user.roleId,
  };

  const filteredUsers = users.filter(
    (user) =>
      user.username !== currentUser.username && user.roleId.priority > (currentUser.roleId?.priority ?? -1)
  );

  return (
    <div className="flex flex-col justify-center items-center h-screen">
      <UsersTable users={filteredUsers} />
      <Link className="m-2" href="/">
        <button className="bg-green-700 hover:bg-green-500 hover:scale-105 transition-all p-2 font-bold rounded-lg text-white">
          Go back
        </button>
      </Link>
    </div>
  );
};

export default page;
