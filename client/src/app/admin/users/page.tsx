import { auth } from "@/src/auth";
import React from "react";
import AdminUsers from "@components/admin/AdminUsers";
import Warning from "@components/Warning";
import { getUsersAction } from "../../actions/actions";
import { SessionProvider } from "next-auth/react";

const page = async () => {
  const session = await auth();

  if (!session?.user.roleId.permissions?.some((permission) => permission === "delete-user" || permission === "update-user")) {
    return (
      <Warning />
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
    <div className="flex flex-col items-center">
      <SessionProvider>
        <AdminUsers users={filteredUsers} />
      </SessionProvider>
    </div>
  );
};

export default page;
