import { auth } from "@/src/auth";
import React from "react";
import AdminUsers from "@components/admin/AdminUsers";
import Warning from "@components/Warning";
import { getUsersAction } from "../../actions/users";
import { SessionProvider } from "next-auth/react";
import { Permissions } from "../../lib/enums";
import { getRoleNamesAction } from "../../actions/roles";
import { hasAnyPermission } from "../../lib/utils";

export const dynamic = "force-dynamic";

const page = async () => {
  const session = await auth();

  if (
    !hasAnyPermission([Permissions.Update, Permissions.Delete], session?.user)
  ) {
    return <Warning />;
  }

  // Fetch users
  const users = await getUsersAction();

  const currentUser = {
    username: session?.user.name,
    roleId: session?.user.roleId,
  };

  const filteredUsers = users.filter(
    (user) =>
      user.username !== currentUser.username &&
      user.roleId.priority > (currentUser.roleId?.priority ?? -1)
  );

  const roleNames = await getRoleNamesAction();

  return (
    <div className="flex flex-col items-center">
      <SessionProvider>
        <AdminUsers users={filteredUsers} initialRoleNames={roleNames} />
      </SessionProvider>
    </div>
  );
};

export default page;
