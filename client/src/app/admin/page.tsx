import { auth } from "@/src/auth";
import Link from "next/link";
import React from "react";
import UsersTable from "@components/admin/UsersTable";
import Warning from "@components/Warning";
import { getUsersAction } from "../actions/actions";

const page = async () => {
  const session = await auth();

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
  const users = await getUsersAction();

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
        <button className="bg-green-700 hover:bg-green-500 hover:scale-105 transition-all p-2 font-bold rounded-lg text-white cursor-pointer">
          Go back
        </button>
      </Link>
    </div>
  );
};

export default page;
